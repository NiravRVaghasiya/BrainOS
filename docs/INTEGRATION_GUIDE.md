# Integration Guide

How to wire BrainOS plugins into the frameworks you already use. Generate the
plugin package first:

```bash
pip install brainos-cli
brainos add all          # writes ./brainos_plugins/*.py
```

Every snippet below imports the real generated classes from `brainos_plugins`
and uses their actual method signatures, so they are copy-pasteable once the
package exists on your import path.

---

## Quick Reference: Plugin -> Framework Mapping

| BrainOS Plugin | LangChain Equivalent | LangGraph Role | Direct Usage |
|---|---|---|---|
| sensory-gate | OutputParser/Preprocessor | Tool output node | Middleware |
| attention-filter | ContextualCompression | State filter node | Retriever wrapper |
| working-memory | ConversationBufferMemory | Graph State | Injected system prompt |
| hippocampal-index | VectorStoreRetriever | Retriever node | Direct class |
| episodic-store | ConversationEntityMemory | Memory node | Direct class |
| semantic-store | Neo4j/KG integration | Knowledge node | Direct class |
| procedural-cache | Tool caching | Conditional edge | Direct class |
| forgetting-engine | (no equivalent) | Maintenance node | Scheduled job |
| salience-tagger | (no equivalent) | Scoring function | Write hook |
| consolidator | (no equivalent) | Background worker | Cron job |

---

## LangChain Integration

### Custom Memory Class

Expose `EpisodicStore` as a LangChain `BaseMemory` so any chain can read/write
conversational events with WHO/WHAT/WHEN bindings.

```python
from typing import Any
from langchain.schema import BaseMemory
from brainos_plugins.episodic_store import EpisodicStore


class EpisodicMemory(BaseMemory):
    """LangChain memory backed by a BrainOS EpisodicStore."""

    store: EpisodicStore = EpisodicStore()
    memory_key: str = "history"

    @property
    def memory_variables(self) -> list[str]:
        return [self.memory_key]

    def load_memory_variables(self, inputs: dict[str, Any]) -> dict[str, str]:
        hits = self.store.query_by_content(inputs.get("input", ""), top_k=5)
        recalled = "\n".join(f"- {h['content']}" for h in hits)
        return {self.memory_key: recalled}

    def save_context(self, inputs: dict[str, Any], outputs: dict[str, str]) -> None:
        self.store.record_event(inputs["input"], who="user", what="turn")
        self.store.record_event(outputs["output"], who="assistant", what="reply")

    def clear(self) -> None:
        self.store = EpisodicStore()
```

### Custom Retriever

Wrap `HippocampalIndex` as a LangChain `BaseRetriever` for drop-in RAG.

```python
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from brainos_plugins.hippocampal_index import HippocampalIndex


class HippocampalRetriever(BaseRetriever):
    """Retrieve documents through a BrainOS hippocampal index."""

    index: HippocampalIndex = HippocampalIndex()
    top_k: int = 5

    def add(self, text: str, **bindings: str) -> None:
        # Store content with optional WHO/WHAT/WHERE context bindings.
        self.index.encode(text, bindings=bindings)

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> list[Document]:
        records = self.index.retrieve(query, top_k=self.top_k)
        return [Document(page_content=r.content, metadata=r.bindings) for r in records]
```

### Tool Output Preprocessing

Use `SensoryGate` as an output parser that strips noise and enforces a token
budget on raw tool/API results before they reach the model.

```python
from langchain.schema import BaseOutputParser
from brainos_plugins.sensory_gate import SensoryGate, GateConfig


class GatedOutputParser(BaseOutputParser[str]):
    """Clean and budget-cap raw tool output via a BrainOS sensory gate."""

    gate: SensoryGate = SensoryGate(GateConfig(max_tokens_per_input=800))

    def parse(self, text: str) -> str:
        result = self.gate.process(text, content_type="auto")
        return result["content"]  # noise removed, capped to the token budget
```

---

## LangGraph Integration

### State Schema

Model the graph state around `WorkingMemory` so active goals, entities, and
results survive across nodes.

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from brainos_plugins.working_memory import WorkingMemory


class AgentState(TypedDict):
    # Chat transcript accumulated by LangGraph.
    messages: Annotated[list, add_messages]
    # Bounded scratchpad of active context (topic, goal, key entities).
    working_memory: WorkingMemory
    # Retrieved long-term context injected into the next LLM call.
    retrieved: list[str]
    # Confidence in the current plan, set by the metacognition monitor.
    confidence: float
```

### Memory-Augmented Agent Graph

A five-node graph: preprocess input, retrieve memories, call the LLM, write
memories, then run maintenance. Uses four BrainOS plugins.

```python
from langgraph.graph import StateGraph, START, END
from brainos_plugins.sensory_gate import SensoryGate
from brainos_plugins.hippocampal_index import HippocampalIndex
from brainos_plugins.forgetting_engine import ForgettingEngine

gate, index, forgetting = SensoryGate(), HippocampalIndex(), ForgettingEngine()
store: list[dict] = []  # forgetting-engine works on memory dicts

def input_processor(state: AgentState) -> dict:
    clean = gate.process(state["messages"][-1].content, content_type="text")["content"]
    return {"messages": state["messages"][:-1] + [("user", clean)]}

def memory_retriever(state: AgentState) -> dict:
    hits = index.retrieve(state["messages"][-1].content, top_k=5)
    return {"retrieved": [h.content for h in hits]}

def llm_caller(state: AgentState) -> dict:
    context = "\n".join(state["retrieved"])
    reply = your_llm(system=context, user=state["messages"][-1].content)  # your call
    return {"messages": [("assistant", reply)]}

def memory_writer(state: AgentState) -> dict:
    rec = index.encode(state["messages"][-1].content, bindings={"who": "assistant"})
    store.append({"id": rec.id, "strength": 1.0, "salience": rec.salience})
    return {}

def maintenance(state: AgentState) -> dict:
    forgetting.apply_decay(store)                 # decay by age
    store[:] = forgetting.prune(store)            # drop weak memories
    return {}

graph = StateGraph(AgentState)
for name, fn in [("input", input_processor), ("retrieve", memory_retriever),
                 ("llm", llm_caller), ("write", memory_writer), ("maintain", maintenance)]:
    graph.add_node(name, fn)
graph.add_edge(START, "input")
graph.add_edge("input", "retrieve")
graph.add_edge("retrieve", "llm")
graph.add_edge("llm", "write")
graph.add_edge("write", "maintain")
graph.add_edge("maintain", END)
app = graph.compile()
```

### Conditional Routing

Let `MetacognitionMonitor` pick the processing path from its confidence in the
current task, so low-confidence tasks get the heavier route.

```python
from brainos_plugins.metacognition import MetacognitionMonitor

monitor = MetacognitionMonitor()

def route_by_confidence(state: AgentState) -> str:
    task = state["messages"][-1].content
    monitor.predict(task, confidence=state["confidence"])
    # High confidence -> answer directly; low confidence -> deep research path.
    return "fast_answer" if state["confidence"] >= 0.7 else "deep_research"

graph.add_conditional_edges(
    "retrieve",
    route_by_confidence,
    {"fast_answer": "llm", "deep_research": "research_subgraph"},
)
```

---

## CrewAI / Multi-Agent

### Shared Memory Architecture

Give every agent a reference to one `HippocampalIndex` so knowledge written by
any agent is retrievable by all of them.

```python
from crewai import Agent
from brainos_plugins.hippocampal_index import HippocampalIndex

# One index shared across the whole crew (collective memory).
shared_index = HippocampalIndex()

def remember(text: str, author: str) -> None:
    shared_index.encode(text, bindings={"who": author})

def recall(query: str, top_k: int = 5) -> list[str]:
    return [r.content for r in shared_index.retrieve(query, top_k=top_k)]

researcher = Agent(role="Researcher", goal="Gather facts", backstory="...")
writer = Agent(role="Writer", goal="Draft report", backstory="...")
# Researcher writes; writer recalls the same store when drafting.
remember("Q3 churn rose 4% in the SMB segment", author="Researcher")
context = recall("churn trends")  # available to the writer
```

### Agent Specialization

Different plugin combos per role: the researcher accumulates and ranks
knowledge; the executor reuses cached procedures within an active workspace.

```python
from brainos_plugins.semantic_store import SemanticStore
from brainos_plugins.attention_filter import AttentionFilter, ContextItem
from brainos_plugins.procedural_cache import ProceduralCache
from brainos_plugins.working_memory import WorkingMemory


class ResearcherMemory:
    """Knowledge accumulation + relevance ranking."""
    def __init__(self) -> None:
        self.knowledge = SemanticStore()                       # facts as triples
        self.attention = AttentionFilter(token_budget=4000)    # rank within budget

    def learn(self, subj: str, pred: str, obj: str) -> None:
        self.knowledge.add(subj, pred, obj)


class ExecutorMemory:
    """Skill reuse + bounded active context."""
    def __init__(self) -> None:
        self.skills = ProceduralCache(similarity_threshold=0.8)  # cached tool runs
        self.workspace = WorkingMemory(max_slots=6)              # current task state

    def reuse_or_run(self, task: str) -> list | None:
        return self.skills.lookup(task)  # returns cached steps or None
```

---

## Vanilla Python (No Framework)

### Minimal Setup

A working memory-augmented loop in ~10 lines: recall, respond, store.

```python
from brainos_plugins.hippocampal_index import HippocampalIndex

index = HippocampalIndex()
while (user := input("you> ")).strip():
    hits = index.retrieve(user, top_k=3)                       # recall prior turns
    context = "\n".join(h.content for h in hits)
    reply = your_llm(system=context, user=user)                # your model call
    print("bot>", reply)
    index.encode(user, bindings={"who": "user"})               # store the turn
    index.encode(reply, bindings={"who": "assistant"})
```

### Full Pipeline

Six plugins working together in one conversation loop: gate input, score
salience, update working memory, retrieve within budget, store, and forget.

```python
from datetime import datetime, timezone
from brainos_plugins.sensory_gate import SensoryGate, GateConfig
from brainos_plugins.working_memory import WorkingMemory
from brainos_plugins.hippocampal_index import HippocampalIndex
from brainos_plugins.attention_filter import AttentionFilter, ContextItem
from brainos_plugins.salience_tagger import SalienceTagger
from brainos_plugins.forgetting_engine import ForgettingEngine

gate = SensoryGate(GateConfig(max_tokens_per_input=500))
wm = WorkingMemory(max_slots=6)
index = HippocampalIndex()
attention = AttentionFilter(token_budget=4000, half_life_hours=48.0)
tagger = SalienceTagger()
forgetting = ForgettingEngine(decay_rate=0.9, prune_threshold=0.3)

store: list[dict] = []
turn = 0

def handle(raw_input: str) -> str:
    global turn
    turn += 1

    # 1) Gate: strip noise, enforce token budget.
    clean = gate.process(raw_input, content_type="text")["content"]

    # 2) Score salience at write time (amygdala analog).
    salience = tagger.score(clean, {"timestamp": datetime.now(timezone.utc)})

    # 3) Update the bounded active workspace.
    wm.update("last_input", clean, priority=salience)

    # 4) Retrieve relevant prior context within the attention budget.
    records = index.retrieve(clean, top_k=8)
    items = [ContextItem(content=r.content, token_count=len(r.content) // 4,
                         timestamp=r.timestamp, salience=r.salience) for r in records]
    selected = attention.filter(items)
    context = "\n".join(it.content for it in selected)

    # 5) Call your model with working memory + retrieved context.
    reply = your_llm(system=f"{wm.get_state()}\n{context}", user=clean)

    # 6) Store both sides of the turn.
    rec = index.encode(clean, bindings={"who": "user"})
    rec.salience = salience
    store.append({"id": rec.id, "strength": 1.0, "salience": salience,
                  "last_accessed": datetime.now(timezone.utc)})
    index.encode(reply, bindings={"who": "assistant"})

    # 7) Forget: decay + prune every 10 turns to keep growth bounded.
    if turn % 10 == 0:
        forgetting.apply_decay(store)
        store[:] = forgetting.prune(store)

    return reply
```

---

## Anti-Patterns

- **Don't use ALL plugins.** Pick 3-4 that match your use case. Stacking every
  plugin adds latency and moving parts without proportional benefit.
- **Don't skip the forgetting-engine.** Unbounded memory grows the retrieval set
  and context size until latency and cost balloon. Bounded memory is the point.
- **Don't use procedural-cache for non-deterministic tasks.** Caching a tool
  sequence only helps when the same task reliably yields the same good steps;
  for stochastic tasks it will replay stale or wrong actions.
- **Don't run consolidator synchronously.** Deduping, merging, and summarizing
  are batch jobs. Run them in a background worker or cron, never in the request
  path.

---

## Architecture Decision Guide

| Use Case | Recommended Stack | Why |
|---|---|---|
| Chatbot with memory | episodic + hippocampal + forgetting | Conversation recall + bounded growth |
| Research agent | semantic + attention + consolidator | Knowledge accumulation + relevance |
| Coding assistant | procedural + working-memory + metacognition | Skill reuse + active context |
| Multi-agent system | All shared stores + per-agent working-memory | Collective knowledge + individual focus |

### How to choose

1. **Start from the bottleneck.** Context overflow -> `sensory-gate` +
   `attention-filter` + `forgetting-engine`. Forgetting conversations ->
   `episodic-store` + `hippocampal-index`. Redundant reasoning ->
   `procedural-cache`.
2. **Add exactly one write-time scorer** (`salience-tagger`) if retrieval
   quality matters more than raw recall.
3. **Add background maintenance** (`consolidator`, `forgetting-engine`) once the
   store is large enough that quality or cost degrades over a session.
4. **Add metacognition last** — it compounds value only after the base memory
   loop is stable and you can measure prediction vs. outcome.
