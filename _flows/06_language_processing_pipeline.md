# 🗣️ Language Processing Pipeline — Sound to Meaning

> From air vibrations to understanding — in ~400 milliseconds.

## Comprehension Pipeline (Hearing → Understanding)

```
TIME:    0ms        50ms       150ms       250ms        400ms       600ms+
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE:   Acoustic → Phonemic → Lexical  → Syntactic → Semantic → Pragmatic
         analysis   decoding   access     parsing     composit.  inference
         
WHAT:    Frequency  Identify   Find word  Build       Compose    Context,
         + timing   speech     in mental  sentence    meaning    intention,
         analysis   sounds     dictionary structure   from parts implicature
         
WHERE:   A1/Belt   STG/STS   Middle      Broca's +   Angular    R.Hemisphere
         areas                Temporal    L.Parietal  Gyrus +    + PFC
                              Gyrus                    mPFC

INPUT:   Waveform   /k/ /æ/ /t/  "cat"    [NP [Det the] Sentence    "She meant
                                           [N cat]]     meaning     the OPPOSITE"
                                                        computed    (sarcasm)
```

## Production Pipeline (Thought → Speech)

```
THOUGHT/INTENTION
        ↓
┌───────────────────────────────────────────────────┐
│  1. CONCEPTUAL PREPARATION (~600ms before speech)  │
│     "I want to express the concept of [cat]"       │
│     Select what to say, in what order               │
└────────────────────────┬──────────────────────────┘
                         ↓
┌───────────────────────────────────────────────────┐
│  2. LEMMA SELECTION (~400ms before speech)          │
│     Select abstract word form: CAT (noun, animate)  │
│     This is where tip-of-tongue FAILS               │
│     (concept activated but lemma can't be accessed) │
└────────────────────────┬──────────────────────────┘
                         ↓
┌───────────────────────────────────────────────────┐
│  3. PHONOLOGICAL ENCODING (~250ms before speech)    │
│     Assemble sound sequence: /k/ + /æ/ + /t/       │
│     Assign stress, rhythm, intonation               │
│     Syllabify: [kæt]                                │
└────────────────────────┬──────────────────────────┘
                         ↓
┌───────────────────────────────────────────────────┐
│  4. PHONETIC ENCODING (~100ms before speech)        │
│     Retrieve motor programs for each phoneme        │
│     Coarticulation planning (smooth transitions)    │
│     Load into articulatory buffer                   │
└────────────────────────┬──────────────────────────┘
                         ↓
┌───────────────────────────────────────────────────┐
│  5. ARTICULATION (speech onset = 0ms)               │
│     100+ muscles execute in coordinated sequence    │
│     Jaw, tongue, lips, larynx, diaphragm           │
│     + SELF-MONITORING (inner/outer loop)            │
│     Detect errors → correct within ~150ms           │
└───────────────────────────────────────────────────┘
```

## Reading Pipeline (Text → Meaning)

```
FIXATION ON WORD (eyes land)
        ↓ (0ms)
┌─────────────────────────────────────────────┐
│  VISUAL FEATURE EXTRACTION                   │
│  Identify letters, letter combinations       │
│  Visual Word Form Area (VWFA) in L. fusiform │
└──────────────────────┬──────────────────────┘
        ↓ (~100ms)
┌───────────────────────────────────────────────────────┐
│  DUAL ROUTE ACTIVATION (in parallel):                  │
│                                                        │
│  ROUTE 1: Direct / Lexical          ROUTE 2: Phonological │
│  (whole-word recognition)           (letter-to-sound rules) │
│  ┌─────────────────────┐           ┌─────────────────────┐ │
│  │ Visual word form     │           │ Grapheme-to-phoneme  │ │
│  │ matched to stored    │           │ conversion rules     │ │
│  │ orthographic entry   │           │ "C-A-T" → /k/-/æ/-/t/│ │
│  │ → meaning directly   │           │ → sound → meaning    │ │
│  └─────────────────────┘           └─────────────────────┘ │
│                                                        │
│  FAST for known words               ESSENTIAL for new words │
│  FAILS for new words                SLOW but flexible       │
│  Used by: Expert readers            Used by: Beginners      │
└──────────────────────┬────────────────────────────────┘
        ↓ (~200-350ms)
┌─────────────────────────────────────────────┐
│  SEMANTIC ACCESS + SYNTACTIC INTEGRATION     │
│  Word meaning retrieved + integrated into    │
│  sentence context being built                │
│  Eye moves to next word (~250ms fixation)    │
└─────────────────────────────────────────────┘
```

## Bilingual Processing

```
BILINGUAL SPEAKER (Both languages ALWAYS active):

Input: "cat"
        ↓
┌────────────────────────────────────────────────┐
│  LANGUAGE-NONSELECTIVE LEXICAL ACCESS           │
│                                                  │
│  English lexicon:  CAT ████████ (high activation)│
│  Spanish lexicon:  GATO ████░░░ (partial activation!)│
│                                                  │
│  Both activate! Even when only one is "needed"   │
└────────────────────┬───────────────────────────┘
                     ↓
┌────────────────────────────────────────────────┐
│  LANGUAGE CONTROL (Left DLPFC + anterior cingulate) │
│  • Suppress non-target language                  │
│  • Select target language output                 │
│  • Monitor for intrusion errors                  │
│  • COSTLY: This is why bilinguals have slower    │
│    lexical access but better executive control   │
└────────────────────────────────────────────────┘

LANGUAGE SWITCHING:
Target: English → Spanish
Cost: ~200-300ms "switch tax" (reconfigure control settings)
More costly: Switching FROM dominant TO weaker language
             (must suppress the stronger competitor)
```
