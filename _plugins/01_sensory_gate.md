# 🚪 Plugin: Sensory Gate

> **Brain Analog**: Sensory Buffer + Thalamic Filter
> **Problem It Solves**: Too much raw input floods the context window.
> **Token Savings**: 50-80% reduction in input tokens.

## What It Does

Pre-processes ALL incoming data (tool outputs, API responses, documents, user messages)
before it ever reaches the LLM's context window. Strips noise, extracts signal.

```
RAW INPUT (10,000 tokens)
        ↓
┌─────────────────────────────┐
│      SENSORY GATE           │
│                             │
│  1. Format Detection        │  ← What type of input is this?
│  2. Schema Extraction       │  ← Pull structured data
│  3. Noise Removal           │  ← Strip boilerplate, headers, whitespace
│  4. Size Gating             │  ← Truncate/summarize if exceeds budget
│  5. Signal Extraction       │  ← Extract only task-relevant portions
│                             │
└─────────────────────────────┘
        ↓
PROCESSED INPUT (2,000 tokens) → LLM
```

## Interface

```python
class SensoryGate:
    def __init__(self, config: GateConfig):
        self.max_tokens_per_input: int = 2000
        self.extractors: dict[str, Extractor]  # by content type
        self.noise_patterns: list[re.Pattern]   # strip these
        self.schema_map: dict[str, Schema]      # structured extraction
    
    def process(self, raw_input: RawInput) -> ProcessedInput:
        """
        Takes raw tool output / document / message.
        Returns compressed, relevant extract.
        """
        content_type = self.detect_type(raw_input)
        cleaned = self.remove_noise(raw_input, content_type)
        extracted = self.extract_schema(cleaned, content_type)
        gated = self.apply_token_budget(extracted)
        return ProcessedInput(
            content=gated,
            metadata=raw_input.metadata,
            original_size=len(raw_input),
            compressed_size=len(gated),
            compression_ratio=len(gated)/len(raw_input)
        )
    
    def detect_type(self, input) -> str:
        """JSON, HTML, Markdown, plaintext, code, error, table..."""
    
    def remove_noise(self, input, content_type) -> str:
        """Strip headers, footers, navigation, boilerplate, repeated structure"""
    
    def extract_schema(self, input, content_type) -> str:
        """If structured (JSON/table), extract only relevant fields"""
    
    def apply_token_budget(self, input) -> str:
        """If still too large: smart truncation or summarization"""
```

## Implementation Patterns

### Pattern 1: Tool Output Gating
```python
# BEFORE (wasteful — full API response in context):
result = search_api(query)  # Returns 50 results, 8000 tokens
messages.append({"role": "tool", "content": json.dumps(result)})

# AFTER (gated — only relevant signal):
result = search_api(query)
gated = sensory_gate.process(RawInput(
    content=json.dumps(result),
    type="search_results",
    task_context="user asked about X"
))
messages.append({"role": "tool", "content": gated.content})
# Now: 800 tokens instead of 8000
```

### Pattern 2: Document Chunking Gate
```python
# Instead of stuffing entire documents into context:
gate_config = GateConfig(
    strategy="extract_relevant",
    max_tokens=1500,
    relevance_query=current_user_query,
    extraction_mode="sentences"  # Return only relevant sentences
)
gate = SensoryGate(gate_config)
processed = gate.process(full_document)
```

### Pattern 3: Conversation History Gate
```python
# Old messages get progressively compressed:
def gate_history(messages: list, token_budget: int) -> list:
    gated = []
    for i, msg in enumerate(reversed(messages)):
        age = len(messages) - i  # Older = more compression
        if age < 3:
            gated.append(msg)  # Recent: full fidelity
        elif age < 10:
            gated.append(summarize(msg, max_tokens=100))  # Medium: compressed
        else:
            gated.append(extract_key_decisions(msg))  # Old: only key points
    return list(reversed(gated))
```

## Configuration

```yaml
sensory_gate:
  max_tokens_per_source: 2000
  noise_patterns:
    - "^\s*$"              # Empty lines
    - "Copyright ©.*"       # Boilerplate
    - "Page \d+ of \d+"   # Pagination
  type_configs:
    json_api:
      extract_fields: ["data", "results", "items"]
      ignore_fields: ["metadata", "pagination", "links", "headers"]
      max_array_items: 5
    html:
      extract: "main, article, .content"
      strip: "nav, footer, sidebar, script, style"
    error:
      extract: "message, code, details"
      ignore: "stack_trace, request_id, timestamp"
    table:
      max_rows: 20
      strategy: "head_tail"  # First 10 + Last 10
```

## When to Install This Plugin

✅ Your agent calls tools that return large JSON/HTML responses
✅ You're stuffing full documents into context
✅ Tool outputs contain 80%+ irrelevant boilerplate
✅ You're hitting context window limits on the input side
✅ Multiple data sources compete for limited context space

## Metrics

| Metric | Target |
|--------|--------|
| Compression ratio | 3:1 to 10:1 |
| Signal preservation | >95% (relevant info retained) |
| Latency overhead | <100ms per input |
| False negatives | <2% (important info incorrectly stripped) |
