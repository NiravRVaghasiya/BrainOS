# 📚 Plugin: Semantic Store

> **Brain Analog**: Semantic Memory (temporal cortex knowledge network)
> **Problem It Solves**: Agent has no persistent world knowledge beyond training data.
> **Use Case**: Facts, concepts, relationships that persist across all conversations.

## What It Does

Stores CONTEXT-FREE knowledge — facts, relationships, and concepts stripped of 
when/where they were learned. Like human semantic memory: you know Paris is in 
France without remembering when you learned it.

```python
class SemanticStore:
    def __init__(self, config):
        self.knowledge_graph: KnowledgeGraph  # Entities + relationships
        self.fact_store: FactStore            # Atomic facts
        self.concept_hierarchy: TaxonomyTree  # Is-a / has-a relationships
    
    def learn(self, fact: Fact):
        """Add a new fact to the semantic store."""
        # Check: Does this contradict existing knowledge?
        existing = self.fact_store.query_related(fact)
        if self.contradicts(fact, existing):
            self.resolve_contradiction(fact, existing)  # Newer wins? Ask user?
        else:
            self.fact_store.upsert(fact)
            self.knowledge_graph.integrate(fact)
    
    def query(self, question: str) -> list[Fact]:
        """Retrieve relevant facts for a question."""
        # Hybrid: keyword + semantic + graph traversal
        return self.knowledge_graph.query(question)
    
    def get_entity_profile(self, entity: str) -> EntityProfile:
        """Everything known about a person/project/concept."""
        facts = self.fact_store.get_by_entity(entity)
        relationships = self.knowledge_graph.get_edges(entity)
        return EntityProfile(entity=entity, facts=facts, relationships=relationships)

# Fact schema:
@dataclass
class Fact:
    subject: str         # "Alice"
    predicate: str       # "works_on"
    object: str          # "Project Aurora"
    confidence: float    # 0-1
    source: str          # Where this was learned
    learned_at: datetime
    last_verified: datetime
    ttl: Optional[int]   # Some facts expire (role changes, etc.)
```

## Difference from Episodic Store

| | Episodic | Semantic |
|--|---------|----------|
| Stores | Events (what happened) | Facts (what IS true) |
| Context | Full (who, when, where) | Stripped (just the fact) |
| Query by | Time, person, context | Topic, entity, relationship |
| Example | "Tuesday's meeting notes" | "Alice's role is PM" |
| Brain region | Hippocampus → Temporal | Temporal cortex directly |
| Consolidation | Episodic → Semantic over time | Stable once learned |
