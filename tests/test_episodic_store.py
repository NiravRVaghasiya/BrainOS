"""Tests for the generated episodic-store plugin."""

import importlib
from datetime import datetime, timezone, timedelta


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.episodic_store")


def test_record_and_query_by_binding(tmp_project):
    mod = _load(tmp_project)
    es = mod.EpisodicStore()
    es.record_event("greeted a colleague", who="Alice")
    es.record_event("filed a report", who="Bob")
    results = es.query_by_binding(who="Alice")
    assert len(results) == 1
    assert results[0]["bindings"]["who"] == "Alice"


def test_query_by_time(tmp_project):
    mod = _load(tmp_project)
    es = mod.EpisodicStore()
    old = datetime.now(timezone.utc) - timedelta(days=5)
    recent = datetime.now(timezone.utc) - timedelta(hours=1)
    es.record_event("old event", when=old)
    es.record_event("recent event", when=recent)

    start = datetime.now(timezone.utc) - timedelta(days=1)
    results = es.query_by_time(start)
    contents = {r["content"] for r in results}
    assert "recent event" in contents
    assert "old event" not in contents


def test_query_by_content(tmp_project):
    mod = _load(tmp_project)
    es = mod.EpisodicStore()
    es.record_event("database migration completed")
    es.record_event("coffee break")
    results = es.query_by_content("migration")
    assert len(results) == 1
    assert "migration" in results[0]["content"]
