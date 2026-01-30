# ISSUE-001: Pytest Configuration Missing After Refactor

**Status:** Open  
**Priority:** High  
**Created:** 2026-01-26  
**Component:** Testing Infrastructure  
**Affects Version:** 0.4.1-alpha

## Problem Description

All automated tests fail with `ImproperlyConfigured` error after project refactor. Tests cannot import Django models because Django settings are not configured before pytest runs.

## Error Output

```
django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED_APPS, 
but settings are not configured. You must either define the environment variable 
DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.
```

## Root Cause

1. Test files moved from `app/*/tests/` to `app/*/test_*.py` during refactor
2. No `conftest.py` exists to configure Django before pytest imports models
3. No pytest configuration in `pyproject.toml` to specify Django settings module

## Technical Details

**Failing Test Files:**
- `app/blocks/test_forms.py`
- `app/blocks/test_templatetags.py`
- `app/blocks/test_views.py`
- `app/components/test_views.py`
- `app/ores/test_views.py`

**Import Chain:**
```
test_views.py → models.py → django.db.models.Model → settings.INSTALLED_APPS → ERROR
```

## Solution

### Step 1: Create `app/conftest.py`

```python
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'se2CalcProject.settings')
django.setup()
```

### Step 2: Add pytest configuration to `pyproject.toml`

Add this section to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "se2CalcProject.settings"
python_files = ["test_*.py", "*_test.py", "tests.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
testpaths = ["app"]
addopts = "--reuse-db --nomigrations"
```

### Step 3: Verify Fix

```bash
uv run pytest -v
```

Expected: All tests should collect and run without import errors.

## Implementation Commands

```bash
# Create conftest.py
cat > app/conftest.py << 'EOF'
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'se2CalcProject.settings')
django.setup()
EOF

# Add to pyproject.toml (manual edit required)
# Add [tool.pytest.ini_options] section as shown above

# Test the fix
uv run pytest -v
```

## Verification Checklist

- [ ] `app/conftest.py` created
- [ ] `[tool.pytest.ini_options]` added to `pyproject.toml`
- [ ] `uv run pytest` runs without import errors
- [ ] All test files are discovered
- [ ] Tests pass or fail on assertions (not imports)

## Related Files

- `app/conftest.py` (missing)
- `pyproject.toml` (needs pytest config)
- `app/blocks/test_*.py`
- `app/components/test_*.py`
- `app/ores/test_*.py`

## Notes

- Manual tests work because `manage.py` configures Django
- Automated tests fail because pytest doesn't know about Django
- This is a standard pytest-django configuration issue
