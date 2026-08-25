# 🎯 Plugin: Attention Filter

> **Brain Analog**: Selective Attention (top-down + bottom-up)
> **Problem It Solves**: Even after gating, too much competes for limited context.
> **Token Savings**: 40-70% of retrieved context tokens.

## What It Does

Scores and ranks ALL available context by RELEVANCE to the current task.
Only the top-N most relevant items enter the LLM's active context.

```
AVAILABLE CONTEXT (20 items, ~30,000 tokens)
├── Conversation history (10 messages)
├── Retrieved memories (5 items)
├── Tool results (3 outputs)
├── System instructions (2 blocks)
        ↓
┌──────────────────────────────────────┐
│         ATTENTION FILTER             │
│                                      │
│  Score each item:                    │
│  ┌──────────────────────────────┐    │
│  │ Relevance to current query   │ ×3 │  ← Top-down (goal-driven)
│  │ Recency (temporal decay)     │ ×2 │
│  │ Salience score (pre-tagged)  │ ×2 │  ← Bottom-up (importance)
│  │ Source authority              │ ×1 │
│  │ Uniqueness (non-redundant)   │ ×1 │
│  └──────────────────────────────┘    │
│                                      │
│  Rank → Select top items within      │
│  TOKEN BUDGET                        │
└──────────────────────────────────────┘
        ↓
ACTIVE CONTEXT (6 items, ~8,000 tokens) → LLM
```

## Interface

```python
class AttentionFilter:
    def __init__(self, config: AttentionConfig):
        self.token_budget: int = 8000
        self.embedding_model: EmbeddingModel
        self.scorer: RelevanceScorer
        self.weights: dict = {
            "semantic_relevance": 3.0,
            "recency": 2.0,
            "salience": 2.0,
            "authority": 1.0,
            "uniqueness": 1.0
        }
    
    def filter(
        self, 
        candidates: list[ContextItem],
        query: str,
        task_state: TaskState
    ) -> list[ContextItem]:
        """
        Score all candidates, return top items within token budget.
        Implements both top-down (query-driven) and bottom-up (salience) attention.
        """
        scored = []
        for item in candidates:
            score = self.compute_score(item, query, task_state)
            scored.append((score, item))
        
        scored.sort(reverse=True)
        
        # Greedy selection within budget
        selected = []
        tokens_used = 0
        for score, item in scored:
            if tokens_used + item.token_count <= self.token_budget:
                selected.append(item)
                tokens_used += item.token_count
        
        return selected
    
    def compute_score(self, item, query, task_state) -> float:
        scores = {
            "semantic_relevance": self.semantic_similarity(item, query),
            "recency": self.temporal_decay(item.timestamp),
            "salience": item.salience_score,  # Pre-computed by salience-tagger
            "authority": item.source_authority,
            "uniqueness": self.novelty_vs_selected(item)
        }
        return sum(scores[k] * self.weights[k] for k in scores)
```

## Scoring Functions

### Semantic Relevance (Top-Down Attention)
```python
def semantic_similarity(self, item: ContextItem, query: str) -> float:
    """Cosine similarity between query embedding and item embedding."""
    query_vec = self.embedding_model.encode(query)
    item_vec = item.embedding  # Pre-computed at storage time
    return cosine_similarity(query_vec, item_vec)
```

### Temporal Decay (Recency Bias)
```python
def temporal_decay(self, timestamp: datetime) -> float:
    """Exponential decay — recent items score higher."""
    age_hours = (now() - timestamp).total_seconds() / 3600
    half_life = 24  # Score halves every 24 hours
    return 0.5 ** (age_hours / half_life)
```

### Uniqueness (Redundancy Suppression)
```python
def novelty_vs_selected(self, item: ContextItem) -> float:
    """Penalize items that are semantically redundant with already-selected items."""
    if not self.selected_so_far:
        return 1.0
    max_sim = max(
        cosine_similarity(item.embedding, s.embedding) 
        for s in self.selected_so_far
    )
    return 1.0 - max_sim  # High similarity → low uniqueness score
```

## Advanced: Multi-Level Attention (Hierarchical)

```python
# Like the brain: Coarse attention first, fine attention second

class HierarchicalAttention:
    def filter(self, candidates, query, budget):
        # LEVEL 1: Category-level filter (fast, cheap)
        categories = self.categorize(candidates)  # Group by topic/type
        relevant_categories = self.score_categories(categories, query)
        pool = flatten(relevant_categories[:top_3])
        
        # LEVEL 2: Item-level scoring (slower, precise)
        scored = [(self.fine_score(item, query), item) for item in pool]
        scored.sort(reverse=True)
        
        # LEVEL 3: Token-budget packing (knapsack)
        return self.pack_within_budget(scored, budget)
```

## Configuration

```yaml
attention_filter:
  token_budget: 8000  # Max tokens fed to LLM per turn
  
  weights:
    semantic_relevance: 3.0
    recency: 2.0
    salience: 2.0
    authority: 1.0
    uniqueness: 1.0
  
  recency:
    half_life_hours: 24
    min_score: 0.05  # Floor (very old items still slightly accessible)
  
  diversity:
    min_uniqueness: 0.3  # Block items >70% similar to already-selected
  
  reserved_budget:
    system_prompt: 1500   # Always reserved
    last_user_message: 500  # Always included
    tool_instructions: 1000  # If tool calls planned
  
  fallback:
    if_no_relevant_context: "include_recent_3"  # Default to recency
```

## When to Install This Plugin

✅ You have multiple memory/retrieval sources competing for context
✅ RAG returns too many chunks and you're stuffing them all in
✅ Agent performance degrades as conversation grows (context noise)
✅ You need deterministic token budgeting (cost control)
✅ Different tasks need different context (not one-size-fits-all)
