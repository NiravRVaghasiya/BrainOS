"""Tests for the generated forgetting-engine plugin."""

import importlib
from datetime import datetime, timezone, timedelta


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.forgetting_engine")


def test_decay_reduces_strength(tmp_project):
    mod = _load(tmp_project)
    fe = mod.ForgettingEngine(decay_rate=0.9)
    old = datetime.now(timezone.utc) - timedelta(days=10)
    memories = [{"id": "1", "strength": 1.0, "last_accessed": old}]
    fe.apply_decay(memories)
    assert memories[0]["strength"] < 1.0


def test_prune_removes_weak(tmp_project):
    mod = _load(tmp_project)
    fe = mod.ForgettingEngine(prune_threshold=0.5)
    memories = [
        {"id": "strong", "strength": 0.9},
        {"id": "weak", "strength": 0.1},
    ]
    kept = fe.prune(memories)
    ids = {m["id"] for m in kept}
    assert "strong" in ids
    assert "weak" not in ids


def test_capacity_enforcement(tmp_project):
    mod = _load(tmp_project)
    fe = mod.ForgettingEngine(max_items=2)
    memories = [
        {"id": "a", "strength": 0.9, "salience": 0.9},   # score 0.81
        {"id": "b", "strength": 0.8, "salience": 0.8},   # score 0.64
        {"id": "c", "strength": 0.1, "salience": 0.1},   # score 0.01
    ]
    kept = fe.enforce_capacity(memories)
    assert len(kept) == 2
    ids = {m["id"] for m in kept}
    assert ids == {"a", "b"}
