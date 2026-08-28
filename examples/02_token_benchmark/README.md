# 02 - Token benchmark

Proves the token-savings claims from the BrainOS README by simulating a
realistic 50-turn agent conversation and counting the tokens each strategy
would send to the model. **No LLM calls** are made - only tokenization.

## What this measures and why it matters

Every token sent to an LLM costs money and latency. The naive way to give an
agent "memory" is to resend the entire conversation history on every call. That
makes per-call context grow with the conversation length, so **cumulative cost
grows quadratically - O(n^2)**. On a long session this dominates the bill.

BrainOS bounds what each call sees:

- **Sensory Gate** strips noise from tool outputs (trace ids, debug logs,
  pagination) and keeps only signal fields before anything is stored.
- **Attention Filter** selects only the most relevant, recent, high-salience
  memories that fit inside a fixed token budget (4000 here) for each call.
- **Forgetting Engine** prunes low-salience memories every 10 turns so the
  memory store itself stops growing.

Together these keep total token usage **O(n)** instead of O(n^2): the cost per
turn stops depending on how long the conversation has been running.

## How to run

```bash
pip install -r requirements.txt
python benchmark.py
```

Runs in under a second and writes `results.json` (full per-turn data) and
`results.md` (formatted table + analysis). Uses tiktoken's `cl100k_base`
(the GPT-4 tokenizer); if tiktoken is unavailable it falls back to a `len/4`
approximation so it still runs offline.

The benchmark uses the real generated BrainOS plugins if a `brainos_plugins`
package is importable (run `brainos add all` first); otherwise it uses
equivalent inline implementations. The header line reports which source is
active.

## Scenarios

1. **Baseline (naive)** - every call includes the full conversation history.
2. **+ Sensory Gate** - tool outputs are gated before storage.
3. **+ Attention Filter** - each call selects top items within a 4000-token budget.
4. **+ Forgetting Engine** - prune low-salience memories every 10 turns.
5. **Full BrainOS stack** - all three combined.

## Summary of results

Measured on a seeded 50-turn conversation (tiktoken `cl100k_base`, inline
plugins). Numbers are reproducible via `python benchmark.py`.

| Scenario                | Total Tokens | Savings % | Peak Context |
|-------------------------|-------------:|----------:|-------------:|
| Baseline (full history) |      424,361 |         - |       16,540 |
| + Sensory Gate          |      278,627 |     34.3% |       10,820 |
| + Attention Filter      |      162,236 |     61.8% |        3,997 |
| + Forgetting Engine     |      138,690 |     67.3% |        5,567 |
| Full BrainOS stack      |       79,381 |     81.3% |        3,114 |

- **Sensory Gate on tool-output tokens: ~53%** (README claim: 50-80%).
- **Attention Filter: ~62%** total savings vs baseline (README claim: 40-70%).
- **Full stack: ~81%** total savings vs baseline.
- **Growth check:** baseline's per-call context in the last 10 turns is ~10x its
  first-10-turn average (the O(n^2) signature), while the full stack stays ~1.7x
  (bounded, O(n)).

Exact numbers vary slightly with the plugin source (generated vs inline) because
the generated `SensoryGate` uses its own extract-field list, but all figures
stay within the README's claimed ranges. See `results.md` for the analysis
regenerated from your run.
