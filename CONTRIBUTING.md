# Contributing to BrainOS

Thank you for considering contributing! This project thrives on community knowledge.

## 📋 How to Contribute

### 1. Adding Content to Existing Modules

Each brain region module has 4 files:
- `README.md` — Overview (what it does, key facts)
- `mechanisms.md` — Biological detail (molecular, circuit, systems level)
- `examples.md` — Real-world demonstrations, experiments, case studies
- `failures.md` — Disorders, edge cases, what breaks

**To add content:** Fork the repo, add to the relevant file, and submit a PR.

### 2. Adding New Plugins

Plugin files follow a standard template:
```markdown
# 🔌 Plugin: [Name]

> **Brain Analog**: [Which brain system]
> **Problem It Solves**: [One sentence]
> **Token Savings**: [Estimate]

## What It Does
[Description with ASCII architecture diagram]

## Interface
[Python class with method signatures]

## Implementation Patterns
[Code examples]

## Configuration
[YAML config block]

## When to Install
[Checklist of use cases]
```

### 3. Adding Research Citations

When adding scientific claims, include:
- Author(s) and year
- Key finding (one sentence)
- Effect size if available (Cohen's d, percentage, etc.)
- Which file the citation supports

### 4. Fixing Errors

Neuroscience evolves. If you find outdated information:
1. Open an issue describing the correction
2. Include the current scientific consensus + source
3. Submit a PR with the fix

## 🎨 Style Guide

- **Tone**: Conversational but precise. Explain like a smart friend, not a textbook.
- **Structure**: Use headers, tables, ASCII diagrams, and bullet points liberally.
- **Analogies**: Every complex mechanism should have at least one analogy.
- **Code examples**: In the `_plugins/` directory, use Python with type hints.
- **Acronyms**: Define on first use, then use freely.

## 🔀 Branch Naming

```
feature/add-[module]-[topic]     (e.g., feature/add-hippocampus-neurogenesis)
fix/correct-[module]-[issue]     (e.g., fix/correct-ltm-capacity-estimate)
plugin/new-[plugin-name]         (e.g., plugin/new-attention-scheduler)
```

## ✅ PR Checklist

- [ ] Content is factually accurate (cite sources for new claims)
- [ ] Follows existing file structure and formatting
- [ ] No broken internal links
- [ ] Markdown renders correctly
- [ ] Spell-checked

## 💡 Ideas Welcome

Open an issue tagged `idea` if you want to discuss:
- New brain regions/systems to add
- New plugin architectures
- Better analogies or examples
- Visualization ideas

---

Thank you for helping map the brain! 🧠
