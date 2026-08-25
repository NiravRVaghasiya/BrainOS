# Architecture Decision Record

## Why This Structure?

### Brain Regions as Numbered Modules (01-08)
Numbers provide natural ordering of the information processing pipeline:
1. Input arrives (sensory)
2. Gets held briefly (working memory)
3. Gets indexed (hippocampus)
4. Gets stored permanently (long-term memory)
5. Gets priority-tagged (emotional)
6. Gets automated (motor)
7. Gets verbalized (language)
8. Gets integrated (default mode)

### Underscore Directories (_system, _flows, _techniques, _plugins)
Underscore prefix means "meta/cross-cutting" — these aren't brain regions but 
supporting documentation that spans multiple regions.

### File Naming Convention
| File | Purpose |
|------|---------|
| `README.md` | Entry point — what, why, key facts |
| `mechanisms.md` | How it works biologically |
| `examples.md` | Real-world demonstrations |
| `failures.md` | What goes wrong (clinical, aging, drugs) |

### Design Principles
1. **Self-contained modules** — Each folder is independently readable
2. **Progressive depth** — README (surface) → mechanisms (deep) → failures (clinical)
3. **Cross-references via `_flows/`** — Connections between modules documented separately
4. **Dual audience** — Neuroscience + Engineering perspectives in parallel
5. **Actionable** — _techniques for humans, _plugins for AI systems
