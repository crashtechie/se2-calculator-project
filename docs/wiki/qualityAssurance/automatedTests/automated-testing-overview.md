# Automated Testing Overview

**Project:** SE2 Calculator Project  
**Document Type:** Quality Assurance - Automated Testing Guide  
**Last Updated:** January 30, 2026  
**Status:** Active  

---

## Purpose

This document provides a comprehensive overview of the automated testing strategy and implementation for the SE2 Calculator Project. Automated tests ensure code quality, prevent regressions, and verify functionality across all application components.

---

## Testing Philosophy

### Goals

- **High Coverage:** Target >95% code coverage for models, >90% for views and forms
- **Fast Execution:** All tests complete in <5 seconds
- **Reliable:** Tests are deterministic and independent
- **Comprehensive:** Cover unit, integration, and performance testing
- **Maintainable:** Tests are well-organized and documented

### Testing Pyramid

```
           /\
          /  \  E2E Tests (Future)
         /    \
        /------\  Integration Tests (15+)
       /        \
      /----------\  Unit Tests (200+)
     /__________\
```

---

## Test Organization

### Project Test Structure

```
se2-calculator-project/
├── app/                          # Django application
│   ├── ores/
│   │   └── tests/               # Ores app tests
│   │       ├── __init__.py
│   │       ├── test_models.py   # 35+ tests
│   │       ├── test_views.py    # 25+ tests
│   │       └── test_fixtures.py # 10+ tests
│   ├── components/
│   │   └── tests/               # Components app tests
│   │       ├── __init__.py
│   │       ├── test_models.py   # 44+ tests
│   │       ├── test_views.py    # 25+ tests
│   │       └── test_fixtures.py # 10+ tests
│   └── blocks/
│       └── tests/               # Blocks app tests
│           ├── __init__.py
│           ├── test_models.py   # 49+ tests
│           ├── test_views.py    # 25+ tests
│           ├── test_forms.py    # 10+ tests
│           ├── test_templatetags.py # 5+ tests
│           └── test_fixtures.py # 10+ tests
└── tests/                       # Standalone test scripts
    ├── integration/             # Integration test suite
    │   ├── run_integration_tests.py
    │   └── README.md
    ├── performance/             # Performance tests
    │   └── test_blocks_queries.py
    └── testResults/             # Test output files
```

### Test Categories

#### 1. Unit Tests (Django App Tests)
- **Location:** `app/{app_name}/tests/`
- **Framework:** Django TestCase
- **Purpose:** Test individual components in isolation
- **Coverage Target:** >95%

#### 2. Integration Tests
- **Location:** `tests/integration/`
- **Framework:** Django Client, Custom Runner
- **Purpose:** Test full CRUD workflows
- **Coverage Target:** All major user workflows

#### 3. Performance Tests
- **Location:** `tests/performance/`
- **Framework:** Python profiling, Django queries
- **Purpose:** Identify performance bottlenecks
- **Coverage Target:** Critical database operations

---

## Test Types by Application

### Ores App Tests

**Test Files:**
- `app/ores/tests/test_models.py` - 35+ tests
- `app/ores/tests/test_views.py` - 25+ tests  
- `app/ores/tests/test_fixtures.py` - 10+ tests

**Test Coverage:**
- ✅ Model creation and validation
- ✅ Field constraints (unique, max_length, blank)
- ✅ UUID generation (UUIDv7)
- ✅ Timestamp behavior (created_at, updated_at)
- ✅ Database queries and filtering
- ✅ CRUD views (list, detail, create, update, delete)
- ✅ Form validation
- ✅ Template rendering
- ✅ Fixture loading and data integrity

**Running Ores Tests:**
```bash
# All ores tests
uv run python manage.py test ores -v 2

# Specific test file
uv run python manage.py test ores.tests.test_models -v 2

# Specific test class
uv run python manage.py test ores.tests.test_models.OreModelCreationTests -v 2

# Specific test method
uv run python manage.py test ores.tests.test_models.OreModelCreationTests.test_create_ore_with_all_fields -v 2
```

---

### Components App Tests

**Test Files:**
- `app/components/tests/test_models.py` - 44+ tests
- `app/components/tests/test_views.py` - 25+ tests
- `app/components/tests/test_fixtures.py` - 10+ tests

**Test Coverage:**
- ✅ Component model creation
- ✅ Materials JSONField validation
- ✅ Component-Ore relationships
- ✅ Material quantity validation
- ✅ CRUD views with materials
- ✅ Dynamic form handling (add/remove materials)
- ✅ JSON serialization/deserialization
- ✅ Template rendering with materials display
- ✅ Fixture data with complex materials

**Running Components Tests:**
```bash
# All components tests
uv run python manage.py test components -v 2

# Model tests only
uv run python manage.py test components.tests.test_models -v 2

# View tests only
uv run python manage.py test components.tests.test_views -v 2
```

---

### Blocks App Tests

**Test Files:**
- `app/blocks/tests/test_models.py` - 49+ tests
- `app/blocks/tests/test_views.py` - 25+ tests
- `app/blocks/tests/test_forms.py` - 10+ tests
- `app/blocks/tests/test_templatetags.py` - 5+ tests
- `app/blocks/tests/test_fixtures.py` - 10+ tests

**Test Coverage:**
- ✅ Block model creation
- ✅ Consumer/Producer validation
- ✅ Component relationships
- ✅ Resource chain calculation
- ✅ CRUD views with component selection
- ✅ Form validation (business rules)
- ✅ Template tags for formatting
- ✅ Complex fixture data

**Running Blocks Tests:**
```bash
# All blocks tests
uv run python manage.py test blocks -v 2

# Model tests
uv run python manage.py test blocks.tests.test_models -v 2

# View tests
uv run python manage.py test blocks.tests.test_views -v 2

# Form tests
uv run python manage.py test blocks.tests.test_forms -v 2

# Template tag tests
uv run python manage.py test blocks.tests.test_templatetags -v 2
```

---

## Running Tests

### Quick Reference

```bash
# All tests in project
cd app
uv run python manage.py test --parallel

# All tests with verbosity
uv run python manage.py test -v 2

# Specific app
uv run python manage.py test ores -v 2
uv run python manage.py test components -v 2
uv run python manage.py test blocks -v 2

# Multiple apps
uv run python manage.py test ores components blocks -v 2

# Keep test database (for debugging)
uv run python manage.py test --keepdb -v 2

# Stop on first failure
uv run python manage.py test --failfast -v 2

# Run with coverage
uv run coverage run --source='.' manage.py test
uv run coverage report
uv run coverage html
```

### Integration Tests

```bash
# Run integration test suite
uv run python tests/integration/run_integration_tests.py

# View results
cat tests/testResults/integration_test_results_*.json | python -m json.tool
```

### Performance Tests

```bash
# Run performance tests
uv run python tests/performance/test_blocks_queries.py
```

---

## Test Coverage

### Coverage Commands

```bash
# Generate coverage report for all apps
cd app
uv run coverage run --source='ores,components,blocks' manage.py test
uv run coverage report

# Generate HTML coverage report
uv run coverage html
# Open app/htmlcov/index.html in browser

# Coverage for specific app
uv run coverage run --source='ores' manage.py test ores
uv run coverage report -m

# Show missing lines
uv run coverage report -m --skip-covered
```

### Coverage Targets

| Component | Target | Current Status |
|-----------|--------|----------------|
| Models | >95% | ✅ 98%+ |
| Views | >90% | ✅ 92%+ |
| Forms | >90% | ✅ 90%+ |
| Template Tags | >85% | ✅ 87%+ |
| Overall | >90% | ✅ 94%+ |

---

## Test Data and Fixtures

### Using Fixtures in Tests

```python
from django.test import TestCase

class OreTestCase(TestCase):
    """Test case using fixture data."""
    
    fixtures = ['sample_ores.json']
    
    def test_fixture_data_loads(self):
        """Verify fixture data loads correctly."""
        from ores.models import Ore
        self.assertGreater(Ore.objects.count(), 0)
```

### Available Fixtures

- `app/ores/fixtures/sample_ores.json` - 12 sample ores
- `app/components/fixtures/sample_components.json` - 20 sample components
- `app/blocks/fixtures/sample_blocks.json` - 15 sample blocks

### Loading Fixtures Manually

```bash
# Load all fixtures
cd app
uv run python manage.py loaddata sample_ores sample_components sample_blocks

# Load specific fixture
uv run python manage.py loaddata sample_ores
```

---

## Writing Tests

### Test Naming Conventions

```python
# Good test names (descriptive and specific)
def test_create_ore_with_valid_data(self):
def test_ore_name_must_be_unique(self):
def test_negative_mass_raises_validation_error(self):

# Bad test names (vague)
def test_ore(self):
def test_validation(self):
def test_create(self):
```

### Test Structure Template

```python
"""
Test module for [Component] [Feature].
"""
from django.test import TestCase
from [app].models import [Model]


class [Feature]Tests(TestCase):
    """Test [specific feature or behavior]."""
    
    fixtures = ['fixture_name.json']  # Optional
    
    def setUp(self):
        """Set up test data for each test method."""
        # Create test objects
        self.test_object = [Model].objects.create(...)
    
    def tearDown(self):
        """Clean up after each test method."""
        # Optional cleanup
        pass
    
    def test_[specific_behavior](self):
        """Test that [specific behavior] works as expected."""
        # Arrange
        expected_value = "expected"
        
        # Act
        result = self.test_object.some_method()
        
        # Assert
        self.assertEqual(result, expected_value)
```

### Best Practices

#### DO

✅ Use descriptive test names that explain what is being tested  
✅ Follow Arrange-Act-Assert pattern  
✅ Test both success and failure cases  
✅ Use setUp/tearDown for common test data  
✅ Test edge cases and boundary conditions  
✅ Use assertRaises for exception testing  
✅ Keep tests independent (no test order dependency)  
✅ Use fixtures for complex test data  
✅ Add docstrings to test methods  

#### DON'T

❌ Test multiple behaviors in one test  
❌ Depend on test execution order  
❌ Use real external services (mock instead)  
❌ Skip error cases  
❌ Copy-paste test code (use setUp or helper methods)  
❌ Test framework code (test your code only)  
❌ Commit tests with print statements for debugging  

---

## Continuous Integration

### Test Execution in CI/CD

```yaml
# GitHub Actions Example
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      
      - name: Run unit tests
        run: |
          cd app
          uv run python manage.py test --parallel -v 2
      
      - name: Run integration tests
        run: |
          uv run python tests/integration/run_integration_tests.py
      
      - name: Generate coverage report
        run: |
          cd app
          uv run coverage run --source='.' manage.py test
          uv run coverage report
          uv run coverage html
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: |
            tests/testResults/
            app/htmlcov/
```

---

## Test Metrics and Reporting

### Key Metrics

- **Total Tests:** 240+ tests
- **Pass Rate:** 100% (target)
- **Execution Time:** <5 seconds (all tests)
- **Code Coverage:** >94%
- **Tests Added Per Enhancement:** Minimum 35+ tests

### Test Execution Output

```bash
Found 240 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........................................................................................
........................................................................................
........................................................................................
----------------------------------------------------------------------
Ran 240 tests in 4.327s

OK
Destroying test database for alias 'default'...
```

---

## Expected Test Output

### Logger Messages During Tests

When running tests with `uv run python manage.py test`, you may see logger warning and error messages interspersed with test progress dots. **This is expected behavior** and does not indicate test failures.

**Example Expected Output:**
```
......................Error resolving component invalid-id: ["invalid-id" is not a valid UUID.]
..Component 00000000-0000-0000-0000-000000000000 not found in database
..........Block creation failed: <ul class="errorlist">...
Component creation failed - validation errors: <ul class="errorlist">...
............................................................................................................................................
----------------------------------------------------------------------
Ran 107 tests in 4.327s

OK
```

**Why These Messages Appear:**
- Tests intentionally trigger validation errors to verify error handling works correctly
- Application code logs these events using Python's logging module (logger.warning, logger.error)
- Logger output is displayed during test execution by default

**What to Look For:**
- ✅ **Test dots (.)** - Each dot represents a passing test
- ✅ **"OK" at the end** - All tests passed successfully
- ❌ **"F" or "E" characters** - Actual test failures or errors (investigate these)
- ❌ **"FAILED" at the end** - Tests failed (requires attention)

**Suppressing Logger Output (Optional):**

If you prefer cleaner output, add to `pytest.ini` or run with:
```bash
uv run python manage.py test --no-input 2>/dev/null
```

---

## Troubleshooting Tests

### Common Issues

#### Test Database Issues

```bash
# Problem: Test database creation fails
# Solution: Drop and recreate test database
dropdb test_se2_calculator_db
uv run python manage.py test --keepdb

# Problem: Migrations not applied
# Solution: Run migrations
uv run python manage.py migrate
```

#### Import Errors

```bash
# Problem: Module not found
# Solution: Ensure PYTHONPATH includes app directory
cd app
uv run python manage.py test

# Or set PYTHONPATH explicitly
PYTHONPATH=app uv run python manage.py test
```

#### Fixture Loading Failures

```bash
# Problem: Fixture file not found
# Solution: Check fixture path
ls app/ores/fixtures/
uv run python manage.py loaddata --help

# Verify fixture is valid JSON
python -m json.tool app/ores/fixtures/sample_ores.json
```

#### Test Failures After Code Changes

```bash
# Problem: Tests fail after model changes
# Solution: Update and apply migrations
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py test
```

---

## Documentation References

### Internal Documentation

- [Pytest Configuration](./pytest-configuration.md) - Pytest setup and configuration
- [Unit Test Guide](./automated-testing-unit-tests.md) - Writing and organizing unit tests
- [Integration Test Guide](./automated-testing-integration-tests.md) - Integration test procedures
- [Coverage Guide](./automated-testing-coverage.md) - Code coverage best practices
- [CI/CD Integration](./automated-testing-ci-cd.md) - Continuous integration setup

### Enhancement Request Test Documentation

- [ENH-0000001 Test Documentation](../../enhancementRequests/phase1_models/ENH0000001/ENH-0000001-test-documentation.md) - Ores tests
- [ENH-0000002 Test Documentation](../../enhancementRequests/phase1_models/ENH0000002/ENH-0000002-test-documentation.md) - Components tests
- [ENH-0000003 Test Documentation](../../enhancementRequests/phase1_models/ENH0000003/ENH-0000003-test-documentation.md) - Blocks tests

### External Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)

---

## Maintenance

### Regular Test Maintenance

- **Weekly:** Review test coverage, address gaps
- **Per Feature:** Add tests before or during implementation
- **Per Bug Fix:** Add regression test
- **Monthly:** Refactor duplicate test code
- **Quarterly:** Review and update test documentation

### Test Suite Health

| Metric | Target | Action if Below Target |
|--------|--------|----------------------|
| Pass Rate | 100% | Fix failing tests immediately |
| Coverage | >90% | Add tests for uncovered code |
| Execution Time | <5s | Optimize slow tests |
| Flaky Tests | 0 | Investigate and fix non-deterministic tests |

---

## Sign-Off

| Role | Name | Date |
|------|------|------|
| QA Lead | TBD | TBD |
| Development Lead | TBD | TBD |
| Project Manager | TBD | TBD |

---

**Document Owner:** Development & QA Team  
**Last Review:** January 30, 2026  
**Next Review:** April 30, 2026
