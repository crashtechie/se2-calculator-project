# Enhancement Request: Create Sample Data Fixtures

**Filename:** `ENH0000004-create-sample-fixtures.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000004  
**Status:** Approved  
**Priority:** Medium  
**Created Date:** 2026-01-20  
**Updated Date:** 2026-01-20  
**Assigned To:**  Dan Smith  
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
- [ ] Migrations required: **No** (fixtures only, no schema changes)
- [ ] New models: **No**
- [ ] Schema changes: **No**

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
Pre-generate UUIDv7 strings for all fixture objects using this script:

**Script:** `scripts/generate_fixture_uuids.py`
```python
from uuid_utils import uuid7

# Generate UUIDs for ores (minimum 5)
print("=== ORES ===")
ores = ["Iron Ore", "Silicon Ore", "Nickel Ore", "Cobalt Ore", "Silver Ore", "Gold Ore", "Platinum Ore", "Uranium Ore"]
for ore_name in ores:
    print(f"{ore_name}: {str(uuid7())}")

print("\n=== COMPONENTS ===")
# Generate UUIDs for components (minimum 10)
components = [
    "Steel Plate", "Construction Component", "Motor", "Computer",
    "Large Steel Tube", "Metal Grid", "Interior Plate", "Small Steel Tube",
    "Display", "Bulletproof Glass", "Girder", "Power Cell"
]
for comp_name in components:
    print(f"{comp_name}: {str(uuid7())}")

print("\n=== BLOCKS ===")
# Generate UUIDs for blocks (minimum 15)
blocks = [
    "Light Armor Block", "Heavy Armor Block", "Small Reactor", "Large Reactor",
    "Battery", "Assembler", "Refinery", "O2/H2 Generator",
    "Cockpit", "Gyroscope", "Thruster", "Container",
    "Connector", "Merge Block", "Landing Gear", "Spotlight",
    "Antenna", "Beacon"
]
for block_name in blocks:
    print(f"{block_name}: {str(uuid7())}")
```

**Run the script:**
```bash
uv run python scripts/generate_fixture_uuids.py > docs/enhancementRequests/phase1_models/ENH0000004/uuid-mapping.txt
```

**Create mapping document:** `docs/enhancementRequests/phase1_models/ENH0000004/uuid-mapping.md`
- Document each UUID with its corresponding entity name
- Use this as reference when creating fixture files
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

**Add fixture tests to existing test files:**
- `ores/tests.py` - Add fixture test classes
- `components/tests.py` - Add fixture test classes
- `blocks/tests.py` - Add fixture test classes

**Or create dedicated fixture test files (recommended for organization):**
- `ores/tests_fixtures.py`
- `components/tests_fixtures.py`
- `blocks/tests_fixtures.py`

**Test requirements:**
- JSON schema validation (35+ tests minimum)
- UUID format validation
- Relationship integrity
- Fixture loading
- Data validation
- Organize into 8+ test classes (see Testing Requirements section)
- Target: 100% pass rate, < 0.5s execution

### Step 8: Test Fixture Loading

**Create verification script:** `scripts/verify_fixtures.py`
```python
#!/usr/bin/env python
"""Verify fixture integrity and relationships."""
import json
import re
from pathlib import Path

# UUIDv7 regex pattern
UUID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
    re.IGNORECASE
)

def verify_fixtures():
    """Verify all fixture files for integrity and relationships."""
    print("🔍 Verifying fixture files...\n")
    
    # Load fixture files
    ores = json.load(open('ores/fixtures/sample_ores.json'))
    components = json.load(open('components/fixtures/sample_components.json'))
    blocks = json.load(open('blocks/fixtures/sample_blocks.json'))
    
    print(f"Loaded {len(ores)} ores, {len(components)} components, {len(blocks)} blocks")
    
    # Collect all UUIDs
    ore_uuids = {ore['pk'] for ore in ores}
    component_uuids = {comp['pk'] for comp in components}
    block_uuids = {block['pk'] for block in blocks}
    
    # Verify counts
    assert len(ores) >= 5, f"Need at least 5 ores, got {len(ores)}"
    assert len(components) >= 10, f"Need at least 10 components, got {len(components)}"
    assert len(blocks) >= 15, f"Need at least 15 blocks, got {len(blocks)}"
    print("✅ Minimum counts met")
    
    # Verify UUID uniqueness
    all_uuids = ore_uuids | component_uuids | block_uuids
    assert len(all_uuids) == len(ores) + len(components) + len(blocks), "Duplicate UUIDs found!"
    print("✅ All UUIDs are unique")
    
    # Verify UUIDv7 format
    for uuid in all_uuids:
        assert UUID_PATTERN.match(uuid), f"Invalid UUIDv7 format: {uuid}"
    print("✅ All UUIDs are valid UUIDv7 format")
    
    # Verify component material references
    for comp in components:
        for ore_id in comp['fields']['materials'].keys():
            assert ore_id in ore_uuids, f"Component '{comp['fields']['name']}' references invalid ore UUID: {ore_id}"
    print("✅ All component material references are valid")
    
    # Verify block component references
    for block in blocks:
        for comp_ref in block['fields']['components']:
            comp_id = comp_ref['component_id']
            assert comp_id in component_uuids, f"Block '{block['fields']['name']}' references invalid component UUID: {comp_id}"
            assert 'component_name' in comp_ref, f"Missing component_name in block '{block['fields']['name']}'"
            assert 'quantity' in comp_ref, f"Missing quantity in block '{block['fields']['name']}'"
    print("✅ All block component references are valid")
    
    print("\n🎉 All fixtures verified successfully!")

if __name__ == '__main__':
    verify_fixtures()
```

**Run verification:**
```bash
uv run python scripts/verify_fixtures.py
```

**Load fixtures and verify data:**
```bash
# Load in correct order
uv run python manage.py loaddata sample_ores sample_components sample_blocks

# Verify in Django shell
uv run python manage.py shell
>>> from ores.models import Ore
>>> from components.models import Component
>>> from blocks.models import Block
>>> print(f"Ores: {Ore.objects.count()}")
>>> print(f"Components: {Component.objects.count()}")
>>> print(f"Blocks: {Block.objects.count()}")
```

---

## Testing Requirements

**Target:** Minimum 35+ automated tests, 100% pass rate, < 0.5s execution time

### Unit Tests (23+ tests)

**Fixture File Validation Tests (FixtureFileValidationTests):** (6 tests)
- [ ] Test ore fixture file is valid JSON
- [ ] Test component fixture file is valid JSON
- [ ] Test block fixture file is valid JSON
- [ ] Test ore fixture has required fields
- [ ] Test component fixture has required fields
- [ ] Test block fixture has required fields

**UUID Format Tests (UUIDFormatValidationTests):** (5 tests)
- [ ] Test all ore UUIDs are valid UUIDv7 format
- [ ] Test all component UUIDs are valid UUIDv7 format
- [ ] Test all block UUIDs are valid UUIDv7 format
- [ ] Test all UUIDs are unique across fixtures
- [ ] Test no duplicate UUIDs within each fixture

**Data Validation Tests (FixtureDataValidationTests):** (6 tests)
- [ ] Test ore names are unique
- [ ] Test component names are unique
- [ ] Test block names are unique
- [ ] Test ore mass values are positive
- [ ] Test component mass values are positive
- [ ] Test block mass values are positive

**JSONField Format Tests (JSONFieldFormatTests):** (6 tests)
- [ ] Test component materials field is valid JSON object
- [ ] Test block components field is valid JSON array
- [ ] Test materials keys are valid UUIDs
- [ ] Test component objects have required fields (component_id, component_name, quantity)
- [ ] Test materials quantities are positive numbers
- [ ] Test component quantities are positive integers

### Integration Tests (15+ tests)

**Fixture Loading Tests (FixtureLoadingTests):** (5 tests)
- [ ] Test loading ores fixture alone
- [ ] Test loading components fixture (with ore dependencies)
- [ ] Test loading blocks fixture (with component dependencies)
- [ ] Test loading all fixtures in correct sequence
- [ ] Test fixture loading is idempotent

**Relationship Integrity Tests (RelationshipIntegrityTests):** (5 tests)
- [ ] Test component materials reference valid ore UUIDs
- [ ] Test block components reference valid component UUIDs
- [ ] Test ore relationships can be queried from components
- [ ] Test component relationships can be queried from blocks
- [ ] Test cascading queries work (block → component → ore)

**Fixture Content Tests (FixtureContentTests):** (3 tests)
- [ ] Test minimum ore count (5+)
- [ ] Test minimum component count (10+)
- [ ] Test minimum block count (15+)

**Admin Integration Tests (AdminIntegrationTests):** (2 tests)
- [ ] Test fixtures display correctly in admin list view
- [ ] Test fixture data can be viewed via admin detail view

**Total: 38 tests across 8 test classes** (exceeds 35+ minimum requirement)

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

**Risk 7: Timestamp Timezone Issues**
- **Risk:** Auto-generated timestamps may not match expected timezone in tests
- **Impact:** Test assertions that compare timestamps may fail
- **Mitigation:** Document that `created_at`/`updated_at` are auto-set on fixture load; exclude from fixture files
- **Testing:** Verify timestamps are timezone-aware (USE_TZ=True) in tests

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

⚠️ **CRITICAL: Loading Order**

Fixtures **must** be loaded in this exact order due to foreign key dependencies:
1. `sample_ores.json` (no dependencies)
2. `sample_components.json` (depends on ores)
3. `sample_blocks.json` (depends on components)

Loading in wrong order will cause `IntegrityError` validation failures!

### Ore Fixture Format

**File:** `ores/fixtures/sample_ores.json`

**Structure:**
```json
[
  {
    "model": "ores.ore",
    "pk": "019e5c8a-3d7f-7b2e-9a1c-4f6d8e0b2a3c",
    "fields": {
      "name": "Iron Ore",
      "description": "Common metallic ore used in basic construction",
      "mass": 0.37
    }
  },
  {
    "model": "ores.ore",
    "pk": "019e5c8a-4e8f-7c3d-8b2a-5g7e9f1c3b4d",
    "fields": {
      "name": "Silicon Ore",
      "description": "Essential ore for computer and display components",
      "mass": 0.42
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
    "pk": "019e5c8a-5f9g-7d4e-9c3b-6h8f0g2d4c5e",
    "fields": {
      "name": "Steel Plate",
      "description": "Basic building material",
      "materials": {
        "019e5c8a-3d7f-7b2e-9a1c-4f6d8e0b2a3c": 21.0
      },
      "crafting_time": 2.5,
      "mass": 20.0,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "019e5c8a-6g0h-7e5f-0d4c-7i9g1h3e5d6f",
    "fields": {
      "name": "Construction Component",
      "description": "Used in constructing blocks",
      "materials": {
        "019e5c8a-3d7f-7b2e-9a1c-4f6d8e0b2a3c": 8.0
      },
      "crafting_time": 1.5,
      "mass": 8.0,
      "fabricator_type": "assembler"
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
    "pk": "019e5c8a-7h1i-7f6g-1e5d-8j0h2i4f6e7g",
    "fields": {
      "name": "Light Armor Block",
      "description": "Basic armor protection",
      "components": [
        {
          "component_id": "019e5c8a-5f9g-7d4e-9c3b-6h8f0g2d4c5e",
          "component_name": "Steel Plate",
          "quantity": 25
        }
      ],
      "mass": 500.0,
      "max_health": 15000,
      "pcu_cost": 1,
      "power_consumer": "",
      "power_consumer_rate": 0.0,
      "power_producer": "",
      "power_producer_rate": 0.0,
      "max_storage": "",
      "max_storage_amount": 0.0
    }
  },
  {
    "model": "blocks.block",
    "pk": "019e5c8a-8i2j-7g7h-2f6e-9k1i3j5g7f8h",
    "fields": {
      "name": "Small Reactor",
      "description": "Generates power from uranium",
      "components": [
        {
          "component_id": "019e5c8a-5f9g-7d4e-9c3b-6h8f0g2d4c5e",
          "component_name": "Steel Plate",
          "quantity": 50
        },
        {
          "component_id": "019e5c8a-6g0h-7e5f-0d4c-7i9g1h3e5d6f",
          "component_name": "Construction Component",
          "quantity": 20
        }
      ],
      "mass": 2500.0,
      "max_health": 25000,
      "pcu_cost": 75,
      "power_consumer": "",
      "power_consumer_rate": 0.0,
      "power_producer": "MW",
      "power_producer_rate": 15.0,
      "max_storage": "",
      "max_storage_amount": 0.0
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

### Expected Directory Structure After Implementation:
```
ores/
  fixtures/
    sample_ores.json (5+ ores)
components/
  fixtures/
    sample_components.json (10+ components)
blocks/
  fixtures/
    sample_blocks.json (15+ blocks)
docs/enhancementRequests/phase1_models/ENH0000004/
  ENH-0000004-deployment-guide.md
  ENH-0000004-post-deployment-review.md
  ENH-0000004-testing-validation.md
  uuid-mapping.md (UUID → entity name reference)
scripts/
  generate_fixture_uuids.py (UUID generation script)
  verify_fixtures.py (fixture validation script)
```

### Sample Data Content:
Sample data should include:
- Common ores: Iron, Silicon, Nickel, Cobalt, Silver, Gold, Platinum, Uranium
- Common components: Steel Plate, Construction Component, Motor, Computer, Large Steel Tube, Metal Grid, Interior Plate, Small Steel Tube, Display, Bulletproof Glass, Girder, Power Cell
- Common blocks: Light Armor, Heavy Armor, Small Reactor, Large Reactor, Battery, Assembler, Refinery, O2/H2 Generator, Cockpit, Gyroscope, Thruster, Container, Connector, Merge Block, Landing Gear, Spotlight, Antenna, Beacon

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
| 2026-01-20 | Approved | Enhancement request reviewed and approved |

---

## Sign-off

**Reviewed By:**  
**Approved By:**  
**Completed By:**  
**Completion Date:**
