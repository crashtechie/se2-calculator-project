# Kiro Specs Directory

This directory contains implementation-focused specs that reference the detailed enhancement documents in `docs/enhancementRequests/`. Specs provide quick-reference checklists and file references for Kiro-assisted implementation.

## Directory Structure

```
.kiro/specs/
├── README.md           # This file
├── INDEX.md           # Complete specs index
├── phase3/            # Phase 3: Build Order Calculator
│   ├── README.md
│   ├── ENH0000009-buildorder-model.md ✅
│   ├── ENH0000010-build-order-views.md
│   ├── ENH0000011-dynamic-block-selector.md
│   └── ENH0000012-build-order-export-import.md
└── phase4/            # Phase 4: Testing & Infrastructure
    ├── README.md
    ├── ENH0000016-cicd-pipeline.md
    ├── ENH0000012-e2e-testing.md
    └── ENH0000019-core-app.md
```

## What are Specs?

Specs are lightweight implementation guides that:
- Reference full enhancement documents in `docs/enhancementRequests/`
- Provide task checklists for tracking progress
- Include file references for quick navigation
- Focus on "what to build" rather than "why to build it"

## Relationship to Enhancement Requests

```
docs/enhancementRequests/     ← Full design, requirements, rationale
    └── phase3_buildorder/
        └── ENH0000009/
            └── ENH0000009-buildorder-model-core-logic.md

.kiro/specs/                  ← Implementation checklist, file refs
    └── phase3/
        └── ENH0000009-buildorder-model.md
```

**Enhancement Docs** = Complete design and requirements  
**Specs** = Implementation checklist with file references

## Using Specs with Kiro

1. **Review the full ENH doc** in `docs/enhancementRequests/` for design details
2. **Use the spec** in `.kiro/specs/` for implementation tracking
3. **Ask Kiro**: "Implement ENH0000010" - I'll reference both documents
4. **Check off tasks** as you complete them
5. **Update status** when finished

## File References

Specs use `#[[file:path]]` syntax for quick navigation:
```markdown
- Model: #[[file:app/buildorders/models.py]]
- Tests: #[[file:app/buildorders/tests.py]]
- ENH Doc: #[[file:docs/enhancementRequests/phase3_buildorder/ENH0000009/]]
```

## Status Values

- **Planned** - Ready to implement
- **In Progress** - Currently being worked on  
- **Complete** ✅ - Implementation finished and tested
- **Blocked** - Waiting on dependencies

---

For more information:
- Enhancement workflow: `.kiro/steering/02-enhancement-workflow.md`
- Full ENH docs: `docs/enhancementRequests/`
- Specs index: `INDEX.md`
