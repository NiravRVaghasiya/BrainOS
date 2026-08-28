"""Tests for the plugin code generator."""

import importlib

from brainos.generator import generate_plugin
from brainos.plugins import PLUGINS


def test_all_plugins_generate_valid_python():
    for name in PLUGINS:
        code = generate_plugin(name)
        # Raises SyntaxError if the generated source is invalid.
        compile(code, f"<{name}>", "exec")


def test_all_plugins_importable(tmp_project):
    for name in PLUGINS:
        module_name = f"brainos_plugins.{name.replace('-', '_')}"
        mod = importlib.import_module(module_name)
        assert mod is not None
