# 🖥️ Plugin: Working Memory Manager

> **Brain Analog**: Prefrontal Cortex Working Memory (4±1 slots)
> **Problem It Solves**: LLM loses track of active goals, sub-tasks, and intermediate results.
> **Token Savings**: 25-45% (eliminates redundant re-stating of context).

## What It Does

Maintains a small, structured "scratchpad" of the agent's CURRENT active state.
Like the brain's ~4 working memory slots — holds only what's immediately relevant.

```
┌─────────────────────────────────────────────────────────────┐
│              WORKING MEMORY (4-6 Slots)                       │
│                                                              │
│  SLOT 1: Current Goal                                        │
│  "User wants a summary of Q3 revenue trends"                │
│                                                              │
│  SLOT 2: Active Sub-task                                     │
│  "Retrieving data from revenue dashboard"                    │
│                                                              │
│  SLOT 3: Intermediate Result                                 │
│  "Q3 revenue: $4.2M (+12% YoY). Source: dashboard query"    │
│                                                              │
│  SLOT 4: Constraints/Preferences                             │
│  "User prefers bullet points. Max 200 words. Include YoY."  │
│                                                              │
│  [SLOT 5: Empty]                                             │
│  [SLOT 6: Empty]                                             │
│                                                              │
│  Total tokens used: ~350 (vs 4000+ for full conversation)    │
└─────────────────────────────────────────────────────────────┘
```

## Interface

```python
class WorkingMemoryManager:
    def __init__(self, max_slots: int = 6, max_tokens_per_slot: int = 200):
        self.slots: dict[str, WMSlot] = {}
        self.max_slots = max_slots
        self.max_tokens_per_slot = max_tokens_per_slot
    
    def update_slot(self, key: str, content: str, priority: float = 1.0):
        """Write/overwrite a working memory slot."""
        if len(self.slots) >= self.max_slots and key not in self.slots:
            self._evict_lowest_priority()
        self.slots[key] = WMSlot(content=content, priority=priority, updated_at=now())
    
    def read_slot(self, key: str) -> Optional[str]:
        """Read a specific slot."""
        return self.slots.get(key, None)
    
    def get_state(self) -> str:
        """Serialize current WM state for injection into LLM context."""
        lines = ["## Active Working Memory"]
        for key, slot in sorted(self.slots.items(), key=lambda x: -x[1].priority):
            lines.append(f"**{key}**: {slot.content}")
        return "\n".join(lines)
    
    def clear_slot(self, key: str):
        """Free a slot when sub-task completes."""
        self.slots.pop(key, None)
    
    def _evict_lowest_priority(self):
        """When full: evict least important slot (like WM displacement)."""
        lowest = min(self.slots.items(), key=lambda x: x[1].priority)
        # Optionally: move evicted content to episodic store before deletion
        self.episodic_store.save(lowest[1])  
        del self.slots[lowest[0]]
```

## Slot Types (Pre-Defined)

```python
SLOT_TYPES = {
    "current_goal": {
        "description": "What the user ultimately wants",
        "priority": 5,  # Never evicted
        "example": "Write a project proposal for the ML pipeline"
    },
    "active_subtask": {
        "description": "What I'm doing RIGHT NOW",
        "priority": 4,
        "example": "Searching for similar proposals to use as reference"
    },
    "intermediate_result": {
        "description": "Key data/output from a completed step",
        "priority": 3,
        "example": "Found 3 reference proposals. Best match: MLOps pipeline doc."
    },
    "constraints": {
        "description": "User preferences, format requirements, boundaries",
        "priority": 4,
        "example": "Max 2 pages. Include timeline. Formal tone."
    },
    "context_key_facts": {
        "description": "Critical background info for this task",
        "priority": 2,
        "example": "Team size: 5. Budget: $50K. Deadline: March 2027."
    },
    "error_state": {
        "description": "What went wrong / what to avoid",
        "priority": 3,
        "example": "API returned 403. Need to use backup endpoint."
    }
}
```

## Integration with LLM Calls

```python
# Inject working memory state into every LLM call:

def build_messages(conversation, wm_manager, attention_filter):
    messages = [
        {"role": "system", "content": system_prompt},
        # Working Memory = always present, minimal tokens, maximum signal
        {"role": "system", "content": wm_manager.get_state()},
    ]
    # Then add filtered conversation history
    filtered_history = attention_filter.filter(conversation, current_query)
    messages.extend(filtered_history)
    messages.append({"role": "user", "content": current_query})
    return messages

# Total WM overhead: ~200-400 tokens (vs. 4000+ for full context replay)
# Contains 100% of what the LLM needs to maintain coherence
```

## The "Gate" Mechanism (What Enters Working Memory?)

```python
class WMGate:
    """Decides what's important enough to occupy a WM slot."""
    
    def should_update(self, event: Event, current_wm: WorkingMemoryManager) -> bool:
        # Goal changes: ALWAYS update
        if event.type == "new_user_message" and self.detects_goal_change(event):
            return True
        
        # Tool results: Only if they contain key information
        if event.type == "tool_result":
            return self.is_decision_relevant(event, current_wm.read_slot("current_goal"))
        
        # Default: Don't update (protect current contents from noise)
        return False
    
    def detects_goal_change(self, event) -> bool:
        """User changed topic or refined their request."""
        # Compare semantic similarity of new message vs current goal
        # Low similarity = likely topic change = update goal slot
        ...
```

## When to Install This Plugin

✅ Multi-turn conversations where the agent loses track of the goal
✅ Complex tasks with multiple steps (agent forgets intermediate results)
✅ Agent repeats itself or re-asks questions it already has answers to
✅ Long conversations where context window fills with redundant history
✅ You want PREDICTABLE token usage (WM = fixed overhead, not growing)
