"""Tests for the generated sensory-gate plugin."""

import importlib
import json


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.sensory_gate")


def test_json_extraction(tmp_project):
    mod = _load(tmp_project)
    gate = mod.SensoryGate()
    raw = json.dumps({
        "data": [1, 2, 3],
        "metadata": {"page": 1},
        "pagination": {"next": None},
    })
    result = gate.process(raw, content_type="json")
    # Only extract_fields (data/results/items) should survive.
    assert "data" in result["content"]
    assert "metadata" not in result["content"]
    assert "pagination" not in result["content"]


def test_noise_removal(tmp_project):
    mod = _load(tmp_project)
    gate = mod.SensoryGate()
    raw = "line one\n\n   \nline two\n"
    result = gate.process(raw, content_type="text")
    lines = [ln for ln in result["content"].split("\n") if ln != ""]
    assert "line one" in result["content"]
    assert "line two" in result["content"]
    # Blank/whitespace-only lines are dropped.
    assert all(ln.strip() != "" for ln in lines)


def test_budget_enforcement(tmp_project):
    mod = _load(tmp_project)
    cfg = mod.GateConfig(max_tokens_per_input=10)
    gate = mod.SensoryGate(cfg)
    raw = "x" * 1000
    result = gate.process(raw, content_type="text")
    assert len(result["content"]) <= 10 * 4


def test_ratio_calculation(tmp_project):
    mod = _load(tmp_project)
    gate = mod.SensoryGate()
    raw = "hello world this is a test"
    result = gate.process(raw, content_type="text")
    expected = round(len(result["content"]) / max(len(raw), 1), 2)
    assert result["ratio"] == expected
    assert 0.0 <= result["ratio"] <= 1.0
