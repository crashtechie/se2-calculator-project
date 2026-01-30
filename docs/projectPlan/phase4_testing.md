# Phase 4: Testing, Documentation & Core Infrastructure

**Duration:** 3-4 days  
**Priority:** High  
**Dependencies:** Phases 1, 2, 3 complete

## Objectives
- Achieve >80% test coverage
- Write comprehensive tests for all features
- Update project documentation
- Perform integration testing
- Fix bugs and polish UI
- **NEW:** Implement core infrastructure (deferred from ENH-0000008)

## Tasks

### 4.0 Core Infrastructure (Deferred from ENH-0000008)
**Duration:** 1-1.5 days  
**Priority:** High

#### 4.0.1 Core App Setup
**Files:** `core/__init__.py`, `core/apps.py`, `core/mixins.py`, `core/utils.py`

- [ ] Create core Django app
- [ ] Add core app to INSTALLED_APPS
- [ ] Create JSONFieldValidationMixin for form validation
- [ ] Create utility functions (validate_uuid, sanitize_html)
- [ ] Create core/templatetags/core_filters.py for reusable template filters
- [ ] Write comprehensive docstrings

#### 4.0.2 API Endpoints
**Files:** `ores/api.py`, `components/api.py`, `blocks/api.py`

- [ ] Create OreAPIListView (GET /ores/api/)
- [ ] Create ComponentAPIListView (GET /components/api/)
- [ ] Create BlockAPIListView (GET /blocks/api/)
- [ ] Return JSON with id, name, mass fields
- [ ] Add API routes to urls.py
- [ ] Return 405 for non-GET methods
- [ ] Add API documentation in docstrings

#### 4.0.3 Structured Logging
**Files:** `se2CalcProject/settings.py`, view files

- [ ] Add LOGGING configuration to settings.py
- [ ] Configure file handler (logs/app.log)
- [ ] Configure console handler
- [ ] Add loggers for ores, components, blocks, core apps
- [ ] Add logging to view operations (CREATE, UPDATE, DELETE)
- [ ] Log API requests and responses
- [ ] Log errors with stack traces

#### 4.0.4 Custom Error Pages
**Files:** `templates/404.html`, `templates/500.html`, `core/views.py`

- [ ] Create custom 404.html template
- [ ] Create custom 500.html template
- [ ] Create error handler views in core/views.py
- [ ] Add handler404 and handler500 to urls.py
- [ ] Test error pages with DEBUG=False

#### 4.0.5 Additional Security Settings
**Files:** `se2CalcProject/settings.py`

- [ ] Add SECURE_BROWSER_XSS_FILTER = True
- [ ] Add SECURE_CONTENT_TYPE_NOSNIFF = True
- [ ] Add CSRF_COOKIE_HTTPONLY = True
- [ ] Add SESSION_COOKIE_HTTPONLY = True
- [ ] Configure production HTTPS settings

#### 4.0.6 CSRF Token JavaScript
**Files:** `static/js/csrf.js`, `templates/base.html`

- [ ] Create csrf.js with getCookie function
- [ ] Export csrftoken constant
- [ ] Include in base.html template
- [ ] Document usage for AJAX requests

#### 4.0.7 Core Infrastructure Tests
**Files:** `core/tests.py`

- [ ] Test JSONFieldValidationMixin (4 tests)
- [ ] Test utility functions (3 tests)
- [ ] Test API endpoints (6 tests)
- [ ] Test error pages (2 tests)
- [ ] Test logging configuration (4 tests)
- [ ] Achieve >80% coverage for core app

#### 4.0.8 Core Infrastructure Documentation
**Files:** Various documentation files

- [ ] Document API endpoint usage
- [ ] Document mixin usage with examples
- [ ] Document logging configuration
- [ ] Document error handling strategy
- [ ] Update CHANGELOG.md
- [ ] Update README.md

### 4.1 Model Tests
**Files:** `ores/tests/test_models.py`, `components/tests/test_models.py`, `blocks/tests/test_models.py`

- [ ] Test Ore model creation and validation
- [ ] Test Component model with JSONField
- [ ] Test Block model with all fields
- [ ] Test BuildOrder model
- [ ] Test model __str__ methods
- [ ] Test timestamp auto-population
- [ ] Test UUIDv7 generation
- [ ] Test unique constraints

### 4.2 View Tests
**Files:** `ores/tests/test_views.py`, `components/tests/test_views.py`, `blocks/tests/test_views.py`

For each app, test:
- [ ] ListView returns correct objects
- [ ] ListView filtering works
- [ ] ListView sorting works
- [ ] DetailView displays correct object
- [ ] CreateView creates object successfully
- [ ] CreateView validation errors
- [ ] UpdateView updates object
- [ ] DeleteView deletes object
- [ ] Proper redirects after actions
- [ ] 404 for non-existent objects

### 4.3 Build Order Calculator Tests
**File:** `blocks/tests/test_calculators.py`

- [ ] Test mass calculation with single block
- [ ] Test mass calculation with multiple blocks
- [ ] Test component aggregation
- [ ] Test ore aggregation (multi-level)
- [ ] Test fabricator time calculation
- [ ] Test with zero quantities
- [ ] Test with missing data (error handling)
- [ ] Test with circular dependencies (if applicable)

### 4.4 Form Tests
**Files:** `ores/tests/test_forms.py`, `components/tests/test_forms.py`, `blocks/tests/test_forms.py`

- [ ] Test valid form submissions
- [ ] Test required field validation
- [ ] Test unique constraint validation
- [ ] Test JSONField validation
- [ ] Test data type validation (float, int)
- [ ] Test custom validators

### 4.5 Integration Tests
**File:** `tests/test_integration.py`

End-to-end workflows:
- [ ] Create ore → Create component using ore → Create block using component
- [ ] Create build order with multiple blocks → Verify calculations
- [ ] Update component materials → Verify block calculations update
- [ ] Delete ore → Verify component validation
- [ ] Full CRUD cycle for each model

### 4.6 URL Tests
**Files:** `ores/tests/test_urls.py`, `components/tests/test_urls.py`, `blocks/tests/test_urls.py`

- [ ] Test all URL patterns resolve correctly
- [ ] Test URL reverse lookups
- [ ] Test URL parameters (UUID)

### 4.7 Admin Tests
**Files:** `ores/tests/test_admin.py`, `components/tests/test_admin.py`, `blocks/tests/test_admin.py`

- [ ] Test admin registration
- [ ] Test list_display fields
- [ ] Test search functionality
- [ ] Test filters
- [ ] Test JSONField display in admin

### 4.8 Test Coverage Report
**Commands:**
```bash
uv run pytest --cov=ores --cov=components --cov=blocks --cov-report=html
uv run pytest --cov=ores --cov=components --cov=blocks --cov-report=term
```

- [ ] Run coverage report
- [ ] Identify untested code
- [ ] Write additional tests to reach >80%
- [ ] Document coverage results

### 4.9 Documentation Updates
**Files:** Various documentation files

- [ ] Update README.md with new features
- [ ] Document JSONField structure in docs/
- [ ] Create API documentation (if applicable)
- [ ] Update CHANGELOG.md
- [ ] Create user guide for build order calculator
- [ ] Document calculation algorithms
- [ ] Add screenshots to documentation

### 4.10 User Acceptance Testing
**Manual testing checklist:**

- [ ] Test all CRUD operations in browser
- [ ] Test filtering and sorting
- [ ] Test build order creation workflow
- [ ] Test calculation accuracy with known data
- [ ] Test responsive design on mobile
- [ ] Test with different browsers
- [ ] Test error messages display correctly
- [ ] Test form validation feedback
- [ ] Test navigation and breadcrumbs
- [ ] Test admin interface

### 4.11 Performance Testing
**File:** `tests/test_performance.py`

- [ ] Test list view with 1000+ records
- [ ] Test build order calculation with 100+ blocks
- [ ] Test database query optimization
- [ ] Add database indexes if needed
- [ ] Profile slow queries

### 4.12 Bug Fixes & Polish
- [ ] Fix any bugs found during testing
- [ ] Improve error messages
- [ ] Add loading indicators for calculations
- [ ] Improve form UX
- [ ] Add confirmation dialogs
- [ ] Improve mobile responsiveness
- [ ] Add tooltips/help text
- [ ] Optimize CSS/JS

## Deliverables
- **NEW:** Core app with utilities, mixins, and API endpoints
- **NEW:** Structured logging configuration
- **NEW:** Custom error pages
- **NEW:** Additional security settings
- Comprehensive test suite with >80% coverage
- Updated documentation
- Bug-free application
- Performance optimizations
- User guide

## Testing Tools
- pytest-django
- pytest-cov (coverage)
- factory_boy (test fixtures)
- faker (test data generation)
- selenium (optional, for browser testing)

## Test Data Setup
**File:** `tests/fixtures.py` or use factory_boy

- [ ] Create OreFactory
- [ ] Create ComponentFactory
- [ ] Create BlockFactory
- [ ] Create BuildOrderFactory
- [ ] Create test data fixtures

## Coverage Goals
- Models: 100%
- Views: >90%
- Forms: >90%
- Calculators: 100%
- Overall: >80%

## Documentation Structure
```
docs/
├── projectPlan/          (this directory)
├── design/
│   └── appsDesign.md
├── api/
│   └── jsonfield_format.md
├── userGuide/
│   ├── getting_started.md
│   ├── managing_ores.md
│   ├── managing_components.md
│   ├── managing_blocks.md
│   └── build_order_calculator.md
└── development/
    ├── testing.md
    └── calculations.md
```

## Notes
- **Core infrastructure from ENH-0000008 is now part of Phase 4**
- Use pytest fixtures for common test data
- Mock external dependencies if any
- Test both success and failure cases
- Document any known limitations
- Create issue tickets for future enhancements
- Core app should not break existing functionality
- API endpoints are read-only (GET only) for now
- Logging should be comprehensive but not verbose
