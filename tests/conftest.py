"""Shared pytest fixtures for the BrainOS test suite."""

import importlib
import subprocess
import sys

import pytest


def _run_cli(args, cwd):
    """Run the brainos CLI via `python -m brainos.cli` and return CompletedProcess."""
    return subprocess.run(
        [sys.executable, "-m", "brainos.cli", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


@pytest.fixture
def run_cli():
    """Return a helper that runs the CLI in a given cwd (function-scoped)."""
    return _run_cli


@pytest.fixture(scope="session")
def _generated_project(tmp_path_factory):
    """Generate all 12 plugins once per session and expose them for import.

    The CLI is invoked a single time (`init` + `add all`); the resulting project
    root is placed on sys.path so `brainos_plugins.*` can be imported by any test.
    """
    root = tmp_path_factory.mktemp("brainos_project")

    init = _run_cli(["init"], root)
    assert init.returncode == 0, f"brainos init failed: {init.stderr}"
    add = _run_cli(["add", "all"], root)
    assert add.returncode == 0, f"brainos add all failed: {add.stderr}"

    project = str(root)
    sys.path.insert(0, project)
    # Ensure a stale brainos_plugins (e.g. from another dir) isn't shadowing ours.
    for mod in list(sys.modules):
        if mod == "brainos_plugins" or mod.startswith("brainos_plugins."):
            del sys.modules[mod]
    importlib.invalidate_caches()

    yield root

    for mod in list(sys.modules):
        if mod == "brainos_plugins" or mod.startswith("brainos_plugins."):
            del sys.modules[mod]
    if project in sys.path:
        sys.path.remove(project)


@pytest.fixture
def tmp_project(_generated_project):
    """Return the shared generated project root (see `_generated_project`).

    Plugin classes are stateless per-instance, so tests can safely share one
    generated copy; each test constructs its own plugin objects.
    """
    return _generated_project


@pytest.fixture
def all_plugins():
    """Return the list of all 12 plugin names from the registry."""
    from brainos.plugins import PLUGINS

    return list(PLUGINS.keys())
