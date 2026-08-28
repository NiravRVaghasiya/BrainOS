"""Tests for the generated attention-filter plugin."""

import importlib
from datetime import datetime, timedelta


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.attention_filter")


def test_budget_respected(tmp_project):
    mod = _load(tmp_project)
    af = mod.AttentionFilter(token_budget=100)
    now = datetime.now()
    items = [
        mod.ContextItem(content=f"item {i}", token_count=40, timestamp=now, salience=0.5)
        for i in range(10)
    ]
    selected = af.filter(items)
    assert sum(i.token_count for i in selected) <= 100


def test_higher_salience_preferred(tmp_project):
    mod = _load(tmp_project)
    # Budget only fits one item; the higher-salience one should win.
    af = mod.AttentionFilter(token_budget=50)
    now = datetime.now()
    low = mod.ContextItem(content="low", token_count=50, timestamp=now, salience=0.1)
    high = mod.ContextItem(content="high", token_count=50, timestamp=now, salience=0.9)
    selected = af.filter([low, high])
    assert len(selected) == 1
    assert selected[0].content == "high"


def test_recency_decay(tmp_project):
    mod = _load(tmp_project)
    af = mod.AttentionFilter(half_life_hours=24.0)
    recent = mod.ContextItem(content="recent", token_count=10,
                             timestamp=datetime.now(), salience=0.5)
    old = mod.ContextItem(content="old", token_count=10,
                          timestamp=datetime.now() - timedelta(days=10), salience=0.5)
    assert af._score(recent, None) > af._score(old, None)
