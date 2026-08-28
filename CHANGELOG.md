# Changelog

All notable changes to BrainOS will be documented here.

## [1.1.0] - 2026-08-28

### Added

- All 12 plugins now generate complete, working implementations
- Full pytest test suite (40+ tests)
- Working demo agent (examples/01_memory_agent/)
- Token savings benchmark with real numbers (examples/02_token_benchmark/)
- GitHub Actions CI (Python 3.10-3.12)
- Architecture diagrams (docs/assets/)
- Framework integration guide (docs/INTEGRATION_GUIDE.md)
- Makefile for common operations

### Fixed

- Duplicate 07_language_networks entry in README architecture tree
- Build artifacts removed from version control
- Added .gitignore

## [1.0.0] - 2026-08-25

### 🎉 Initial Release

#### Core Architecture (8 Brain Regions)
- `01_sensory_buffer/` — Iconic, echoic, and haptic memory buffers
- `02_working_memory/` — Baddeley's model, theta-gamma coupling, central executive
- `03_hippocampus/` — Trisynaptic circuit, LTP, place cells, consolidation
- `04_long_term_memory/` — Explicit (episodic + semantic) and Implicit (procedural + priming + conditioning)
- `05_emotional_tagging/` — Amygdala modulation, inverted-U, fear conditioning
- `06_motor_memory/` — Cerebellum, basal ganglia, automaticity stages
- `07_language_networks/` — Dual-stream model, mental lexicon, production pipeline
- `08_default_mode_network/` — DMN-TPN anti-correlation, incubation, future simulation

#### Support Systems
- `_system/` — Neurotransmitters, sleep consolidation, neuroplasticity, forgetting mechanisms

#### Information Flow Pathways (`_flows/`)
- 8 detailed pathway files mapping data movement between all brain systems
- Complete timing breakdowns (ms-by-ms processing)
- Cross-system interaction matrix

#### Practical Techniques (`_techniques/`)
- 10 evidence-based learning methods with effectiveness rankings
- Each tied to specific neuroscience mechanisms
- Protocols, schedules, and implementation guides

#### AI Plugins (`_plugins/`)
- 12 brain-inspired architecture components for AI/Agent systems
- Python interfaces with full method signatures
- Configuration templates and integration patterns
- Token savings estimates per plugin
