# Enhancement Request: Blocks Views & Templates

**Filename:** `inReview-enh0000007-blocks-views-templates.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000007  
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

Implement complete CRUD views and templates for the Blocks app with JSONField component handling, dynamic form inputs, and full resource chain visualization.

---

## Description

Create web interface for managing block data including list, detail, create, update, and delete views. Blocks have JSONField components that reference components, requiring dynamic form handling similar to ENH-0000006. This enhancement completes Phase 2 and enables Phase 3 build order calculator.

**Key Features:**
- Dynamic component selector (adapted from material selector in ENH-0000006)
- Detail view shows full resource chain: Block → Components → Ores
- Validation using Phase 1 Block.validate_components() helper
- Display of block statistics (total mass, component count, ore breakdown)

**Benefits:**
- Users can manage blocks via web interface
- Full resource chain visibility from ore to final block
- Foundation for multi-block build order calculator
- Completes Phase 2 CRUD functionality

---

## Current Behavior

- Blocks can only be managed through Django admin interface
- JSONField components display as raw JSON in admin
- No dynamic component selection interface
- No resource chain visualization
- No public-facing views exist

---

## Proposed Behavior

- Complete CRUD interface accessible at `/blocks/` URLs
- List view with filtering by name and sorting by mass
- Detail view showing:
  - All block properties
  - Formatted components list with quantities
  - Full resource chain (components → ores breakdown)
  - Total mass calculation
  - Component count statistics
- Create/Update forms with dynamic component selector (JavaScript)
- Component selector allows adding/removing component rows with quantities
- Component dropdown populated from database
- Delete confirmation page
- Validation using Phase 1 Block.validate_components() helper
- Success/error messages for all operations

---

## Acceptance Criteria

- [ ] BlockListView displays all blocks with fixture data
- [ ] Search functionality searches both name and description fields
- [ ] Sorting by mass (ascending/descending) works
- [ ] Pagination displays 25 items per page
- [ ] BlockDetailView shows all properties including formatted components
- [ ] Components display as "Component Name: Quantity" not raw JSON
- [ ] Detail view shows full resource chain (Block → Components → Ores)
- [ ] BlockCreateView creates blocks with component validation
- [ ] Dynamic component selector adds/removes rows via JavaScript
- [ ] Component dropdown populated from Component.objects.all()
- [ ] BlockUpdateView modifies existing blocks
- [ ] Existing components pre-populate form on update
- [ ] BlockDeleteView requires confirmation before deletion
- [ ] Form validation uses Block.validate_components() from Phase 1
- [ ] Success messages display after create/update/delete
- [ ] Error messages display for validation failures (invalid UUIDs, negative quantities)
- [ ] All templates are mobile responsive
- [ ] URL namespaces use `blocks:` prefix (e.g., `blocks:block_list`)
- [ ] Navigation integration in base template works
- [ ] Bootstrap 5 styling applied consistently
- [ ] Empty state messages display when no blocks exist
- [ ] Query parameter preservation works across pagination
- [ ] Minimum 25 automated tests (view + form + resource chain)
- [ ] All tests pass with 100% pass rate
- [ ] Test execution time <2 seconds
- [ ] Test coverage ≥85% for blocks package
- [ ] Documentation updated
- [ ] Code reviewed

---

## Technical Details

### Dependencies
- No new packages required
- Reuses material-selector.js pattern from ENH-0000006
- Uses Django 6.0.1 JSONField and generic views

### Affected Components
- `blocks` app
- `components` app (for component selection)
- `ores` app (for resource chain display)
- Static JavaScript files

### Files to Modify/Create

**New Files:**
- `blocks/urls.py` (needs population)
- `blocks/forms.py` (new)
- `blocks/templates/blocks/block_list.html` (new)
- `blocks/templates/blocks/block_detail.html` (new)
- `blocks/templates/blocks/block_form.html` (new)
- `blocks/templates/blocks/block_confirm_delete.html` (new)
- `static/js/block-component-selector.js` (new, adapted from material-selector.js)
- `blocks/test_views.py` (new)
- `blocks/tests_forms.py` (new)
- `blocks/templatetags/__init__.py` (new)
- `blocks/templatetags/block_filters.py` (new, for component name resolution)

**Modified Files:**
- `blocks/views.py` (currently empty)
- `se2CalcProject/urls.py` (add blocks URL include: path('blocks/', include('blocks.urls', namespace='blocks')))
- `templates/base.html` (add Blocks navigation entry)

### Database Changes
- [ ] No migrations required
- [ ] No new models
- [ ] No schema changes

---

## Implementation Plan

### Step 1: Forms with JSONField Handling
- Create `blocks/forms.py` following ComponentForm pattern from ENH-0000006
- Use hidden `components_json` field (analogous to `materials_json` in ENH-0000006)
- Convert component_id[], quantity[] arrays to JSON format
- Add custom clean() method with validation
- Integrate Phase 1 Block.validate_components() helper
- Handle conversion between form data (component_id[], quantity[]) and JSON storage
- Apply Bootstrap 5 form styling to all widgets

### Step 2: URL Configuration
- Update `se2CalcProject/urls.py` to include blocks URLs with namespace
- Add: `path('blocks/', include('blocks.urls', namespace='blocks'))`
- Create URL patterns in `blocks/urls.py` with namespace='blocks':
  - `''` → BlockListView (name='block_list', accessible as 'blocks:block_list')
  - `'<uuid:pk>/'` → BlockDetailView (name='block_detail')
  - `'create/'` → BlockCreateView (name='block_create')
  - `'<uuid:pk>/update/'` → BlockUpdateView (name='block_update')
  - `'<uuid:pk>/delete/'` → BlockDeleteView (name='block_delete')

### Step 3: Views Implementation
- Implement BlockListView with search (name/description) and sorting
- Implement BlockDetailView with:
  - Formatted components display
  - Resource chain calculation (components → ores) in get_context_data()
  - Statistics (total mass, component count)
- Implement BlockCreateView with component form handling
- Implement BlockUpdateView with component pre-population
- Implement BlockDeleteView with confirmation
- Add get_context_data() to pass components queryset to templates

### Step 4: JavaScript Component Selector
- Create `static/js/block-component-selector.js` (adapt material-selector.js from ENH-0000006)
- Implement addComponentRow() function
- Implement removeComponentRow() function
- Populate component dropdown from template context
- Validate quantities client-side (positive integers)
- Handle form submission (convert rows to JSON)
- Include CSRF token handling for AJAX requests

### Step 5: Resource Chain Display
- Create template tags in `blocks/templatetags/block_filters.py`
- Implement get_component_name filter (analogous to get_ore_name in ENH-0000006)
- Calculate resource chain in view's get_context_data() method, not template
- Cache component lookups (5 minute TTL) for performance
- Display full breakdown: Block → Components (with quantities) → Ores (with quantities)
- Example output:
  ```
  Light Armor Block (1x)
  ├─ Steel Plate (25x)
  │  ├─ Iron Ore (175 kg)
  │  └─ Nickel Ore (17.5 kg)
  └─ Construction Component (10x)
     ├─ Iron Ore (80 kg)
     └─ Silicon Ore (3 kg)
  
  Total Ores Required:
  - Iron Ore: 255 kg
  - Nickel Ore: 17.5 kg
  - Silicon Ore: 3 kg
  ```

### Step 6: Templates
- Create `block_list.html` (similar to component_list.html)
- Create `block_detail.html` with:
  - Block properties
  - Components list (formatted)
  - Resource chain visualization
  - Statistics panel
- Create `block_form.html` with dynamic component selector
- Create `block_confirm_delete.html`

### Step 7: Testing
- Create `blocks/test_views.py` (20+ tests)
- Create `blocks/test_forms.py` (10+ tests)
- Test JSONField validation with invalid UUIDs
- Test resource chain calculation with fixture data
- Test component selector with fixture data
- Use `fixtures = ['sample_ores.json', 'sample_components.json', 'sample_blocks.json']`
- Verify 100% pass rate and <2s execution time (cumulative project suite)
- Achieve ≥85% test coverage for blocks package

### Step 8: Documentation
- Document resource chain calculation algorithm
- Create deployment guide
- Add code comments for component conversion logic
- Update README.md with Phase 2 completion status
- Create Phase 2 summary report

---

## Testing Requirements

### Unit Tests (Minimum 25)

**BlockListView (5 tests):**
- [ ] View renders successfully with fixture data
- [ ] Context contains block_list queryset
- [ ] Filtering by name works correctly
- [ ] Sorting by mass ascending works
- [ ] Sorting by mass descending works

**BlockDetailView (6 tests):**
- [ ] View renders successfully for valid UUID
- [ ] View returns 404 for invalid UUID
- [ ] Context contains correct block object
- [ ] Components display formatted (not raw JSON)
- [ ] Resource chain calculates correctly
- [ ] Statistics display correctly (mass, component count)

**BlockCreateView (5 tests):**
- [ ] GET request renders form with component dropdown
- [ ] POST with valid data creates block
- [ ] POST with invalid component UUID shows error
- [ ] POST with negative quantity shows error
- [ ] POST with empty components shows error

**BlockUpdateView (3 tests):**
- [ ] GET request renders form with existing components
- [ ] POST with valid data updates block
- [ ] Existing components pre-populate correctly

**BlockDeleteView (2 tests):**
- [ ] GET request renders confirmation page
- [ ] POST request deletes block

**Form Tests (6 tests):**
- [ ] BlockForm validates components structure
- [ ] Form rejects invalid component UUIDs
- [ ] Form rejects negative quantities
- [ ] Form accepts valid components JSON
- [ ] Form converts form data to JSON correctly
- [ ] Form uses Phase 1 validate_components() helper

**Resource Chain Tests (5 tests):**
- [ ] Resource chain calculates ores from components
- [ ] Resource chain handles multiple components
- [ ] Resource chain totals ores correctly
- [ ] Resource chain handles missing component data gracefully
- [ ] Resource chain displays in correct format

### Integration Tests (Minimum 5)
- [ ] Create block with components → Detail view shows resource chain
- [ ] Update block components → Resource chain updates
- [ ] Delete block → Components data removed
- [ ] Create with fixture component UUIDs → Validation passes
- [ ] Resource chain matches manual calculation

### JavaScript Tests (Manual)
- [ ] Add component row button works
- [ ] Remove component row button works
- [ ] Component dropdown populates correctly
- [ ] Quantity validation prevents negative numbers
- [ ] Form submission converts rows to JSON

### Template Tests (Minimum 3)
- [ ] block_list.html renders with fixture data
- [ ] block_detail.html displays formatted components and resource chain
- [ ] block_form.html includes component selector JavaScript

---

## Deliverables

- [ ] Working CRUD interface for blocks at `/blocks/` URLs
- [ ] Dynamic component selector with JavaScript
- [ ] Resource chain visualization in detail view
- [ ] JSONField form handling pattern documented
- [ ] Navigation integration in base template
- [ ] Automated test suite (25+ tests, all passing)
- [ ] Test execution time <2 seconds (cumulative project suite)
- [ ] Test coverage ≥85% for blocks package
- [ ] Deployment guide completed
- [ ] Post-deployment review completed
- [ ] Phase 2 completion report
- [ ] CHANGELOG.md updated
- [ ] README.md updated with Phase 2 completion

---

## Documentation Updates

- [ ] README.md - Update Phase 2 status to "Completed"
- [ ] CHANGELOG.md - Add ENH-0000007 entry
- [ ] Create ENH-0000007 deployment guide
- [ ] Create ENH-0000007 test documentation
- [ ] Document resource chain calculation algorithm
- [ ] Add docstrings to all views and form methods
- [ ] Document JavaScript component selector API
- [ ] Create Phase 2 summary report

---

## Risks and Considerations

**Risk 1: Resource Chain Calculation Complexity**
- **Impact:** Medium
- **Likelihood:** Medium
- **Mitigation:**
  - Start with simple component → ore lookup
  - Test with fixture data extensively
  - Handle missing data gracefully (component not found)
  - Consider caching for performance

**Risk 2: JSONField Form Complexity**
- **Impact:** Medium (mitigated by ENH-0000006 patterns)
- **Likelihood:** Low
- **Mitigation:**
  - Reuse material-selector.js pattern
  - Adapt ComponentForm pattern from ENH-0000006
  - Test early with fixture data

**Risk 3: Component UUID Lookup Performance**
- **Impact:** Low
- **Likelihood:** Low
- **Mitigation:**
  - Cache component queryset in view context
  - Use select_related() if needed
  - Monitor with Django Debug Toolbar

**Risk 4: Resource Chain Display Performance**
- **Impact:** Low (only 15 blocks in fixtures)
- **Likelihood:** Low
- **Mitigation:**
  - Calculate resource chain in view, not template
  - Cache results if needed
  - Optimize queries with prefetch_related()

---

## Alternatives Considered

### Alternative 1: Raw JSON Textarea
**Rejected:** Poor UX, error-prone, requires users to know UUID format.

### Alternative 2: Inline Formsets
**Rejected:** Requires separate BlockComponent model, breaks Phase 1 JSONField design.

### Alternative 3: AJAX Component Search
**Rejected:** Over-engineering for 15 components. Can add later if needed.

### Alternative 4: Separate Resource Chain View
**Considered:** Could create `/blocks/<uuid>/resources/` endpoint. May add in Phase 3 if detail view too cluttered.

---

## Related Issues/Enhancements

- **Depends On:** ENH-0000001 (Ores Model) - ✅ Completed
- **Depends On:** ENH-0000002 (Components Model) - ✅ Completed
- **Depends On:** ENH-0000003 (Blocks Model) - ✅ Completed
- **Depends On:** ENH-0000005 (Ores Views) - ✅ Completed (2026-01-25)
- **Depends On:** ENH-0000006 (Components Views) - ✅ Completed (2026-01-25)
- **Enables:** Phase 3 Build Order Calculator
- **Enables:** Multi-block resource calculation

---

## Notes

- This enhancement completes Phase 2 CRUD functionality
- Resource chain visualization is foundation for Phase 3 build order calculator
- JavaScript component selector adapted from material selector (ENH-0000006)
- Phase 1 validation helpers (validate_components) must be reused
- Test with fixture data extensively - all 15 blocks have valid components
- Consider creating helper method in Block model for resource chain calculation
- Resource chain display should be clear and hierarchical (tree structure)
- Phase 2 completion report should summarize all three enhancements

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
