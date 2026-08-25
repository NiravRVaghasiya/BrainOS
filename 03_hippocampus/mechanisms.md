# ⚙️ Hippocampus — Mechanisms

## Anatomy: The Trisynaptic Circuit

```
Input from Cortex (Entorhinal Cortex)
         ↓
┌─────────────────────┐
│  DENTATE GYRUS (DG) │  ← Pattern Separation
│  (Sparse coding)     │     Orthogonalizes similar inputs
└─────────┬───────────┘
          ↓ (Mossy fibers)
┌─────────────────────┐
│       CA3            │  ← Pattern Completion (Auto-associator)
│  (Recurrent network) │     Partial cue → full memory
└─────────┬───────────┘
          ↓ (Schaffer collaterals)
┌─────────────────────┐
│       CA1            │  ← Comparator / Output
│  (Mismatch detector) │     Compares prediction with reality
└─────────┬───────────┘
          ↓
  Output to Cortex (for consolidation)
```

## Long-Term Potentiation (LTP) — How Synapses Strengthen

### The Molecular Cascade:
1. **Pre-synaptic neuron** releases glutamate
2. **AMPA receptors** open → small depolarization
3. **IF** post-synaptic cell is ALSO depolarized (coincidence!) →
4. **NMDA receptor** unblocks (Mg²⁺ plug removed by voltage) → Ca²⁺ floods in
5. **Ca²⁺ influx** activates CaMKII (kinase enzyme)
6. **CaMKII** → inserts MORE AMPA receptors into the synapse
7. **Result**: Same signal now produces BIGGER response = STRONGER CONNECTION

### Why NMDA is the "Coincidence Detector":
- Requires BOTH pre-synaptic glutamate AND post-synaptic depolarization
- This IS Hebb's Rule in molecular form: "Neurons that fire together, wire together"
- Without coincidence → no LTP → no memory

### Early vs. Late LTP:
| Phase | Duration | Mechanism | Requires |
|-------|----------|-----------|----------|
| Early LTP (E-LTP) | 1-3 hours | Existing protein modification | Nothing special |
| Late LTP (L-LTP) | Hours → permanent | New protein synthesis + structural growth | Gene transcription, BDNF |

## Place Cells and Cognitive Maps

### Place Cells (O'Keefe, 1971 — Nobel Prize 2014):
- Individual hippocampal neurons fire when animal is at a SPECIFIC location
- Each cell = one "place field"
- Population of cells = complete map of environment
- New environment → new map (remapping)

### Grid Cells (Entorhinal Cortex, Moser & Moser — Nobel 2014):
- Fire in a hexagonal grid pattern across space
- Provide the COORDINATE SYSTEM that place cells reference
- Like GPS triangulation for the brain

### Time Cells:
- Some hippocampal neurons encode WHEN in a sequence (not where)
- Fire at specific time points during a delay interval
- Provides temporal scaffolding for episodic memories

## Replay and Consolidation

### Sharp-Wave Ripples (SWRs):
- During rest/sleep: Hippocampus generates 150-250 Hz oscillatory bursts
- During each ripple: Place cells replay recent experience IN SEQUENCE
- Replay is compressed (20x faster than real-time)
- Cortex "listens" during ripples and strengthens corresponding connections

### Two-Stage Consolidation Model:
1. **Encoding (awake)**: Fast hippocampal learning (sparse, pattern-separated)
2. **Consolidation (sleep)**: Slow cortical learning (interleaved replay avoids catastrophic forgetting)
3. **Independence**: Over weeks/months, cortical connections strengthen enough → hippocampus no longer needed
4. **Result**: Old memories survive hippocampal damage; new memories don't

## Neurogenesis (New Neurons!)
- **Location**: Dentate gyrus (one of only 2 brain regions with adult neurogenesis)
- **Rate**: ~700 new neurons/day in humans (declines with age)
- **Function**: New neurons improve pattern separation (fresh, uncontaminated coding)
- **Enhanced by**: Exercise, learning, enriched environments
- **Suppressed by**: Chronic stress, aging, depression
