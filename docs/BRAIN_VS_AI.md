# Brain ↔ AI Mapping Reference

## Quick-Reference Translation Table

| Brain System | AI/ML Equivalent | Key Similarity | Key Difference |
|---|---|---|---|
| Sensory Buffer | Input preprocessing / Tokenizer | Raw data → structured | Brain: massive parallel; AI: sequential |
| Attention Gate | Query relevance scoring (BM25/embedding) | Select what matters | Brain: continuous; AI: discrete per-call |
| Working Memory | Context window / KV cache | Limited active capacity | Brain: 4 items; GPT-4: 128K tokens |
| Hippocampus | Vector DB + Index (FAISS/Pinecone) | Embed, store, retrieve | Brain: also CONSOLIDATES; AI doesn't |
| LTP (Learning) | Fine-tuning / Gradient descent | Strengthening connections | Brain: per-synapse; AI: all weights |
| Episodic Memory | Conversation logs + RAG | Store events with context | Brain: reconstructive; AI: verbatim |
| Semantic Memory | Knowledge Graph (Neo4j/KG) | Facts + relationships | Brain: associative; KG: explicit edges |
| Procedural Memory | Tool use cache / Few-shot examples | Learned action patterns | Brain: unconscious; AI: explicit |
| Amygdala | Salience/priority scoring | Importance weighting | Brain: emotional; AI: heuristic |
| Sleep Consolidation | Background jobs (cron summarization) | Offline processing | Brain: mandatory; AI: optional |
| Forgetting | TTL / Cache eviction / Pruning | Bounded storage | Brain: adaptive; AI: policy-driven |
| Cerebellum | PID controller / Error correction | Predict-compare-adjust | Brain: timing; AI: loss minimization |
| DMN | Background agents / Scheduled tasks | Processing when "idle" | Brain: always on; AI: must be triggered |
| Neuroplasticity | Online learning / RLHF | System improves with use | Brain: structural; AI: weight updates |
| Pattern Separation | Embedding distinctness (contrastive loss) | Make similar things distinguishable | Same principle, different substrate |
| Pattern Completion | Nearest-neighbor search / Autoregressive generation | Partial → whole | Brain: hippocampal; AI: transformer attention |
| Chunking | Tokenization / Abstraction layers | Compress for efficiency | Brain: expertise-based; AI: fixed vocabulary |
| Basal Ganglia Gate | Tool-use decision (function calling) | Select actions | Brain: dopamine-driven; AI: logit-driven |
| Broca's Area | Text generation / Decoder | Produce structured output | Brain: grammar engine; AI: autoregressive |
| Wernicke's Area | Text understanding / Encoder | Parse input meaning | Brain: modality-independent; AI: text-only |

## Architecture Pattern Mapping

```
HUMAN BRAIN ARCHITECTURE          AI AGENT ARCHITECTURE
━━━━━━━━━━━━━━━━━━━━━━━━━         ━━━━━━━━━━━━━━━━━━━━━━━━
Sensory Buffer (500ms)       ←→   Input preprocessing layer
         ↓                                ↓
Thalamic Gate (attention)    ←→   Relevance filter / retriever
         ↓                                ↓
Working Memory (4 slots)     ←→   Context window (token budget)
         ↓                                ↓
Hippocampus (index + bind)   ←→   Vector store + metadata index
         ↓                                ↓
Neocortex (permanent store)  ←→   Long-term storage (DB/KG/files)
         ↓                                ↓
Amygdala (importance tag)    ←→   Salience scoring function
         ↓                                ↓
Sleep (consolidation)        ←→   Background summarization jobs
         ↓                                ↓
Prefrontal (executive)       ←→   Orchestrator / Router agent
```
