# Implementation Checklist

Quick reference for tracking project progress.

## Phase 1: Models & Database ⬜

### Setup
- [x] Create ores app
- [ ] Create components app  
- [ ] Create blocks app
- [ ] Register apps in settings.py

### Models
- [ ] Ore model with all fields
- [ ] Component model with JSONField
- [ ] Block model with all fields
- [ ] BuildOrder model

### Database
- [ ] Create migrations
- [ ] Apply migrations
- [ ] Test in Django shell

### Admin
- [ ] Register Ore in admin
- [ ] Register Component in admin
- [ ] Register Block in admin
- [ ] Configure list displays and filters

### Testing
- [ ] Model creation tests
- [ ] Field validation tests
- [ ] Admin interface tests

---

## Phase 2: Views & Templates ⬜

### URLs
- [ ] Configure main urls.py
- [ ] Create ores/urls.py
- [ ] Create components/urls.py
- [ ] Create blocks/urls.py

### Views - Ores
- [ ] OreListView (with filter/sort)
- [ ] OreDetailView
- [ ] OreCreateView
- [ ] OreUpdateView
- [ ] OreDeleteView

### Views - Components
- [ ] ComponentListView (with filter/sort)
- [ ] ComponentDetailView
- [ ] ComponentCreateView
- [ ] ComponentUpdateView
- [ ] ComponentDeleteView

### Views - Blocks
- [ ] BlockListView (with filter/sort)
- [ ] BlockDetailView
- [ ] BlockCreateView
- [ ] BlockUpdateView
- [ ] BlockDeleteView

### Forms
- [ ] OreForm
- [ ] ComponentForm with JSONField widget
- [ ] BlockForm with JSONField widget

### Templates - Base
- [ ] base.html with navigation
- [ ] home.html

### Templates - Ores
- [ ] ore_list.html
- [ ] ore_detail.html
- [ ] ore_form.html
- [ ] ore_confirm_delete.html

### Templates - Components
- [ ] component_list.html
- [ ] component_detail.html
- [ ] component_form.html
- [ ] component_confirm_delete.html

### Templates - Blocks
- [ ] block_list.html
- [ ] block_detail.html
- [ ] block_form.html
- [ ] block_confirm_delete.html

### Static Files
- [ ] main.css
- [ ] material-selector.js
- [ ] component-selector.js

### Testing
- [ ] View tests for all CRUD operations
- [ ] Form validation tests
- [ ] URL routing tests
- [ ] Template rendering tests

---

## Phase 3: Build Order Calculator ⬜

### Model & Logic
- [ ] BuildOrder model
- [ ] calculate_total_mass()
- [ ] calculate_required_components()
- [ ] calculate_required_ores()
- [ ] calculate_fabricator_times()

### Views
- [ ] BuildOrderListView
- [ ] BuildOrderDetailView with calculations
- [ ] BuildOrderCreateView with block selection
- [ ] BuildOrderUpdateView
- [ ] BuildOrderDeleteView

### Templates
- [ ] buildorder_list.html
- [ ] buildorder_detail.html (with breakdowns)
- [ ] buildorder_form.html (with block selector)
- [ ] buildorder_confirm_delete.html

### JavaScript
- [ ] buildorder.js for dynamic selection
- [ ] Block search/filter
- [ ] Add/remove blocks
- [ ] Quantity updates
- [ ] Live preview calculations

### URLs
- [ ] BuildOrder URL patterns

### Testing
- [ ] Calculation accuracy tests
- [ ] Component aggregation tests
- [ ] Ore aggregation tests
- [ ] Fabricator time tests
- [ ] Edge case tests

---

## Phase 4: Testing & Documentation ⬜

### Unit Tests
- [ ] Model tests (all apps)
- [ ] View tests (all apps)
- [ ] Form tests (all apps)
- [ ] Calculator tests
- [ ] URL tests

### Integration Tests
- [ ] End-to-end workflows
- [ ] Cross-app dependencies
- [ ] Build order full cycle

### Coverage
- [ ] Run coverage report
- [ ] Achieve >80% coverage
- [ ] Document coverage results

### Documentation
- [ ] Update README.md
- [ ] Document JSONField formats
- [ ] Create user guide
- [ ] Document calculations
- [ ] Update CHANGELOG.md

### UAT
- [ ] Manual browser testing
- [ ] Mobile responsiveness
- [ ] Cross-browser testing
- [ ] Error handling verification

### Polish
- [ ] Fix bugs
- [ ] Improve error messages
- [ ] Add loading indicators
- [ ] Optimize performance
- [ ] Final UI improvements

---

## Deployment Checklist ⬜

- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up production database
- [ ] Collect static files
- [ ] Run migrations on production
- [ ] Load initial data/fixtures
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Create backup strategy
- [ ] Document deployment process

---

## Progress Tracking

**Phase 1:** ⬜ Not Started | 🟡 In Progress | ✅ Complete  
**Phase 2:** ⬜ Not Started | 🟡 In Progress | ✅ Complete  
**Phase 3:** ⬜ Not Started | 🟡 In Progress | ✅ Complete  
**Phase 4:** ⬜ Not Started | 🟡 In Progress | ✅ Complete  

**Overall Progress:** 0% Complete

---

## Notes

- Update this checklist as you complete tasks
- Mark phases with 🟡 when started, ✅ when complete
- Add notes for any blockers or issues
- Track time spent on each phase
