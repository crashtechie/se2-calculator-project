# Pytest Configuration

**Project:** SE2 Calculator Project  
**Document Type:** Quality Assurance - Testing Setup  
**Last Updated:** January 26, 2026  
**Status:** Active  

---

## Overview

The SE2 Calculator Project uses pytest with pytest-django for automated testing. This document describes the pytest configuration and setup required for running tests.

---

## Configuration Files

### conftest.py

**Location:** `app/conftest.py`

```python
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'se2CalcProject.settings')
django.setup()
```

This file configures Django settings before pytest imports any models or views.

### pyproject.toml

**Location:** `pyproject.toml`

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "se2CalcProject.settings"
python_files = ["test_*.py", "*_test.py", "tests.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
testpaths = ["app"]
addopts = "--reuse-db --nomigrations"
```

**Configuration Options:**
- `DJANGO_SETTINGS_MODULE`: Django settings module path
- `python_files`: Test file naming patterns
- `python_classes`: Test class naming patterns
- `python_functions`: Test function naming patterns
- `testpaths`: Directories to search for tests
- `addopts`: Default pytest options (reuse database, skip migrations)

---

## Running Tests

### Basic Commands

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific app tests
uv run pytest app/blocks/
uv run pytest app/components/
uv run pytest app/ores/

# Run specific test file
uv run pytest app/blocks/test_views.py

# Run specific test class
uv run pytest app/blocks/test_views.py::BlockListViewTest

# Run specific test method
uv run pytest app/blocks/test_views.py::BlockListViewTest::test_view_renders_successfully
```

### Coverage Commands

```bash
# Run with coverage
uv run pytest --cov

# Generate HTML coverage report
uv run pytest --cov --cov-report=html

# View coverage for specific app
uv run pytest --cov=app/blocks app/blocks/

# Show missing lines
uv run pytest --cov --cov-report=term-missing
```

### Advanced Options

```bash
# Stop on first failure
uv run pytest -x

# Run last failed tests
uv run pytest --lf

# Run tests in parallel
uv run pytest -n auto

# Show local variables in tracebacks
uv run pytest -l

# Disable output capture (see print statements)
uv run pytest -s
```

---

## Test Discovery

Pytest automatically discovers tests based on naming conventions:

**Test Files:**
- `test_*.py`
- `*_test.py`
- `tests.py`

**Test Classes:**
- `Test*`

**Test Functions:**
- `test_*`

**Example Structure:**
```
app/
├── blocks/
│   ├── test_forms.py          # Discovered
│   ├── test_views.py          # Discovered
│   ├── test_templatetags.py   # Discovered
│   └── models.py              # Not a test file
├── components/
│   └── test_views.py          # Discovered
└── ores/
    └── test_views.py          # Discovered
```

---

## Database Configuration

### Test Database

Pytest-django creates a test database for each test run:
- Database name: `test_<DB_NAME>`
- Automatically created before tests
- Automatically destroyed after tests

### Reusing Test Database

The `--reuse-db` option (configured in `pyproject.toml`) reuses the test database between runs:

**Benefits:**
- Faster test execution
- No database recreation overhead

**When to recreate:**
```bash
# Force database recreation
uv run pytest --create-db
```

### Skipping Migrations

The `--nomigrations` option (configured in `pyproject.toml`) creates tables directly from models:

**Benefits:**
- Faster test database setup
- No migration execution overhead

**When to run migrations:**
```bash
# Run with migrations
uv run pytest --migrations
```

---

## Fixtures

### Django Fixtures

Load test data using Django fixtures:

```python
from django.test import TestCase

class BlockViewTest(TestCase):
    fixtures = ['sample_ores.json', 'sample_components.json', 'sample_blocks.json']
    
    def test_with_fixture_data(self):
        from blocks.models import Block
        self.assertGreater(Block.objects.count(), 0)
```

### Pytest Fixtures

Create reusable test data with pytest fixtures:

```python
import pytest
from ores.models import Ore

@pytest.fixture
def sample_ore(db):
    return Ore.objects.create(
        name='Test Ore',
        mass=100.0,
        description='Test description'
    )

@pytest.mark.django_db
def test_ore_creation(sample_ore):
    assert sample_ore.name == 'Test Ore'
```

---

## Troubleshooting

### Import Errors

**Problem:** `ImproperlyConfigured: Requested setting INSTALLED_APPS`

**Solution:** Ensure `app/conftest.py` exists and configures Django settings.

### Test Discovery Issues

**Problem:** Tests not discovered

**Solution:** 
- Check file naming matches patterns (`test_*.py`)
- Verify files are in `app/` directory
- Run `uv run pytest --collect-only` to see discovered tests

### Database Errors

**Problem:** Database connection errors

**Solution:**
- Verify `.env` file exists with database credentials
- Ensure database server is running
- Check `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` in `.env`

### Fixture Loading Errors

**Problem:** Fixture file not found

**Solution:**
- Verify fixture path: `app/{app_name}/fixtures/{fixture_name}.json`
- Check fixture JSON is valid: `python -m json.tool fixture.json`

---

## Best Practices

1. **Use `--reuse-db`** for faster test execution
2. **Use `--nomigrations`** unless testing migrations
3. **Run specific tests** during development
4. **Run full suite** before committing
5. **Check coverage** regularly with `--cov`
6. **Use fixtures** for complex test data
7. **Keep tests independent** (no shared state)

---

## Related Documentation

- [Automated Testing Overview](./automated-testing-overview.md)
- [Unit Test Guide](./automated-testing-unit-tests.md)
- [Coverage Guide](./automated-testing-coverage.md)
- [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

---

**Document Owner:** Development & QA Team  
**Last Review:** January 26, 2026  
**Next Review:** April 26, 2026
