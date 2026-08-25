# 📅 Plugin: Episodic Store

> **Brain Analog**: Episodic Memory (hippocampus → temporal cortex)
> **Problem It Solves**: Agent has no memory of WHAT HAPPENED (past conversations, events, interactions).
> **Use Case**: "What did we discuss last week?" / "Remember when I asked about X?"

## What It Does

Stores and retrieves EVENTS — timestamped, contextualized records of what happened.
Like human episodic memory: WHO did WHAT, WHEN, WHERE, and HOW it felt.

```python
class EpisodicStore:
    def __init__(self, config):
        self.vector_db: VectorDB
        self.timeline: TimelineIndex
        self.entity_index: EntityIndex
    
    def store_episode(self, episode: Episode):
        """Store a new experience with full context."""
        record = EpisodicRecord(
            id=generate_id(),
            timestamp=episode.timestamp,
            participants=episode.participants,     # WHO
            content=episode.content,               # WHAT  
            context=episode.context,               # WHERE (channel, file, meeting)
            goal=episode.goal,                     # WHY (user's intent)
            outcome=episode.outcome,               # HOW it resolved
            emotional_valence=episode.importance,  # HOW important
            embedding=self.embed(episode.content),
            conversation_id=episode.conversation_id
        )
        self.vector_db.upsert(record)
        self.timeline.insert(record)
        self.entity_index.link(record)
    
    def recall(self, query: str, filters: EpisodicFilters = None) -> list[Episode]:
        """Retrieve relevant past episodes."""
        results = self.vector_db.hybrid_search(
            query=query,
            filters=filters,  # time range, participants, context
            top_k=5
        )
        return [self.reconstruct_episode(r) for r in results]
    
    def recall_timeline(self, start: datetime, end: datetime) -> list[Episode]:
        """Retrieve episodes in chronological order (time-based recall)."""
        return self.timeline.range_query(start, end)
    
    def recall_about_entity(self, entity: str) -> list[Episode]:
        """Everything that involved this person/project/topic."""
        return self.entity_index.get_episodes(entity)
```

## Episode Schema

```python
@dataclass
class Episode:
    # Identity
    id: str
    conversation_id: str
    
    # Context (WHERE/WHEN)
    timestamp: datetime
    context: str  # "slack #engineering" / "email thread" / "document review"
    
    # Content (WHAT)
    summary: str             # Compressed version (for retrieval display)
    content: str             # Full content (for reconstruction)
    key_decisions: list[str] # Extracted decisions
    action_items: list[str]  # Extracted todos
    
    # Participants (WHO)
    participants: list[str]
    
    # Significance (HOW IMPORTANT)
    importance: float        # 0-1 salience score
    outcome: str             # How it resolved
    
    # Retrieval aids
    embedding: np.ndarray
    tags: list[str]
    entities_mentioned: list[str]
```

## When to Install

✅ Agent needs to remember past conversations (multi-session continuity)
✅ User asks "what did we discuss?" / "remember when?"
✅ Agent needs to track what happened over time (timeline queries)
✅ Project context accumulates across sessions (not just within one)
