# 01 - Memory Agent

A terminal conversational agent that thinks with a brain-inspired memory
architecture. Every user turn flows through the BrainOS plugin pipeline before
the model ever sees it, and past turns are recalled on demand instead of being
stuffed into the prompt.

## What this demo shows

- A full **BrainOS plugin pipeline** wired into a real chat loop:
  sensory gating, working memory, hippocampal indexing, attention-based
  retrieval, and periodic active forgetting.
- **Memory in action** you can see: each turn prints exactly what was gated,
  which working-memory slot changed, what was stored, and what was retrieved.
- **Recall across topics**: switch subjects, then ask about something from
  several turns ago and watch the agent pull it back out of the index.
- **Active forgetting**: every 10 turns the forgetting engine decays and prunes
  weak, low-salience memories so the store does not grow without bound.

## Prerequisites

- Python 3.10+
- (Optional) An OpenAI API key for `--live` mode. **Not required** - the default
  `--mock` mode runs a rule-based responder with zero network calls.

## Quick start

```bash
pip install -r requirements.txt
python agent.py
```

That launches **mock mode** (no API key, no network). To use a real model:

```bash
export OPENAI_API_KEY=sk-...      # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
python agent.py --live
```

If `--live` is requested but no key is present, the agent prints a notice and
falls back to mock mode so the demo never hard-fails.

### Using the real generated plugins (optional)

The agent will use the actual generated BrainOS plugin classes if it finds a
`brainos_plugins` package on the import path. Generate them once with the CLI:

```bash
brainos add all          # creates ./brainos_plugins/*.py
python agent.py
```

If `brainos_plugins` is not found, the agent falls back to equivalent inline
implementations, so it still runs standalone. The startup banner reports which
source is active (`brainos_plugins (generated)` vs `inline fallback`).

## What to try

1. Introduce yourself and describe a project (turns 1-3).
2. Switch to a completely different topic (turns 4-6).
3. Ask **"What was the project I mentioned earlier?"** - the agent queries the
   hippocampal index and replays the earlier memory.
4. Keep going past turn 10 to watch the **forgetting engine** decay and prune
   weak memories (the `Active` count in the stats line drops).
5. Reference something from turn 1 near the end and see whether it survived.

Exit any time with **Ctrl+C** (or `/quit`); the agent prints final memory stats.

Each turn prints a stats line:

```
[Stats: WM 3/6 | Indexed: 20 | Active: 15 | Pruned: 5]
```

- **WM** - working-memory slots in use / capacity
- **Indexed** - total memories written to the hippocampal index
- **Active** - memories still alive after forgetting
- **Pruned** - memories removed so far by the forgetting engine

## Architecture

```
                        User Input
                            |
                 +----------v-----------+
                 |   Sensory Gate       |  strip noise, enforce token budget
                 +----------+-----------+
                            |
                 +----------v-----------+
                 |  Working Memory      |  update slots: topic / entities / goal
                 +----------+-----------+
                            |
                 +----------v-----------+
                 |  Attention Filter    |  retrieve relevant PAST context
                 |  (query the index)   |  within a token budget
                 +----------+-----------+
                            |
                 +----------v-----------+
                 |  Hippocampal Index   |  store this turn with
                 |                      |  WHO / WHAT / WHEN bindings
                 +----------+-----------+
                            |
                 +----------v-----------+
                 |      LLM Call        |  system + working memory
                 |  (mock or OpenAI)    |  + retrieved context + user msg
                 +----------+-----------+
                            |
                 +----------v-----------+
                 |     Response         |  also stored in the index
                 +----------+-----------+
                            |
                 +----------v-----------+
                 |  Forgetting Engine   |  every 10 turns: decay + prune
                 +----------------------+
```

Note: relevant past context is retrieved *before* the current turn is stored, so
recall surfaces earlier memories rather than echoing the message just sent.

## Files

- `agent.py` - the agent and plugin pipeline (single file, < 500 lines)
- `requirements.txt` - dependencies for `--live` mode and the real plugins
- `conversation.md` - an annotated 15-turn sample transcript
