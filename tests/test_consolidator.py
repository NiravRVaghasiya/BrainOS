"""Tests for the generated consolidator plugin."""

import importlib
from datetime import datetime, timezone


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.consolidator")


def _mem(id, content, salience=0.5):
    return {
        "id": id,
        "content": content,
        "timestamp": datetime.now(timezone.utc),
        "salience": salience,
        "access_count": 1,
        "bindings": {},
    }


def test_dedup_removes_near_duplicates(tmp_project):
    mod = _load(tmp_project)
    c = mod.Consolidator(similarity_threshold=0.85)
    memories = [
        _mem("1", "The deployment failed because of a network timeout"),
        _mem("2", "The deployment failed because of a network timeout!"),
        _mem("3", "Completely unrelated note about lunch"),
    ]
    out = c.deduplicate(memories)
    assert len(out) == 2


def test_merge_combines_content(tmp_project):
    mod = _load(tmp_project)
    c = mod.Consolidator()
    group = [
        _mem("a", "short version", salience=0.4),
        _mem("b", "a much longer and more detailed version", salience=0.6),
    ]
    merged = c.merge(group)
    # merged_from records both sources; content comes from one of them.
    assert set(merged["merged_from"]) == {"a", "b"}
    assert merged["content"] in {"short version", "a much longer and more detailed version"}
    assert merged["content"]


def test_compress_truncates(tmp_project):
    mod = _load(tmp_project)
    c = mod.Consolidator()
    long_mem = _mem("big", "y" * 2000)
    compressed = c.compress(long_mem)
    assert len(compressed["content"]) <= c.config.max_chars + 3  # allow "..."
    assert compressed.get("compressed") is True
