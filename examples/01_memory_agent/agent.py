"""BrainOS memory agent demo.

A terminal conversational agent wired through the BrainOS plugin pipeline:

    User Input
       |
    [Sensory Gate] ---- strip noise, enforce token budget
       |
    [Working Memory] -- update active context slots
       |
    [Hippocampal Index] store the turn with WHO/WHAT/WHEN bindings
       |
    [Attention Filter] retrieve relevant past context within budget
       |
    [LLM Call] ------- system + working memory + retrieved + user
       |
    [Response] ------- also stored in hippocampal index
       |
    [Every 10 turns] - Forgetting Engine decays + prunes memories

Run:  python agent.py            # mock mode (no API key, zero network)
      python agent.py --live     # OpenAI mode (needs OPENAI_API_KEY)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import uuid
from datetime import datetime, timezone


# --------------------------------------------------------------------------- #
# ANSI colors (no external deps)
# --------------------------------------------------------------------------- #
class C:
    RESET = "\033[0m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"
    RED = "\033[31m"
    GREY = "\033[90m"


def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if sys.platform == "win32":
        # Enable ANSI on modern Windows terminals.
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            return False
    return True


_COLOR = _supports_color()


def paint(text: str, color: str) -> str:
    return f"{color}{text}{C.RESET}" if _COLOR else text


def annotate(arrow: str, body: str, color: str = C.GREY) -> None:
    print(paint(f"  -> [{arrow}] {body}", color))


# --------------------------------------------------------------------------- #
# Plugin loading: prefer real brainos_plugins, else inline fallbacks.
# --------------------------------------------------------------------------- #
def _load_plugins():
    """Return (plugins_module_like, source_label).

    Tries the generated `brainos_plugins` package first; if missing, returns a
    namespace of equivalent inline implementations so the demo always runs.
    """
    try:
        from brainos_plugins import sensory_gate, working_memory
        from brainos_plugins import hippocampal_index, attention_filter, forgetting_engine

        class _Real:
            SensoryGate = sensory_gate.SensoryGate
            GateConfig = sensory_gate.GateConfig
            WorkingMemory = working_memory.WorkingMemory
            HippocampalIndex = hippocampal_index.HippocampalIndex
            AttentionFilter = attention_filter.AttentionFilter
            ContextItem = attention_filter.ContextItem
            ForgettingEngine = forgetting_engine.ForgettingEngine

        return _Real, "brainos_plugins (generated)"
    except Exception:
        return _inline_plugins(), "inline fallback"


def _inline_plugins():
    """Minimal equivalents of the BrainOS plugins used by this demo."""
    import math
    from dataclasses import dataclass, field

    @dataclass
    class GateConfig:
        max_tokens_per_input: int = 2000

    class SensoryGate:
        def __init__(self, config=None):
            self.config = config or GateConfig()

        def process(self, raw: str, content_type: str = "auto") -> dict:
            lines = [l for l in raw.split("\n") if l.strip() != ""]
            cleaned = "\n".join(lines)
            max_chars = self.config.max_tokens_per_input * 4
            gated = cleaned[:max_chars]
            return {
                "content": gated,
                "original_tokens": len(raw) // 4,
                "gated_tokens": len(gated) // 4,
                "ratio": round(len(gated) / max(len(raw), 1), 2),
            }

    @dataclass
    class WMSlot:
        content: str
        priority: float
        updated_at: datetime

    class WorkingMemory:
        def __init__(self, max_slots: int = 6):
            self.max_slots = max_slots
            self._slots: dict = {}

        def update(self, key: str, content: str, priority: float = 1.0):
            if len(self._slots) >= self.max_slots and key not in self._slots:
                k = min(self._slots, key=lambda x: self._slots[x].priority)
                del self._slots[k]
            self._slots[key] = WMSlot(content, priority, datetime.now(timezone.utc))

        def read(self, key: str):
            s = self._slots.get(key)
            return s.content if s else None

        def get_state(self) -> str:
            if not self._slots:
                return ""
            lines = ["## Working Memory"]
            for k, s in sorted(self._slots.items(), key=lambda x: -x[1].priority):
                lines.append(f"- **{k}**: {s.content}")
            return "\n".join(lines)

    @dataclass
    class MemoryRecord:
        id: str = field(default_factory=lambda: str(uuid.uuid4()))
        content: str = ""
        bindings: dict = field(default_factory=dict)
        timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
        salience: float = 0.5

    class HippocampalIndex:
        def __init__(self, embedding_fn=None, vector_store=None):
            self._records: list = []

        def encode(self, content: str, bindings: dict = None) -> MemoryRecord:
            record = MemoryRecord(content=content, bindings=bindings or {})
            self._records.append(record)
            return record

        def retrieve(self, query: str, top_k: int = 5) -> list:
            q = query.lower()
            return [r for r in self._records if q in r.content.lower()][:top_k]

    @dataclass
    class ContextItem:
        content: str
        token_count: int
        timestamp: datetime
        salience: float = 0.5
        embedding: list = None

    class AttentionFilter:
        def __init__(self, token_budget: int = 8000, half_life_hours: float = 24.0):
            self.token_budget = token_budget
            self.half_life = half_life_hours

        def filter(self, candidates: list, query_emb=None) -> list:
            scored = sorted(candidates, key=lambda c: -self._score(c, query_emb))
            selected, used = [], 0
            for item in scored:
                if used + item.token_count <= self.token_budget:
                    selected.append(item)
                    used += item.token_count
            return selected

        def _score(self, item, query_emb) -> float:
            return self._decay(item.timestamp) * 2 + item.salience * 2

        def _decay(self, ts: datetime) -> float:
            ref = ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
            age_h = (datetime.now(timezone.utc) - ref).total_seconds() / 3600
            return 0.5 ** (age_h / self.half_life)

    class ForgettingEngine:
        def __init__(self, decay_rate=0.95, prune_threshold=0.05, max_items=10000):
            self.decay_rate = decay_rate
            self.prune_threshold = prune_threshold
            self.max_items = max_items

        def apply_decay(self, memories: list) -> list:
            now = datetime.now(timezone.utc)
            for m in memories:
                days = (now - m.get("last_accessed", now)).days
                m["strength"] = m.get("strength", 1.0) * (self.decay_rate ** max(days, 0))
            return memories

        def prune(self, memories: list) -> list:
            return [m for m in memories if m.get("strength", 1.0) >= self.prune_threshold]

    class _Inline:
        pass

    _Inline.GateConfig = GateConfig
    _Inline.SensoryGate = SensoryGate
    _Inline.WorkingMemory = WorkingMemory
    _Inline.HippocampalIndex = HippocampalIndex
    _Inline.AttentionFilter = AttentionFilter
    _Inline.ContextItem = ContextItem
    _Inline.ForgettingEngine = ForgettingEngine
    return _Inline


# --------------------------------------------------------------------------- #
# Lightweight NLP helpers used by the pipeline (no external deps).
# --------------------------------------------------------------------------- #
KEYWORDS = ("decision", "deadline", "urgent", "important", "critical",
            "project", "goal", "plan", "problem", "blocker")
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "to",
    "of", "in", "on", "for", "with", "my", "i", "we", "you", "it", "me",
    "this", "that", "what", "about", "earlier", "mentioned", "also",
    # common sentence openers / fillers that get capitalized at line start
    "hi", "hello", "hey", "anyway", "right", "great", "thanks", "ok", "okay",
    "can", "could", "would", "should", "do", "does", "did", "let", "lets",
    "main", "so", "well", "yeah", "yes", "no", "please", "sure",
}


def extract_entities(text: str) -> list[str]:
    """Capitalized multi/single word tokens as a cheap proper-noun proxy."""
    words = re.findall(r"\b[A-Z][a-zA-Z0-9]+\b", text)
    seen, out = set(), []
    for w in words:
        if w.lower() not in STOPWORDS and w not in seen:
            seen.add(w)
            out.append(w)
    return out


def salience_of(text: str) -> float:
    t = text.lower()
    kw = sum(1 for k in KEYWORDS if k in t)
    ent = len(extract_entities(text))
    score = 0.4 + 0.1 * kw + 0.08 * ent
    return round(min(1.0, score), 2)


def topic_of(text: str) -> str:
    ents = extract_entities(text)
    if ents:
        return " ".join(ents[:2])
    tokens = [w for w in re.findall(r"[a-zA-Z]{4,}", text.lower()) if w not in STOPWORDS]
    return tokens[0].capitalize() if tokens else "general chat"


def keyword_query(text: str) -> str:
    tokens = [w for w in re.findall(r"[a-zA-Z]{4,}", text.lower()) if w not in STOPWORDS]
    return tokens[0] if tokens else text.strip()


# --------------------------------------------------------------------------- #
# Responders
# --------------------------------------------------------------------------- #
class MockResponder:
    """Rule-based responder. Zero external calls."""

    label = "mock"

    def reply(self, user_msg: str, wm_state: str, retrieved: list[str]) -> str:
        msg = user_msg.lower()
        if retrieved and any(w in msg for w in ("earlier", "mentioned", "remember",
                                                 "what was", "recall", "remind", "when is")):
            recalled = retrieved[0]
            return f"Earlier you told me: \"{recalled}\". Want to pick that back up?"
        if any(g in msg for g in ("hi ", "hello", "hey", "i'm", "i am", "my name")):
            name = None
            m = re.search(r"\b(?:i'm|i am|my name is)\s+([A-Z][a-zA-Z]+)", user_msg)
            if m:
                name = m.group(1)
            elif extract_entities(user_msg):
                name = extract_entities(user_msg)[0]
            who = f" Nice to meet you, {name}." if name else ""
            return f"Hello!{who} Tell me what you're working on and I'll keep track of it."
        if "?" in user_msg:
            if retrieved:
                return f"Based on what we discussed ({retrieved[0][:60]}...), here's my take: it sounds worth prioritizing."
            return "Good question. I don't have earlier context on that yet, so tell me more."
        topic = topic_of(user_msg)
        return f"Got it - noting the focus on {topic}. What's the next step you're considering?"


class LiveResponder:
    """OpenAI-backed responder. Requires OPENAI_API_KEY."""

    label = "live (OpenAI)"

    def __init__(self, model: str = "gpt-4o-mini"):
        from openai import OpenAI  # imported lazily so mock mode needs no dep

        self.client = OpenAI()
        self.model = model

    def reply(self, user_msg: str, wm_state: str, retrieved: list[str]) -> str:
        context = "\n".join(f"- {r}" for r in retrieved) or "(none)"
        system = (
            "You are a helpful assistant with a brain-inspired memory system. "
            "Use the working memory and retrieved memories to stay consistent.\n\n"
            f"{wm_state or '## Working Memory\\n(empty)'}\n\n"
            f"## Retrieved memories\n{context}"
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()


# --------------------------------------------------------------------------- #
# The agent: wires the plugin pipeline together.
# --------------------------------------------------------------------------- #
class MemoryAgent:
    FORGET_EVERY = 10

    def __init__(self, plugins, responder, token_budget: int = 1200):
        self.responder = responder
        self.gate = plugins.SensoryGate(plugins.GateConfig(max_tokens_per_input=500))
        self.wm = plugins.WorkingMemory(max_slots=6)
        self.index = plugins.HippocampalIndex()
        self.attention = plugins.AttentionFilter(token_budget=token_budget, half_life_hours=48.0)
        self.forgetting = plugins.ForgettingEngine(decay_rate=0.9, prune_threshold=0.3)
        self.ContextItem = plugins.ContextItem

        self.turn = 0
        self.pruned_total = 0
        # meta[id] -> mutable dict the forgetting engine can decay/prune.
        self.meta: dict[str, dict] = {}

    # ---- pipeline stages -------------------------------------------------- #
    def _gate(self, user_msg: str) -> str:
        result = self.gate.process(user_msg, content_type="text")
        annotate("SENSORY GATE",
                 f"{result['original_tokens']} -> {result['gated_tokens']} tokens",
                 C.CYAN)
        return result["content"]

    def _update_wm(self, text: str) -> None:
        topic = topic_of(text)
        self.wm.update("topic", topic, priority=1.0)
        annotate("WM UPDATE", f"slot 'topic' = \"{topic}\"", C.YELLOW)
        ents = extract_entities(text)
        if ents:
            self.wm.update("entities", ", ".join(ents[:4]), priority=0.8)
        if "?" in text:
            self.wm.update("user_goal", text.strip()[:60], priority=0.9)

    def _store(self, content: str, role: str) -> None:
        when = datetime.now(timezone.utc)
        bindings = {"who": role, "what": topic_of(content), "when": when.isoformat()}
        record = self.index.encode(content, bindings=bindings)
        record.salience = salience_of(content)
        self.meta[record.id] = {
            "id": record.id,
            "strength": 1.0,
            "salience": record.salience,
            "last_accessed": when,
            "born_turn": self.turn,
        }
        annotate("STORED",
                 f"memory #{len(self.index._records)} (salience: {record.salience:.2f})",
                 C.GREEN)

    def _retrieve(self, user_msg: str) -> list[str]:
        # Query the index with several cues, not just one: capitalized entities
        # (e.g. "Project", "Atlas") first, then other salient tokens. This lets a
        # question like "when is the Project Atlas deadline?" match an earlier
        # turn even though the leading word ("Remind") is not itself a keyword.
        terms: list[str] = []
        for ent in extract_entities(user_msg):
            terms.append(ent.lower())
        terms.extend(
            w for w in re.findall(r"[a-zA-Z]{4,}", user_msg.lower())
            if w not in STOPWORDS
        )
        if not terms:
            terms = [keyword_query(user_msg)]

        candidates, seen = [], set()
        for term in terms:
            for rec in self.index.retrieve(term, top_k=8):
                if rec.id not in seen:
                    seen.add(rec.id)
                    candidates.append(rec)
        if not candidates:
            return []
        items = [
            self.ContextItem(
                content=r.content,
                token_count=max(1, len(r.content) // 4),
                timestamp=r.timestamp,
                salience=getattr(r, "salience", 0.5),
            )
            for r in candidates
        ]
        selected = self.attention.filter(items)
        if selected:
            scores = [self.attention._score(it, None) for it in selected]
            norm = max(scores) or 1.0
            labels = ", ".join(f"{s / norm:.2f}" for s in scores[:3])
            annotate("RETRIEVED", f"{len(selected)} memories (relevance: {labels})", C.BLUE)
        return [it.content for it in selected]

    def _maybe_forget(self) -> None:
        if self.turn % self.FORGET_EVERY != 0:
            return
        mems = list(self.meta.values())
        # Age each memory by how many turns old it is (compressed into "days"),
        # then weight by salience so important, recent memories survive. This
        # gives the short demo session a visible decay/prune effect.
        for m in mems:
            age_turns = max(0, self.turn - m.get("born_turn", self.turn))
            m["strength"] = m["salience"] * (self.forgetting.decay_rate ** age_turns)
        survivors = self.forgetting.prune(mems)
        pruned = len(mems) - len(survivors)
        self.pruned_total += pruned
        keep_ids = {m["id"] for m in survivors}
        self.meta = {mid: m for mid, m in self.meta.items() if mid in keep_ids}
        annotate("FORGETTING ENGINE",
                 f"decayed {len(mems)} memories, pruned {pruned}", C.RED)

    def stats_line(self) -> str:
        wm_slots = len(self.wm._slots)
        indexed = len(self.index._records)
        active = len(self.meta)
        body = (f"WM {wm_slots}/{self.wm.max_slots} | Indexed: {indexed} | "
                f"Active: {active} | Pruned: {self.pruned_total}")
        return paint(f"  [Stats: {body}]", C.DIM)

    # ---- one full turn ---------------------------------------------------- #
    def handle(self, user_msg: str) -> str:
        self.turn += 1
        print(paint(f"[Turn {self.turn}] ", C.BOLD) + paint("User: ", C.CYAN) + user_msg)

        gated = self._gate(user_msg)
        self._update_wm(gated)
        # Retrieve relevant PRIOR context before storing the current turn, so
        # recall surfaces earlier memories rather than the message just sent.
        retrieved = self._retrieve(gated)
        self._store(gated, role="user")

        reply = self.responder.reply(gated, self.wm.get_state(), retrieved)

        self._store(reply, role="agent")
        self._maybe_forget()

        print(paint("Agent: ", C.GREEN) + reply)
        print(self.stats_line())
        print()
        return reply


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
BANNER = """
+-----------------------------------------------------------+
|  BrainOS Memory Agent                                     |
|  Sensory Gate -> Working Memory -> Hippocampal Index ->   |
|  Attention Filter -> LLM -> (every 10 turns) Forgetting   |
+-----------------------------------------------------------+
"""


def build_responder(live: bool):
    if live:
        if not os.environ.get("OPENAI_API_KEY"):
            print(paint("OPENAI_API_KEY not set; falling back to mock mode.", C.YELLOW))
            return MockResponder()
        try:
            return LiveResponder()
        except Exception as e:  # missing openai package, bad key, etc.
            print(paint(f"Live mode unavailable ({e}); using mock mode.", C.YELLOW))
            return MockResponder()
    return MockResponder()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="BrainOS memory agent demo")
    parser.add_argument("--live", action="store_true", help="Use OpenAI API (needs OPENAI_API_KEY)")
    parser.add_argument("--mock", action="store_true", help="Force mock mode (default)")
    args = parser.parse_args(argv)

    plugins, source = _load_plugins()
    responder = build_responder(live=args.live and not args.mock)

    print(paint(BANNER, C.CYAN))
    print(paint(f"  plugin source : {source}", C.DIM))
    print(paint(f"  responder     : {responder.label}", C.DIM))
    print(paint("  Type your message. Ctrl+C to exit.\n", C.DIM))

    agent = MemoryAgent(plugins, responder)
    try:
        while True:
            try:
                user_msg = input(paint("you> ", C.CYAN)).strip()
            except EOFError:
                break
            if not user_msg:
                continue
            if user_msg.lower() in ("/quit", "/exit"):
                break
            agent.handle(user_msg)
    except KeyboardInterrupt:
        print()
    finally:
        print(paint("\n=== Final memory stats ===", C.BOLD))
        print(agent.stats_line())
        print(paint(f"  Total turns: {agent.turn}", C.DIM))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
