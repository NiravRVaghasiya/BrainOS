# 📅 Spaced Repetition — Defeating the Forgetting Curve

> The single most evidence-backed study technique in cognitive science.
> Effect size: d = 0.42–0.79 across meta-analyses (massive for an educational intervention).

## The Neuroscience Behind It

### Why It Works (4 Mechanisms):

**1. Repeated Consolidation Cycles**
- Each review triggers a new round of hippocampal replay during subsequent sleep
- Multiple consolidation events = stronger cortical trace
- Like saving a file to multiple backup drives

**2. Desirable Difficulty**
- Retrieving at the POINT OF FORGETTING maximizes strengthening
- Easy retrieval (too soon) = minimal learning signal
- Impossible retrieval (too late) = just re-encoding from scratch
- Optimal: Just barely retrievable → maximum LTP potentiation

**3. Contextual Variability**
- Each spaced review occurs in a DIFFERENT context (different day, mood, environment)
- Multiple contexts encoded → more retrieval cues available later
- Massed practice = single context → fragile, context-dependent memory

**4. Synaptic Tagging + Protein Synthesis**
- First exposure creates synaptic tags
- Tags last ~1-2 hours waiting for consolidation proteins
- Spaced review REACTIVATES the tag → captures new proteins → strengthens further
- Each cycle builds structural resilience

## The Optimal Spacing Schedule

### Leitner System (Simple Box Method)
```
BOX 1: Review DAILY (new/difficult items)
 ↓ Got it right → moves to Box 2
BOX 2: Review every 3 DAYS
 ↓ Got it right → moves to Box 3
BOX 3: Review WEEKLY
 ↓ Got it right → moves to Box 4
BOX 4: Review every 2 WEEKS
 ↓ Got it right → moves to Box 5
BOX 5: Review MONTHLY

Got it WRONG at any box → BACK TO BOX 1

Simple, effective, no technology required.
```

### SuperMemo SM-2 Algorithm (Used by Anki)
```python
# Core algorithm:
interval(1) = 1 day
interval(2) = 6 days
interval(n) = interval(n-1) × EF

# EF (Easiness Factor) updated after each review:
EF_new = EF_old + (0.1 - (5 - quality) × (0.08 + (5 - quality) × 0.02))

# quality: 0 = total blackout, 5 = perfect recall
# EF minimum = 1.3 (never goes below)

# If quality < 3: Reset interval to 1 day (item needs relearning)
```

### Research-Backed Simple Schedule
```
After initial learning:
  Review 1:    1 day later     (24 hours)
  Review 2:    3 days later    (day 4)
  Review 3:    7 days later    (day 11)
  Review 4:   14 days later    (day 25)
  Review 5:   30 days later    (day 55)
  Review 6:   60 days later    (day 115)
  Review 7:  120 days later    (day 235)
  
After ~7 successful retrievals at expanding intervals:
  → Memory approaches "permastore" status (Bahrick, 1984)
  → Retrieve annually to maintain indefinitely
```

## Spacing Effect: The Data

```
Retention after 1 week:

MASSED (all at once):     ████████████░░░░░░░░░░░░░░░░  ~35%
SPACED (same total time): ████████████████████████░░░░░░  ~70%

Same total study time. DOUBLE the retention.
The only difference: WHEN you review.
```

## Practical Implementation

### Tool Options:
| Tool | Best For | Algorithm |
|------|----------|-----------|
| Anki | Language vocab, med school, facts | SM-2 |
| RemNote | Connected knowledge, documents | Modified SM-2 |
| Mnemosyne | Research-grade tracking | SM-2 |
| Physical flashcards + Leitner boxes | Low-tech, tactile learners | Leitner |
| Self-made spreadsheet | Custom tracking | Manual scheduling |

### Card Design Rules (Critical for Effectiveness):
1. **Minimum information principle**: One fact per card (atomic)
2. **Active cue, not passive**: "What is X?" not "X is [definition]"
3. **Use images**: Dual coding doubles retention
4. **Add context**: "In the context of Y, what is X?"
5. **Make it personal**: Connect to your experience
6. **Cloze deletions work**: "The hippocampus is responsible for ___"
7. **Avoid orphan cards**: Every card should connect to a bigger understanding

### What NOT to Put in SRS:
- Information you can easily look up and rarely need
- Complex procedures (use deliberate practice instead)
- Anything you don't understand yet (understand FIRST, then space)
- Entire paragraphs (too large — violates minimum information principle)

## Combining Spaced Repetition with Other Techniques

```
ENCODING PHASE:
  Elaborative interrogation + Dual coding + Chunking
  → Creates STRONG initial trace with multiple hooks
  
REVIEW PHASE (spaced):
  Active recall + Self-explanation + Interleaving
  → Each review strengthens via DIFFERENT pathways
  
SLEEP PHASE:
  Post-study sleep within 12 hours
  → Consolidation of the day's reviews
  
RESULT: Each technique multiplies the other's effectiveness
```

## The "20 Rules of Formulating Knowledge" (Piotr Wozniak, SuperMemo)
1. Do not learn if you do not understand
2. Learn before you memorize
3. Build upon the basics
4. Stick to the minimum information principle
5. Cloze deletion is simple and effective
6. Use imagery
7. Use mnemonic techniques
8. Graphic deletion is as good as cloze deletion
9. Avoid sets (use enumerations instead)
10. Avoid enumerations (break into atomic cards)
11. Combat interference (distinguish similar items explicitly)
12. Optimize wording (short, unambiguous)
13. Refer to other memories (cross-reference cards)
14. Personalize and provide examples
15. Rely on emotional states
16. Context cues simplify wording
17. Redundancy does not contradict minimum information
18. Provide sources (for verification)
19. Date-stamp volatile knowledge
20. Prioritize (not everything deserves SRS time)
