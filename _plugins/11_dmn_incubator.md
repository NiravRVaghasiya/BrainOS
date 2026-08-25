# 💭 Plugin: DMN Incubator (Background Processing)

> **Brain Analog**: Default Mode Network (creative connections, pattern finding)
> **Problem It Solves**: Agent only processes when directly prompted — misses connections.
> **Use Case**: Background enrichment, cross-conversation insights, proactive suggestions.

## What It Does

Runs BETWEEN conversations (or on idle) to:
- Find connections between unrelated memories
- Generate proactive insights
- Pre-compute likely next steps
- Identify patterns the user hasn't asked about

```python
class DMNIncubator:
    def __init__(self, config):
        self.memory_store: MemoryStore
        self.knowledge_graph: KnowledgeGraph
        self.insight_queue: InsightQueue
        self.llm: LLMClient
    
    async def run_incubation(self):
        """Background processing — find non-obvious connections."""
        
        # 1. Cross-topic connection finding
        recent = self.memory_store.get_recent(days=7)
        clusters = self.cluster_by_topic(recent)
        for pair in combinations(clusters, 2):
            connection = await self.find_bridge(pair[0], pair[1])
            if connection.strength > 0.7:
                self.insight_queue.add(connection)
        
        # 2. Pattern detection across time
        patterns = await self.detect_recurring_patterns(
            self.memory_store.get_recent(days=30)
        )
        for pattern in patterns:
            self.insight_queue.add(Insight(
                type="pattern",
                content=f"I've noticed: {pattern.description}",
                confidence=pattern.confidence
            ))
        
        # 3. Proactive preparation
        upcoming = self.calendar.get_upcoming(hours=24)
        for event in upcoming:
            briefing = await self.prepare_briefing(event)
            self.insight_queue.add(briefing)
    
    async def find_bridge(self, topic_a, topic_b) -> Connection:
        """Find non-obvious connections between two topics."""
        prompt = f"Given these two topics the user has been working on:\n"
                 f"Topic A: {topic_a.summary}\n"
                 f"Topic B: {topic_b.summary}\n"
                 f"Is there a useful connection, insight, or action item?"
        return await self.llm.generate(prompt)
```

## When to Install

✅ You want your agent to PROACTIVELY surface insights (not just respond)
✅ Cross-conversation pattern detection (user behaviors, recurring themes)
✅ Pre-computation of likely needs (predictive context loading)
✅ Creative connection finding between disparate topics
