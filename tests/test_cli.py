"""CLI-level tests driven through subprocess."""

import subprocess
import sys

from brainos.plugins import PLUGINS


def _cli(args, cwd):
    return subprocess.run(
        [sys.executable, "-m", "brainos.cli", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


def test_list_command(tmp_path):
    result = _cli(["list"], tmp_path)
    assert result.returncode == 0, result.stderr
    for name in PLUGINS:
        assert name in result.stdout, f"{name} missing from `brainos list` output"


def test_add_single(tmp_path):
    result = _cli(["add", "sensory-gate"], tmp_path)
    assert result.returncode == 0, result.stderr
    plugin_file = tmp_path / "brainos_plugins" / "sensory_gate.py"
    assert plugin_file.exists()


def test_add_all(tmp_path):
    result = _cli(["add", "all"], tmp_path)
    assert result.returncode == 0, result.stderr
    plugin_dir = tmp_path / "brainos_plugins"
    py_files = [p for p in plugin_dir.glob("*.py") if p.name != "__init__.py"]
    assert len(py_files) == len(PLUGINS) == 12


def test_init(tmp_path):
    result = _cli(["init"], tmp_path)
    assert result.returncode == 0, result.stderr
    for d in ["brainos_plugins", "config", "tests"]:
        assert (tmp_path / d).is_dir(), f"{d}/ was not created"
