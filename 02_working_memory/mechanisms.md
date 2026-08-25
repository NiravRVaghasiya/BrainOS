# ⚙️ Working Memory — Mechanisms

## Neural Basis: Persistent Firing

### The Core Mechanism: Delay-Period Activity
- Neurons in Prefrontal Cortex (PFC) fire CONTINUOUSLY while holding an item in mind
- This is metabolically expensive → strict capacity limits (4±1 items)
- Each "slot" = a distinct population of PFC neurons maintaining a representation

### Supporting Evidence (Electrophysiology):
- Fuster (1971): Recorded PFC neurons firing during delay periods in monkeys
- Goldman-Rakic: Showed different PFC columns hold different items simultaneously
- Modern fMRI: Dorsolateral PFC (DLPFC) activation scales with working memory load

## Baddeley's Model — Neural Correlates

```
COMPONENT                 BRAIN REGION              MECHANISM
─────────────────────────────────────────────────────────────────
Central Executive      → DLPFC (BA 9/46)         → Attention allocation
Phonological Loop      → Left BA 40 + BA 44       → Rehearsal circuit
Visuospatial Sketchpad → Right posterior parietal  → Spatial maintenance
Episodic Buffer        → Hippocampus + anterior PFC→ Binding across modalities
```

## How Capacity is Limited

### The Biased Competition Model:
1. Multiple items compete for PFC representation
2. Attention biases competition toward relevant items
3. Winners maintain firing; losers get suppressed (lateral inhibition)
4. Adding items → competition increases → representation quality degrades
5. At ~4 items: Signal-to-noise ratio collapses → information lost

### Why 4 and Not More?
- Each maintained item produces oscillatory interference with others
- Items are stored as gamma bursts (~30-80 Hz) nested within theta cycles (~4-8 Hz)
- One theta cycle can carry ~4-7 gamma bursts → capacity limit!
- This is the **theta-gamma coupling** model (Lisman & Jensen, 2013)

## Theta-Gamma Coupling (Storage Mechanism)

```
Theta wave (4-8 Hz):  ╱╲___╱╲___╱╲___╱╲___
                     /    ╲   /    ╲
Gamma bursts:     ∿∿∿∿  ∿∿∿∿  ∿∿∿∿  ∿∿∿∿   ← Each = 1 item
                  Item1 Item2 Item3 Item4
```

- Each gamma burst (~30-80 Hz) within a theta cycle = one memory item
- Items are separated in TIME, not space (phase coding)
- First item fires at theta peak, next at descending phase, etc.
- This temporal ordering explains why serial position matters in memory

## Refreshing / Maintenance

### Rehearsal (Phonological Loop):
- Subvocal articulation reactivates decaying phonological traces
- Speed of rehearsal = limiting factor (word-length effect)
- Loop time: ~1.5-2 seconds → items that can be said in this time are maintained

### Attentional Refreshing (Central Executive):
- Brief attentional "pulses" re-boost decaying representations
- Functions like a juggler — quickly visiting each item in rotation
- Different from rehearsal: works for non-verbal items too

## Gating Mechanism (What Gets In?)

### Prefrontal-Basal Ganglia Gate:
1. Basal ganglia tonically INHIBITS thalamus → default state = gate CLOSED
2. Dopamine signal = "this input is relevant" → gate OPENS briefly
3. Item enters PFC and begins sustained firing
4. Gate CLOSES again → protects contents from distraction
5. Too much dopamine → gate too open → distractibility (ADHD, mania)
6. Too little dopamine → gate too closed → can't update (rigidity)
