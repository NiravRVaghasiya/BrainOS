"""Tests for the generated working-memory plugin."""

import importlib


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.working_memory")


def test_update_and_read(tmp_project):
    mod = _load(tmp_project)
    wm = mod.WorkingMemory()
    wm.update("goal", "ship the feature")
    assert wm.read("goal") == "ship the feature"


def test_eviction_on_overflow(tmp_project):
    mod = _load(tmp_project)
    wm = mod.WorkingMemory(max_slots=2)
    wm.update("a", "alpha", priority=0.1)   # lowest priority
    wm.update("b", "bravo", priority=0.9)
    wm.update("c", "charlie", priority=0.8)  # triggers eviction of "a"
    assert wm.read("a") is None
    assert wm.read("b") == "bravo"
    assert wm.read("c") == "charlie"


def test_clear(tmp_project):
    mod = _load(tmp_project)
    wm = mod.WorkingMemory()
    wm.update("x", "value")
    wm.clear("x")
    assert wm.read("x") is None


def test_get_state_format(tmp_project):
    mod = _load(tmp_project)
    wm = mod.WorkingMemory()
    assert wm.get_state() == ""  # empty state
    wm.update("goal", "do the thing", priority=1.0)
    state = wm.get_state()
    assert state.startswith("## Working Memory")
    assert "**goal**" in state
    assert "do the thing" in state
