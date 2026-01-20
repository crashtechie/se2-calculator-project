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

## Lessons from Previous Enhancements

**UUID Implementation Pattern (from ENH-0000001, ENH-0000002, ENH-0000003):**
- ✅ All models use `generate_uuid()` helper function for runtime UUID generation
- ✅ Fixtures must contain **pre-generated UUIDv7 strings** (static values)
- ✅ Each fixture UUID must be unique across all fixture files
- ✅ Material/component references in fixtures must use exact UUID matches
- ✅ Fixture loading order matters: ores → components → blocks
- ⚠️ Do NOT use lambda functions or function calls in fixture files (use static strings only)

**Testing Standards (from ENH-0000001, ENH-0000002, ENH-0000003):**
- Minimum 35+ automated tests per enhancement
- 100% test pass rate required
- Test execution time < 0.5 seconds
- Organized into 8+ test classes by functionality

**Documentation Requirements (from ENH-0000001, ENH-0000002, ENH-0000003):**
- Deployment guide required
- Post-deployment review required
- Testing validation document required
- All docs in `/docs/enhancementRequests/phase1_models/ENH0000004/` directory

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

### Fixture Content Requirements
- [ ] Ore fixtures created with at least 5 sample ores
- [ ] Component fixtures created with at least 10 sample components
- [ ] Block fixtures created with at least 15 sample blocks
- [ ] All fixtures use valid UUIDv7 format (pre-generated strings)
- [ ] All UUIDs are unique across all fixture files
- [ ] JSONField data properly formatted (materials, components)
- [ ] Fixtures load without errors using `loaddata` command
- [ ] Relationships between fixtures are valid (foreign key references)
- [ ] Material quantities are realistic and balanced

### Testing Requirements
- [ ] Comprehensive automated test suite (minimum 35+ tests)
- [ ] 100% test pass rate
- [ ] Test execution time < 0.5 seconds
- [ ] Tests organized into 8+ test classes by functionality
- [ ] All tests include descriptive docstrings

### Documentation Requirements
- [ ] ENH-0000004 Deployment Guide created
- [ ] ENH-0000004 Post-Deployment Review completed
- [ ] ENH-0000004 Testing Validation document created
- [ ] README.md updated with fixture loading instructions
- [ ] Phase 1 checklist updated
- [ ] CHANGELOG.md updated

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
- `ores/tests.py` (add fixture tests)
- `components/tests.py` (add fixture tests)
- `blocks/tests.py` (add fixture tests)
- `docs/enhancementRequests/phase1_models/ENH0000004/ENH-0000004-deployment-guide.md`
- `docs/enhancementRequests/phase1_models/ENH0000004/ENH-0000004-post-deployment-review.md`
- `docs/enhancementRequests/phase1_models/ENH0000004/ENH-0000004-testing-validation.md`
- `docs/projectPlan/phase1_models.md` (update with fixture info)
- `README.md` (add fixture loading instructions)
- `CHANGELOG.md` (add ENH-0000004 entry)

### Database Changes
- [ ] Migrations required
- [ ] New models
- [ ] Schema changes

---

## Implementation Plan

### Step 1: Create Fixture Directories
Create fixtures/ directories in ores/, components/, and blocks/ apps if they don't exist

### Step 2: Research SE2 Data
Gather realistic ore, component, and block data from Space Engineers 2:
- Ore names, descriptions, and masses
- Component recipes (which ores, quantities)
- Block requirements (which components, quantities)
- Crafting times and fabricator types

### Step 3: Generate UUIDv7 Strings
Pre-generate UUIDv7 strings for all fixture objects:
- Use Python script with `uuid_utils.uuid7()` to generate strings
- Create a mapping document (UUIDs to entity names) for reference
- Ensure all UUIDs are unique across all fixtures

### Step 4: Create Ore Fixtures
Create `ores/fixtures/sample_ores.json` with sample ores:
- Minimum 5 ores (Iron, Silicon, Nickel, Cobalt, Silver)
- Each with pre-generated UUIDv7 string as pk
- Include name, description, and realistic mass values

### Step 5: Create Component Fixtures
Create `components/fixtures/sample_components.json` with sample components:
- Minimum 10 components (Steel Plate, Construction Component, Motor, etc.)
- Each with pre-generated UUIDv7 string as pk
- materials JSONField references ore UUIDs from Step 4
- Include crafting_time, mass, and fabricator_type

### Step 6: Create Block Fixtures
Create `blocks/fixtures/sample_blocks.json` with sample blocks:
- Minimum 15 blocks (Light Armor, Heavy Armor, Reactor, etc.)
- Each with pre-generated UUIDv7 string as pk
- components JSONField references component UUIDs from Step 5
- Include all block-specific fields (health, pcu, consumer/producer rates, etc.)

### Step 7: Create Comprehensive Test Suite
Create automated tests covering:
- JSON schema validation (35+ tests minimum)
- UUID format validation
- Relationship integrity
- Fixture loading
- Data validation
- Organize into 8+ test classes
- Target: 100% pass rate, < 0.5s execution

### Step 8: Test Fixture Loading
Load fixtures and verify data integrity and relationships

---

## Testing Requirements

**Target:** Minimum 35+ automated tests, 100% pass rate, < 0.5s execution time

### Unit Tests (20+ tests)

**Fixture File Validation Tests (FixtureFileValidationTests):**
- [ ] Test ore fixture file is valid JSON
- [ ] Test component fixture file is valid JSON
- [ ] Test block fixture file is valid JSON
- [ ] Test ore fixture has required fields
- [ ] Test component fixture has required fields
- [ ] Test block fixture has required fields

**UUID Format Tests (UUIDFormatValidationTests):**
- [ ] Test all ore UUIDs are valid UUIDv7 format
- [ ] Test all component UUIDs are valid UUIDv7 format
- [ ] Test all block UUIDs are valid UUIDv7 format
- [ ] Test all UUIDs are unique across fixtures
- [ ] Test no duplicate UUIDs within each fixture

**Data Validation Tests (FixtureDataValidationTests):**
- [ ] Test ore names are unique
- [ ] Test component names are unique
- [ ] Test block names are unique
- [ ] Test ore mass values are positive
- [ ] Test component mass values are positive
- [ ] Test block mass values are positive

### Integration Tests (10+ tests)

**Fixture Loading Tests (FixtureLoadingTests):**
- [ ] Test loading ores fixture alone
- [ ] Test loading components fixture (with ore dependencies)
- [ ] Test loading blocks fixture (with component dependencies)
- [ ] Test loading all fixtures in correct sequence
- [ ] Test fixture loading is idempotent

**Relationship Integrity Tests (RelationshipIntegrityTests):**
- [ ] Test component materials reference valid ore UUIDs
- [ ] Test block components reference valid component UUIDs
- [ ] Test ore relationships can be queried from components
- [ ] Test component relationships can be queried from blocks
- [ ] Test cascading queries work (block → component → ore)

### Manual Testing
- [ ] Load fixtures into fresh database
- [ ] Verify data appears correctly in admin
- [ ] Verify relationships are intact
- [ ] Verify JSON fields display properly
- [ ] Test fixture reload (ensure no errors on re-run)

---

## Documentation Updates

### Required Documents (following ENH-0000001/002/003 pattern):

1. **ENH-0000004 Deployment Guide** (`ENH-0000004-deployment-guide.md`)
   - Step-by-step fixture creation instructions
   - UUID generation procedure
   - Fixture loading commands
   - Verification steps

2. **ENH-0000004 Post-Deployment Review** (`ENH-0000004-post-deployment-review.md`)
   - Deployment validation results
   - Test suite results
   - Issues encountered and resolutions
   - Metrics and performance data

3. **ENH-0000004 Testing Validation** (`ENH-0000004-testing-validation.md`)
   - Complete test case documentation
   - Test execution results
   - Coverage analysis

### Updates to Existing Documents:
- [ ] README.md (add fixture loading instructions with examples)
- [ ] `docs/projectPlan/phase1_models.md` (mark ENH-0000004 complete)
- [ ] `docs/projectPlan/checklist.md` (update completion status)
- [ ] CHANGELOG.md (add ENH-0000004 entry with date)

### Directory Structure:
All ENH-0000004 documentation in:  
`/docs/enhancementRequests/phase1_models/ENH0000004/`

---

## Risks and Considerations

### High Priority Risks

**Risk 1: UUID Format Incompatibility**
- **Risk:** Using incorrect UUID format or non-UUIDv7 strings
- **Impact:** Database primary key validation failures
- **Mitigation:** Use `uuid_utils.uuid7()` to generate strings; validate with regex pattern
- **Lesson from:** ENH-0000001, ENH-0000002

**Risk 2: Hardcoded UUIDs Conflict with Existing Data**
- **Risk:** Fixture UUIDs may conflict with existing database records
- **Impact:** loaddata command will fail with primary key conflicts
- **Mitigation:** Document that fixtures are for fresh databases only; provide flush command
- **Status:** Acceptable for development/testing environments

**Risk 3: Invalid Relationship References**
- **Risk:** Component materials reference non-existent ore UUIDs
- **Impact:** Data integrity violations, validation failures
- **Mitigation:** Create UUID mapping document; validate references before committing
- **Testing:** Comprehensive relationship integrity tests required

### Medium Priority Risks

**Risk 4: SE2 Game Data Changes**
- **Risk:** Space Engineers 2 balancing updates may invalidate fixture data
- **Impact:** Fixtures contain outdated information
- **Mitigation:** Version fixtures (v1.0, v1.1); update as needed; document version in filenames

**Risk 5: Incomplete Test Coverage**
- **Risk:** Missing edge cases in fixture validation
- **Impact:** Runtime errors when fixtures are loaded
- **Mitigation:** Achieve minimum 35+ tests covering all validation scenarios
- **Lesson from:** ENH-0000002 (44 tests), ENH-0000003 (49 tests)

**Risk 6: Poor Documentation**
- **Risk:** Developers may not understand how to use fixtures
- **Impact:** Reduced adoption, support burden
- **Mitigation:** Follow ENH-0000001/002/003 documentation template; include examples

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

## Fixture Format Specification

### Ore Fixture Format

**File:** `ores/fixtures/sample_ores.json`

**Structure:**
```json
[
  {
    "model": "ores.ore",
    "pk": "019d1234-5678-7abc-def0-123456789abc",
    "fields": {
      "name": "Iron Ore",
      "description": "Common metallic ore used in basic construction",
      "mass": 0.37
    }
  },
  {
    "model": "ores.ore",
    "pk": "019d1234-5678-7abc-def0-123456789abd",
    "fields": {
      "name": "Silicon Ore",
      "description": "Essential for electronic components",
      "mass": 0.27
    }
  }
]
```

**Important Notes:**
- `pk` field contains pre-generated UUIDv7 string (NOT a function call)
- All UUIDs must be unique across all fixture files
- `created_at` and `updated_at` are auto-generated, do not include in fixtures

### Component Fixture Format

**File:** `components/fixtures/sample_components.json`

**Structure:**
```json
[
  {
    "model": "components.component",
    "pk": "019d5678-1234-7def-0123-456789abcdef",
    "fields": {
      "name": "Steel Plate",
      "description": "Basic construction material made from iron",
      "materials": {
        "019d1234-5678-7abc-def0-123456789abc": 3
      },
      "mass": 20.0,
      "crafting_time": 2.5,
      "fabricator_type": "Assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "019d5678-1234-7def-0123-456789abcdf0",
    "fields": {
      "name": "Computer",
      "description": "Advanced component for control systems",
      "materials": {
        "019d1234-5678-7abc-def0-123456789abd": 2
      },
      "mass": 0.5,
      "crafting_time": 5.0,
      "fabricator_type": "Assembler"
    }
  }
]
```

**Important Notes:**
- `materials` is a JSON object: `{"<ore_uuid>": <quantity>}`
- Ore UUIDs in `materials` must match ores from `sample_ores.json`
- Use empty dict `{}` for components with no materials (not common)

### Block Fixture Format

**File:** `blocks/fixtures/sample_blocks.json`

**Structure:**
```json
[
  {
    "model": "blocks.block",
    "pk": "019d9abc-def0-7123-4567-89abcdef0123",
    "fields": {
      "name": "Light Armor Block",
      "description": "Basic armor block for ship construction",
      "components": [
        {
          "component_id": "019d5678-1234-7def-0123-456789abcdef",
          "component_name": "Steel Plate",
          "quantity": 5
        }
      ],
      "mass": 100.0,
      "health": 400.0,
      "pcu": 1,
      "snap_size": 1.25,
      "input_mass": 0,
      "output_mass": 0,
      "consumer_type": "",
      "consumer_rate": 0.0,
      "producer_type": "",
      "producer_rate": 0.0,
      "storage_capacity": 0.0
    }
  },
  {
    "model": "blocks.block",
    "pk": "019d9abc-def0-7123-4567-89abcdef0124",
    "fields": {
      "name": "Small Reactor",
      "description": "Compact nuclear reactor for power generation",
      "components": [
        {
          "component_id": "019d5678-1234-7def-0123-456789abcdef",
          "component_name": "Steel Plate",
          "quantity": 10
        },
        {
          "component_id": "019d5678-1234-7def-0123-456789abcdf0",
          "component_name": "Computer",
          "quantity": 5
        }
      ],
      "mass": 625.0,
      "health": 1000.0,
      "pcu": 15,
      "snap_size": 1.25,
      "input_mass": 0,
      "output_mass": 0,
      "consumer_type": "Uranium",
      "consumer_rate": 0.002,
      "producer_type": "Power",
      "producer_rate": 15000.0,
      "storage_capacity": 0.0
    }
  }
]
```

**Important Notes:**
- `components` is a JSON array of objects with `component_id`, `component_name`, and `quantity`
- Component UUIDs must match components from `sample_components.json`
- Include `component_name` for readability (used by validation helpers)
- Consumer/producer fields can be empty strings and 0.0 for non-functional blocks

---

## Notes

Sample data should include:
- Common ores: Iron, Silicon, Nickel, Cobalt, Silver, Gold, Platinum, Uranium
- Common components: Steel Plate, Construction Component, Motor, Computer, etc.
- Common blocks: Light Armor, Heavy Armor, Reactor, Battery, Assembler, etc.

### Fixture Loading Commands:

**Load all fixtures in correct order:**
```bash
# Load in sequence (order matters!)
uv run python manage.py loaddata sample_ores
uv run python manage.py loaddata sample_components
uv run python manage.py loaddata sample_blocks
```

**Or load all at once:**
```bash
uv run python manage.py loaddata sample_ores sample_components sample_blocks
```

**For fresh database (flush existing data first):**
```bash
# WARNING: This deletes all data!
uv run python manage.py flush --no-input
uv run python manage.py loaddata sample_ores sample_components sample_blocks
```

**Verify fixtures loaded:**
```bash
uv run python manage.py shell
>>> from ores.models import Ore
>>> from components.models import Component
>>> from blocks.models import Block
>>> print(f"Ores: {Ore.objects.count()}")
>>> print(f"Components: {Component.objects.count()}")
>>> print(f"Blocks: {Block.objects.count()}")
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
