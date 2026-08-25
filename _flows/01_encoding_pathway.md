# 📥 Encoding Pathway — From World to Memory

> The journey of a new experience from sensory contact to hippocampal registration.

## The Full Encoding Pipeline

```
STEP 1          STEP 2           STEP 3           STEP 4            STEP 5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRANSDUCTION    SENSORY BUFFER   ATTENTION GATE   WORKING MEMORY    HIPPOCAMPAL
                                                                     ENCODING
                                                                     
Photons →       Iconic store     Selective        Maintained in     Bound into
 electrical     (~250ms)         attention        PFC (~4 items,    coherent
 signal                          filters          15-30s)           episode &
                                                                    indexed
Sound →         Echoic store     Top-down &       Rehearsed &       
 neural code    (~3-4s)          bottom-up        manipulated       Synaptic
                                 competition                        tagging for
Touch →         Haptic store                      Chunked &         consolidation
 spike trains   (~2s)                             integrated        
                                                                    
Duration:       Duration:        Duration:        Duration:         Duration:
Instant         200ms-4s         50-200ms         15-30s            Seconds-minutes
                                 (selection)       (maintenance)     (registration)
```

## Step-by-Step Detail

### Step 1: Transduction (Receptor → Neural Code)
```
Physical energy → Specialized receptor → Graded potential → Action potential
```
- **Visual**: Photons → Retinal rods/cones → Bipolar cells → Ganglion cells → Optic nerve
- **Auditory**: Sound pressure → Hair cells (cochlea) → Auditory nerve
- **Olfactory**: Molecules → Olfactory receptors → Olfactory bulb (BYPASSES thalamus!)
- **Output**: Frequency-coded spike trains representing stimulus features

### Step 2: Sensory Buffer (Briefly Hold Everything)
```
ALL transduced input held for ~200ms-4s
├── Resolution: Complete (everything in the sensory field)
├── Format: Raw, uninterpreted features
├── Decay: Exponential (50% gone by ~100ms for visual)
└── Transfer: Only ATTENDED items pass through
```
- **Parallel processing**: Feature extraction happens automatically (edge detection, pitch analysis, texture)
- **Pre-attentive features detected**: Color, orientation, motion, loudness
- **NOT detected pre-attentively**: Conjunctions ("red AND square" requires attention)

### Step 3: Attention Gate (Select What Matters)

```
                    Bottom-Up (stimulus-driven)
                    ├── Sudden onset/movement
                    ├── Your name spoken
                    ├── Emotional faces
                    ├── Survival threats
                    ↓
SELECTION ← ─ ─ ─ COMPETITION ─ ─ ─ → SUPPRESSION
                    ↑                    (losers gated out)
                    Top-Down (goal-driven)
                    ├── Current task goals
                    ├── Expectations/predictions
                    ├── Search templates ("looking for red car")
                    └── Emotional priorities (anxious → threats)
```

**Neural mechanism**: 
- Frontal Eye Fields + DLPFC send bias signals to sensory cortex
- Bias amplifies target representation, suppresses distractors
- Pulvinar (thalamic nucleus) coordinates binding of attended features

### Step 4: Working Memory (Hold & Process)
```
ATTENDED INPUT → Enters PFC sustained firing
                      ↓
              ┌───────────────────────────────────┐
              │         WORKING MEMORY             │
              │                                    │
              │  [Item 1] [Item 2] [Item 3] [Item 4]  ← Capacity limit
              │                                    │
              │  Operations:                       │
              │  • Rehearsal (keeps items alive)    │
              │  • Binding (link features together)│
              │  • Manipulation (transform, compare)│
              │  • Decision (what to do with this?) │
              └───────────────────┬───────────────┘
                                  ↓
                      Hippocampal encoding
                      (if important enough)
```

**What determines transfer to hippocampus?**
- Repetition (rehearsed multiple times)
- Depth of processing (meaningful analysis > shallow perception)
- Emotional significance (amygdala modulation)
- Novelty (prediction error signals "this is new, encode it!")
- Intentional effort (deliberate memorization attempt)
- Connection to existing knowledge (schema activation)

### Step 5: Hippocampal Encoding (Bind & Index)
```
From Working Memory / Direct from sensory (for emotional events):
        ↓
┌─────────────────────────────────────────────────────────┐
│               HIPPOCAMPAL ENCODING                       │
│                                                          │
│  1. PATTERN SEPARATION (Dentate Gyrus)                   │
│     → Assign unique code to this specific experience     │
│     → Distinguish from similar previous experiences      │
│                                                          │
│  2. BINDING (CA3)                                        │
│     → Link all elements: WHO + WHAT + WHERE + WHEN + HOW │
│     → Create unified episode representation              │
│                                                          │
│  3. INDEXING (CA1 → Entorhinal Cortex)                   │
│     → Create retrieval pointers back to cortical traces  │
│     → Register associations (what connects to this?)     │
│                                                          │
│  4. SYNAPTIC TAGGING                                     │
│     → Mark active synapses for consolidation             │
│     → Start the clock: 1-2 hours to consolidate or lose  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Encoding Modifiers (What Changes the Flow)

### Depth of Processing (Craik & Lockhart, 1972)
```
SHALLOW ─────────────────────────────────────── DEEP

Physical     →    Phonological    →    Semantic
"Is it in    →    "Does it rhyme  →    "Does it fit
uppercase?"       with 'brain'?"       in this category?"

WEAK encoding ────────────────────── STRONG encoding
(surface features)                   (meaning, connections)
```

### The Encoding Specificity Principle
```
ENCODING CONTEXT                    RETRIEVAL CONTEXT
┌──────────────┐                    ┌──────────────┐
│ Physical     │                    │ Physical     │
│ environment  │── MATCH ═══════════│ environment  │ → GOOD recall
│ Mood state   │                    │ Mood state   │
│ Mental state │                    │ Mental state │
└──────────────┘                    └──────────────┘

MISMATCH between encoding and retrieval contexts → POOR recall
(even if the memory is intact — the retrieval cue doesn't find it)
```

## Speed of the Pipeline
| Stage | Latency | Bottleneck |
|-------|---------|-----------|
| Transduction | 1-50ms | Receptor type (vision=fast, pain=slow) |
| Sensory buffer | 0ms (immediate) | Capacity (unlimited but fleeting) |
| Attention selection | 50-200ms | Competition resolution time |
| WM encoding | ~300ms per item | Capacity (4 items max) |
| Hippocampal binding | ~500ms-2s | Theta cycle phase-locking |
| Synaptic tagging | ~seconds | Molecular signaling cascade |
| Consolidated → LTM | Hours (sleep required) | Protein synthesis |

## What BYPASSES the Normal Pipeline

### 1. Fear Conditioning (Amygdala Fast Track)
```
Threat stimulus → Thalamus → AMYGDALA (12ms!) → Fight/Flight response
                      └──→ Cortex (200ms) → "Oh it's just a stick"
                      
The fear memory is ALREADY FORMED before you consciously perceive the stimulus!
```

### 2. Procedural Learning (Basal Ganglia Track)
```
Motor sequence → Cortex → Basal Ganglia → Repeated → Automatic
                          (not hippocampus)
                          
This is why amnesics can learn motor skills — different pathway entirely.
```

### 3. Priming (Cortical Repetition Suppression)
```
Stimulus → Sensory cortex (less activation if seen before)
           No hippocampus needed. No conscious memory formed.
           Just: "This is familiar" signal from reduced neural effort.
```
