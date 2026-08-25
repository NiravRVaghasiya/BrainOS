<div align="center">

# 🧠 BrainOS

### The Human Brain as a Software Architecture

**A complete knowledge repository that maps neuroscience to engineering —<br>from neurons to production-ready AI memory systems.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![PyPI](https://img.shields.io/badge/pip%20install-brainos-orange.svg)](cli/)
[![Docs](https://img.shields.io/badge/docs-90%20files-purple.svg)](#repository-structure)
[![Stars](https://img.shields.io/github/stars/niravvaghasiya/brainos?style=social)](https://github.com/niravvaghasiya/brainos)

<br>

*"The brain is not a filing cabinet. It's a living, rewiring, pattern-matching network."*

<br>

[Explore the Architecture](#-architecture) · [Install via CLI](#-install) · [Browse Plugins](#-plugins-brain-inspired-ai-components) · [Learn a Technique](#-techniques-evidence-based-methods) · [Understand the Flows](#-flows-information-pathways)

</div>

---

## 🤔 What Is This?

**BrainOS** treats the human brain as a software system and documents it like one:

| If you're a... | You'll use this for... |
|---|---|
| 🤖 **AI/ML Engineer** | Brain-inspired memory architecture plugins for your agents |
| 🧑‍🎓 **Student** | Evidence-based study techniques grounded in neuroscience |
| 🧠 **Neuroscience Learner** | Structured, code-like understanding of brain systems |
| 🏗️ **Systems Architect** | Bio-inspired patterns for retrieval, caching, and orchestration |

**No paywall. No fluff. Just 90 markdown files of structured knowledge you can actually use.**

---

## ⚡ Install

### Via CLI (scaffold plugins into your project)

```bash
pip install brainos
```

```bash
# See all 12 plugins
brainos list

# Initialize project structure
brainos init

# Add a specific plugin (generates working Python class + config + tests)
brainos add sensory-gate --with-config --with-tests

# Add all plugins at once
brainos add all

# Get details about any plugin
brainos info hippocampal-index
```

### Or just read the docs

Clone and explore — zero dependencies, pure markdown:

```bash
git clone https://github.com/niravvaghasiya/BrainOS.git
cd BrainOS
```

> Each plugin in `_plugins/` is a complete architecture spec. The CLI generates starter code from these specs into your project.

---

## 📐 Architecture

The brain's information storage system, mapped as 8 numbered modules + 4 support systems:

```
brainos/
│
├── 01_sensory_buffer/          → Input preprocessing (200ms–3s buffer)
├── 02_working_memory/          → Active workspace (4±1 slots, 15–30s)
├── 03_hippocampus/             → Indexer & Consolidation Router
├── 04_long_term_memory/        → Permanent distributed storage (~2.5 PB)
│   ├── explicit_declarative/   → Conscious recall (episodic + semantic)
│   └── implicit_nondeclarative/→ Unconscious (procedural + priming + conditioning)
├── 05_emotional_tagging/       → Priority scoring (amygdala)
├── 06_motor_memory/            → Cerebellum (body autopilot)
├── 07_language_networks/       → Broca + Wernicke (speech/comprehension)
├── 07_language_networks/       → Broca + Wernicke (speech/comprehension)
├── 08_default_mode_network/    → Background processing (creativity, simulation)
│
├── _system/                    → Infrastructure (neurotransmitters, sleep, plasticity)
├── _flows/                     → Information pathways between systems
├── _techniques/                → Evidence-based learning methods
├── _plugins/                   → Brain-inspired AI/Agent component specs
└── cli/                        → pip-installable CLI (brainos add <plugin>)
```

Every module contains:
- `README.md` — What it does and how it works
- `mechanisms.md` — Biological machinery (molecular → circuit level)
- `examples.md` — Real-world demonstrations and experiments
- `failures.md` — Disorders, decay, and what breaks

---

## 🔌 Plugins: Brain-Inspired AI Components

> **The killer feature.** Each brain system is translated into an installable architecture component for AI agents.

| Plugin | Brain Analog | What It Does | Token Savings |
|--------|-------------|-------------|---------------|
| [`sensory-gate`](_plugins/01_sensory_gate.md) | Thalamic Filter | Pre-filter raw tool/API outputs | 50-80% |
| [`attention-filter`](_plugins/02_attention_filter.md) | Selective Attention | Score & rank context by relevance | 40-70% |
| [`working-memory`](_plugins/03_working_memory_manager.md) | Prefrontal WM | 4-6 slot active state scratchpad | 25-45% |
| [`hippocampal-index`](_plugins/04_hippocampal_index.md) | Hippocampus | Embed + bind + pattern-complete retrieval | 20-40% |
| [`consolidator`](_plugins/05_consolidator.md) | Sleep Consolidation | Offline summarize, dedupe, extract patterns | 60-80% storage |
| [`episodic-store`](_plugins/06_episodic_store.md) | Episodic Memory | Event memory (WHO/WHAT/WHEN/WHERE) | — |
| [`semantic-store`](_plugins/07_semantic_store.md) | Knowledge Graph | Persistent facts + relationships | — |
| [`procedural-cache`](_plugins/08_procedural_cache.md) | Basal Ganglia | Cache action sequences, skip re-reasoning | 30-50% |
| [`salience-tagger`](_plugins/09_salience_tagger.md) | Amygdala | Priority-score memories at storage time | 20-40% |
| [`forgetting-engine`](_plugins/10_forgetting_engine.md) | Active Forgetting | TTL, decay, pruning (bounded growth) | ∞ (prevents bloat) |
| [`dmn-incubator`](_plugins/11_dmn_incubator.md) | Default Mode Network | Background insight generation | — |
| [`metacognition`](_plugins/12_metacognition_monitor.md) | Prefrontal Monitor | Self-eval + strategy selection | Compounds |

### Quick Start: Which plugins solve your problem?

```
Context window overflows?     → sensory-gate + attention-filter + forgetting-engine
Agent forgets conversations?  → episodic-store + consolidator
Redundant tool calls?         → procedural-cache + pattern-separator
Can't find relevant context?  → hippocampal-index + salience-tagger
No self-improvement?          → metacognition + dmn-incubator
```

Each plugin includes a **Python interface**, **implementation patterns**, **YAML config**, and **integration examples**.

---

## 🛠️ Techniques: Evidence-Based Methods

> For humans who want to learn better — backed by the neuroscience in this repo.

| # | Technique | Effectiveness | Key Insight |
|---|-----------|--------------|-------------|
| 01 | [Spaced Repetition](_techniques/01_spaced_repetition.md) | ★★★★★ | Intervene at the point of forgetting |
| 02 | [Active Recall](_techniques/02_active_recall.md) | ★★★★★ | Testing > re-reading by 2x |
| 03 | [Method of Loci](_techniques/03_method_of_loci.md) | ★★★★☆ | Hijack hippocampal spatial indexing |
| 04 | [Chunking](_techniques/04_chunking_strategies.md) | ★★★★☆ | Compress items to fit WM slots |
| 05 | [Elaborative Encoding](_techniques/05_elaborative_encoding.md) | ★★★★☆ | Depth of processing = durability |
| 06 | [Sleep Optimization](_techniques/06_sleep_optimization.md) | ★★★★☆ | Study before sleep, not after waking |
| 07 | [Interleaving](_techniques/07_interleaving.md) | ★★★★☆ | Mix topics for better discrimination |
| 08 | [Dual Coding](_techniques/08_dual_coding.md) | ★★★☆☆ | Words + images = 2x encoding |
| 09 | [Exercise & Memory](_techniques/09_exercise_and_memory.md) | ★★★★☆ | 30 min aerobic = BDNF → hippocampal growth |
| 10 | [Meta-Learning](_techniques/10_meta_learning.md) | ★★★★★ | Learning how to learn (the master skill) |

---

## 🔀 Flows: Information Pathways

> How data moves BETWEEN systems — from first contact to permanent storage to recall.

| Flow | What It Maps | Key Timing |
|------|-------------|-----------|
| [Encoding](_flows/01_encoding_pathway.md) | World → Sensory → Attention → WM → Hippocampus | 0 → 500ms |
| [Consolidation](_flows/02_consolidation_pathway.md) | Hippocampus → Sleep replay → Cortical permanence | Hours → Years |
| [Retrieval](_flows/03_retrieval_pathway.md) | Cue → Pattern completion → Reconstruction | 200ms → 2s |
| [Emotional Modulation](_flows/04_emotional_modulation.md) | Amygdala amplifies/blocks at every stage | 12ms (fast path) |
| [Motor Learning](_flows/05_motor_learning_pathway.md) | Cortex → Basal Ganglia → Cerebellum → Auto | Days → Permanent |
| [Language Pipeline](_flows/06_language_processing_pipeline.md) | Sound → Phonemes → Words → Syntax → Meaning | 0 → 400ms |
| [Forgetting](_flows/07_forgetting_pathway.md) | Decay, interference, pruning, suppression | Hours → Years |
| [Cross-System](_flows/08_cross_system_interactions.md) | Full communication matrix + real-time walkthrough | Parallel |

---

## 📊 Key Principles

| # | Principle | Implication |
|---|-----------|-------------|
| 1 | **Distributed Storage** | No single neuron holds a memory — patterns across networks |
| 2 | **Associative Indexing** | Memories link by meaning, not by address |
| 3 | **Reconstruction ≠ Playback** | Recall rebuilds from fragments + context + inference |
| 4 | **Use-It-or-Lose-It** | Synapses weaken without reactivation (forgetting = feature) |
| 5 | **Emotional Priority** | Amygdala tags "important" → fast-tracked consolidation |
| 6 | **Sleep = Save** | Consolidation happens offline during deep sleep & REM |
| 7 | **Capacity Limits = Features** | 4-slot WM forces prioritization → better decisions |

---

## 📈 By the Numbers

| Metric | Value |
|--------|-------|
| Total files | 100+ |
| Total size | ~350 KB |
| CLI installable | `pip install brainos` |
| Brain regions covered | 8 primary + 4 support systems |
| Information flow pathways | 8 |
| Practical techniques | 10 |
| Installable AI plugins | 12 |
| Disorders/failures documented | 50+ |
| Real-world examples | 80+ |
| Research citations | 100+ |

---

## 🧭 How to Navigate

**I want to understand a brain region:**
```
01_sensory_buffer/README.md → mechanisms.md → examples.md → failures.md
```

**I want to build better AI memory:**
```
_plugins/README.md → Pick your problem → Install the plugin(s)
```

**I want to study more effectively:**
```
_techniques/README.md → Pick by effectiveness rating → Follow the protocol
```

**I want to understand information flow:**
```
_flows/README.md → Follow the numbered pathway → See cross-system interactions
```

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas especially open for contribution:
- 🔬 Additional research citations and experiment descriptions
- 🧪 Plugin implementations (Python packages from the architecture specs)
- 📊 Diagrams and visualizations of pathways
- 🌍 Translations
- 🧑‍⚕️ Clinical case studies for the `failures.md` files

---

## 📄 License

MIT License — see [LICENSE](LICENSE). Use freely, build on it, credit appreciated.

---

## ⭐ Star History

If this helped you understand brains, build better AI, or study more effectively — consider starring the repo.

---

<div align="center">

**Built by [Nirav Vaghasiya](https://linkedin.com/in/niravrvaghasiya)**

*Neuroscience × Software Architecture × AI Memory Systems*

</div>
