# Create Enhancement Request

Use this prompt to create a new enhancement request following project standards.

## Instructions

1. **Determine Phase**: Which phase does this enhancement belong to?
   - Phase 1: Models & Database
   - Phase 2: Views & Templates
   - Phase 3: Build Order Calculator
   - Phase 4: Testing & Documentation

2. **Generate ENH Number**: Use next available 7-digit number (check `docs/enhancementRequests/ENHANCEMENT_INDEX.md`)

3. **Create ENH Document** in appropriate phase directory:
   - Location: `docs/enhancementRequests/phase{N}_{name}/ENH{number}/`
   - Filename: `ENH{number}-{brief-description}.md`

4. **Required Sections**:
   - Header (ID, Title, Status, Priority, Phase, Effort)
   - Overview (Description, Business Value, Dependencies)
   - Requirements (Functional, Non-functional, Acceptance Criteria)
   - Technical Design (Implementation, Data Structures, API, Database)
   - Testing Strategy (Scenarios, Coverage, Edge Cases)
   - Documentation (User, Developer, API)
   - Implementation Checklist

5. **Update Index**: Add entry to `ENHANCEMENT_INDEX.md`

6. **Create Branch** (optional): `feature/ENH{number}-description`

## Template Variables

- `{ENH_NUMBER}`: 7-digit enhancement number
- `{TITLE}`: Brief descriptive title
- `{PHASE}`: Phase number and name
- `{PRIORITY}`: Critical/High/Medium/Low
- `{EFFORT}`: Estimated hours or days

## Example

```
ENH0000017: Add Export Functionality for Build Orders
Phase: 3 - Build Order Calculator
Priority: Medium
Effort: 8 hours
```

## Checklist

- [ ] ENH number is unique and sequential
- [ ] Placed in correct phase directory
- [ ] All required sections completed
- [ ] Acceptance criteria are testable
- [ ] Dependencies documented
- [ ] Added to ENHANCEMENT_INDEX.md
