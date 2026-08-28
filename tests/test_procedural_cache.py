"""Tests for the generated procedural-cache plugin."""

import importlib


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.procedural_cache")


def _steps():
    return [{"tool": "http_get", "args": {"url": "/api"}, "result": "200 OK"}]


def test_cache_hit(tmp_project):
    mod = _load(tmp_project)
    pc = mod.ProceduralCache()
    pc.record("fetch the user profile from the api", _steps(), success=True)
    hit = pc.lookup("fetch the user profile from the api")
    assert hit == _steps()


def test_cache_miss(tmp_project):
    mod = _load(tmp_project)
    pc = mod.ProceduralCache(similarity_threshold=0.8)
    pc.record("fetch the user profile from the api", _steps(), success=True)
    assert pc.lookup("render a completely different chart widget") is None


def test_hit_rate(tmp_project):
    mod = _load(tmp_project)
    pc = mod.ProceduralCache(similarity_threshold=0.8)
    pc.record("fetch the user profile from the api", _steps(), success=True)
    pc.lookup("fetch the user profile from the api")   # hit
    pc.lookup("fetch the user profile from the api")   # hit
    pc.lookup("zzz totally unrelated task string")     # miss
    assert round(pc.hit_rate(), 2) == 0.67
