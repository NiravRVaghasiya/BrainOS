# 🔌 Brain-Inspired Plugins for AI Systems

> Every brain system maps to an installable component for your AI/Agent project. Install what you need. Each plugin reduces token waste, improves recall, and adds intelligence.

## The Plugin Registry

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BRAIN-INSPIRED AI PLUGIN STACK                             │
│                                                                              │
│  LAYER 1: INPUT PROCESSING                                                   │
│  ┌──────────────────┐  ┌────────────────────┐  ┌─────────────────────────┐  │
│  │ sensory-gate     │  │ attention-filter    │  │ chunker                 │  │
│  │ (preprocessing)  │  │ (relevance scoring) │  │ (context compression)   │  │
│  └──────────────────┘  └────────────────────┘  └─────────────────────────┘  │
│                                                                              │
│  LAYER 2: ACTIVE CONTEXT                                                     │
│  ┌──────────────────┐  ┌────────────────────┐  ┌─────────────────────────┐  │
│  │ working-memory   │  │ context-window-mgr  │  │ executive-router        │  │
│  │ (slot manager)   │  │ (token budgeting)   │  │ (task orchestration)    │  │
│  └──────────────────┘  └────────────────────┘  └─────────────────────────┘  │
│                                                                              │
│  LAYER 3: INDEXING & CONSOLIDATION                                           │
│  ┌──────────────────┐  ┌────────────────────┐  ┌─────────────────────────┐  │
│  │ hippocampal-index│  │ consolidator       │  │ pattern-separator       │  │
│  │ (embed + route)  │  │ (summarize + store)│  │ (dedup + distinguish)   │  │
│  └──────────────────┘  └────────────────────┘  └─────────────────────────┘  │
│                                                                              │
│  LAYER 4: LONG-TERM STORAGE                                                  │
│  ┌──────────────────┐  ┌────────────────────┐  ┌─────────────────────────┐  │
│  │ episodic-store   │  │ semantic-store      │  │ procedural-cache        │  │
│  │ (event memory)   │  │ (knowledge graph)   │  │ (skill/tool memory)     │  │
│  └──────────────────┘  └────────────────────┘  └─────────────────────────┘  │
│                                                                              │
│  LAYER 5: MODULATION & OPTIMIZATION                                          │
│  ┌──────────────────┐  ┌────────────────────┐  ┌─────────────────────────┐  │
│  │ salience-tagger  │  │ forgetting-engine   │  │ sleep-consolidator      │  │
│  │ (priority flags) │  │ (TTL + pruning)     │  │ (offline enrichment)    │  │
│  └──────────────────┘  └────────────────────┘  └─────────────────────────┘  │
│                                                                              │
│  LAYER 6: META / ORCHESTRATION                                               │
│  ┌──────────────────┐  ┌────────────────────┐  ┌─────────────────────────┐  │
│  │ dmn-incubator    │  │ multi-agent-cortex  │  │ metacognition-monitor   │  │
│  │ (background      │  │ (specialized agent  │  │ (self-eval + strategy   │  │
│  │  processing)     │  │  routing)           │  │  selection)             │  │
│  └──────────────────┘  └────────────────────┘  └─────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

```

## Quick Install Guide (Pick What You Need)

| Problem | Install These Plugins | Token Savings |
| --- | --- | --- |
| Context window overflows | `attention-filter` + `chunker` + `forgetting-engine` | 40-70% |
| Agent forgets past conversations | `episodic-store` + `consolidator` | N/A (adds recall) |
| Redundant tool calls | `procedural-cache` + `pattern-separator` | 30-50% |
| Can't find relevant context | `hippocampal-index` + `salience-tagger` | 20-40% |
| Slow multi-step reasoning | `working-memory` + `executive-router` | 25-45% |
| No persistent knowledge | `semantic-store` + `sleep-consolidator` | Long-term ROI |
| Information overload from tools | `sensory-gate` + `attention-filter` | 50-80% |
| Agent lacks self-improvement | `metacognition-monitor` + `dmn-incubator` | Compounds over time |

## Architecture Principles (From Neuroscience)

1. **Layered Processing** — Don't dump everything into the LLM. Pre-filter, compress, prioritize.
2. **Separation of Storage Systems** — Facts (semantic) ≠ Events (episodic) ≠ Skills (procedural). Store differently, retrieve differently.
3. **Active Forgetting** — Not storing everything is a FEATURE. TTL, decay, pruning = efficiency.
4. **Consolidation is Offline** — Background jobs that summarize, deduplicate, and compress stored memories.
5. **Retrieval is Reconstruction** — Don't try to return verbatim history. Reconstruct relevant context from fragments.
6. **Emotional Tagging = Priority Scoring** — Not all information is equal. Score and weight.
7. **Capacity Limits are Features** — The 4-slot working memory constraint FORCES prioritization. Embrace token budgets.

## Plugin Files

| # | Plugin | Brain Analog | File |
| --- | --- | --- | --- |
| 01 | Sensory Gate | Sensory Buffer + Thalamus | `01_sensory_gate.md` |
| 02 | Attention Filter | Selective Attention | `02_attention_filter.md` |
| 03 | Working Memory Manager | Prefrontal WM | `03_working_memory_manager.md` |
| 04 | Hippocampal Index | Hippocampus | `04_hippocampal_index.md` |
| 05 | Consolidator | Sleep Consolidation | `05_consolidator.md` |
| 06 | Episodic Store | Episodic Memory | `06_episodic_store.md` |
| 07 | Semantic Store | Semantic Memory / KG | `07_semantic_store.md` |
| 08 | Procedural Cache | Procedural Memory | `08_procedural_cache.md` |
| 09 | Salience Tagger | Amygdala | `09_salience_tagger.md` |
| 10 | Forgetting Engine | Active Forgetting | `10_forgetting_engine.md` |
| 11 | DMN Incubator | Default Mode Network | `11_dmn_incubator.md` |
| 12 | Metacognition Monitor | Prefrontal Monitoring | `12_metacognition_monitor.md` |

