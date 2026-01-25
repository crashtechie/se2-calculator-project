# Phase 2 Enhancement Requests: Views & Templates

This directory contains enhancement requests for Phase 2 of the SE2 Calculator Project, focusing on implementing CRUD views and templates for all three core apps.

---

## Overview

**Phase:** 2 - Views & Templates  
**Duration:** 3-4 days  
**Status:** In Review  
**Dependencies:** Phase 1 Complete (ENH-0000001 through ENH-0000004)

---

## Enhancement Requests

### ENH-0000005: Ores Views & Templates
**Directory:** `ENH0000005/`  
**File:** `ENH0000005-ores-views-templates.md`  
**Priority:** High  
**Estimated Effort:** 1-2 days  
**Status:** In Review

**Summary:** Implement complete CRUD views and templates for the Ores app with filtering, sorting, and pagination. Establishes base template patterns for the project.

**Key Deliverables:**
- OreListView, OreDetailView, OreCreateView, OreUpdateView, OreDeleteView
- Base templates (base.html, home.html)
- Static files infrastructure (CSS)
- URL routing configuration
- 15+ automated tests

**Dependencies:** None (first Phase 2 enhancement)

---

### ENH-0000006: Components Views & Templates
**Directory:** `ENH0000006/`  
**File:** `ENH0000006-components-views-templates.md`  
**Priority:** High  
**Estimated Effort:** 1.5-2 days  
**Status:** In Review

**Summary:** Implement complete CRUD views and templates for the Components app with JSONField material handling and dynamic form inputs.

**Key Deliverables:**
- ComponentListView, ComponentDetailView, ComponentCreateView, ComponentUpdateView, ComponentDeleteView
- Dynamic material selector (JavaScript)
- JSONField form handling pattern
- Material display formatting
- 20+ automated tests

**Dependencies:** ENH-0000005 (for base template patterns)

**Key Challenge:** JSONField materials require dynamic form interface for selecting ores and quantities with validation.

---

### ENH-0000007: Blocks Views & Templates
**Directory:** `ENH0000007/`  
**File:** `ENH0000007-blocks-views-templates.md`  
**Priority:** High  
**Estimated Effort:** 1.5-2 days  
**Status:** In Review

**Summary:** Implement complete CRUD views and templates for the Blocks app with JSONField component handling and full resource chain visualization.

**Key Deliverables:**
- BlockListView, BlockDetailView, BlockCreateView, BlockUpdateView, BlockDeleteView
- Dynamic component selector (JavaScript)
- Resource chain visualization (Block → Components → Ores)
- Statistics display (total mass, component count)
- 20+ automated tests

**Dependencies:** 
- ENH-0000005 (for base template patterns)
- ENH-0000006 (for JSONField form patterns)

**Key Feature:** Full resource chain display showing complete ore breakdown for each block.

---

### ENH-0000008: Core Infrastructure & Best Practices
**Directory:** `ENH0000008/`  
**File:** `ENH0000008-core-infrastructure.md`  
**Priority:** High  
**Estimated Effort:** 1 day  
**Status:** In Review

**Summary:** Create core infrastructure app with shared utilities, API endpoints, validation mixins, logging, error handling, and security improvements.

**Key Deliverables:**
- Core app with reusable utilities
- API endpoints for AJAX
- Validation mixins (DRY principle)
- Structured logging
- Custom error pages
- Security enhancements
- 15+ automated tests

**Dependencies:** None (implements first)

**Key Feature:** Foundation for all Phase 2 views with shared infrastructure.

---

## Implementation Order

**Recommended sequence:**

1. **ENH-0000008 (Core Infrastructure)** - Foundation first
   - Core app with utilities
   - API endpoints
   - Validation mixins
   - Logging and security

2. **ENH-0000005 (Ores)** - Establishes patterns
   - Base templates
   - URL patterns
   - Static files
   - Simple CRUD (no JSONField complexity)

3. **ENH-0000006 (Components)** - Adds complexity
   - JSONField form handling
   - Dynamic material selector
   - Ore relationship display

4. **ENH-0000007 (Blocks)** - Completes Phase 2
   - Reuses JSONField patterns
   - Resource chain calculation
   - Full ore breakdown display

---

## Common Patterns

### URL Structure
All apps follow consistent URL patterns:
```
/<app>/                     - List view
/<app>/<uuid>/              - Detail view
/<app>/create/              - Create view
/<app>/<uuid>/update/       - Update view
/<app>/<uuid>/delete/       - Delete view
```

### View Classes
All apps use Django generic class-based views:
- ListView (with filtering and sorting)
- DetailView
- CreateView (with success messages)
- UpdateView (with success messages)
- DeleteView (with confirmation)

### Testing Standards
- Minimum 15-20 tests per enhancement
- 100% pass rate required
- Execution time <1.5 seconds per enhancement
- Use fixtures for test data: `fixtures = ['sample_ores.json', 'sample_components.json', 'sample_blocks.json']`

### JSONField Handling (ENH-0000006, ENH-0000007)
- Dynamic form inputs with JavaScript
- Validation using Phase 1 model helpers
- Formatted display in detail views (not raw JSON)
- Conversion between form data and JSON storage

---

## Phase 2 Success Criteria

- [ ] Core infrastructure app created (ENH-0000008)
- [ ] All four enhancements have complete CRUD interfaces
- [ ] Base templates created and reusable
- [ ] Static files infrastructure in place
- [ ] URL routing configured for all apps
- [ ] Filtering and sorting work on list views
- [ ] Pagination implemented (25 items per page)
- [ ] JSONField data displays formatted (not raw JSON)
- [ ] Dynamic form inputs work for materials and components
- [ ] Resource chain visualization works for blocks
- [ ] Minimum 70+ automated tests total (15+15+20+20)
- [ ] 100% test pass rate maintained
- [ ] All templates are mobile responsive
- [ ] Success/error messages display correctly
- [ ] Documentation updated (README, CHANGELOG)
- [ ] Phase 2 completion report created

---

## Testing Strategy

### Unit Tests
- View rendering with fixture data
- Context data validation
- Filtering and sorting logic
- Form validation
- JSONField conversion

### Integration Tests
- Full CRUD workflows
- Success/error message display
- Pagination with large datasets
- Resource chain calculation

### Manual Tests
- Browser testing (Chrome, Firefox, Safari)
- Mobile responsiveness
- JavaScript functionality
- Form submission workflows

---

## Documentation Requirements

Each enhancement must include:
- [ ] Deployment guide
- [ ] Test documentation
- [ ] Post-deployment review
- [ ] Code comments and docstrings
- [ ] CHANGELOG.md entry
- [ ] README.md update

---

## Related Documentation

- **Phase 2 Plan:** `/docs/projectPlan/phase2_views.md`
- **Phase 2 Recommendations:** `/docs/projectPlan/phase2_recommendations.md`
- **Enhancement Template:** `/docs/enhancementRequests/enhancementRequestTemplate.md`
- **Phase 1 Enhancements:** `/docs/enhancementRequests/phase1_models/`
- **Best Practices:** `BEST_PRACTICES_SUMMARY.md`
- **Improvements Guide:** `RECOMMENDED_IMPROVEMENTS.md`

---

## Notes

- All enhancements currently in review status
- ENH-0000008 should be implemented first (core infrastructure)
- Waiting for approval to begin implementation
- Phase 1 must be 100% complete before starting Phase 2
- Fixture data (15 ores, 15 components, 15 blocks) should be loaded before development
- Run `uv run python scripts/verify_fixtures.py` before starting
- Base templates from ENH-0000005 will be reused in ENH-0000006 and ENH-0000007
- JSONField form patterns from ENH-0000006 will be adapted for ENH-0000007

---

## Questions or Issues

For questions about Phase 2 enhancements, refer to:
- Phase 2 project plan: `/docs/projectPlan/phase2_views.md`
- Phase 2 recommendations: `/docs/projectPlan/phase2_recommendations.md`
- Enhancement request template: `/docs/enhancementRequests/enhancementRequestTemplate.md`

---

**Last Updated:** 2026-01-24  
**Status:** Ready for Review
