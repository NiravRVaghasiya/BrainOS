"""Tests for the generated metacognition plugin."""

import importlib


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.metacognition")


def test_predict_and_outcome(tmp_project):
    mod = _load(tmp_project)
    mc = mod.MetacognitionMonitor()
    mc.predict("task-1", 0.8)
    mc.record_outcome("task-1", True)  # should not raise


def test_calibration_error(tmp_project):
    mod = _load(tmp_project)

    perfect = mod.MetacognitionMonitor()
    perfect.predict("t1", 1.0)
    perfect.record_outcome("t1", True)
    perfect.predict("t2", 0.0)
    perfect.record_outcome("t2", False)
    assert perfect.calibration_error() == 0.0

    wrong = mod.MetacognitionMonitor()
    wrong.predict("t1", 1.0)
    wrong.record_outcome("t1", False)
    wrong.predict("t2", 1.0)
    wrong.record_outcome("t2", False)
    assert wrong.calibration_error() > 0.5


def test_strategy_selection(tmp_project):
    mod = _load(tmp_project)
    mc = mod.MetacognitionMonitor()
    mc.register_strategy("fast", ["parsing"])
    mc.register_strategy("careful", ["parsing"])
    # "careful" performs better on parsing tasks historically.
    mc.record_strategy_outcome("careful", "parsing", True)
    mc.record_strategy_outcome("careful", "parsing", True)
    mc.record_strategy_outcome("fast", "parsing", False)
    assert mc.select_strategy("parsing") == "careful"
