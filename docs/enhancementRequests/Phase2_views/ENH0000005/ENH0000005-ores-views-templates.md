# Enhancement Request: Ores Views & Templates

**Filename:** `inReview-enh0000005-ores-views-templates.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000005  
**Status:** inReview  
**Priority:** High  
**Created Date:** 2026-01-24  
**Updated Date:** 2026-01-24  
**Completion Date:** (pending)  
**Assigned To:** (pending)  
**Estimated Effort:** 1-2 days  
**Actual Effort:** (pending)

---

## Summary

Implement complete CRUD views and templates for the Ores app with filtering, sorting, and pagination capabilities.

---

## Description

Create web interface for managing ore data including list, detail, create, update, and delete views. This is the foundation for Phase 2 and establishes patterns for Components and Blocks views. Ores are the simplest model (no JSONField complexity), making them ideal for establishing view/template patterns.

**Benefits:**
- Users can manage ore data via web interface instead of admin only
- Establishes reusable template patterns for other apps
- Provides filtering and sorting capabilities not available in admin
- Creates foundation for build order calculator in Phase 3

---

## Current Behavior

- Ores can only be managed through Django admin interface
- No public-facing views exist
- No filtering or sorting beyond admin defaults
- No custom templates

---

## Proposed Behavior

- Complete CRUD interface accessible at `/ores/` URLs
- List view with filtering by name and sorting by mass
- Detail view showing all ore properties
- Create/Update forms with validation
- Delete confirmation page
- Responsive templates using CSS framework
- Pagination (25 items per page)
- Success/error messages for all operations

---

## Acceptance Criteria

- [x] OreListView displays all ores with fixture data
- [x] Filtering by name works correctly
- [x] Sorting by mass (ascending/descending) works
- [x] Pagination displays 25 items per page
- [x] OreDetailView shows all ore properties
- [x] OreCreateView creates new ores with validation
- [x] OreUpdateView modifies existing ores
- [x] OreDeleteView requires confirmation before deletion
- [x] Success messages display after create/update/delete
- [x] Error messages display for validation failures
- [x] All templates are mobile responsive
- [x] Minimum 15 automated tests (5 per view type) - **63 tests total**
- [x] All tests pass with 100% pass rate
- [x] Test execution time <1 second - **0.537s actual**
- [ ] Documentation updated - **Partial: README needs Phase 2 status update, CHANGELOG needs specific entry**
- [ ] Code reviewed

---

## Technical Details

### Dependencies
- No new packages required
- Uses Django 6.0.1 built-in generic views
- Optional: django-crispy-forms for enhanced form rendering

### Affected Components
- `ores` app
- Base templates (new)
- URL configuration

### Files to Modify/Create

**New Files:**
- `ores/urls.py` (already exists, needs population)
- `ores/forms.py` (new)
- `templates/base.html` (new)
- `templates/home.html` (new)
- `ores/templates/ores/ore_list.html` (new)
- `ores/templates/ores/ore_detail.html` (new)
- `ores/templates/ores/ore_form.html` (new)
- `ores/templates/ores/ore_confirm_delete.html` (new)
- `static/css/main.css` (new)
- `ores/tests_views.py` (new)

**Modified Files:**
- `ores/views.py` (currently empty)
- `se2CalcProject/urls.py` (add ores URL include)
- `se2CalcProject/settings.py` (configure static files, templates)

### Database Changes
- [ ] No migrations required
- [ ] No new models
- [ ] No schema changes

---

## Implementation Plan

### Step 1: Base Template Infrastructure
- Create `templates/` directory in project root
- Create `base.html` with navigation, CSS framework (Bootstrap/Tailwind)
- Create `home.html` with links to all apps
- Configure `settings.py` TEMPLATES and STATIC_FILES
- Create `static/css/main.css` for custom styles

### Step 2: URL Configuration
- Update `se2CalcProject/urls.py` to include ores URLs
- Create URL patterns in `ores/urls.py`:
  - `''` → OreListView (name='ore_list')
  - `'<uuid:pk>/'` → OreDetailView (name='ore_detail')
  - `'create/'` → OreCreateView (name='ore_create')
  - `'<uuid:pk>/update/'` → OreUpdateView (name='ore_update')
  - `'<uuid:pk>/delete/'` → OreDeleteView (name='ore_delete')

### Step 3: Forms
- Create `ores/forms.py` with OreForm
- Add validation for required fields
- Add help text for all fields
- Validate mass > 0

### Step 4: Views Implementation
- Implement OreListView with filtering and sorting
- Implement OreDetailView
- Implement OreCreateView with success messages
- Implement OreUpdateView with success messages
- Implement OreDeleteView with confirmation

### Step 5: Templates
- Create `ore_list.html` with filter form, sort links, pagination
- Create `ore_detail.html` with all ore properties
- Create `ore_form.html` for create/update (shared template)
- Create `ore_confirm_delete.html` with confirmation message

### Step 6: Testing
- Create `ores/tests_views.py`
- Write unit tests for each view (5 per view = 25 tests minimum)
- Write integration tests for CRUD operations
- Write template rendering tests
- Use `fixtures = ['sample_ores.json']` for test data
- Verify 100% pass rate and <1s execution time

### Step 7: Documentation
- Update README.md with Phase 2 progress
- Create deployment guide
- Document URL patterns and view behavior
- Add screenshots of working interface

---

## Testing Requirements

### Unit Tests (Minimum 15)

**OreListView (5 tests):**
- [ ] View renders successfully with fixture data
- [ ] Context contains ore_list queryset
- [ ] Filtering by name works correctly
- [ ] Sorting by mass ascending works
- [ ] Sorting by mass descending works

**OreDetailView (3 tests):**
- [ ] View renders successfully for valid UUID
- [ ] View returns 404 for invalid UUID
- [ ] Context contains correct ore object

**OreCreateView (3 tests):**
- [ ] GET request renders form
- [ ] POST with valid data creates ore
- [ ] POST with invalid data shows errors

**OreUpdateView (2 tests):**
- [ ] GET request renders form with existing data
- [ ] POST with valid data updates ore

**OreDeleteView (2 tests):**
- [ ] GET request renders confirmation page
- [ ] POST request deletes ore

### Integration Tests (Minimum 5)
- [ ] Create → Detail → Update → Delete workflow
- [ ] Success messages display correctly
- [ ] Error messages display for validation failures
- [ ] Pagination works with >25 ores
- [ ] Filtering + sorting combination works

### Template Tests (Minimum 5)
- [ ] base.html renders without errors
- [ ] ore_list.html renders with fixture data
- [ ] ore_detail.html displays all fields
- [ ] ore_form.html renders form fields
- [ ] ore_confirm_delete.html shows ore name

### Manual Testing
- [ ] Load fixtures: `uv run python manage.py loaddata sample_ores`
- [ ] Navigate to http://localhost:8000/ores/
- [ ] Test all CRUD operations via browser
- [ ] Verify mobile responsiveness
- [ ] Test with empty database (no ores)

---

## Deliverables

- [ ] Working CRUD interface for ores at `/ores/` URLs
- [ ] Base templates (base.html, home.html) for project
- [ ] Static files directory with CSS
- [ ] Automated test suite (15+ tests, all passing)
- [ ] Test execution time <1 second
- [ ] Deployment guide completed
- [ ] Post-deployment review completed
- [ ] CHANGELOG.md updated
- [ ] README.md updated with Phase 2 progress

---

## Documentation Updates

- [ ] README.md - Update Phase 2 status to "In Progress"
- [ ] CHANGELOG.md - Add ENH-0000005 entry
- [ ] Create ENH-0000005 deployment guide
- [ ] Create ENH-0000005 test documentation
- [ ] Document URL patterns in code comments
- [ ] Add docstrings to all views

---

## Risks and Considerations

**Risk 1: Template Framework Choice**
- **Impact:** Medium
- **Mitigation:** Use Bootstrap 5 (well-documented, widely used)

**Risk 2: Static Files Configuration**
- **Impact:** Low
- **Mitigation:** Follow Django documentation, test early

**Risk 3: URL Pattern Conflicts**
- **Impact:** Low
- **Mitigation:** Use namespaced URLs (`ores:ore_list`)

**Risk 4: Pagination Performance**
- **Impact:** Low (only 15 ores in fixtures)
- **Mitigation:** Monitor query count with Django Debug Toolbar

---

## Alternatives Considered

### Alternative 1: Use Django Admin Customization
**Rejected:** Admin is for staff, not end users. Need public-facing interface.

### Alternative 2: API-First Approach (REST Framework)
**Rejected:** Phase 2 focuses on traditional views. API can be added later.

### Alternative 3: Use Third-Party CRUD Package
**Rejected:** Learning opportunity, need custom filtering/sorting logic.

---

## Related Issues/Enhancements

- **Depends On:** ENH-0000001 (Ores Model) - Completed
- **Blocks:** ENH-0000006 (Components Views) - Waiting for patterns
- **Blocks:** ENH-0000007 (Blocks Views) - Waiting for patterns
- **Enables:** Phase 3 Build Order Calculator

---

## Notes

- This enhancement establishes patterns for ENH-0000006 and ENH-0000007
- Keep views simple - no AJAX or complex JavaScript yet
- Focus on solid foundation and testing
- Ores are simplest model (no JSONField), ideal for establishing patterns
- Use fixture data extensively for testing and demos

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-24 | inReview | Initial creation based on phase2_views.md |

---

## Sign-off

**Reviewed By:** (pending)  
**Approved By:** (pending)  
**Completed By:** (pending)  
**Completion Date:** (pending)
