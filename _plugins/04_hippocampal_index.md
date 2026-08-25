# 🗂️ Plugin: Hippocampal Index

> **Brain Analog**: Hippocampus (indexer, router, pattern completer)
> **Problem It Solves**: Can't find the right memory/context when you need it.
> **Token Savings**: 20-40% (retrieve precisely instead of stuffing everything).

## What It Does

Like the real hippocampus: it DOESN'T store the memories themselves.
It stores an INDEX that can find and reconstruct any memory from a partial cue.

```
NEW EXPERIENCE (message, tool output, document)
        ↓
┌──────────────────────────────────────────────────────┐
│              HIPPOCAMPAL INDEX                         │
│                                                       │
│  1. ENCODE: Generate embedding + metadata             │
│  2. PATTERN SEPARATE: Ensure distinctness from similar │
│  3. BIND: Link WHO + WHAT + WHEN + WHERE + WHY        │
│  4. INDEX: Store retrieval pointers                    │
│                                                       │
│  At retrieval time:                                    │
│  5. PATTERN COMPLETE: Partial cue → full memory        │
│  6. ROUTE: Send to appropriate storage system          │
│                                                       │
└──────────────────────────────────────────────────────┘
```

## Interface

```python
class HippocampalIndex:
    def __init__(self, config: IndexConfig):
        self.vector_store: VectorDB          # Embedding-based retrieval
        self.metadata_store: MetadataDB      # Structured attributes
        self.binding_graph: Graph            # Relationships between memories
        self.embedding_model: EmbeddingModel
    
    def encode(self, experience: Experience) -> MemoryRecord:
        """Index a new experience (conversation turn, tool output, document)."""
        # 1. Embed the content
        embedding = self.embedding_model.encode(experience.content)
        
        # 2. Pattern separation (ensure distinctness)
        similar = self.vector_store.query(embedding, top_k=3)
        if self.too_similar(similar, embedding):
            # Merge with existing (don't create duplicate)
            return self.merge_with_existing(similar[0], experience)
        
        # 3. Bind context (WHO/WHAT/WHEN/WHERE)
        bindings = self.extract_bindings(experience)
        
        # 4. Store index entry
        record = MemoryRecord(
            id=generate_id(),
            embedding=embedding,
            content_ref=experience.storage_location,  # Pointer, not content!
            bindings=bindings,
            timestamp=now(),
            salience=experience.salience_score,
            access_count=0
        )
        self.vector_store.upsert(record)
        self.metadata_store.upsert(record)
        self.binding_graph.add_node(record, edges=bindings)
        return record
    
    def retrieve(self, query: str, filters: dict = None, top_k: int = 5) -> list:
        """Pattern completion: partial cue → relevant memories."""
        query_embedding = self.embedding_model.encode(query)
        
        # Hybrid retrieval: vector similarity + metadata filters + graph traversal
        vector_results = self.vector_store.query(query_embedding, top_k=top_k*3)
        
        if filters:
            vector_results = self.apply_metadata_filters(vector_results, filters)
        
        # Graph expansion: Follow bindings for related context
        expanded = self.expand_via_graph(vector_results, hops=1)
        
        # Re-rank by combined score
        ranked = self.rerank(expanded, query_embedding)
        return ranked[:top_k]
    
    def pattern_separate(self, new_record, existing_similar):
        """Ensure new memory is stored distinctly from similar ones."""
        # Add discriminating metadata: WHAT makes this one DIFFERENT?
        distinguishing_features = self.compute_distinction(new_record, existing_similar)
        new_record.bindings["distinguishing"] = distinguishing_features
        # e.g., "This is about TUESDAY's meeting, not Monday's"
```

## The Binding Structure (Episodic Context)

```python
@dataclass
class MemoryBindings:
    who: list[str]       # People involved
    what: str            # Topic/content summary
    when: datetime       # Timestamp
    where: str           # Context (channel, file, meeting)
    why: str             # Goal/intention at the time
    emotional_tag: float # Salience score (0-1)
    
    # Enables queries like:
    # "What did Alice say about the budget?" → filter: who=Alice, what~=budget
    # "What happened in yesterday's meeting?" → filter: when=yesterday, where=meeting
    # "What was that important decision?" → filter: emotional_tag > 0.8
```

## Pattern Completion (The Magic)

```python
def pattern_complete(self, partial_cue: str) -> list[Memory]:
    """
    Like smelling cookies and remembering grandma's kitchen.
    A PARTIAL cue activates the FULL associated memory.
    """
    # Step 1: Find memories that partially match the cue
    candidates = self.retrieve(partial_cue, top_k=10)
    
    # Step 2: For each candidate, reconstruct the full context
    completed = []
    for candidate in candidates:
        # Follow binding graph to get associated memories
        context = self.binding_graph.get_neighborhood(candidate.id, hops=1)
        full_memory = self.reconstruct(candidate, context)
        completed.append(full_memory)
    
    return completed
```

## When to Install This Plugin

✅ You need retrieval over conversation history (not just RAG over documents)
✅ Simple vector search returns too many false positives
✅ You need contextual retrieval ("what did X say about Y in context Z?")
✅ Your agent needs to distinguish between similar-but-different memories
✅ You want graph-based memory traversal (follow relationships)
