# Enhancement Request: Create Components App and Model

**Filename:** `inReview-enh0000002-create-components-app-model.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000002  
**Status:** inReview  
**Priority:** High  
**Created Date:** 2026-01-20  
**Updated Date:** 2026-01-20  
**Assigned To:**  
**Estimated Effort:** 6 hours  

---

## Summary

Create the components Django app with Component model including JSONField for material recipes and admin interface.

---

## Description

Implement the components app as part of Phase 1 database setup. This app manages component data including materials (ores), fabricator type, and crafting time. Components are intermediate items crafted from ores and used to build blocks.

The JSONField for materials requires validation helpers to ensure data integrity. This enhancement establishes the middle layer of the resource calculation chain.

---

## Current Behavior

The components app does not exist in the project.

---

## Proposed Behavior

- Django app `components` created and registered in settings
- Component model with UUIDv7 primary keys and JSONField for materials
- Foreign key validation helper methods for ore references
- Admin interface with JSONField display
- Migrations applied successfully

---

## Acceptance Criteria

- [ ] Components app created via `python manage.py startapp components`
- [ ] App registered in `se2CalcProject/settings.py` INSTALLED_APPS
- [ ] Component model defined with all required fields
- [ ] JSONField validation helpers implemented
- [ ] Admin interface displays components with formatted JSON
- [ ] Migrations created and applied
- [ ] **Comprehensive automated test suite created (35+ tests minimum)** ← Updated per ENH-0000001
- [ ] All tests pass (100% pass rate required)
- [ ] Documentation updated (deployment guide, post-deployment review, test documentation)

---

## Technical Details

### Dependencies
- uuid-utils library for UUIDv7 support (use lambda wrapper: `default=lambda: str(uuid7())`)
- Django 6.0.1 (includes JSONField)
- ENH-0000001 (Ores app must exist first) ✅ **Now completed**
- **Note:** Based on ENH-0000001 deployment, always wrap uuid7() in lambda to convert to string for Django compatibility

### Affected Components
- components app (new)
- se2CalcProject/settings.py

### Files to Modify/Create
- `components/__init__.py`
- `components/models.py`
- `components/admin.py`
- `components/apps.py`
- `components/migrations/0001_initial.py`
- `se2CalcProject/settings.py`

### Database Changes
- [x] Migrations required
- [x] New models
- [ ] Schema changes

---

## Implementation Plan

**Reference:** See [ENH-0000001 Deployment Guide](../enh0000001/ENH-0000001-deployment-guide.md) for detailed step-by-step process example.

### Step 1: Create Django App
Run `uv run python manage.py startapp components` and register in INSTALLED_APPS

### Step 2: Define Component Model
Create model with base fields plus material (JSONField), fabricator, crafting_time

**Important:** Use `default=lambda: str(uuid7())` for component_id field (not just `default=uuid7`)
- This ensures Django's UUIDField validation passes
- Converts uuid_utils.UUID to string format expected by Django

### Step 3: Add Validation Helpers
Implement methods to validate ore_id references in material JSONField

### Step 4: Configure Admin
Register Component model with custom JSONField display formatting

### Step 5: Create and Apply Migrations
Generate and apply migrations to database

### Step 6: Create Comprehensive Test Suite
Based on ENH-0000001 experience:
- Create 35+ automated tests minimum
- Organize into logical test classes (creation, validation, relationships, integration)
- Aim for 100% code path coverage
- Include tests for JSONField validation and ore reference validation
- Tests should run in < 0.5 seconds

**Test Categories to Include:**
- Model creation tests (with and without optional fields)
- JSONField format validation tests
- Foreign key validation helper tests
- Admin interface tests
- Integration tests for complete workflows
- Relationship tests with Ore model

---

## Testing Requirements

**Updated based on ENH-0000001 best practices:**

### Unit Tests
- [ ] Test Component model creation (with all fields)
- [ ] Test Component model creation (minimal fields)
- [ ] Test UUIDv7 generation and uniqueness
- [ ] Test JSONField material format validation
- [ ] Test invalid material data rejection
- [ ] Test foreign key validation helpers
- [ ] Test __str__ method
- [ ] Test timestamp auto-population (created_at, updated_at)
- [ ] Test timestamp immutability (created_at doesn't change)
- [ ] Test ore_id validation in materials JSON
- [ ] Test mass field with various numeric values
- [ ] Test unique name constraint
- [ ] **Minimum 12+ unit tests** (ENH-0000001 had 20+ core unit tests)

### Integration Tests
- [ ] Test admin interface CRUD operations (create, read, update, delete)
- [ ] Test material JSONField with valid ore references
- [ ] Test bulk component creation
- [ ] Test component queries and filtering
- [ ] Test update operations with JSONField changes
- [ ] Test relationship integrity with Ore model
- [ ] **Minimum 6+ integration tests** (ENH-0000001 had 4 core integration tests)

### Manual Testing
- [ ] Create component via Django shell with valid material JSON
- [ ] Create component via admin interface
- [ ] Verify JSONField displays correctly in admin
- [ ] Test that invalid ore_id references are caught
- [ ] Test component ordering and filtering

### Additional Requirements
- [ ] **Total test coverage: 35+ tests minimum** (target same as ENH-0000001)
- [ ] **All tests passing (100% pass rate)**
- [ ] **Tests run in < 0.5 seconds**
- [ ] **Organized into 8+ test classes by functionality**
- [ ] **All tests include descriptive docstrings**

---

## Documentation Updates

- [ ] CHANGELOG.md
- [ ] Phase 1 checklist
- [ ] JSONField format documentation for frontend

---

## Risks and Considerations

- Risk: JSONField validation complexity - Mitigation: Create comprehensive validation helpers (validate in model methods)
- Risk: Ore references in JSON not enforced by database - Mitigation: Application-level validation required in model validators
- **Risk: UUID library compatibility** - Mitigation: Use `default=lambda: str(uuid7())` wrapper (learned from ENH-0000001)
- **Risk: Incomplete testing** - Mitigation: Create 35+ tests minimum per ENH-0000001 standards
- **Risk: Poor documentation** - Mitigation: Follow ENH-0000001 documentation templates (deployment guide, post-review, test docs)

---

## Alternatives Considered

### Alternative 1: Use ManyToMany relationship instead of JSONField
Not chosen because quantities are required per ore, and JSONField provides flexibility

### Alternative 2: Separate ComponentMaterial model
Not chosen to keep initial implementation simple; can refactor later if needed

---

## Related Issues/Enhancements

- ENH-0000001: Create Ores App and Model (dependency)
- ENH-0000003: Create Blocks App and Model

---

## Notes

### Model Implementation Notes
Model fields:
- component_id: `UUIDField(primary_key=True, default=lambda: str(uuid7()))` ← **Lambda wrapper is critical**
- name: CharField(max_length=100), unique, required
- description: TextField, blank=True
- mass: FloatField, required
- material: JSONField - Format: [{
    "ore_id": "uuid-string",
    "quantity": float
  }]
- fabricator: CharField(max_length=50)
- crafting_time: FloatField (in seconds)
- created_at: DateTimeField, auto_now_add=True
- updated_at: DateTimeField, auto_now=True

### Material JSONField Validation
Implement model method to validate material data:
```python
def validate_materials(self):
    """Validate material JSONField references valid ores."""
    if not self.material:
        return
    
    for material in self.material:
        if 'ore_id' not in material:
            raise ValidationError("Each material must have 'ore_id'")
        
        # Check if ore exists
        try:
            Ore.objects.get(ore_id=material['ore_id'])
        except Ore.DoesNotExist:
            raise ValidationError(f"Invalid ore_id: {material['ore_id']}")
```

### Lessons from ENH-0000001 Deployment
- ✅ Always wrap uuid7() in lambda for Django compatibility: `default=lambda: str(uuid7())`
- ✅ Create comprehensive test suite immediately (35+ tests minimum)
- ✅ Organize tests into 8+ logical test classes
- ✅ Include deployment, post-deployment, and test documentation
- ✅ Target 100% pass rate and < 0.5 second execution time
- ✅ Document all decisions and issues encountered
- ✅ Create README.md in enhancement directory for quick reference
- ✅ Reference ENH-0000001 documentation templates for consistency

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
