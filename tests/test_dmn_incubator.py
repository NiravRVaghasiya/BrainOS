"""Tests for the generated dmn-incubator plugin."""

import importlib
from datetime import datetime, timezone


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.dmn_incubator")


def test_incubate_finds_connections(tmp_project):
    mod = _load(tmp_project)
    di = mod.DMNIncubator(sample_size=20)
    now = datetime.now(timezone.utc)
    memories = [
        {"id": "a", "content": "database migration performance optimization work", "timestamp": now},
        {"id": "b", "content": "performance optimization during database migration", "timestamp": now},
    ]
    insights = di.incubate(memories)
    assert len(insights) >= 1
    insight = insights[0]
    assert insight["connection"]
    assert {insight["memory_a_id"], insight["memory_b_id"]} == {"a", "b"}
    assert 0.0 <= insight["confidence"] <= 1.0


def test_empty_memories(tmp_project):
    mod = _load(tmp_project)
    di = mod.DMNIncubator()
    assert di.incubate([]) == []
