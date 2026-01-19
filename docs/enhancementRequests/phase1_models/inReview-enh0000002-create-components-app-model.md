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
- [ ] All tests pass
- [ ] Documentation updated

---

## Technical Details

### Dependencies
- uuid-utils library for UUIDv7 support
- Django 6.0.1 (includes JSONField)
- ENH-0000001 (Ores app must exist first)

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

### Step 1: Create Django App
Run `uv run python manage.py startapp components` and register in INSTALLED_APPS

### Step 2: Define Component Model
Create model with base fields plus material (JSONField), fabricator, crafting_time

### Step 3: Add Validation Helpers
Implement methods to validate ore_id references in material JSONField

### Step 4: Configure Admin
Register Component model with custom JSONField display formatting

### Step 5: Create and Apply Migrations
Generate and apply migrations to database

---

## Testing Requirements

### Unit Tests
- [ ] Test Component model creation
- [ ] Test JSONField material format validation
- [ ] Test foreign key validation helpers
- [ ] Test __str__ method
- [ ] Test invalid material data rejection

### Integration Tests
- [ ] Test admin interface CRUD operations
- [ ] Test material JSONField with valid ore references

### Manual Testing
- [ ] Create component via Django shell with valid material JSON
- [ ] Create component via admin interface
- [ ] Verify JSONField displays correctly in admin

---

## Documentation Updates

- [ ] CHANGELOG.md
- [ ] Phase 1 checklist
- [ ] JSONField format documentation for frontend

---

## Risks and Considerations

- Risk: JSONField validation complexity - Mitigation: Create comprehensive validation helpers
- Risk: Ore references in JSON not enforced by database - Mitigation: Application-level validation required

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

Model fields:
- object_id: UUIDv7, primary key
- name: CharField(max_length=100), unique, required
- description: TextField, blank=True
- mass: FloatField, required
- material: JSONField - Format: [{"ore_id": "uuid", "quantity": float}]
- fabricator: CharField(max_length=50)
- crafting_time: FloatField (in seconds)
- created_at: DateTimeField, auto_now_add=True
- updated_at: DateTimeField, auto_now=True

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
