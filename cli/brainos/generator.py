"""Code generator for BrainOS plugins."""

from brainos.plugins import PLUGINS

# Class names that don't follow the default dash-split capitalization rule.
CLASS_NAME_OVERRIDES = {
    "dmn-incubator": "DMNIncubator",
    "metacognition": "MetacognitionMonitor",
}


def class_name_for(name: str) -> str:
    """Return the class name for a plugin, honoring explicit overrides."""
    if name in CLASS_NAME_OVERRIDES:
        return CLASS_NAME_OVERRIDES[name]
    return "".join(word.capitalize() for word in name.split("-"))


def generate_plugin(name: str) -> str:
    """Generate Python source for a plugin."""
    info = PLUGINS[name]
    class_name = class_name_for(name)

    header = f"""\"""
BrainOS Plugin: {class_name}
Brain Analog: {info['brain_analog']}
Token Savings: {info['token_savings']}

{info['description']}
\"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Any
"""

    if name == "sensory-gate":
        return header + _sensory_gate_body()
    elif name == "attention-filter":
        return header + _attention_filter_body()
    elif name == "working-memory":
        return header + _working_memory_body()
    elif name == "hippocampal-index":
        return header + _hippocampal_index_body()
    elif name == "forgetting-engine":
        return header + _forgetting_engine_body()
    elif name == "consolidator":
        return header + _consolidator_body()
    elif name == "episodic-store":
        return header + _episodic_store_body()
    elif name == "procedural-cache":
        return header + _procedural_cache_body()
    elif name == "semantic-store":
        return header + _semantic_store_body()
    elif name == "salience-tagger":
        return header + _salience_tagger_body()
    elif name == "dmn-incubator":
        return header + _dmn_incubator_body()
    elif name == "metacognition":
        return header + _metacognition_body()
    else:
        return header + _generic_body(class_name, info)


def _sensory_gate_body():
    return """import re
import json


@dataclass
class GateConfig:
    max_tokens_per_input: int = 2000
    noise_patterns: list[str] = field(default_factory=lambda: [r"^\\s*$"])
    extract_fields: list[str] = field(default_factory=lambda: ["data", "results", "items"])
    ignore_fields: list[str] = field(default_factory=lambda: ["metadata", "pagination"])


class SensoryGate:
    \"\"\"Pre-filter raw inputs before they reach the LLM context.\"\"\"

    def __init__(self, config: Optional[GateConfig] = None):
        self.config = config or GateConfig()
        self._noise_re = [re.compile(p) for p in self.config.noise_patterns]

    def process(self, raw: str, content_type: str = "auto") -> dict:
        \"\"\"Gate input: detect type, strip noise, extract signal, enforce budget.\"\"\"
        if content_type == "auto":
            content_type = self._detect_type(raw)
        cleaned = self._remove_noise(raw)
        extracted = self._extract(cleaned, content_type)
        gated = self._budget(extracted)
        return {
            "content": gated,
            "original_tokens": len(raw) // 4,
            "gated_tokens": len(gated) // 4,
            "ratio": round(len(gated) / max(len(raw), 1), 2),
        }

    def _detect_type(self, text: str) -> str:
        t = text.strip()
        if t.startswith("{") or t.startswith("["):
            return "json"
        if "<html" in t.lower():
            return "html"
        return "text"

    def _remove_noise(self, text: str) -> str:
        lines = text.split("\\n")
        return "\\n".join(l for l in lines if not any(p.match(l) for p in self._noise_re))

    def _extract(self, text: str, ctype: str) -> str:
        if ctype == "json":
            try:
                data = json.loads(text)
                if isinstance(data, dict):
                    keep = {k: v for k, v in data.items() if k in self.config.extract_fields}
                    if keep:
                        return json.dumps(keep, indent=2, default=str)
            except json.JSONDecodeError:
                pass
        return text

    def _budget(self, text: str) -> str:
        max_chars = self.config.max_tokens_per_input * 4
        return text[:max_chars] if len(text) > max_chars else text
"""


def _attention_filter_body():
    return """import math


@dataclass
class ContextItem:
    content: str
    token_count: int
    timestamp: datetime
    salience: float = 0.5
    embedding: Optional[list[float]] = None


class AttentionFilter:
    \"\"\"Score and rank context by relevance. Select within token budget.\"\"\"

    def __init__(self, token_budget: int = 8000, half_life_hours: float = 24.0):
        self.token_budget = token_budget
        self.half_life = half_life_hours

    def filter(self, candidates: list[ContextItem], query_emb: list[float] = None) -> list[ContextItem]:
        scored = [(self._score(c, query_emb), c) for c in candidates]
        scored.sort(key=lambda x: -x[0])
        selected, used = [], 0
        for score, item in scored:
            if used + item.token_count <= self.token_budget:
                selected.append(item)
                used += item.token_count
        return selected

    def _score(self, item: ContextItem, query_emb) -> float:
        sim = self._cosine(item.embedding, query_emb) if (item.embedding and query_emb) else 0.5
        recency = self._decay(item.timestamp)
        return sim * 3 + recency * 2 + item.salience * 2

    def _cosine(self, a, b) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x**2 for x in a))
        nb = math.sqrt(sum(x**2 for x in b))
        return dot / (na * nb) if na and nb else 0.0

    def _decay(self, ts: datetime) -> float:
        age_h = (datetime.now(timezone.utc) - ts.replace(tzinfo=timezone.utc)).total_seconds() / 3600
        return 0.5 ** (age_h / self.half_life)
"""


def _working_memory_body():
    return """

@dataclass
class WMSlot:
    content: str
    priority: float
    updated_at: datetime


class WorkingMemory:
    \"\"\"Fixed-slot scratchpad. Inject into every LLM call.\"\"\"

    def __init__(self, max_slots: int = 6):
        self.max_slots = max_slots
        self._slots: dict[str, WMSlot] = {}

    def update(self, key: str, content: str, priority: float = 1.0):
        if len(self._slots) >= self.max_slots and key not in self._slots:
            self._evict()
        self._slots[key] = WMSlot(content=content, priority=priority, updated_at=datetime.now(timezone.utc))

    def read(self, key: str) -> Optional[str]:
        s = self._slots.get(key)
        return s.content if s else None

    def clear(self, key: str):
        self._slots.pop(key, None)

    def get_state(self) -> str:
        if not self._slots:
            return ""
        lines = ["## Working Memory"]
        for k, s in sorted(self._slots.items(), key=lambda x: -x[1].priority):
            lines.append(f"- **{k}**: {s.content}")
        return "\\n".join(lines)

    def _evict(self):
        if self._slots:
            k = min(self._slots, key=lambda x: self._slots[x].priority)
            del self._slots[k]
"""


def _hippocampal_index_body():
    return """import uuid


@dataclass
class MemoryRecord:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    bindings: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    salience: float = 0.5


class HippocampalIndex:
    \"\"\"Embed, bind, and retrieve with pattern completion.\"\"\"

    def __init__(self, embedding_fn=None, vector_store=None):
        self.embedding_fn = embedding_fn
        self.vector_store = vector_store
        self._records: list[MemoryRecord] = []

    def encode(self, content: str, bindings: dict = None) -> MemoryRecord:
        record = MemoryRecord(content=content, bindings=bindings or {})
        self._records.append(record)
        if self.vector_store and self.embedding_fn:
            emb = self.embedding_fn(content)
            self.vector_store.add(ids=[record.id], embeddings=[emb], documents=[content])
        return record

    def retrieve(self, query: str, top_k: int = 5) -> list[MemoryRecord]:
        if self.vector_store and self.embedding_fn:
            emb = self.embedding_fn(query)
            results = self.vector_store.query(query_embeddings=[emb], n_results=top_k)
            return [MemoryRecord(id=results['ids'][0][i], content=doc)
                    for i, doc in enumerate(results['documents'][0])]
        return [r for r in self._records if query.lower() in r.content.lower()][:top_k]
"""


def _forgetting_engine_body():
    return """

class ForgettingEngine:
    \"\"\"Apply decay, resolve interference, enforce capacity.\"\"\"

    def __init__(self, decay_rate=0.95, prune_threshold=0.05, max_items=10000):
        self.decay_rate = decay_rate
        self.prune_threshold = prune_threshold
        self.max_items = max_items

    def apply_decay(self, memories: list[dict]) -> list[dict]:
        for m in memories:
            days = (datetime.now(timezone.utc) - m.get("last_accessed", datetime.now(timezone.utc))).days
            m["strength"] = m.get("strength", 1.0) * (self.decay_rate ** days)
        return memories

    def prune(self, memories: list[dict]) -> list[dict]:
        return [m for m in memories if m.get("strength", 1.0) >= self.prune_threshold]

    def enforce_capacity(self, memories: list[dict]) -> list[dict]:
        if len(memories) <= self.max_items:
            return memories
        memories.sort(key=lambda m: m.get("strength", 0) * m.get("salience", 0.5), reverse=True)
        return memories[:self.max_items]

    def on_access(self, memory: dict, boost: float = 0.3):
        memory["strength"] = min(1.0, memory.get("strength", 0.5) + boost)
        memory["last_accessed"] = datetime.now(timezone.utc)
"""


def _consolidator_body():
    return """from difflib import SequenceMatcher


@dataclass
class ConsolidatorConfig:
    similarity_threshold: float = 0.85
    max_chars: int = 500
    min_group_size: int = 2


class Consolidator:
    \"\"\"Offline memory maintenance: deduplicate, merge, and compress memories.

    Brain analog: sleep-dependent consolidation, where the hippocampus replays
    and the neocortex integrates overlapping traces into compact schemas.
    \"\"\"

    def __init__(self, similarity_threshold: float = 0.85, summarize_fn: Optional[Any] = None):
        self.config = ConsolidatorConfig(similarity_threshold=similarity_threshold)
        self.summarize_fn = summarize_fn

    def run(self, memories: list[dict]) -> list[dict]:
        \"\"\"Full consolidation pass: dedupe, then compress each survivor.\"\"\"
        deduped = self.deduplicate(memories)
        return [self.compress(m) for m in deduped]

    def deduplicate(self, memories: list[dict]) -> list[dict]:
        \"\"\"Remove near-duplicates, merging each cluster into a single memory.\"\"\"
        remaining = list(memories)
        result: list[dict] = []
        while remaining:
            seed = remaining.pop(0)
            group = [seed]
            rest = []
            for m in remaining:
                if self._similarity(seed.get("content", ""), m.get("content", "")) >= self.config.similarity_threshold:
                    group.append(m)
                else:
                    rest.append(m)
            remaining = rest
            result.append(self.merge(group) if len(group) >= self.config.min_group_size else seed)
        return result

    def merge(self, group: list[dict]) -> dict:
        \"\"\"Merge a group of related memories into one representative memory.\"\"\"
        if not group:
            return {}
        if len(group) == 1:
            return dict(group[0])
        primary = max(group, key=lambda m: m.get("salience", 0.0))
        merged_bindings: dict = {}
        for m in group:
            merged_bindings.update(m.get("bindings", {}) or {})
        contents = [m.get("content", "") for m in group if m.get("content")]
        merged_content = max(contents, key=len) if contents else ""
        timestamps = [m.get("timestamp") for m in group if m.get("timestamp") is not None]
        return {
            "id": primary.get("id"),
            "content": merged_content,
            "timestamp": min(timestamps) if timestamps else primary.get("timestamp"),
            "salience": max((m.get("salience", 0.0) for m in group), default=0.0),
            "access_count": sum(m.get("access_count", 0) for m in group),
            "bindings": merged_bindings,
            "merged_from": [m.get("id") for m in group],
        }

    def compress(self, memory: dict) -> dict:
        \"\"\"Reduce verbose memories via summarize_fn or truncation to max_chars.\"\"\"
        content = memory.get("content", "") or ""
        if len(content) <= self.config.max_chars:
            return memory
        out = dict(memory)
        if self.summarize_fn is not None:
            out["content"] = self.summarize_fn(content)
        else:
            out["content"] = content[: self.config.max_chars].rstrip() + "..."
        out["compressed"] = True
        return out

    def _similarity(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a or "", b or "").ratio()
"""


def _episodic_store_body():
    return """import uuid


@dataclass
class Event:
    id: str
    content: str
    timestamp: datetime
    bindings: dict


class EpisodicStore:
    \"\"\"Store and query events with WHO/WHAT/WHEN/WHERE/WHY context bindings.

    Brain analog: episodic memory, which stitches together the elements of an
    experience into a retrievable, time-stamped whole.
    \"\"\"

    def __init__(self, embedding_fn: Optional[Any] = None, vector_store: Optional[Any] = None):
        self.embedding_fn = embedding_fn
        self.vector_store = vector_store
        self._events: list[Event] = []
        if self.vector_store is None:
            try:
                import chromadb  # noqa: F401
                self._chromadb_available = True
            except ImportError:
                self._chromadb_available = False

    def record_event(self, content: str, who=None, what=None, when=None,
                     where=None, why=None) -> dict:
        \"\"\"Record an event with optional context bindings.\"\"\"
        ts = when if isinstance(when, datetime) else datetime.now(timezone.utc)
        bindings = {
            "who": who,
            "what": what if what is not None else content,
            "when": when,
            "where": where,
            "why": why,
        }
        event = Event(id=str(uuid.uuid4()), content=content, timestamp=ts, bindings=bindings)
        self._events.append(event)
        if self.vector_store is not None and self.embedding_fn is not None:
            emb = self.embedding_fn(content)
            self.vector_store.add(ids=[event.id], embeddings=[emb], documents=[content])
        return self._to_dict(event)

    def query_by_time(self, start: datetime, end: Optional[datetime] = None) -> list:
        \"\"\"Return events within the temporal range [start, end].\"\"\"
        end = end or datetime.now(timezone.utc)
        return [self._to_dict(e) for e in self._events if start <= e.timestamp <= end]

    def query_by_binding(self, **kwargs) -> list:
        \"\"\"Filter events by any binding field (who/what/when/where/why).\"\"\"
        def matches(event: Event) -> bool:
            for key, value in kwargs.items():
                if event.bindings.get(key) != value:
                    return False
            return True
        return [self._to_dict(e) for e in self._events if matches(e)]

    def query_by_content(self, query: str, top_k: int = 5) -> list:
        \"\"\"Semantic search with vector store, falling back to substring match.\"\"\"
        if self.vector_store is not None and self.embedding_fn is not None:
            emb = self.embedding_fn(query)
            results = self.vector_store.query(query_embeddings=[emb], n_results=top_k)
            ids = results["ids"][0]
            by_id = {e.id: e for e in self._events}
            return [self._to_dict(by_id[i]) for i in ids if i in by_id]
        q = query.lower()
        matched = [e for e in self._events if q in e.content.lower()]
        return [self._to_dict(e) for e in matched[:top_k]]

    def _to_dict(self, event: Event) -> dict:
        return {
            "id": event.id,
            "content": event.content,
            "timestamp": event.timestamp,
            "bindings": event.bindings,
        }
"""


def _procedural_cache_body():
    return """from difflib import SequenceMatcher


@dataclass
class CacheEntry:
    task: str
    steps: list[dict]
    success: bool
    created_at: datetime


class ProceduralCache:
    \"\"\"Cache successful tool-call sequences to skip re-reasoning on similar tasks.

    Brain analog: the basal ganglia, which chunk repeated action sequences into
    automatic procedures so the cortex no longer has to deliberate over them.
    \"\"\"

    def __init__(self, similarity_threshold: float = 0.8, max_entries: int = 500):
        self.similarity_threshold = similarity_threshold
        self.max_entries = max_entries
        self._entries: list[CacheEntry] = []
        self._lookups = 0
        self._hits = 0

    def record(self, task: str, steps: list[dict], success: bool) -> None:
        \"\"\"Store a completed action sequence for a task.\"\"\"
        if not success:
            return
        existing = self._find_exact(task)
        if existing is not None:
            existing.steps = steps
            existing.success = success
            existing.created_at = datetime.now(timezone.utc)
            return
        self._entries.append(
            CacheEntry(task=task, steps=steps, success=success, created_at=datetime.now(timezone.utc))
        )
        if len(self._entries) > self.max_entries:
            self._entries.pop(0)

    def lookup(self, task: str) -> Optional[list[dict]]:
        \"\"\"Return cached steps for the most similar successful task, if any.\"\"\"
        self._lookups += 1
        best: Optional[CacheEntry] = None
        best_score = 0.0
        for entry in self._entries:
            score = SequenceMatcher(None, task, entry.task).ratio()
            if score >= self.similarity_threshold and score > best_score:
                best, best_score = entry, score
        if best is not None:
            self._hits += 1
            return best.steps
        return None

    def hit_rate(self) -> float:
        \"\"\"Return the fraction of lookups that found a cached sequence.\"\"\"
        if self._lookups == 0:
            return 0.0
        return self._hits / self._lookups

    def invalidate(self, task: str) -> None:
        \"\"\"Remove any cached entry whose task exactly matches.\"\"\"
        self._entries = [e for e in self._entries if e.task != task]

    def _find_exact(self, task: str) -> Optional[CacheEntry]:
        for entry in self._entries:
            if entry.task == task:
                return entry
        return None
"""


def _semantic_store_body():
    return """from collections import defaultdict, deque

try:
    import networkx as nx
    _HAS_NETWORKX = True
except ImportError:
    nx = None
    _HAS_NETWORKX = False


@dataclass
class Triple:
    subject: str
    predicate: str
    obj: str
    metadata: dict = field(default_factory=dict)


class SemanticStore:
    \"\"\"Knowledge graph of (subject, predicate, object) triples.

    Brain analog: semantic memory, the brain's timeless web of facts and
    relationships abstracted away from any single episode.
    \"\"\"

    def __init__(self):
        self._triples: list[Triple] = []
        self._by_subject: dict[str, list[Triple]] = defaultdict(list)
        self._graph = nx.MultiDiGraph() if _HAS_NETWORKX else None

    def add(self, subject: str, predicate: str, obj: str, metadata: Optional[dict] = None) -> None:
        \"\"\"Add a (subject, predicate, object) triple.\"\"\"
        triple = Triple(subject=subject, predicate=predicate, obj=obj, metadata=metadata or {})
        self._triples.append(triple)
        self._by_subject[subject].append(triple)
        if self._graph is not None:
            self._graph.add_edge(subject, obj, predicate=predicate)

    def query(self, subject=None, predicate=None, obj=None) -> list[tuple]:
        \"\"\"Pattern-match triples; None matches any value in that position.\"\"\"
        result = []
        for t in self._triples:
            if subject is not None and t.subject != subject:
                continue
            if predicate is not None and t.predicate != predicate:
                continue
            if obj is not None and t.obj != obj:
                continue
            result.append((t.subject, t.predicate, t.obj))
        return result

    def get_neighbors(self, entity: str, hops: int = 1) -> list:
        \"\"\"Return entities reachable from `entity` within `hops` edges.\"\"\"
        visited = {entity}
        frontier = {entity}
        for _ in range(hops):
            nxt: set = set()
            for node in frontier:
                for t in self._by_subject.get(node, []):
                    nxt.add(t.obj)
                for t in self._triples:
                    if t.obj == node:
                        nxt.add(t.subject)
            nxt -= visited
            visited |= nxt
            frontier = nxt
            if not frontier:
                break
        return sorted(visited - {entity})

    def shortest_path(self, start: str, end: str) -> list:
        \"\"\"Return a shortest path of entities between start and end (BFS).\"\"\"
        if start == end:
            return [start]
        adjacency: dict[str, set] = defaultdict(set)
        for t in self._triples:
            adjacency[t.subject].add(t.obj)
            adjacency[t.obj].add(t.subject)
        queue = deque([[start]])
        seen = {start}
        while queue:
            path = queue.popleft()
            for neighbor in adjacency[path[-1]]:
                if neighbor == end:
                    return path + [neighbor]
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(path + [neighbor])
        return []

    def all_entities(self) -> set:
        \"\"\"Return the set of all unique entities (subjects and objects).\"\"\"
        entities: set = set()
        for t in self._triples:
            entities.add(t.subject)
            entities.add(t.obj)
        return entities
"""


def _salience_tagger_body():
    return """import math
import re


@dataclass
class SalienceWeights:
    recency: float = 0.25
    frequency: float = 0.25
    entity_density: float = 0.25
    keywords: float = 0.25


class SalienceTagger:
    \"\"\"Score memories at write-time to prioritize storage and retrieval.

    Brain analog: the amygdala, which tags experiences with emotional and
    motivational significance so important events are preferentially retained.
    \"\"\"

    KEYWORDS = ("decision", "deadline", "urgent", "important", "critical", "action", "blocker")

    def __init__(self, weights: Optional[dict] = None):
        if weights:
            self.weights = SalienceWeights(**weights)
        else:
            self.weights = SalienceWeights()

    def score(self, content: str, metadata: Optional[dict] = None) -> float:
        \"\"\"Return a 0-1 salience score combining weighted signals.\"\"\"
        metadata = metadata or {}
        signals = {
            "recency": self._recency_signal(metadata.get("timestamp")),
            "frequency": self._frequency_signal(metadata.get("access_count", 0)),
            "entity_density": self._entity_density_signal(content),
            "keywords": self._keyword_signal(content),
        }
        w = self.weights
        total_weight = w.recency + w.frequency + w.entity_density + w.keywords
        if total_weight == 0:
            return 0.0
        weighted = (
            signals["recency"] * w.recency
            + signals["frequency"] * w.frequency
            + signals["entity_density"] * w.entity_density
            + signals["keywords"] * w.keywords
        )
        return max(0.0, min(1.0, weighted / total_weight))

    def _recency_signal(self, timestamp) -> float:
        \"\"\"Exponential decay: recent memories score near 1.0.\"\"\"
        if not isinstance(timestamp, datetime):
            return 0.5
        ts = timestamp if timestamp.tzinfo else timestamp.replace(tzinfo=timezone.utc)
        age_hours = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
        if age_hours < 0:
            age_hours = 0.0
        return math.exp(-age_hours / 24.0)

    def _frequency_signal(self, access_count) -> float:
        \"\"\"Log-normalized access frequency, saturating toward 1.0.\"\"\"
        count = max(0, int(access_count or 0))
        return min(1.0, math.log1p(count) / math.log1p(100))

    def _entity_density_signal(self, content: str) -> float:
        \"\"\"Ratio of capitalized (proper-noun-like) words to total words.\"\"\"
        words = re.findall(r"[A-Za-z][A-Za-z0-9']*", content or "")
        if not words:
            return 0.0
        proper = sum(1 for w in words if w[0].isupper())
        return min(1.0, proper / len(words))

    def _keyword_signal(self, content: str) -> float:
        \"\"\"Fraction of high-importance keywords present in the content.\"\"\"
        text = (content or "").lower()
        hits = sum(1 for kw in self.KEYWORDS if kw in text)
        return min(1.0, hits / max(1, len(self.KEYWORDS) // 2))
"""


def _dmn_incubator_body():
    return """import random
import re


@dataclass
class IncubatorConfig:
    sample_size: int = 10
    keyword_overlap_threshold: int = 2
    temporal_window_hours: float = 48.0


class DMNIncubator:
    \"\"\"Background insight discovery over random memory pairs.

    Brain analog: the default mode network, active during rest, which recombines
    stored memories to surface non-obvious connections and creative insights.
    \"\"\"

    def __init__(self, insight_fn: Optional[Any] = None, sample_size: int = 10):
        self.config = IncubatorConfig(sample_size=sample_size)
        self.insight_fn = insight_fn or self._default_insight_fn

    def incubate(self, memories: list[dict]) -> list[dict]:
        \"\"\"Run one incubation pass, returning discovered insight dicts.\"\"\"
        insights: list[dict] = []
        for mem_a, mem_b in self._sample_pairs(memories):
            connection = self.insight_fn(mem_a, mem_b)
            if connection:
                insights.append({
                    "memory_a_id": mem_a.get("id"),
                    "memory_b_id": mem_b.get("id"),
                    "connection": connection,
                    "confidence": self._confidence(mem_a, mem_b),
                })
        return insights

    def _sample_pairs(self, memories: list[dict]) -> list[tuple]:
        \"\"\"Draw random distinct memory pairs to inspect.\"\"\"
        if len(memories) < 2:
            return []
        pairs: list[tuple] = []
        seen: set = set()
        attempts = self.config.sample_size * 4
        for _ in range(attempts):
            if len(pairs) >= self.config.sample_size:
                break
            a, b = random.sample(range(len(memories)), 2)
            key = (min(a, b), max(a, b))
            if key in seen:
                continue
            seen.add(key)
            pairs.append((memories[a], memories[b]))
        return pairs

    def _default_insight_fn(self, mem_a: dict, mem_b: dict) -> Optional[str]:
        \"\"\"Heuristic: keyword overlap plus temporal proximity implies a link.\"\"\"
        shared = self._shared_keywords(mem_a, mem_b)
        if len(shared) >= self.config.keyword_overlap_threshold:
            return "shared concepts: " + ", ".join(sorted(shared))
        if self._temporally_close(mem_a, mem_b) and shared:
            return "temporally linked via: " + ", ".join(sorted(shared))
        return None

    def _shared_keywords(self, mem_a: dict, mem_b: dict) -> set:
        def tokens(m: dict) -> set:
            words = re.findall(r"[a-z]{4,}", (m.get("content", "") or "").lower())
            return set(words)
        return tokens(mem_a) & tokens(mem_b)

    def _temporally_close(self, mem_a: dict, mem_b: dict) -> bool:
        ta, tb = mem_a.get("timestamp"), mem_b.get("timestamp")
        if not isinstance(ta, datetime) or not isinstance(tb, datetime):
            return False
        delta_hours = abs((ta - tb).total_seconds()) / 3600
        return delta_hours <= self.config.temporal_window_hours

    def _confidence(self, mem_a: dict, mem_b: dict) -> float:
        shared = self._shared_keywords(mem_a, mem_b)
        base = min(1.0, len(shared) / 5.0)
        if self._temporally_close(mem_a, mem_b):
            base = min(1.0, base + 0.2)
        return round(base, 2)
"""


def _metacognition_body():
    return """from collections import defaultdict


@dataclass
class StrategyStats:
    successes: int = 0
    attempts: int = 0

    @property
    def success_rate(self) -> float:
        return self.successes / self.attempts if self.attempts else 0.0


class MetacognitionMonitor:
    \"\"\"Self-evaluation: track confidence, compare predictions to outcomes.

    Brain analog: prefrontal metacognitive monitoring, which estimates the
    reliability of one's own judgments and selects strategies accordingly.
    \"\"\"

    def __init__(self):
        self._predictions: dict[str, float] = {}
        self._outcomes: list[tuple] = []
        self._strategies: dict[str, list[str]] = {}
        self._strategy_stats: dict[str, dict[str, StrategyStats]] = defaultdict(
            lambda: defaultdict(StrategyStats)
        )

    def predict(self, task: str, confidence: float) -> None:
        \"\"\"Register a confidence prediction before executing a task.\"\"\"
        self._predictions[task] = max(0.0, min(1.0, confidence))

    def record_outcome(self, task: str, success: bool) -> None:
        \"\"\"Record the actual result for a previously predicted task.\"\"\"
        confidence = self._predictions.get(task)
        self._outcomes.append((task, confidence, bool(success)))

    def calibration_error(self) -> float:
        \"\"\"Mean absolute gap between confidence and actual success.\"\"\"
        scored = [(c, s) for _, c, s in self._outcomes if c is not None]
        if not scored:
            return 0.0
        return sum(abs(c - (1.0 if s else 0.0)) for c, s in scored) / len(scored)

    def register_strategy(self, name: str, task_types: list[str]) -> None:
        \"\"\"Register a named strategy applicable to the given task types.\"\"\"
        self._strategies[name] = list(task_types)

    def record_strategy_outcome(self, name: str, task_type: str, success: bool) -> None:
        \"\"\"Update historical performance for a strategy on a task type.\"\"\"
        stats = self._strategy_stats[task_type][name]
        stats.attempts += 1
        if success:
            stats.successes += 1

    def select_strategy(self, task_type: str) -> str:
        \"\"\"Pick the best strategy for a task type by historical success rate.\"\"\"
        candidates = [n for n, types in self._strategies.items() if task_type in types]
        if not candidates:
            candidates = list(self._strategies.keys())
        if not candidates:
            return ""
        stats = self._strategy_stats.get(task_type, {})

        def key(name: str):
            s = stats.get(name)
            if s is None:
                return (0.0, 0)
            return (s.success_rate, s.attempts)

        return max(candidates, key=key)
"""


def _generic_body(class_name, info):
    return f"""

class {class_name}:
    \"\"\"{info['description']}.

    Brain Analog: {info['brain_analog']}
    \"\"\"

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {{}}

    # TODO: Implement methods based on _plugins/{class_name} spec
    # See: https://github.com/niravvaghasiya/BrainOS/_plugins/
"""


def generate_config(name: str) -> str:
    """Generate YAML config template."""
    return f"# BrainOS: {name} configuration\n# See: https://github.com/niravvaghasiya/BrainOS/_plugins/\n\n{name.replace('-', '_')}:\n  enabled: true\n"


def generate_test(name: str) -> str:
    """Generate test skeleton."""
    class_name = class_name_for(name)
    module = name.replace("-", "_")
    return f"""\"\"\"{name} plugin tests.\"\"\"

import pytest
from brainos_plugins.{module} import {class_name}


def test_init():
    plugin = {class_name}()
    assert plugin is not None
"""
