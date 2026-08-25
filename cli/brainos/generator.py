"""Code generator for BrainOS plugins."""

from brainos.plugins import PLUGINS


def generate_plugin(name: str) -> str:
    """Generate Python source for a plugin."""
    info = PLUGINS[name]
    class_name = "".join(word.capitalize() for word in name.split("-"))
    module_name = name.replace("-", "_")

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
    class_name = "".join(w.capitalize() for w in name.split("-"))
    module = name.replace("-", "_")
    return f"""\"\"\"{name} plugin tests.\"\"\"

import pytest
from brainos_plugins.{module} import {class_name}


def test_init():
    plugin = {class_name}()
    assert plugin is not None
"""
