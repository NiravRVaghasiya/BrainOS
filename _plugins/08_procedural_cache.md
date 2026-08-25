# ⚡ Plugin: Procedural Cache

> **Brain Analog**: Procedural Memory (Basal Ganglia + Cerebellum)
> **Problem It Solves**: Agent re-reasons common patterns from scratch every time.
> **Token Savings**: 30-50% (skip reasoning for cached procedures).

## What It Does

Caches SUCCESSFUL action sequences so the agent can replay them without re-reasoning.
Like muscle memory: once you've solved a type of problem, just execute — don't re-think.

```python
class ProceduralCache:
    def __init__(self, config):
        self.procedure_store: dict[str, Procedure]
        self.pattern_matcher: PatternMatcher
        self.success_tracker: SuccessTracker
    
    def check_cache(self, task: Task) -> Optional[Procedure]:
        """Does a cached procedure match this task?"""
        pattern = self.pattern_matcher.extract_pattern(task)
        match = self.procedure_store.get(pattern)
        if match and match.success_rate > 0.85:
            return match  # Execute directly, skip reasoning
        return None  # No cache hit — reason from scratch
    
    def record_success(self, task: Task, steps: list[Step], outcome: Outcome):
        """After successful task completion, cache the procedure."""
        if outcome.success:
            pattern = self.pattern_matcher.extract_pattern(task)
            procedure = Procedure(
                pattern=pattern,
                steps=steps,
                success_count=1,
                template=self.templatize(steps)  # Parameterize for reuse
            )
            self.procedure_store.upsert(pattern, procedure)
    
    def execute_cached(self, procedure: Procedure, task: Task) -> Outcome:
        """Execute cached procedure with current task's parameters."""
        # Fill template with current parameters
        concrete_steps = procedure.template.fill(task.parameters)
        # Execute steps directly (no LLM reasoning needed!)
        for step in concrete_steps:
            step.execute()
        return Outcome(success=True, method="cached_procedure")

# Example cached procedure:
# Pattern: "send_email(to, subject, body)"
# Template: [compose_email(to={to}, subject={subject}, body={body}), send(), confirm()]
# On match: Execute directly. No LLM call needed. Saves 500+ tokens.
```

## When to Install

✅ Agent performs the same task patterns repeatedly (email, scheduling, lookups)
✅ You want sub-second responses for common operations
✅ Token costs are dominated by re-reasoning known procedures
✅ Agent should get FASTER over time (not stay constant)
