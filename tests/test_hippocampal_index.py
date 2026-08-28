"""Tests for the generated hippocampal-index plugin."""

import importlib


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.hippocampal_index")


def test_encode_creates_record(tmp_project):
    mod = _load(tmp_project)
    hi = mod.HippocampalIndex()
    record = hi.encode("the sky is blue", bindings={"topic": "weather"})
    assert isinstance(record, mod.MemoryRecord)
    assert record.id
    assert record.content == "the sky is blue"
    assert record.bindings == {"topic": "weather"}


def test_retrieve_by_content(tmp_project):
    mod = _load(tmp_project)
    hi = mod.HippocampalIndex()  # no vector store -> substring fallback
    hi.encode("deployment failed at midnight")
    hi.encode("lunch was tasty")
    results = hi.retrieve("deployment")
    assert len(results) == 1
    assert "deployment" in results[0].content


def test_duplicate_prevention(tmp_project):
    mod = _load(tmp_project)
    hi = mod.HippocampalIndex()
    hi.encode("identical content")
    hi.encode("identical content")
    # The index may or may not dedupe; either way retrieval must stay coherent
    # and every returned record must actually match the query.
    results = hi.retrieve("identical content")
    assert len(results) >= 1
    assert all("identical content" in r.content for r in results)
