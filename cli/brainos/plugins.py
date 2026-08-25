"""Plugin registry for BrainOS CLI."""

PLUGINS = {
    "sensory-gate": {
        "brain_analog": "Thalamic Filter",
        "token_savings": "50-80%",
        "description": "Pre-filter raw tool/API outputs before they reach the LLM",
        "dependencies": [],
    },
    "attention-filter": {
        "brain_analog": "Selective Attention",
        "token_savings": "40-70%",
        "description": "Score and rank context items by relevance to current task",
        "dependencies": ["numpy", "sentence-transformers"],
    },
    "working-memory": {
        "brain_analog": "Prefrontal WM (4 slots)",
        "token_savings": "25-45%",
        "description": "Fixed-slot scratchpad for active goals, results, constraints",
        "dependencies": [],
    },
    "hippocampal-index": {
        "brain_analog": "Hippocampus",
        "token_savings": "20-40%",
        "description": "Embed + bind + pattern-complete retrieval with context graphs",
        "dependencies": ["chromadb", "sentence-transformers", "networkx"],
    },
    "consolidator": {
        "brain_analog": "Sleep Consolidation",
        "token_savings": "60-80% storage",
        "description": "Offline summarize, deduplicate, extract patterns",
        "dependencies": [],
    },
    "episodic-store": {
        "brain_analog": "Episodic Memory",
        "token_savings": "-",
        "description": "Event memory with WHO/WHAT/WHEN/WHERE bindings",
        "dependencies": ["chromadb"],
    },
    "semantic-store": {
        "brain_analog": "Knowledge Graph",
        "token_savings": "-",
        "description": "Persistent facts and relationships",
        "dependencies": ["networkx"],
    },
    "procedural-cache": {
        "brain_analog": "Basal Ganglia",
        "token_savings": "30-50%",
        "description": "Cache successful action sequences, skip re-reasoning",
        "dependencies": [],
    },
    "salience-tagger": {
        "brain_analog": "Amygdala",
        "token_savings": "20-40%",
        "description": "Priority-score memories at write-time",
        "dependencies": [],
    },
    "forgetting-engine": {
        "brain_analog": "Active Forgetting",
        "token_savings": "Prevents bloat",
        "description": "TTL, access-based decay, capacity limits",
        "dependencies": [],
    },
    "dmn-incubator": {
        "brain_analog": "Default Mode Network",
        "token_savings": "-",
        "description": "Background processing for cross-topic insights",
        "dependencies": [],
    },
    "metacognition": {
        "brain_analog": "Prefrontal Monitor",
        "token_savings": "Compounds",
        "description": "Self-eval, confidence calibration, strategy selection",
        "dependencies": [],
    },
}
