"""Tests for the generated salience-tagger plugin."""

import importlib


def _load(tmp_project):
    return importlib.import_module("brainos_plugins.salience_tagger")


def test_score_range(tmp_project):
    mod = _load(tmp_project)
    st = mod.SalienceTagger()
    for content in ["", "a plain sentence", "URGENT critical deadline decision"]:
        score = st.score(content, {})
        assert 0.0 <= score <= 1.0


def test_keywords_boost(tmp_project):
    mod = _load(tmp_project)
    st = mod.SalienceTagger()
    high = st.score("urgent deadline for the critical decision", {})
    low = st.score("nice weather outside today", {})
    assert high > low


def test_custom_weights(tmp_project):
    mod = _load(tmp_project)
    content = "urgent deadline blocker"

    keyword_heavy = mod.SalienceTagger(weights={
        "recency": 0.0, "frequency": 0.0, "entity_density": 0.0, "keywords": 1.0,
    })
    keyword_light = mod.SalienceTagger(weights={
        "recency": 1.0, "frequency": 0.0, "entity_density": 0.0, "keywords": 0.0,
    })
    # Keyword-only weighting should rate this keyword-rich, low-recency content
    # differently than recency-only weighting.
    assert keyword_heavy.score(content, {}) != keyword_light.score(content, {})
