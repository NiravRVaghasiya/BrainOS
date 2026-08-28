# Token benchmark results

**Tokenizer:** tiktoken/cl100k_base &nbsp;|&nbsp; **Plugins:** inline fallback &nbsp;|&nbsp; **Turns:** 50 &nbsp;|&nbsp; **Attention budget:** 4000 tokens

| Scenario                |   Total Tokens | Savings %   |   Peak Context |
|-------------------------|----------------|-------------|----------------|
| Baseline (full history) |        424,361 | -           |         16,540 |
| + Sensory Gate          |        278,627 | 34.3%       |         10,820 |
| + Attention Filter      |        162,236 | 61.8%       |          3,997 |
| + Forgetting Engine     |        138,690 | 67.3%       |          5,567 |
| Full BrainOS stack      |         79,381 | 81.3%       |          3,114 |

## Analysis

The naive baseline resends the entire conversation history on every call, so
its per-call context grows linearly with the turn count and its cumulative token
usage grows **quadratically** - roughly O(n^2). Over this 50-turn session the
average context in the final 10 turns is about **10.3x** larger than
in the first 10 turns.

The **sensory gate** strips noise from tool outputs (request ids, trace ids,
debug logs, pagination) and keeps only signal fields, cutting tool-output tokens
by **52.8%** - inside the README's claimed 50-80% range. The
**attention filter** bounds each call to a 4000-token budget by
selecting only the most relevant, recent, high-salience memories, saving
**61.8%** of total tokens versus baseline (README claim:
40-70%). The **forgetting engine** prunes low-salience memories every 10 turns so
the store itself stops growing.

Stacked together, the **full BrainOS pipeline** uses **81.3%** fewer
tokens than the baseline across the session, and its per-call context stays
essentially flat (final-10 vs first-10 growth of only **1.70x**).
That is the key result: BrainOS converts the naive O(n^2) token cost into O(n)
by bounding context size, so cost per turn stops depending on how long the
conversation has been running.
