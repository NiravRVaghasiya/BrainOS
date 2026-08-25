# 🪞 Plugin: Metacognition Monitor

> **Brain Analog**: Prefrontal metacognitive monitoring
> **Problem It Solves**: Agent can't evaluate its own performance or improve strategies.
> **Use Case**: Self-improvement, strategy selection, confidence calibration.

## What It Does

Monitors the agent's own performance and adapts strategies accordingly.
Like human metacognition: "Do I actually know this?" / "Is my approach working?"

```python
class MetacognitionMonitor:
    def __init__(self, config):
        self.strategy_log: StrategyLog
        self.confidence_calibrator: ConfidenceCalibrator
        self.performance_tracker: PerformanceTracker
    
    def evaluate_confidence(self, response: str, context: Context) -> float:
        """How confident should the agent be in this response?"""
        signals = {
            "source_quality": self.assess_sources(context.sources),
            "knowledge_coverage": self.assess_coverage(response, context.query),
            "internal_consistency": self.check_consistency(response, context.known_facts),
            "hedge_indicators": self.detect_uncertainty_language(response),
        }
        return self.confidence_calibrator.compute(signals)
    
    def select_strategy(self, task: Task) -> Strategy:
        """Based on past performance, which approach works best for this task type?"""
        task_type = self.classify_task(task)
        history = self.strategy_log.get_by_type(task_type)
        
        # Pick strategy with best success rate for this task type
        best = max(history, key=lambda s: s.success_rate)
        return best.strategy
    
    def post_task_reflection(self, task: Task, outcome: Outcome):
        """After completing a task, evaluate what worked and didn't."""
        reflection = {
            "task_type": self.classify_task(task),
            "strategy_used": task.strategy,
            "success": outcome.success,
            "tokens_used": outcome.tokens,
            "time_taken": outcome.duration,
            "user_feedback": outcome.feedback,
        }
        self.strategy_log.record(reflection)
        
        # Update strategy preferences
        if outcome.success:
            self.strategy_log.boost(task.strategy, task_type=reflection["task_type"])
        else:
            self.strategy_log.penalize(task.strategy, task_type=reflection["task_type"])
    
    def should_ask_for_help(self, confidence: float, task_importance: float) -> bool:
        """Know when to say 'I'm not sure' instead of confabulating."""
        # Low confidence + high importance = ask for clarification
        return confidence < 0.6 and task_importance > 0.7
```

## Self-Improvement Loop

```
TASK → Execute with strategy → Outcome → Reflect → Update strategy weights
                                    ↑                         ↓
                                    └── Next similar task ←───┘
                                        (use best strategy)
```

## When to Install

✅ Agent needs to improve over time (not just stay static)
✅ You want calibrated confidence (knows what it doesn't know)
✅ Different task types need different approaches (strategy selection)
✅ Agent should learn from failures (not repeat mistakes)
✅ You want honest "I'm not sure" instead of confabulation
