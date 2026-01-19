# Enhancement Request: Create Blocks App and Model

**Filename:** `inReview-enh0000003-create-blocks-app-model.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000003  
**Status:** inReview  
**Priority:** High  
**Created Date:** 2026-01-20  
**Updated Date:** 2026-01-20  
**Assigned To:**  
**Estimated Effort:** 8 hours  

---

## Summary

Create the blocks Django app with Block model including complex fields for components, power, and storage.

---

## Description

Implement the blocks app as part of Phase 1 database setup. This app manages block data including component requirements, health, PCU, power consumption/production, and storage capacity. Blocks are the final buildable items in Space Engineers 2.

The Block model is the most complex, requiring validation for consumer/producer logic and JSONField for component recipes. This enhancement completes the three-tier resource calculation system (ores → components → blocks).

---

## Current Behavior

The blocks app does not exist in the project.

---

## Proposed Behavior

- Django app `blocks` created and registered in settings
- Block model with UUIDv7 primary keys and extensive fields
- JSONField for component requirements with validation
- Consumer/producer validation logic
- Admin interface with formatted displays
- Migrations applied successfully

---

## Acceptance Criteria

- [ ] Blocks app created via `python manage.py startapp blocks`
- [ ] App registered in `se2CalcProject/settings.py` INSTALLED_APPS
- [ ] Block model defined with all required fields
- [ ] Consumer/producer validation implemented
- [ ] JSONField validation for components implemented
- [ ] Admin interface displays blocks with formatted JSON
- [ ] Migrations created and applied
- [ ] All tests pass
- [ ] Documentation updated

---

## Technical Details

### Dependencies
- uuid-utils library for UUIDv7 support
- Django 6.0.1 (includes JSONField)
- ENH-0000002 (Components app must exist first)

### Affected Components
- blocks app (new)
- se2CalcProject/settings.py

### Files to Modify/Create
- `blocks/__init__.py`
- `blocks/models.py`
- `blocks/admin.py`
- `blocks/apps.py`
- `blocks/migrations/0001_initial.py`
- `se2CalcProject/settings.py`

### Database Changes
- [x] Migrations required
- [x] New models
- [ ] Schema changes

---

## Implementation Plan

### Step 1: Create Django App
Run `uv run python manage.py startapp blocks` and register in INSTALLED_APPS

### Step 2: Define Block Model
Create model with base fields plus components, health, pcu, snap_size, mass fields, consumer/producer fields, storage_capacity

### Step 3: Add Validation Logic
Implement validation for consumer/producer type/rate relationships

### Step 4: Add Component Validation
Implement methods to validate component_id references in components JSONField

### Step 5: Configure Admin
Register Block model with custom JSONField display and field grouping

### Step 6: Create and Apply Migrations
Generate and apply migrations to database

---

## Testing Requirements

### Unit Tests
- [ ] Test Block model creation
- [ ] Test JSONField components format validation
- [ ] Test consumer validation (type requires rate)
- [ ] Test producer validation (type requires rate)
- [ ] Test __str__ method
- [ ] Test optional fields (consumer, producer, storage)

### Integration Tests
- [ ] Test admin interface CRUD operations
- [ ] Test components JSONField with valid component references

### Manual Testing
- [ ] Create block via Django shell with all field types
- [ ] Create power consumer block
- [ ] Create power producer block
- [ ] Create storage block
- [ ] Verify all fields display correctly in admin

---

## Documentation Updates

- [ ] CHANGELOG.md
- [ ] Phase 1 checklist
- [ ] JSONField format documentation for frontend
- [ ] Consumer/producer validation rules documentation

---

## Risks and Considerations

- Risk: Complex validation logic may have edge cases - Mitigation: Comprehensive test coverage
- Risk: Component references in JSON not enforced by database - Mitigation: Application-level validation required
- Risk: Optional field combinations may be confusing - Mitigation: Clear documentation and admin help text

---

## Alternatives Considered

### Alternative 1: Separate BlockComponent model
Not chosen to keep initial implementation simple; can refactor later if needed

### Alternative 2: Separate models for consumer/producer blocks
Not chosen because many blocks have both capabilities

---

## Related Issues/Enhancements

- ENH-0000001: Create Ores App and Model
- ENH-0000002: Create Components App and Model (dependency)

---

## Notes

Model fields:
- object_id: UUIDv7, primary key
- name: CharField(max_length=100), unique, required
- description: TextField, blank=True
- mass: FloatField, required
- components: JSONField - Format: [{"component_id": "uuid", "quantity": int}]
- health: FloatField
- pcu: IntegerField (Performance Cost Units)
- snap_size: FloatField
- input_mass: IntegerField
- output_mass: IntegerField
- consumer_type: CharField(max_length=50), optional (e.g., "Power", "Hydrogen")
- consumer_rate: FloatField, default=0
- producer_type: CharField(max_length=50), optional
- producer_rate: FloatField, default=0
- storage_capacity: FloatField, optional
- created_at: DateTimeField, auto_now_add=True
- updated_at: DateTimeField, auto_now=True

Validation rules:
- If consumer_type is set, consumer_rate must be > 0
- If producer_type is set, producer_rate must be > 0

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
