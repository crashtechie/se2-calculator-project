# Specs Index

Quick reference for all implementation specs in the project.

## Phase 3: Build Order Calculator

| Spec | Status | ENH Doc | Description |
|------|--------|---------|-------------|
| [ENH0000009](phase3/ENH0000009-buildorder-model.md) | ✅ Complete | [📄](../docs/enhancementRequests/phase3_buildorder/ENH0000009/) | BuildOrder model & calculations |
| [ENH0000010](phase3/ENH0000010-build-order-views.md) | Planned | [📄](../docs/enhancementRequests/phase3_buildorder/ENH0000010/) | CRUD views & templates |
| [ENH0000011](phase3/ENH0000011-dynamic-block-selector.md) | Planned | [📄](../docs/enhancementRequests/phase3_buildorder/ENH0000011/) | Dynamic block selector UI |
| [ENH0000012](phase3/ENH0000012-build-order-export-import.md) | Planned | [📄](../docs/enhancementRequests/phase3_buildorder/ENH0000012/) | Export/import functionality |

## Phase 4: Testing & Infrastructure

| Spec | Status | ENH Doc | Description |
|------|--------|---------|-------------|
| [ENH0000016](phase4/ENH0000016-cicd-pipeline.md) | Planned | [📄](../docs/enhancementRequests/phase4_testing/ENH0000016/) | CI/CD automated testing |
| [ENH0000012](phase4/ENH0000012-e2e-testing.md) | Planned | [📄](../docs/enhancementRequests/phase4_testing/ENH0000012/) | E2E testing with Playwright |
| [ENH0000019](phase4/ENH0000019-core-app.md) | Planned | (spec only) | Core app utilities |

## Directory Structure

```
.kiro/specs/
├── README.md           # Overview and usage
├── INDEX.md           # This file
├── phase3/            # Phase 3 specs
│   ├── README.md
│   ├── ENH0000009-buildorder-model.md
│   ├── ENH0000010-build-order-views.md
│   ├── ENH0000011-dynamic-block-selector.md
│   └── ENH0000012-build-order-export-import.md
└── phase4/            # Phase 4 specs
    ├── README.md
    ├── ENH0000016-cicd-pipeline.md
    ├── ENH0000012-e2e-testing.md
    └── ENH0000019-core-app.md
```

## How to Use

1. **Review the spec** for quick reference and file links
2. **Read the full ENH doc** for complete design details
3. **Ask Kiro to implement**: "Implement ENH0000010"
4. **Track progress** by checking off tasks in the spec

## Spec vs ENH Doc

- **Spec** (`.kiro/specs/`) = Implementation checklist + file references
- **ENH Doc** (`docs/enhancementRequests/`) = Full design + requirements + rationale

Both work together to guide implementation.
