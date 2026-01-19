# Enhancement Request: Create Sample Data Fixtures

**Filename:** `inReview-enh0000004-create-sample-fixtures.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000004  
**Status:** inReview  
**Priority:** Medium  
**Created Date:** 2026-01-20  
**Updated Date:** 2026-01-20  
**Assigned To:**  
**Estimated Effort:** 4 hours  

---

## Summary

Create JSON fixtures with sample ore, component, and block data for testing and development.

---

## Description

Create fixture files containing realistic sample data from Space Engineers 2 for ores, components, and blocks. These fixtures will be used for testing, development, and demonstration purposes.

Fixtures provide consistent test data and allow developers to quickly populate the database with realistic examples. This enhancement benefits both developers (for testing) and end-users (for demonstration).

---

## Current Behavior

No sample data exists. Database must be manually populated for testing.

---

## Proposed Behavior

- JSON fixture files created for each app
- Sample data includes realistic SE2 game data
- Fixtures can be loaded with `python manage.py loaddata`
- Data includes proper relationships (ores → components → blocks)

---

## Acceptance Criteria

- [ ] Ore fixtures created with at least 5 sample ores
- [ ] Component fixtures created with at least 10 sample components
- [ ] Block fixtures created with at least 15 sample blocks
- [ ] All fixtures use valid UUIDv7 format
- [ ] JSONField data properly formatted
- [ ] Fixtures load without errors
- [ ] Relationships between fixtures are valid
- [ ] Documentation updated with fixture usage

---

## Technical Details

### Dependencies
- ENH-0000001: Create Ores App and Model (dependency)
- ENH-0000002: Create Components App and Model (dependency)
- ENH-0000003: Create Blocks App and Model (dependency)

### Affected Components
- ores/fixtures/
- components/fixtures/
- blocks/fixtures/

### Files to Modify/Create
- `ores/fixtures/sample_ores.json`
- `components/fixtures/sample_components.json`
- `blocks/fixtures/sample_blocks.json`
- `docs/projectPlan/phase1_models.md` (update with fixture info)

### Database Changes
- [ ] Migrations required
- [ ] New models
- [ ] Schema changes

---

## Implementation Plan

### Step 1: Research SE2 Data
Gather realistic ore, component, and block data from Space Engineers 2

### Step 2: Create Ore Fixtures
Create JSON file with sample ores (Iron, Silicon, Nickel, etc.)

### Step 3: Create Component Fixtures
Create JSON file with sample components referencing ore UUIDs

### Step 4: Create Block Fixtures
Create JSON file with sample blocks referencing component UUIDs

### Step 5: Test Fixture Loading
Load fixtures and verify data integrity and relationships

---

## Testing Requirements

### Unit Tests
- [ ] Test fixture files are valid JSON
- [ ] Test UUIDs are valid UUIDv7 format

### Integration Tests
- [ ] Test loading ores fixture
- [ ] Test loading components fixture (with ore dependencies)
- [ ] Test loading blocks fixture (with component dependencies)
- [ ] Test loading all fixtures in sequence

### Manual Testing
- [ ] Load fixtures into fresh database
- [ ] Verify data appears correctly in admin
- [ ] Verify relationships are intact

---

## Documentation Updates

- [ ] README.md (add fixture loading instructions)
- [ ] Phase 1 checklist
- [ ] CHANGELOG.md

---

## Risks and Considerations

- Risk: Hardcoded UUIDs may conflict with existing data - Mitigation: Document that fixtures are for fresh databases
- Risk: SE2 game data may change - Mitigation: Version fixtures and update as needed

---

## Alternatives Considered

### Alternative 1: Use factory_boy for dynamic fixtures
Not chosen because static JSON fixtures are simpler for initial implementation

### Alternative 2: Create fixtures via Django admin export
Not chosen because manual JSON creation provides better control

---

## Related Issues/Enhancements

- ENH-0000001: Create Ores App and Model (dependency)
- ENH-0000002: Create Components App and Model (dependency)
- ENH-0000003: Create Blocks App and Model (dependency)

---

## Notes

Sample data should include:
- Common ores: Iron, Silicon, Nickel, Cobalt, Silver, Gold, Platinum, Uranium
- Common components: Steel Plate, Construction Component, Motor, Computer, etc.
- Common blocks: Light Armor, Heavy Armor, Reactor, Battery, Assembler, etc.

Fixture loading command:
```bash
uv run python manage.py loaddata sample_ores sample_components sample_blocks
```

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-20 | inReview | Initial creation |

---

## Sign-off

**Reviewed By:**  
**Approved By:**  
**Completed By:**  
**Completion Date:**
