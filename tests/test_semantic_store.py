"""Tests for the generated semantic-store plugin."""

import importlib


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.semantic_store")


def test_add_and_query(tmp_project):
    mod = _load(tmp_project)
    ss = mod.SemanticStore()
    ss.add("Alice", "knows", "Bob")
    results = ss.query(subject="Alice")
    assert ("Alice", "knows", "Bob") in results
    assert len(results) == 1


def test_wildcard_query(tmp_project):
    mod = _load(tmp_project)
    ss = mod.SemanticStore()
    ss.add("Alice", "knows", "Bob")
    ss.add("Alice", "likes", "coffee")
    # predicate=None is a wildcard -> both triples for subject Alice.
    results = ss.query(subject="Alice", predicate=None)
    assert len(results) == 2
    predicates = {p for _, p, _ in results}
    assert predicates == {"knows", "likes"}


def test_neighbors(tmp_project):
    mod = _load(tmp_project)
    ss = mod.SemanticStore()
    ss.add("Alice", "knows", "Bob")
    ss.add("Alice", "knows", "Carol")
    ss.add("Bob", "knows", "Dan")  # 2 hops from Alice
    neighbors = ss.get_neighbors("Alice", hops=1)
    assert "Bob" in neighbors
    assert "Carol" in neighbors
    assert "Dan" not in neighbors
