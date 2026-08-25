# 🗑️ Plugin: Forgetting Engine

> **Brain Analog**: Active Forgetting (synaptic homeostasis, interference, decay)
> **Problem It Solves**: Memory stores grow unbounded → slow, expensive, noisy retrieval.
> **Token Savings**: Prevents storage bloat; keeps retrieval fast and precise.

## What It Does

ACTIVELY removes or compresses memories that are no longer useful.
Forgetting is not failure — it's maintenance. Without it, memory systems collapse.

```python
class ForgettingEngine:
    def __init__(self, config: ForgettingConfig):
        self.decay_rate: float = 0.95        # Per-day retention factor
        self.access_boost: float = 0.3       # Boost per access
        self.pruning_threshold: float = 0.05 # Below this → archive
        self.max_store_size: int = 10000     # Hard cap
    
    def apply_decay(self, memory_store: MemoryStore):
        """Apply time-based decay to all memories (Ebbinghaus curve)."""
        for memory in memory_store.get_all():
            days_since_access = (now() - memory.last_accessed).days
            memory.strength *= self.decay_rate ** days_since_access
            
            if memory.strength < self.pruning_threshold:
                memory_store.archive(memory)  # Move to cold storage
    
    def on_access(self, memory: MemoryRecord):
        """Strengthen memory when accessed (retrieval = practice)."""
        memory.strength = min(1.0, memory.strength + self.access_boost)
        memory.access_count += 1
        memory.last_accessed = now()
    
    def resolve_interference(self, memory_store: MemoryStore):
        """Remove redundant/contradicting memories."""
        # Find clusters of similar memories
        clusters = self.cluster_similar(memory_store, threshold=0.9)
        for cluster in clusters:
            if len(cluster) > 1:
                # Keep the STRONGEST (most accessed, highest salience)
                keeper = max(cluster, key=lambda m: m.strength * m.salience)
                for other in cluster:
                    if other != keeper:
                        memory_store.archive(other)
    
    def enforce_capacity(self, memory_store: MemoryStore):
        """Hard cap: When full, evict weakest memories."""
        if memory_store.count() > self.max_store_size:
            excess = memory_store.count() - self.max_store_size
            weakest = memory_store.get_weakest(n=excess)
            for memory in weakest:
                memory_store.archive(memory)
```

## Decay Schedule

```yaml
forgetting_engine:
  # Strength decay (applied daily)
  decay:
    rate: 0.95  # 5% per day without access
    min_strength: 0.01
    exempt_if: 
      - salience > 0.9  # Very important items don't decay
      - pinned: true     # User-pinned items are permanent
  
  # Pruning (archive below threshold)
  pruning:
    threshold: 0.05
    schedule: "daily"
    action: "archive"  # Move to cold storage, not hard delete
  
  # Interference resolution (weekly)
  dedup:
    similarity_threshold: 0.92
    keep_strategy: "strongest"  # Keep highest strength × salience
    schedule: "weekly"
  
  # Hard cap
  capacity:
    max_items: 10000
    eviction: "weakest_first"
```

## When to Install

✅ Memory store grows without bound (storage costs, retrieval latency)
✅ Old/irrelevant memories pollute search results
✅ You need predictable storage costs (bounded growth)
✅ Contradicting memories exist (old facts vs new facts)
✅ You want memories that "self-maintain" without manual cleanup
