# 🔥 Plugin: Salience Tagger

> **Brain Analog**: Amygdala (emotional significance detector)
> **Problem It Solves**: All memories treated equally → retrieval returns noise.
> **Token Savings**: 20-40% (retrieve high-signal items first, skip low-salience).

## What It Does

Scores every piece of information by IMPORTANCE before storage.
High-salience items get priority in retrieval, consolidation, and context injection.

```python
class SalienceTagger:
    def __init__(self, config):
        self.classifier: ImportanceClassifier
        self.user_signals: UserSignalTracker
    
    def score(self, content: str, context: EventContext) -> float:
        """Score content importance from 0.0 (noise) to 1.0 (critical)."""
        signals = {
            "user_explicit": self.detect_explicit_importance(content),
            # "Remember this", "Important:", "Don't forget", action items
            
            "decision_made": self.detect_decision(content),
            # Choices, commitments, plans, deadlines
            
            "novel_information": self.detect_novelty(content, context),
            # First time seeing this entity/fact (vs. repeated info)
            
            "emotional_weight": self.detect_emotion(content),
            # Frustration, urgency, excitement (user affect signals)
            
            "task_relevance": self.detect_task_relevance(content, context.current_goal),
            # Directly relevant to what we're trying to accomplish
            
            "entity_density": self.count_named_entities(content) / len(content.split()),
            # Dense with specific names, dates, numbers = factual content
            
            "user_engagement": self.measure_engagement(context),
            # Long message, multiple questions, follow-ups = high engagement
        }
        
        # Weighted combination
        weights = {"user_explicit": 5, "decision_made": 4, "novel_information": 3,
                   "emotional_weight": 2, "task_relevance": 3, 
                   "entity_density": 1, "user_engagement": 1}
        
        score = sum(signals[k] * weights[k] for k in signals) / sum(weights.values())
        return min(1.0, max(0.0, score))

    def tag(self, memory: MemoryRecord) -> MemoryRecord:
        """Attach salience score to a memory before storage."""
        memory.salience = self.score(memory.content, memory.context)
        memory.salience_reasons = self.explain_score(memory)
        return memory
```

## Salience Signals (What Makes Something "Important")

```yaml
high_salience_signals:
  - User explicitly says "remember this" / "important" / "don't forget"
  - Decisions made ("let's go with option B")
  - Deadlines mentioned ("due by Friday")
  - Action items created ("I need to...")
  - Errors/failures (what went wrong — avoid repeating)
  - Preferences stated ("I prefer..." / "always do X")
  - Novel entities first mentioned (new person, project, concept)
  - Emotional intensity (frustration, urgency, excitement)

low_salience_signals:
  - Greetings, filler ("hey", "thanks", "ok sounds good")
  - Repeated information (already known/stored)
  - Transient context (weather, time-of-day references)
  - Meta-conversation ("let me think...", "hmm")
  - Generic questions with generic answers
```

## When to Install

✅ Retrieval returns too much noise (low-quality matches crowd out important ones)
✅ You want importance-weighted forgetting (low salience decays first)
✅ Memory store needs prioritization (not all memories are equal)
✅ You want to detect "user really cares about this" signals automatically
