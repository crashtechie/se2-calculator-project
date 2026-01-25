# Enhancement Request: Components Views & Templates

**Filename:** `inReview-enh0000006-components-views-templates.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000006  
**Status:** inReview  
**Priority:** High  
**Created Date:** 2026-01-24  
**Updated Date:** 2026-01-25  
**Completion Date:** (pending)  
**Assigned To:** (pending)  
**Estimated Effort:** 1.5-2 days  
**Actual Effort:** (pending)

---

## Summary

Implement complete CRUD views and templates for the Components app with JSONField material handling, dynamic form inputs, and ore relationship display.

---

## Description

Create web interface for managing component data including list, detail, create, update, and delete views. Components have JSONField materials that reference ores, requiring dynamic form handling with JavaScript for adding/removing material rows. This enhancement builds on patterns established in ENH-0000005 (Ores Views).

**Key Challenge:** JSONField materials require user-friendly form interface for selecting ores and quantities, with validation against Phase 1 model validation helpers.

**Benefits:**
- Users can manage components via web interface
- Dynamic material selection provides better UX than raw JSON editing
- Reuses Phase 1 validation helpers for data integrity
- Displays material breakdown in detail views
- Foundation for block component selection

---

## Current Behavior

- Components can only be managed through Django admin interface
- JSONField materials display as raw JSON in admin
- No dynamic material selection interface
- No public-facing views exist

---

## Proposed Behavior

- Complete CRUD interface accessible at `/components/` URLs
- List view with filtering by name and sorting by mass
- Detail view showing all properties including formatted materials list
- Create/Update forms with dynamic material selector (JavaScript)
- Material selector allows adding/removing ore rows with quantities
- Ore dropdown populated from database
- Delete confirmation page
- Validation using Phase 1 Component.validate_materials() helper
- Success/error messages for all operations

---

## Acceptance Criteria

- [ ] ComponentListView displays all components with fixture data
- [ ] Filtering by name works correctly
- [ ] Sorting by mass (ascending/descending) works
- [ ] Pagination displays 25 items per page
- [ ] ComponentDetailView shows all properties including formatted materials
- [ ] Materials display as "Ore Name: Quantity kg" not raw JSON
- [ ] ComponentCreateView creates components with material validation
- [ ] Dynamic material selector adds/removes rows via JavaScript
- [ ] Ore dropdown populated from Ore.objects.all()
- [ ] ComponentUpdateView modifies existing components
- [ ] Existing materials pre-populate form on update
- [ ] ComponentDeleteView requires confirmation before deletion
- [ ] Form validation uses Component.validate_materials() from Phase 1
- [ ] Success messages display after create/update/delete
- [ ] Error messages display for validation failures (invalid UUIDs, negative quantities)
- [ ] All templates are mobile responsive
- [ ] URL namespaces use `components:` prefix (e.g., `components:component_list`)
- [ ] Query parameter preservation works across pagination
- [ ] Search functionality searches both name and description fields
- [ ] Bootstrap 5 styling applied consistently
- [ ] Empty state messages display when no components exist
- [ ] Navigation integration in base template works
- [ ] Minimum 25 automated tests (view + form + JavaScript validation)
- [ ] All tests pass with 100% pass rate
- [ ] Test execution time <1.5 seconds
- [ ] Documentation updated
- [ ] Code reviewed

---

## Technical Details

### Dependencies
- No new packages required
- **JavaScript:** Use vanilla JavaScript (ES6+) to match ENH0000005 patterns
- **Optional:** jQuery if already included in base template from ENH0000005
- Confirm JavaScript framework choice with team before Step 4
- Optional: django-widget-tweaks for form customization
- Uses Django 6.0.1 JSONField and generic views

### Affected Components
- `components` app
- `ores` app (for material selection)
- Static JavaScript files

### Files to Modify/Create

**New Files:**
- `components/urls.py` (needs population)
- `components/forms.py` (new)
- `components/templates/components/component_list.html` (new)
- `components/templates/components/component_detail.html` (new)
- `components/templates/components/component_form.html` (new)
- `components/templates/components/component_confirm_delete.html` (new)
- `static/js/material-selector.js` (new)
- `components/tests_views.py` (new)
- `components/tests_forms.py` (new)

**Modified Files:**
- `components/views.py` (currently empty)
- `se2CalcProject/urls.py` (add components URL include)

### Database Changes
- [ ] No migrations required
- [ ] No new models
- [ ] No schema changes

### Performance Considerations
- Use `select_related()` when fetching components with ore lookups
- Cache ore queryset in form context to avoid N+1 queries
- Monitor with Django Debug Toolbar (already in pyproject.toml)
- Consider caching material display formatting for detail view
- Target: < 50ms per request for list view with 25 items

---

## Implementation Plan

### Step 0: Pre-Implementation Verification
- Run fixture verification: `uv run python scripts/utils/verify_fixtures.py`
- Confirm sample_components.json has valid ore UUIDs
- Verify ENH0000005 base templates exist
- Check ENH0000005 Bootstrap version (should be 5.x)
- Review ENH0000005 test patterns in `ores/test_views.py`

### Step 1: Forms with JSONField Handling
- Create `components/forms.py` with ComponentForm
- Override __init__ to exclude materials from ModelForm
- Add custom clean_materials() method
- Integrate Phase 1 Component.validate_materials() helper
- Handle conversion between form data (ore_id[], quantity[]) and JSON storage

### Step 2: URL Configuration
- Update `se2CalcProject/urls.py` to include components URLs
- Create URL patterns in `components/urls.py`:
  - `''` → ComponentListView (name='component_list')
  - `'<uuid:pk>/'` → ComponentDetailView (name='component_detail')
  - `'create/'` → ComponentCreateView (name='component_create')
  - `'<uuid:pk>/update/'` → ComponentUpdateView (name='component_update')
  - `'<uuid:pk>/delete/'` → ComponentDeleteView (name='component_delete')

### Step 3: Views Implementation
- Implement ComponentListView with filtering and sorting
- Implement ComponentDetailView with formatted materials display
- Implement ComponentCreateView with material form handling
- Implement ComponentUpdateView with material pre-population
- Implement ComponentDeleteView with confirmation
- Add get_context_data() to pass ores queryset to templates

### Step 4: JavaScript Material Selector
- Create `static/js/material-selector.js`
- Implement addMaterialRow() function
- Implement removeMaterialRow() function
- Populate ore dropdown from template context
- Validate quantities client-side (positive numbers)
- Handle form submission (convert rows to JSON)

### Step 5: Templates
- Create `component_list.html` (similar to ore_list.html)
- Create `component_detail.html` with materials formatting:
  ```html
  <h3>Materials Required:</h3>
  <ul>
  {% for ore_id, quantity in component.materials.items %}
    <li>{{ ore_id|get_ore_name }}: {{ quantity }} kg</li>
  {% endfor %}
  </ul>
  ```
- Create `component_form.html` with dynamic material selector
- Create `component_confirm_delete.html`

### Step 5.5: Template Filters and Context Processors
- Create `components/templatetags/` directory with `__init__.py`
- Create `components/templatetags/component_filters.py`
- Implement `get_ore_name` filter:
  ```python
  from django import template
  from ores.models import Ore
  
  register = template.Library()
  
  @register.filter
  def get_ore_name(ore_id):
      try:
          return Ore.objects.get(ore_id=ore_id).name
      except Ore.DoesNotExist:
          return f"Unknown Ore ({ore_id})"
  ```
- Load in templates: `{% load component_filters %}`
- Test filter with invalid UUIDs
- Consider caching ore lookups for performance

### Step 6: Testing
- Create `components/tests_views.py` (15+ tests)
- Create `components/tests_forms.py` (10+ tests)
- Test JSONField validation with invalid UUIDs
- Test material selector with fixture data
- Use `fixtures = ['sample_ores.json', 'sample_components.json']`
- Verify 100% pass rate and <1.5s execution time

### Step 7: Documentation
- Document JSONField form handling pattern
- Create deployment guide with JavaScript setup
- Add code comments for material conversion logic
- Update README.md with Phase 2 progress

---

## Testing Requirements

### Testing Success Metrics
**Target:** 25+ tests minimum (based on ENH0000005's 63 tests for simpler model)  
**Performance:** <1.5 seconds execution time  
**Coverage:** Aim for 95%+ code coverage on new view code  
**Pass Rate:** 100% (all tests must pass)

### Unit Tests (Minimum 25)

**ComponentListView (5 tests):**
- [ ] View renders successfully with fixture data
- [ ] Context contains component_list queryset
- [ ] Filtering by name works correctly
- [ ] Sorting by mass ascending works
- [ ] Sorting by mass descending works

**ComponentDetailView (4 tests):**
- [ ] View renders successfully for valid UUID
- [ ] View returns 404 for invalid UUID
- [ ] Context contains correct component object
- [ ] Materials display formatted (not raw JSON)

**ComponentCreateView (5 tests):**
- [ ] GET request renders form with ore dropdown
- [ ] POST with valid data creates component
- [ ] POST with invalid ore UUID shows error
- [ ] POST with negative quantity shows error
- [ ] POST with empty materials shows error

**ComponentUpdateView (3 tests):**
- [ ] GET request renders form with existing materials
- [ ] POST with valid data updates component
- [ ] Existing materials pre-populate correctly

**ComponentDeleteView (2 tests):**
- [ ] GET request renders confirmation page
- [ ] POST request deletes component

**Form Tests (6 tests):**
- [ ] ComponentForm validates materials structure
- [ ] Form rejects invalid ore UUIDs
- [ ] Form rejects negative quantities
- [ ] Form accepts valid materials JSON
- [ ] Form converts form data to JSON correctly
- [ ] Form uses Phase 1 validate_materials() helper

### Integration Tests (Minimum 5)
- [ ] Create component with materials → Detail view shows formatted materials
- [ ] Update component materials → Changes persist
- [ ] Delete component → Materials data removed
- [ ] Create with fixture ore UUIDs → Validation passes
- [ ] Create with invalid UUID → Validation fails with clear error

### JavaScript Tests (Manual)
- [ ] Add material row button works
- [ ] Remove material row button works
- [ ] Ore dropdown populates correctly
- [ ] Quantity validation prevents negative numbers
- [ ] Form submission converts rows to JSON

### Template Tests (Minimum 3)
- [ ] component_list.html renders with fixture data
- [ ] component_detail.html displays formatted materials
- [ ] component_form.html includes material selector JavaScript

---

## Deliverables

- [ ] Working CRUD interface for components at `/components/` URLs
- [ ] Dynamic material selector with JavaScript
- [ ] JSONField form handling pattern documented
- [ ] Automated test suite (25+ tests, all passing)
- [ ] Test execution time <1.5 seconds
- [ ] **Deployment guide completed** (follow ENH-0000005-deployment-guide.md template)
- [ ] **Post-deployment report completed** (follow ENH-0000005-POST-DEPLOYMENT-REPORT.md template)
- [ ] CHANGELOG.md updated
- [ ] README.md updated with Phase 2 progress

---

## Success Metrics

### Quantitative Metrics
- **Test Count:** 25+ tests (minimum), aim for 30+
- **Test Pass Rate:** 100%
- **Test Execution Time:** <1.5 seconds
- **Code Coverage:** >90% for new view code
- **Page Load Time:** <500ms for list view
- **Form Submission Time:** <300ms for create/update

### Qualitative Metrics
- Material selector is intuitive (no user training needed)
- Error messages are actionable
- Mobile responsive on iOS/Android
- Consistent with ENH0000005 UI patterns
- Code review approval with no major issues

---

## Documentation Updates

- [ ] README.md - Update Phase 2 status
- [ ] CHANGELOG.md - Add ENH-0000006 entry
- [ ] Create ENH-0000006 deployment guide
- [ ] Create ENH-0000006 test documentation
- [ ] Document JSONField form pattern for ENH-0000007 reference
- [ ] Add docstrings to all views and form methods
- [ ] Document JavaScript material selector API

---

## Risks and Considerations

**Risk 1: JSONField Form Complexity**
- **Impact:** High
- **Likelihood:** Medium
- **Mitigation:** 
  - Prototype JavaScript selector early
  - Test with fixture data immediately
  - Reuse Phase 1 validation helpers
  - Consider django-formset library if complexity grows

**Risk 2: Ore UUID Lookup Performance**
- **Impact:** Low
- **Likelihood:** Low
- **Mitigation:** 
  - Cache ore queryset in view context
  - Use select_related() if needed
  - Monitor with Django Debug Toolbar

**Risk 3: JavaScript Browser Compatibility**
- **Impact:** Medium
- **Likelihood:** Low
- **Mitigation:**
  - Use vanilla JavaScript (ES6+) or jQuery
  - Test in Chrome, Firefox, Safari
  - Provide fallback for no-JS users (raw JSON textarea)

**Risk 4: Material Data Migration**
- **Impact:** Low (fixtures already have valid materials)
- **Likelihood:** Low
- **Mitigation:** Run verify_fixtures.py before starting

---

## Security Considerations

**Input Sanitization:**
- Validate all ore UUID inputs against database
- Sanitize quantity inputs (reject negative, NaN, infinite values)
- Use Django's built-in CSRF protection for all forms
- Validate materials JSON structure server-side (never trust client)

**JavaScript Security:**
- Avoid using `eval()` or `innerHTML` for dynamic content
- Use `textContent` or jQuery `.text()` instead of `.html()`
- Validate JSON structure before submission
- Sanitize all user inputs in JavaScript before DOM manipulation

**Error Handling:**
- Don't expose stack traces to users in production
- Log security-relevant errors (invalid UUIDs, suspicious quantities)
- Return generic error messages for authentication failures
- Use Django's `Http404` for not-found errors (no UUID exposure)

**Performance Security:**
- Rate-limit form submissions if needed
- Prevent DDOS via excessive material rows (limit to 20-50 rows)
- Monitor for unusual patterns in logs

---

## Alternatives Considered

### Alternative 1: Raw JSON Textarea
**Rejected:** Poor UX, error-prone, requires users to know UUID format.

### Alternative 2: Inline Formsets
**Rejected:** Requires separate Material model, breaks Phase 1 JSONField design.

### Alternative 3: AJAX Ore Search
**Rejected:** Over-engineering for 15 ores. Can add later if needed.

### Alternative 4: Third-Party JSONField Widget
**Considered:** django-jsonform or similar. May revisit if custom solution too complex.

---

## Related Issues/Enhancements

- **Depends On:** ENH-0000001 (Ores Model) - ✅ Completed
- **Depends On:** ENH-0000002 (Components Model) - ✅ Completed
- **Depends On:** ENH-0000005 (Ores Views) - ✅ Completed (2026-01-25)
- **Blocks:** ENH-0000007 (Blocks Views) - Waiting for JSONField patterns
- **Enables:** Phase 3 Build Order Calculator

---

## Notes

- This enhancement establishes JSONField form patterns for ENH-0000007
- JavaScript material selector will be adapted for component selector in Blocks
- Phase 1 validation helpers (validate_materials) must be reused
- Test with fixture data extensively - all 15 components have valid materials
- Consider creating template filter for ore name lookup: `{{ ore_id|get_ore_name }}`
- Material selector JavaScript should be reusable for ENH-0000007

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-24 | inReview | Initial creation based on phase2_views.md and phase2_recommendations.md |

---

## Sign-off

**Reviewed By:** (pending)  
**Approved By:** (pending)  
**Completed By:** (pending)  
**Completion Date:** (pending)
