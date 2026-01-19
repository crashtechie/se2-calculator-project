# Enhancement Request: Create Ores App and Model

**Filename:** `inReview-enh0000001-create-ores-app-model.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000001  
**Status:** inReview  
**Priority:** High  
**Created Date:** 2026-01-20  
**Updated Date:** 2026-01-20  
**Assigned To:**  
**Estimated Effort:** 4 hours  

---

## Summary

Create the ores Django app with Ore model including UUIDv7 primary keys and admin interface.

---

## Description

Implement the foundational ores app as part of Phase 1 database setup. This app will manage ore data including name, description, mass, and timestamps. The Ore model serves as the base resource type for the Space Engineers 2 calculator, as components are crafted from ores.

This enhancement benefits developers and end-users by establishing the core data structure for resource calculations.

---

## Current Behavior

The ores app does not exist in the project.

---

## Proposed Behavior

- Django app `ores` created and registered in settings
- Ore model with UUIDv7 primary keys
- Admin interface for managing ore data
- Migrations applied successfully

---

## Acceptance Criteria

- [ ] Ores app created via `python manage.py startapp ores`
- [ ] App registered in `se2CalcProject/settings.py` INSTALLED_APPS
- [ ] Ore model defined with all required fields
- [ ] UUIDv7 primary key implementation working
- [ ] Admin interface displays ores correctly
- [ ] Migrations created and applied
- [ ] All tests pass
- [ ] Documentation updated

---

## Technical Details

### Dependencies
- uuid-utils library for UUIDv7 support
- Django 6.0.1

### Affected Components
- ores app (new)
- se2CalcProject/settings.py

### Files to Modify/Create
- `ores/__init__.py`
- `ores/models.py`
- `ores/admin.py`
- `ores/apps.py`
- `ores/migrations/0001_initial.py`
- `se2CalcProject/settings.py`

### Database Changes
- [x] Migrations required
- [x] New models
- [ ] Schema changes

---

## Implementation Plan

### Step 1: Create Django App
Run `uv run python manage.py startapp ores` and register in INSTALLED_APPS

### Step 2: Define Ore Model
Create model with fields: object_id (UUIDv7), name, description, mass, created_at, updated_at

### Step 3: Configure Admin
Register Ore model with list_display, search_fields, and list_filter

### Step 4: Create and Apply Migrations
Generate and apply migrations to database

---

## Testing Requirements

### Unit Tests
- [ ] Test Ore model creation
- [ ] Test UUIDv7 generation
- [ ] Test __str__ method
- [ ] Test timestamp auto-population

### Integration Tests
- [ ] Test admin interface CRUD operations

### Manual Testing
- [ ] Create ore via Django shell
- [ ] Create ore via admin interface
- [ ] Verify all fields save correctly

---

## Documentation Updates

- [ ] CHANGELOG.md
- [ ] Phase 1 checklist

---

## Risks and Considerations

- Risk: UUIDv7 library compatibility with Django 6.0.1 - Mitigation: Test thoroughly before proceeding
- Risk: Migration conflicts if database already exists - Mitigation: Fresh database recommended

---

## Alternatives Considered

### Alternative 1: Use standard UUID4
Not chosen because UUIDv7 provides time-ordered benefits for database indexing

---

## Related Issues/Enhancements

- ENH-0000002: Create Components App and Model
- ENH-0000003: Create Blocks App and Model

---

## Notes

Model fields:
- object_id: UUIDv7, primary key
- name: CharField(max_length=100), unique, required
- description: TextField, blank=True
- mass: FloatField, required
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
