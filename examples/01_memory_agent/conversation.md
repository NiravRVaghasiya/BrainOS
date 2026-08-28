# Sample conversation (15 turns)

An annotated transcript from **mock mode** (`python agent.py`). System
annotations show what each plugin did on every turn. The forgetting engine runs
every 10 turns; you can see it fire at Turn 10, after which the `Active` memory
count drops below `Indexed`.

Annotation legend:

- `[SENSORY GATE]` raw -> gated token estimate
- `[WM UPDATE]` which working-memory slot changed
- `[STORED]` a memory written to the hippocampal index (with salience)
- `[RETRIEVED]` relevant prior memories pulled back (with relevance)
- `[FORGETTING ENGINE]` decay + prune pass

---

## Phase 1 - Introduction & a project (Turns 1-3)

```
[Turn 1] User: Hi, I'm Maria and I'm working on Project Atlas
  -> [SENSORY GATE] 11 -> 11 tokens
  -> [WM UPDATE] slot 'topic' = "Maria Project"
  -> [STORED] memory #1 (salience: 0.82)
Agent: Hello! Nice to meet you, Maria. Tell me what you're working on and I'll keep track of it.
  [Stats: WM 2/6 | Indexed: 2 | Active: 2 | Pruned: 0]

[Turn 2] User: Project Atlas has a deadline next Friday
  -> [SENSORY GATE] 10 -> 10 tokens
  -> [WM UPDATE] slot 'topic' = "Project Atlas"
  -> [RETRIEVED] memories #1 (relevance: 1.00)
  -> [STORED] memory #3 (salience: 0.84)
Agent: Got it - noting the focus on Project Atlas. What's the next step you're considering?
  [Stats: WM 2/6 | Indexed: 4 | Active: 4 | Pruned: 0]

[Turn 3] User: The main blocker is the database migration
  -> [SENSORY GATE] 10 -> 10 tokens
  -> [WM UPDATE] slot 'topic' = "Blocker"
  -> [STORED] memory #5 (salience: 0.60)
Agent: Got it - noting the focus on Blocker. What's the next step you're considering?
  [Stats: WM 2/6 | Indexed: 6 | Active: 6 | Pruned: 0]
```

## Phase 2 - Topic switch (Turns 4-6)

```
[Turn 4] User: Anyway, I also enjoy hiking on weekends
  -> [SENSORY GATE] 9 -> 9 tokens
  -> [WM UPDATE] slot 'topic' = "Enjoy"
  -> [STORED] memory #7 (salience: 0.48)
Agent: Got it - noting the focus on Enjoy. What's the next step you're considering?
  [Stats: WM 2/6 | Indexed: 8 | Active: 8 | Pruned: 0]

[Turn 5] User: My favorite trail is near Boulder Canyon
  -> [SENSORY GATE] 10 -> 10 tokens
  -> [WM UPDATE] slot 'topic' = "Boulder Canyon"
  -> [STORED] memory #9 (salience: 0.56)
Agent: Got it - noting the focus on Boulder Canyon. What's the next step you're considering?
  [Stats: WM 2/6 | Indexed: 10 | Active: 10 | Pruned: 0]

[Turn 6] User: I usually go hiking with my dog Rex
  -> [SENSORY GATE] 8 -> 8 tokens
  -> [WM UPDATE] slot 'topic' = "Rex"
  -> [STORED] memory #11 (salience: 0.48)
Agent: Got it - noting the focus on Rex. What's the next step you're considering?
  [Stats: WM 2/6 | Indexed: 12 | Active: 12 | Pruned: 0]
```

## Phase 3 - Recall from earlier (Turn 7)

The user asks about a topic from three turns back. Relevant memories are
retrieved from the hippocampal index *before* this turn is stored, so the agent
replays the earlier project memory rather than the question itself.

```
[Turn 7] User: What was the project I mentioned earlier?
  -> [SENSORY GATE] 10 -> 10 tokens
  -> [WM UPDATE] slot 'topic' = "Project"
  -> [RETRIEVED] memories #3, #1, #4 (relevance: 1.00, 0.95, 0.95)
  -> [STORED] memory #13 (salience: 0.50)
Agent: Earlier you told me: "Project Atlas has a deadline next Friday". Want to pick that back up?
  [Stats: WM 3/6 | Indexed: 14 | Active: 14 | Pruned: 0]
```

## Phase 4 - Building on retrieved context (Turns 8-10)

```
[Turn 8] User: Right, the migration is the critical part
  -> [SENSORY GATE] 10 -> 10 tokens
  -> [WM UPDATE] slot 'topic' = "Migration"
  -> [RETRIEVED] memories #5 (relevance: 1.00)
  -> [STORED] memory #15 (salience: 0.66)
Agent: Got it - noting the focus on Migration. What's the next step you're considering?
  [Stats: WM 3/6 | Indexed: 16 | Active: 16 | Pruned: 0]

[Turn 9] User: Can you help me plan the migration steps?
  -> [SENSORY GATE] 10 -> 10 tokens
  -> [WM UPDATE] slot 'topic' = "Migration"
  -> [RETRIEVED] memories #5, #15 (relevance: 1.00, 0.92)
  -> [STORED] memory #17 (salience: 0.66)
Agent: Based on what we discussed (the database migration...), here's my take: it sounds worth prioritizing.
  [Stats: WM 4/6 | Indexed: 18 | Active: 18 | Pruned: 0]
```

## Phase 5 - Forgetting engine runs (Turn 10)

At the 10th turn the forgetting engine decays every memory by age and salience,
then prunes those that fall below threshold. Weak, low-salience small talk
(e.g. the hiking asides) is dropped; salient project memories survive. Watch
`Active` fall below `Indexed`.

```
[Turn 10] User: Step one is backing up the production data
  -> [SENSORY GATE] 11 -> 11 tokens
  -> [WM UPDATE] slot 'topic' = "Step"
  -> [RETRIEVED] memories #5, #15, #17 (relevance: 1.00, 0.94, 0.91)
  -> [STORED] memory #19 (salience: 0.56)
  -> [FORGETTING ENGINE] decayed 20 memories, pruned 5
Agent: Got it - noting the focus on Step. What's the next step you're considering?
  [Stats: WM 4/6 | Indexed: 20 | Active: 15 | Pruned: 5]
```

## Phase 6 - Testing memory against early context (Turns 11-15)

The high-salience Project Atlas memories from Turn 1-2 survived the prune, so
references back to them still resolve.

```
[Turn 11] User: Let us also discuss the testing strategy
  -> [SENSORY GATE] 9 -> 9 tokens
  -> [WM UPDATE] slot 'topic' = "Discuss"
  -> [STORED] memory #21 (salience: 0.48)
Agent: Got it - noting the focus on Discuss. What's the next step you're considering?
  [Stats: WM 4/6 | Indexed: 22 | Active: 17 | Pruned: 5]

[Turn 12] User: Remind me - what is Project Atlas about?
  -> [SENSORY GATE] 10 -> 10 tokens
  -> [WM UPDATE] slot 'topic' = "Project Atlas"
  -> [RETRIEVED] memories #3, #1, #15 (relevance: 1.00, 0.96, 0.90)
  -> [STORED] memory #23 (salience: 0.84)
Agent: Earlier you told me: "Project Atlas has a deadline next Friday". Want to pick that back up?
  [Stats: WM 4/6 | Indexed: 24 | Active: 19 | Pruned: 5]

[Turn 13] User: And who did I say I was?
  -> [SENSORY GATE] 8 -> 8 tokens
  -> [WM UPDATE] slot 'user_goal' = "And who did I say I was?"
  -> [RETRIEVED] memories #1 (relevance: 1.00)
Agent: Earlier you told me: "Hi, I'm Maria and I'm working on Project Atlas". Want to pick that back up?
  [Stats: WM 5/6 | Indexed: 26 | Active: 21 | Pruned: 5]

[Turn 14] User: Great, back to the Project Atlas deadline
  -> [SENSORY GATE] 10 -> 10 tokens
  -> [WM UPDATE] slot 'topic' = "Project Atlas"
  -> [RETRIEVED] memories #3, #1, #23 (relevance: 1.00, 0.93, 0.90)
  -> [STORED] memory #27 (salience: 0.84)
Agent: Got it - noting the focus on Project Atlas. What's the next step you're considering?
  [Stats: WM 5/6 | Indexed: 28 | Active: 23 | Pruned: 5]

[Turn 15] User: Thanks for keeping track of everything
  -> [SENSORY GATE] 8 -> 8 tokens
  -> [WM UPDATE] slot 'topic' = "Keeping"
  -> [STORED] memory #29 (salience: 0.48)
Agent: Got it - noting the focus on Keeping. What's the next step you're considering?
  [Stats: WM 5/6 | Indexed: 30 | Active: 25 | Pruned: 5]
```

---

### Takeaways

- **Working memory** stays small and bounded (max 6 slots) while the
  **hippocampal index** grows with every turn.
- **Retrieval** happens before storage, so recall pulls genuine prior context.
- **Salience** matters: high-salience project memories survive the Turn 10
  prune while low-salience small talk is forgotten - which is why the early
  Project Atlas / "I'm Maria" memories can still be recalled at Turns 12-14.
