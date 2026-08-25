# brainos CLI

Install brain-inspired memory plugins into your AI agent project.

## Install

```bash
pip install brainos

```

Or install from source:

```bash
cd cli/
pip install -e .

```

## Usage

```bash
# List all plugins
brainos list

# Initialize project structure
brainos init

# Add a plugin
brainos add sensory-gate
brainos add hippocampal-index --with-config --with-tests

# Add all plugins
brainos add all

# Plugin details
brainos info attention-filter

```

## What gets generated

```
your-project/
  brainos_plugins/
    __init__.py
    sensory_gate.py        <- Working Python class
    attention_filter.py
  config/
    sensory_gate.yaml      <- Config template
  tests/
    test_sensory_gate.py   <- Test skeleton

```

## Plugins

| Name | Brain Analog | Saves |
| --- | --- | --- |
| sensory-gate | Thalamic Filter | 50-80% tokens |
| attention-filter | Selective Attention | 40-70% tokens |
| working-memory | Prefrontal WM | 25-45% tokens |
| hippocampal-index | Hippocampus | 20-40% tokens |
| consolidator | Sleep Consolidation | 60-80% storage |
| episodic-store | Episodic Memory | - |
| semantic-store | Knowledge Graph | - |
| procedural-cache | Basal Ganglia | 30-50% tokens |
| salience-tagger | Amygdala | 20-40% tokens |
| forgetting-engine | Active Forgetting | Prevents bloat |
| dmn-incubator | Default Mode Network | - |
| metacognition | Prefrontal Monitor | Compounds |

