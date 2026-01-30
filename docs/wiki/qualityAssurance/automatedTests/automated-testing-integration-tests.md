# Automated Testing: Integration Tests

**Project:** SE2 Calculator Project  
**Document Type:** Quality Assurance - Integration Testing Guide  
**Last Updated:** January 30, 2026  
**Status:** Active  

---

## Purpose

This document provides comprehensive guidance for running and understanding integration tests in the SE2 Calculator Project. Integration tests verify that multiple components work together correctly in complete workflows.

---

## Integration Testing Overview

### What is Integration Testing?

Integration tests verify that different parts of the application work together:
- Views interact correctly with models
- Forms properly save data to database
- Templates render with real data
- Complete CRUD workflows function end-to-end
- Multiple apps interact correctly

### Integration vs Unit Tests

| Aspect | Unit Tests | Integration Tests |
|--------|-----------|-------------------|
| Scope | Single component | Multiple components |
| Speed | Very fast (<1ms) | Fast (10-100ms) |
| Database | Optional | Required |
| External deps | Mocked | Real (test versions) |
| Purpose | Component correctness | Workflow verification |
| Quantity | Many (200+) | Fewer (15-30) |

---

## Integration Test Suite

### Available Test Suites

#### 1. Ores CRUD Integration Tests

**Location:** `tests/integration/run_integration_tests.py`

**Purpose:** Verify complete CRUD workflow for ores module

**Tests Performed:**
1. Create ore via view (POST to create endpoint)
2. Read ore detail page (GET ore detail)
3. Update ore data (POST to update endpoint)
4. Read ore list page (GET ore list)
5. Delete ore via view (POST to delete endpoint)
6. Verify deletion in database (query database)
7. Verify deletion in list view (check list doesn't contain ore)

**Total Tests:** 7

**Execution Time:** ~1 second

---

## Running Integration Tests

### Quick Start

```bash
# Navigate to project root
cd /home/dsmi001/app/se2-calculator-project

# Run integration tests
uv run python tests/integration/run_integration_tests.py
```

### Expected Output (Success)

```
======================================================================
Running Integration Tests for Ores Module
======================================================================

Environment:
  - Django: 6.0.1
  - Python: 3.13.7
  - Database: PostgreSQL
  - Test Database: test_se2_calculator_db

======================================================================
Running Tests...
======================================================================

✓ Test 1: Create ore via view
  └─ Status: 302 (redirect)
  └─ Ore ID: 01947c3e-7890-7abc-def0-123456789abc

✓ Test 2: Read ore detail page
  └─ Status: 200
  └─ Contains: Integration Test Ore

✓ Test 3: Update ore data
  └─ Status: 302 (redirect)
  └─ Mass updated: 75.5

✓ Test 4: Read ore list page
  └─ Status: 200
  └─ Contains updated ore

✓ Test 5: Delete ore via view
  └─ Status: 302 (redirect)

✓ Test 6: Verify deletion in database
  └─ Ore does not exist in database

✓ Test 7: Verify deletion in list view
  └─ Ore not in list

======================================================================
Test Summary
======================================================================

Total Tests:  7
Passed:       7
Failed:       0
Pass Rate:    100.0%

✓ All tests passed!

Results saved to:
  tests/testResults/integration_test_results_20260130_143022.json

======================================================================
```

### Expected Output (Failure)

```
======================================================================
Running Integration Tests for Ores Module
======================================================================

Environment:
  - Django: 6.0.1
  - Python: 3.13.7
  - Database: PostgreSQL
  - Test Database: test_se2_calculator_db

======================================================================
Running Tests...
======================================================================

✓ Test 1: Create ore via view
  └─ Status: 302 (redirect)

✗ Test 2: Read ore detail page
  └─ Status: 404 (expected 200)
  └─ ERROR: Detail view not found

✗ Test 3: Update ore data
  └─ Skipped due to previous failure

... (remaining tests skipped)

======================================================================
Test Summary
======================================================================

Total Tests:  7
Passed:       1
Failed:       1
Skipped:      5
Pass Rate:    14.3%

✗ 1 test(s) failed. Please review the errors above.

Troubleshooting Tips:
  1. Ensure the ores app is installed and migrations applied
  2. Check that URLs are configured in ores/urls.py
  3. Verify views are correctly implemented in ores/views.py
  4. Check form validation: add print(response.content)
  5. Review Django logs for detailed error messages

======================================================================
```

---

## Test Results

### Result File Location

Integration test results are saved to:
```
tests/testResults/integration_test_results_<timestamp>.json
```

Example:
```
tests/testResults/integration_test_results_20260130_143022.json
```

### Result File Format

```json
{
  "timestamp": "2026-01-30T14:30:22.123456",
  "environment": {
    "django_version": "6.0.1",
    "python_version": "3.13.7",
    "database": "PostgreSQL",
    "test_database": "test_se2_calculator_db"
  },
  "summary": {
    "total": 7,
    "passed": 7,
    "failed": 0,
    "pass_rate": 100.0
  },
  "tests": [
    {
      "number": 1,
      "name": "Create ore via view",
      "passed": true,
      "duration": 0.123,
      "details": {
        "status_code": 302,
        "ore_id": "01947c3e-7890-7abc-def0-123456789abc"
      }
    },
    {
      "number": 2,
      "name": "Read ore detail page",
      "passed": true,
      "duration": 0.045,
      "details": {
        "status_code": 200,
        "content_check": "passed"
      }
    }
    // ... more tests
  ]
}
```

### Viewing Results

```bash
# List all result files
ls -lah tests/testResults/

# View latest results (pretty-printed)
python -m json.tool tests/testResults/integration_test_results_*.json | tail -100

# Get quick summary
python -c "
import json
import glob
from pathlib import Path
result_file = sorted(glob.glob('tests/testResults/integration_test_results_*.json'))[-1]
result = json.loads(Path(result_file).read_text())
print(f\"Test Results: {result['summary']['passed']}/{result['summary']['total']} passed\")
print(f\"Pass Rate: {result['summary']['pass_rate']}%\")
print(f\"Timestamp: {result['timestamp']}\")
"

# View specific test result
cat tests/testResults/integration_test_results_20260130_143022.json
```

---

## Integration Test Details

### Test 1: Create Ore via View

**Purpose:** Verify ore creation through web interface

**Request:**
- Method: POST
- URL: `/ores/create/`
- Data: `{'name': 'Integration Test Ore', 'mass': 50.0, 'description': 'Test ore'}`

**Validation:**
- Status code: 302 (redirect after successful creation)
- Ore created in database
- Ore ID generated (UUIDv7)
- Timestamps created

**Failure Scenarios:**
- Status 200 (form errors, data not saved)
- Status 404 (URL not configured)
- Status 500 (server error)

---

### Test 2: Read Ore Detail Page

**Purpose:** Verify ore detail view displays correctly

**Request:**
- Method: GET
- URL: `/ores/<ore_id>/`

**Validation:**
- Status code: 200
- Response contains ore name
- Response contains ore mass
- Response contains ore description

**Failure Scenarios:**
- Status 404 (view not found or ore doesn't exist)
- Status 500 (template error)
- Content missing expected data

---

### Test 3: Update Ore Data

**Purpose:** Verify ore can be updated through web interface

**Request:**
- Method: POST
- URL: `/ores/<ore_id>/update/`
- Data: `{'name': 'Updated Ore', 'mass': 75.5, 'description': 'Updated'}`

**Validation:**
- Status code: 302 (redirect after update)
- Database reflects changes
- updated_at timestamp changed
- created_at timestamp unchanged

**Failure Scenarios:**
- Status 200 (validation errors)
- Status 404 (URL or ore not found)
- Data not saved to database

---

### Test 4: Read Ore List Page

**Purpose:** Verify ore list displays all ores

**Request:**
- Method: GET
- URL: `/ores/`

**Validation:**
- Status code: 200
- Response contains updated ore
- List view renders correctly

**Failure Scenarios:**
- Status 404 (URL not configured)
- Updated ore not in list
- Template errors

---

### Test 5: Delete Ore via View

**Purpose:** Verify ore deletion through web interface

**Request:**
- Method: POST
- URL: `/ores/<ore_id>/delete/`

**Validation:**
- Status code: 302 (redirect after deletion)
- Ore removed from database

**Failure Scenarios:**
- Status 404 (URL or ore not found)
- Ore still exists in database
- Cascade deletion issues

---

### Test 6: Verify Deletion in Database

**Purpose:** Confirm ore was deleted from database

**Validation:**
- Database query returns 0 objects
- Ore ID no longer exists

**Failure Scenarios:**
- Ore still exists in database
- Soft delete instead of hard delete

---

### Test 7: Verify Deletion in List View

**Purpose:** Confirm deleted ore doesn't appear in UI

**Request:**
- Method: GET
- URL: `/ores/`

**Validation:**
- Deleted ore not in response content
- List view doesn't show deleted ore

**Failure Scenarios:**
- Deleted ore still visible in list
- List view shows stale data

---

## Integration Test Implementation

### Test Runner Architecture

```python
class IntegrationTestRunner:
    """Run integration tests for ores module."""
    
    def __init__(self):
        """Initialize test runner."""
        self.client = Client()
        self.results = {
            'passed': [],
            'failed': [],
            'summary': {}
        }
        self.test_ore_id = None
    
    def run_all_tests(self):
        """Run all integration tests."""
        self.test_create_ore()
        self.test_read_ore_detail()
        self.test_update_ore()
        self.test_read_ore_list()
        self.test_delete_ore()
        self.test_verify_deletion_db()
        self.test_verify_deletion_list()
    
    def test_create_ore(self):
        """Test creating ore via view."""
        data = {
            'name': 'Integration Test Ore',
            'mass': 50.0,
            'description': 'Test ore for integration testing'
        }
        
        response = self.client.post(
            reverse('ores:ore_create'),
            data=data
        )
        
        # Validate response
        if response.status_code == 302:
            # Extract ore_id from redirect URL
            self.test_ore_id = extract_ore_id(response.url)
            self.mark_test_passed(1, "Create ore via view")
        else:
            self.mark_test_failed(1, "Create ore via view", 
                                 f"Expected 302, got {response.status_code}")
```

### Test Cleanup

Integration tests automatically clean up:

**Before Tests:**
```python
def cleanup_previous_test_data(self):
    """Remove any ores from previous test runs."""
    Ore.objects.filter(name__icontains='Integration Test').delete()
```

**After Tests:**
```python
def tearDown(self):
    """Clean up after all tests."""
    # Test data is already deleted by Test 5
    # Additional cleanup if needed
    pass
```

---

## Writing New Integration Tests

### Integration Test Template

```python
#!/usr/bin/env python
"""
Integration tests for [Module Name].

Tests complete CRUD workflows through Django views.
"""
import os
import sys
import django
from django.test import Client
from django.urls import reverse

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../app'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'se2CalcProject.settings')
django.setup()


class [Module]IntegrationTestRunner:
    """Integration test runner for [module]."""
    
    def __init__(self):
        """Initialize test runner."""
        self.client = Client()
        self.results = []
        self.test_object_id = None
    
    def test_create_via_view(self):
        """Test creating object via view."""
        data = {'field': 'value'}
        response = self.client.post(reverse('app:create'), data=data)
        
        if response.status_code == 302:
            self.test_object_id = self.extract_id(response.url)
            return True
        return False
    
    def test_read_detail(self):
        """Test reading object detail."""
        response = self.client.get(
            reverse('app:detail', args=[self.test_object_id])
        )
        
        return response.status_code == 200
    
    def run(self):
        """Execute all tests."""
        print("Running Integration Tests...")
        
        if self.test_create_via_view():
            print("✓ Create test passed")
        else:
            print("✗ Create test failed")
        
        if self.test_read_detail():
            print("✓ Read test passed")
        else:
            print("✗ Read test failed")


if __name__ == '__main__':
    runner = [Module]IntegrationTestRunner()
    runner.run()
```

---

## Continuous Integration

### CI/CD Integration

**GitHub Actions:**
```yaml
name: Integration Tests

on: [push, pull_request]

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
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
      
      - name: Run migrations
        run: |
          cd app
          uv run python manage.py migrate
      
      - name: Run integration tests
        run: |
          uv run python tests/integration/run_integration_tests.py
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: integration-test-results
          path: tests/testResults/
```

### Exit Codes

Integration tests use standard exit codes:

- **0** - All tests passed
- **1** - One or more tests failed

**Usage in scripts:**
```bash
# Run and check result
uv run python tests/integration/run_integration_tests.py
if [ $? -eq 0 ]; then
    echo "✓ All integration tests passed"
else
    echo "✗ Integration tests failed"
    exit 1
fi
```

---

## Troubleshooting

### Common Issues

#### Issue: URL Not Found (404)

**Symptom:**
```
✗ Test 1: Create ore via view
  └─ Status: 404 (expected 302)
```

**Solutions:**
1. Check URL configuration:
   ```bash
   cd app
   uv run python manage.py show_urls | grep ores
   ```

2. Verify `ores/urls.py` exists and is included in main `urls.py`

3. Check URL names match:
   ```python
   # ores/urls.py
   path('create/', views.OreCreateView.as_view(), name='ore_create')
   ```

---

#### Issue: Form Validation Errors (200 instead of 302)

**Symptom:**
```
✗ Test 1: Create ore via view
  └─ Status: 200 (expected 302)
  └─ Form validation failed
```

**Solutions:**
1. Check form validation in view:
   ```python
   # Add debug output to integration test
   if response.status_code == 200:
       print(f"Form errors: {response.context['form'].errors}")
   ```

2. Verify model field requirements match form data

3. Check for missing CSRF token (handled by test client automatically)

---

#### Issue: Database Connection

**Symptom:**
```
Error: Could not connect to database
```

**Solutions:**
1. Ensure database is running:
   ```bash
   docker-compose up -d database
   ```

2. Check database settings in `.env` file

3. Verify migrations are applied:
   ```bash
   cd app
   uv run python manage.py migrate
   ```

---

#### Issue: Test Data Conflicts

**Symptom:**
```
IntegrityError: duplicate key value violates unique constraint
```

**Solutions:**
1. Run cleanup before tests:
   ```python
   Ore.objects.filter(name__icontains='Integration Test').delete()
   ```

2. Use unique test data:
   ```python
   import uuid
   name = f'Test Ore {uuid.uuid4().hex[:8]}'
   ```

---

## Best Practices

### Integration Test Guidelines

✅ **Test Complete Workflows** - Test full CRUD cycles  
✅ **Use Realistic Data** - Test with data similar to production  
✅ **Clean Up After Tests** - Remove test data  
✅ **Test Happy Path First** - Verify success cases  
✅ **Test Error Handling** - Verify failure cases  
✅ **Keep Tests Independent** - Don't rely on test order  
✅ **Document Test Purpose** - Clear test descriptions  
✅ **Save Test Results** - Keep results for analysis  

### What to Test

✅ Complete CRUD workflows  
✅ Form submission and validation  
✅ Database operations  
✅ View rendering with real data  
✅ URL routing  
✅ Template rendering  
✅ Success and error messages  
✅ Redirects after operations  

### What Not to Test

❌ Individual model methods (use unit tests)  
❌ Form field validation (use unit tests)  
❌ CSS/JavaScript (use E2E tests)  
❌ Performance (use performance tests)  
❌ Security vulnerabilities (use security tests)  

---

## Future Enhancements

### Planned Integration Tests

1. **Components CRUD Integration Tests**
   - Create component with materials
   - Update materials dynamically
   - Delete component and verify cascades

2. **Blocks CRUD Integration Tests**
   - Create block with consumer/producer
   - Verify component relationships
   - Test resource chain display

3. **Cross-App Integration Tests**
   - Create ore → use in component → use in block
   - Test complete resource chain
   - Verify cascading operations

4. **API Integration Tests**
   - Test REST API endpoints
   - Verify JSON responses
   - Test API authentication

---

## Resources

- [Integration Test Script](../../../tests/integration/run_integration_tests.py)
- [Integration Test README](../../../tests/integration/README.md)
- [Django Testing Client](https://docs.djangoproject.com/en/stable/topics/testing/tools/#the-test-client)

---

**Document Owner:** Development & QA Team  
**Last Updated:** January 30, 2026  
**Next Review:** April 30, 2026
