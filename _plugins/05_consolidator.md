# 💤 Plugin: Consolidator (Offline Memory Processing)

> **Brain Analog**: Sleep Consolidation (SWS replay + REM integration)
> **Problem It Solves**: Raw memories accumulate endlessly, degrading retrieval quality.
> **Token Savings**: 60-80% storage reduction; faster retrieval.

## What It Does

Runs OFFLINE (background job / cron / post-conversation) to:
1. **Summarize** verbose memories into compressed representations
2. **Deduplicate** overlapping memories
3. **Extract patterns** across multiple experiences
4. **Promote** important memories (strengthen) / **Decay** unimportant ones
5. **Integrate** new knowledge into existing schemas

```
RAW MEMORY STORE (100 conversation turns, 50K tokens)
        ↓ (Background consolidation job)
┌──────────────────────────────────────────────────────────┐
│                   CONSOLIDATOR                             │
│                                                           │
│  PASS 1: Summarize (compression)                          │
│    "10 messages about project X" → "Key decisions: A, B"  │
│                                                           │
│  PASS 2: Deduplicate (pattern separation)                 │
│    "User mentioned deadline 3× in different words"        │
│    → Single canonical entry: "Deadline: March 15"         │
│                                                           │
│  PASS 3: Extract (pattern recognition)                    │
│    "User always asks for bullet points"                   │
│    → New preference: format=bullets                       │
│                                                           │
│  PASS 4: Strengthen/Decay (importance weighting)          │
│    Accessed 5× this week → salience ↑                     │
│    Not accessed in 30 days → salience ↓ (or delete)       │
│                                                           │
│  PASS 5: Integrate (schema assimilation)                  │
│    New fact connects to existing knowledge graph node      │
│    → Create relationship edge                             │
│                                                           │
└──────────────────────────────────────────────────────────┘
        ↓
CONSOLIDATED STORE (20 distilled entries, 5K tokens)
  + Knowledge graph updates
  + Preference updates
  + Decayed/deleted entries
```

## Interface

```python
class Consolidator:
    def __init__(self, config: ConsolidationConfig):
        self.llm: LLMClient                    # For summarization
        self.memory_store: MemoryStore
        self.knowledge_graph: KnowledgeGraph
        self.preference_store: PreferenceStore
        self.schedule: CronSchedule            # When to run
    
    async def run_consolidation(self):
        """Full consolidation pass (like a night of sleep)."""
        # Phase 1: Compress (Slow-Wave Sleep analog)
        await self.compress_recent_memories()
        
        # Phase 2: Integrate (REM Sleep analog)
        await self.integrate_into_schemas()
        
        # Phase 3: Prune (Synaptic homeostasis)
        await self.decay_and_prune()
    
    async def compress_recent_memories(self):
        """Summarize raw conversation turns into distilled memories."""
        recent = self.memory_store.get_unconsolidated()
        
        # Group by topic/conversation
        grouped = self.cluster_by_topic(recent)
        
        for topic, memories in grouped.items():
            if len(memories) > 3:  # Worth summarizing
                summary = await self.llm.summarize(
                    memories,
                    instruction="Extract: key facts, decisions, action items, preferences. "
                               "Discard: filler, greetings, repeated info. "
                               "Be extremely concise."
                )
                # Replace N raw memories with 1 consolidated entry
                consolidated = ConsolidatedMemory(
                    content=summary,
                    source_ids=[m.id for m in memories],
                    topic=topic,
                    consolidated_at=now()
                )
                self.memory_store.replace(memories, consolidated)
    
    async def integrate_into_schemas(self):
        """Find patterns, extract preferences, update knowledge graph."""
        recent_consolidated = self.memory_store.get_recently_consolidated()
        
        # Extract entities and relationships
        for memory in recent_consolidated:
            entities = await self.extract_entities(memory)
            for entity in entities:
                self.knowledge_graph.upsert(entity)
        
        # Detect repeated patterns → promote to preferences
        patterns = self.detect_patterns(recent_consolidated)
        for pattern in patterns:
            if pattern.frequency >= 3:
                self.preference_store.add(pattern.as_preference())
    
    async def decay_and_prune(self):
        """Weaken unused memories, delete truly irrelevant ones."""
        all_memories = self.memory_store.get_all()
        for memory in all_memories:
            memory.salience *= self.decay_factor(memory)
            if memory.salience < self.pruning_threshold:
                self.memory_store.archive(memory)  # Don't hard delete — archive
```

## Consolidation Levels (Progressive Compression)

```
LEVEL 0 — RAW (full verbatim)
  "Hey can you help me with the quarterly report? I need the revenue
   numbers from Q3 broken down by region. Oh and also include YoY comparison.
   The format should be a table. Thanks!"
  [~50 tokens]

LEVEL 1 — COMPRESSED (key content)
  "User requested: Q3 revenue report, by region, with YoY comparison, table format"
  [~15 tokens, 70% reduction]

LEVEL 2 — FACTUAL (only extractable facts)
  "Task: Q3 revenue summary | Format: table | Breakdown: by region + YoY"
  [~12 tokens, 76% reduction]

LEVEL 3 — INDEXED (metadata only)
  {type: "request", topic: "revenue", period: "Q3", format: "table"}
  [~8 tokens, 84% reduction — content reconstructable from other sources]
```

## Scheduling

```yaml
consolidation:
  # Light pass: After every conversation ends
  post_conversation:
    - compress_if_longer_than: 10 turns
    - extract_preferences: true
    - extract_entities: true
  
  # Medium pass: Daily (like a nap)
  daily:
    schedule: "0 3 * * *"  # 3 AM
    operations:
      - deduplicate_similar_memories: {threshold: 0.92}
      - decay_unaccessed: {days: 7, factor: 0.8}
      - promote_frequently_accessed: {min_accesses: 5}
  
  # Deep pass: Weekly (like deep sleep)
  weekly:
    schedule: "0 4 * * 0"  # Sunday 4 AM
    operations:
      - full_summarization_pass: true
      - knowledge_graph_integration: true
      - prune_below_threshold: {salience: 0.1}
      - archive_old_raw: {older_than_days: 30}
      - compute_statistics: true
```

## When to Install This Plugin

✅ Memory store grows unbounded and retrieval quality degrades
✅ You're storing full conversation transcripts (expensive, slow to search)
✅ Agent needs to "learn" preferences over time (not just recall facts)
✅ Knowledge should compound across conversations (not start fresh each time)
✅ You need predictable storage costs (consolidation controls growth)
