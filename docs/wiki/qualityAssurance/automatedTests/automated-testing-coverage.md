# Automated Testing: Code Coverage

**Project:** SE2 Calculator Project  
**Document Type:** Quality Assurance - Code Coverage Guide  
**Last Updated:** January 30, 2026  
**Status:** Active  

---

## Purpose

This document provides comprehensive guidance for measuring, analyzing, and improving code coverage in the SE2 Calculator Project. Code coverage helps identify untested code and ensures comprehensive test suites.

---

## Code Coverage Overview

### What is Code Coverage?

Code coverage measures the percentage of code executed during tests:

- **Line Coverage** - Percentage of code lines executed
- **Branch Coverage** - Percentage of decision branches taken
- **Function Coverage** - Percentage of functions called
- **Statement Coverage** - Percentage of statements executed

### Why Code Coverage Matters

✅ **Identifies Untested Code** - Shows which code lacks tests  
✅ **Improves Quality** - Higher coverage often means fewer bugs  
✅ **Guides Testing** - Helps prioritize test writing  
✅ **Prevents Regressions** - Ensures changes are tested  
✅ **Documentation** - Shows project test investment  

### Coverage Goals

| Component | Target | Current |
|-----------|--------|---------|
| Models | >95% | 98% |
| Views | >90% | 92% |
| Forms | >90% | 90% |
| Template Tags | >85% | 87% |
| Utilities | >90% | 94% |
| **Overall** | **>90%** | **94%** |

---

## Tools and Setup

### Coverage.py

The project uses `coverage.py` for measuring code coverage.

**Installation:**
```bash
# Already included in pyproject.toml
uv sync
```

**Configuration:**

File: `pyproject.toml`
```toml
[tool.coverage.run]
source = ["app"]
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/admin.py",
    "*/apps.py",
    "manage.py",
    "*/settings.py",
    "*/wsgi.py",
    "*/asgi.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]

[tool.coverage.html]
directory = "app/htmlcov"
```

---

## Running Coverage

### Quick Start

```bash
cd app

# Run tests with coverage
uv run coverage run --source='.' manage.py test

# Generate report
uv run coverage report

# Generate HTML report
uv run coverage html
```

### Coverage Commands

#### Basic Coverage

```bash
# Run all tests with coverage
cd app
uv run coverage run --source='.' manage.py test

# Show coverage summary
uv run coverage report

# Show detailed report with line numbers
uv run coverage report -m
```

#### App-Specific Coverage

```bash
# Coverage for specific app
cd app
uv run coverage run --source='ores' manage.py test ores
uv run coverage report

# Multiple apps
uv run coverage run --source='ores,components,blocks' manage.py test ores components blocks
uv run coverage report
```

#### HTML Reports

```bash
# Generate interactive HTML report
cd app
uv run coverage html

# Open in browser
# Linux
xdg-open htmlcov/index.html
# macOS
open htmlcov/index.html
# Windows
start htmlcov/index.html
```

#### Coverage for Specific Files

```bash
# Coverage for specific module
cd app
uv run coverage run --source='ores.models' manage.py test ores.tests.test_models
uv run coverage report
```

---

## Understanding Coverage Reports

### Terminal Report

```
Name                                   Stmts   Miss  Cover   Missing
--------------------------------------------------------------------
ores/__init__.py                          0      0   100%
ores/admin.py                            15      0   100%
ores/apps.py                              4      0   100%
ores/forms.py                            28      2    93%   45-46
ores/models.py                           42      1    98%   67
ores/urls.py                              6      0   100%
ores/views.py                            85      7    92%   123-129
--------------------------------------------------------------------
TOTAL                                   180      10   94%
```

**Columns:**
- **Stmts** - Total statements in file
- **Miss** - Statements not executed during tests
- **Cover** - Coverage percentage
- **Missing** - Line numbers not covered

### HTML Report

The HTML report provides:

1. **Overview Page** (`index.html`)
   - Overall coverage percentage
   - List of all files with coverage
   - Sortable columns
   - Color-coded coverage

2. **File Detail Pages**
   - Source code with syntax highlighting
   - Line-by-line coverage:
     - **Green** - Line executed
     - **Red** - Line not executed
     - **Yellow** - Partial branch coverage
   - Branch coverage indicators

**Example HTML Report:**
```
Coverage Report: 94%

Files                    Coverage
─────────────────────────────────
ores/models.py          98% ████████████████████░
ores/views.py           92% ████████████████░░░
ores/forms.py           93% ████████████████░░░
components/models.py    97% ████████████████████░
blocks/models.py        96% ████████████████████░
```

---

## Analyzing Coverage

### Identifying Uncovered Code

```bash
# Show missing lines
cd app
uv run coverage report -m

# Output shows missing line numbers:
ores/views.py    92%   123-129
```

**Check those lines:**
```bash
# View specific lines in file
sed -n '123,129p' ores/views.py
```

### Skip Covered Code

```bash
# Only show files with missing coverage
cd app
uv run coverage report --skip-covered
```

### Coverage by Directory

```bash
# Show coverage organized by directory
cd app
uv run coverage report | sort
```

---

## Improving Coverage

### Step 1: Identify Gaps

```bash
cd app
uv run coverage run --source='.' manage.py test
uv run coverage html
# Open htmlcov/index.html
```

1. Find files with low coverage (<90%)
2. Click on filename to see uncovered lines (red)
3. Identify patterns:
   - Error handling not tested
   - Edge cases not covered
   - Specific branches not taken

### Step 2: Write Tests for Gaps

**Example: Uncovered error handling**

Uncovered code (line 45-46 in forms.py):
```python
def clean_mass(self):
    mass = self.cleaned_data.get('mass')
    if mass < 0:  # Line 45 - NOT COVERED
        raise ValidationError("Mass cannot be negative")  # Line 46 - NOT COVERED
    return mass
```

**Write test to cover:**
```python
def test_mass_cannot_be_negative(self):
    """Test that negative mass raises validation error."""
    form = OreForm(data={
        'name': 'Test',
        'mass': -10.0  # Trigger the validation
    })
    
    self.assertFalse(form.is_valid())
    self.assertIn('mass', form.errors)
```

### Step 3: Verify Improvement

```bash
cd app
uv run coverage run --source='ores' manage.py test ores
uv run coverage report -m

# Check that lines 45-46 are now covered
```

---

## Coverage Best Practices

### DO

✅ **Aim for >90% Coverage** - Industry standard  
✅ **Test Error Paths** - Don't just test happy path  
✅ **Test Edge Cases** - Boundary conditions matter  
✅ **Use Coverage as Guide** - Not absolute requirement  
✅ **Review Coverage Reports** - Regularly check gaps  
✅ **Ignore Generated Code** - Migrations, admin, etc.  
✅ **Focus on Business Logic** - Critical code first  
✅ **Document Exclusions** - Use `pragma: no cover` with reason  

### DON'T

❌ **Write Tests Just for Coverage** - Quality over quantity  
❌ **Aim for 100% Coverage** - Diminishing returns  
❌ **Test Framework Code** - Test your code only  
❌ **Ignore Low-Coverage Files** - May indicate issues  
❌ **Skip Edge Cases** - Often where bugs hide  
❌ **Test Implementation Details** - Test behavior  
❌ **Duplicate Tests** - For coverage padding  

---

## Excluding Code from Coverage

### Using `pragma: no cover`

```python
def debug_only_function():  # pragma: no cover
    """This function is only used for debugging."""
    print("Debug info")
    
def __repr__(self):  # pragma: no cover
    """String representation (excluded by config)."""
    return f"<Ore: {self.name}>"

if __name__ == '__main__':  # pragma: no cover
    # Script entry point
    main()
```

### Configuration-Based Exclusions

In `pyproject.toml`:
```toml
[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",           # String representations
    "raise AssertionError",   # Defensive programming
    "raise NotImplementedError",  # Abstract methods
    "if __name__ == .__main__.:",  # Script entry points
    "if TYPE_CHECKING:",      # Type checking imports
    "@(abc\\.)?abstractmethod",  # Abstract methods
]
```

### File Exclusions

In `pyproject.toml`:
```toml
[tool.coverage.run]
omit = [
    "*/migrations/*",    # Database migrations
    "*/tests/*",         # Test files themselves
    "*/admin.py",        # Django admin configuration
    "*/apps.py",         # App configuration
    "manage.py",         # Django management script
    "*/settings.py",     # Settings files
    "*/wsgi.py",         # WSGI configuration
    "*/asgi.py",         # ASGI configuration
]
```

---

## Coverage in CI/CD

### GitHub Actions Integration

```yaml
name: Tests with Coverage

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
      
      - name: Run tests with coverage
        run: |
          cd app
          uv run coverage run --source='.' manage.py test
          uv run coverage report
          uv run coverage html
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./app/.coverage
          fail_ci_if_error: true
      
      - name: Upload HTML report
        uses: actions/upload-artifact@v3
        with:
          name: coverage-report
          path: app/htmlcov/
      
      - name: Check coverage threshold
        run: |
          cd app
          uv run coverage report --fail-under=90
```

### Coverage Badges

Add to README.md:
```markdown
![Coverage](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)
```

### Enforcing Coverage Thresholds

```bash
# Fail if coverage below 90%
cd app
uv run coverage run --source='.' manage.py test
uv run coverage report --fail-under=90

# Exit code 2 if below threshold
if [ $? -eq 2 ]; then
    echo "Coverage below 90%"
    exit 1
fi
```

---

## Coverage Analysis Examples

### Example 1: Identifying Missing Tests

**Coverage Report:**
```
ores/views.py    85%   87-92, 115-118
```

**Check the code:**
```python
# Lines 87-92 (not covered)
def handle_error(self):
    if self.error_type == 'validation':
        messages.error(self.request, "Validation failed")
        return redirect('ores:ore_list')
    else:
        raise Exception("Unknown error")
```

**Analysis:**
- Error handling code not tested
- Need tests for validation errors
- Need tests for unknown error type

**Solution:**
```python
def test_validation_error_handling(self):
    """Test validation error shows message."""
    # Trigger validation error
    response = self.client.post(
        reverse('ores:ore_create'),
        {'name': '', 'mass': -10}  # Invalid data
    )
    
    # Check error message displayed
    messages = list(response.context['messages'])
    self.assertEqual(str(messages[0]), "Validation failed")

def test_unknown_error_handling(self):
    """Test unknown error raises exception."""
    with self.assertRaises(Exception):
        view = OreView()
        view.error_type = 'unknown'
        view.handle_error()
```

---

### Example 2: Branch Coverage

**Uncovered branch:**
```python
def calculate_total(self, include_tax=False):
    total = self.base_amount
    if include_tax:  # Branch 1: True - COVERED
        total += self.tax  # COVERED
    # Branch 2: False - NOT COVERED
    return total
```

**Current test (only covers include_tax=True):**
```python
def test_total_with_tax(self):
    result = self.obj.calculate_total(include_tax=True)
    self.assertEqual(result, 110)  # base 100 + tax 10
```

**Add test for other branch:**
```python
def test_total_without_tax(self):
    result = self.obj.calculate_total(include_tax=False)
    self.assertEqual(result, 100)  # just base, no tax

def test_total_default(self):
    """Test default behavior (no tax)."""
    result = self.obj.calculate_total()  # Default is False
    self.assertEqual(result, 100)
```

---

## Advanced Coverage Techniques

### Combining Coverage from Multiple Runs

```bash
# Run different test suites
cd app
uv run coverage run --source='.' manage.py test ores
uv run coverage run -a --source='.' manage.py test components  # -a = append
uv run coverage run -a --source='.' manage.py test blocks

# Generate combined report
uv run coverage report
```

### Coverage for Parallel Tests

```bash
cd app
uv run coverage run --source='.' --parallel-mode manage.py test --parallel
uv run coverage combine
uv run coverage report
```

### Generating Different Report Formats

```bash
cd app

# Terminal report
uv run coverage report

# Terminal with missing lines
uv run coverage report -m

# HTML report
uv run coverage html

# XML report (for CI tools)
uv run coverage xml

# JSON report
uv run coverage json
```

---

## Troubleshooting Coverage

### Issue: No Coverage Data

**Symptom:**
```
No data to report.
```

**Solutions:**
1. Ensure coverage run was executed:
   ```bash
   uv run coverage run --source='.' manage.py test
   ```

2. Check .coverage file exists:
   ```bash
   ls -la .coverage
   ```

3. Verify source path is correct

---

### Issue: Wrong Files Covered

**Symptom:**
Coverage includes site-packages or wrong directories

**Solutions:**
1. Specify source explicitly:
   ```bash
   uv run coverage run --source='ores,components,blocks' manage.py test
   ```

2. Check pyproject.toml configuration:
   ```toml
   [tool.coverage.run]
   source = ["app"]
   ```

---

### Issue: HTML Report Not Generating

**Symptom:**
```
No data to report.
```

**Solutions:**
1. Run coverage first:
   ```bash
   uv run coverage run --source='.' manage.py test
   uv run coverage html
   ```

2. Check output directory:
   ```bash
   ls -la htmlcov/
   ```

---

## Coverage Metrics and Reports

### Coverage History Tracking

Track coverage over time:

```bash
# Save coverage report with timestamp
cd app
uv run coverage report > ../docs/testValidation/coverage_$(date +%Y%m%d).txt

# Create coverage trend report
echo "Date,Coverage" > coverage_trend.csv
for file in docs/testValidation/coverage_*.txt; do
    date=$(basename $file .txt | cut -d_ -f2)
    coverage=$(grep "TOTAL" $file | awk '{print $NF}')
    echo "$date,$coverage" >> coverage_trend.csv
done
```

### Coverage Dashboard

Create simple dashboard:

```python
# generate_coverage_dashboard.py
import json
from pathlib import Path

coverage_file = Path('app/.coverage')
if coverage_file.exists():
    # Generate dashboard HTML
    html = """
    <html>
    <head><title>Coverage Dashboard</title></head>
    <body>
        <h1>Coverage Dashboard</h1>
        <h2>Overall: 94%</h2>
        <ul>
            <li>Models: 98%</li>
            <li>Views: 92%</li>
            <li>Forms: 90%</li>
        </ul>
    </body>
    </html>
    """
    Path('coverage_dashboard.html').write_text(html)
```

---

## Resources

### Internal Documentation

- [Automated Testing Overview](./automated-testing-overview.md)
- [Unit Testing Guide](./automated-testing-unit-tests.md)
- [Integration Testing Guide](./automated-testing-integration-tests.md)

### External Resources

- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Codecov Documentation](https://docs.codecov.io/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)

---

## Summary

### Quick Reference

```bash
# Run tests with coverage
cd app
uv run coverage run --source='.' manage.py test

# View terminal report
uv run coverage report

# View detailed report
uv run coverage report -m

# Generate HTML report
uv run coverage html
open htmlcov/index.html

# Check threshold
uv run coverage report --fail-under=90
```

### Coverage Goals

- Overall: >90%
- Models: >95%
- Views: >90%
- Forms: >90%
- Critical paths: 100%

---

**Document Owner:** Development & QA Team  
**Last Updated:** January 30, 2026  
**Next Review:** April 30, 2026
