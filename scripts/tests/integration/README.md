# Integration Tests for Ores Module

Comprehensive integration test suite for the ores views and templates CRUD workflow.

## Quick Start

```bash
# Run integration tests
uv run python scripts/tests/integration/run_integration_tests.py
```

## Features

- **Automated Testing**: Runs all 7 CRUD tests with error handling
- **Detailed Validation**: Checks status codes, data integrity, and content
- **Result Logging**: Saves results to JSON file with timestamp
- **Pass/Fail Tracking**: Clear indicators for each test step
- **Error Reporting**: Helpful troubleshooting tips on failure
- **Pre-test Cleanup**: Removes test data from previous runs
- **Environment Info**: Captures Django version, Python version, database

## Usage

```bash
# Basic usage
uv run python scripts/tests/integration/run_integration_tests.py

# The script will:
# 1. Clean up any previous test data
# 2. Run all 7 tests
# 3. Display results in terminal
# 4. Save results to ores/testResults/integration_test_results_<timestamp>.json
```

## Exit Codes

- **0**: All tests passed
- **1**: One or more tests failed

This allows the script to be used in CI/CD pipelines:

```bash
# Run tests
uv run python scripts/tests/integration/run_integration_tests.py

# Check result
if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Tests failed!"
    exit 1
fi
```

## Tests Performed

1. **Create Ore**: POST request to create a new ore via view
2. **Read Detail**: GET request to view ore detail page
3. **Update Ore**: POST request to update ore data
4. **Read List**: GET request to view ore list page
5. **Delete Ore**: POST request to delete ore via view
6. **Verify Deletion**: Check database to confirm deletion
7. **Verify List Updated**: Confirm deleted ore removed from list

## Expected Output (Success)

```
======================================================================
CRUD Integration Test - Ores Module
======================================================================

[PRE-TEST] Cleaning up test data...
✓ Removed 0 test ore(s)

[TEST 1] Creating ore via view...
✓ PASS: Create Ore
  └─ ID: 019bf683-db89-7142-8bca-fdfd0a944796, Mass: 999.99
[TEST 2] Reading ore detail page...
✓ PASS: Read Detail
  └─ Status: 200, Content verified
[TEST 3] Updating ore via view...
✓ PASS: Update Ore
  └─ Name: Integration Test Ore Updated, Mass: 1111.11
[TEST 4] Reading ore list page...
✓ PASS: Read List
  └─ Status: 200, Content verified
[TEST 5] Deleting ore via view...
✓ PASS: Delete Ore
  └─ Ore successfully removed from database
[TEST 6] Verifying deletion in database...
✓ PASS: Verify Deletion
  └─ No ore record found in database
[TEST 7] Verifying ore removed from list...
✓ PASS: Verify List Updated
  └─ Deleted ore no longer in list

======================================================================
TEST SUMMARY
======================================================================
Total Tests:  7
Passed:       7
Failed:       0
Pass Rate:    100.0%

✓ All integration tests passed successfully!
======================================================================

✓ Test results saved to: ores/testResults/integration_test_results_20260125_185635.json
```

## Viewing Results

All test results are saved in `scripts/tests/testResults/` directory:

```bash
# List all test results
ls -lah scripts/tests/testResults/

# View latest results (human-readable)
python -m json.tool scripts/tests/testResults/integration_test_results_*.json | tail -60

# View specific results
cat scripts/tests/testResults/integration_test_results_20260125_185635.json

# Get summary from results
python -c "
import json
import glob
from pathlib import Path
result = json.loads(Path(sorted(glob.glob('scripts/tests/testResults/*.json'))[-1]).read_text())
print(f\"Pass Rate: {(result['summary']['passed'] / result['summary']['total']) * 100:.1f}%\")
print(f\"Passed: {result['summary']['passed']}/{result['summary']['total']}\")
"
```

## Prerequisites

- Django 6.0.1+
- Python 3.13+
- UV package manager
- Ores app installed and migrations applied
- URLs configured in `ores/urls.py`
- Views implemented in `ores/views.py`

## Environment Setup

The script automatically:
1. Adds project root to Python path
2. Configures Django settings
3. Adds 'testserver' to ALLOWED_HOSTS for testing
4. Cleans up test data before and after runs

No additional configuration needed!

## Troubleshooting

**Issue: `DisallowedHost: Invalid HTTP_HOST header: 'testserver'`**
- Solution: Script automatically adds 'testserver' to ALLOWED_HOSTS. If error persists, check `se2CalcProject/settings.py`

**Issue: `ModuleNotFoundError: No module named 'ores'`**
- Solution: Ensure ores app is installed in `INSTALLED_APPS` in settings.py

**Issue: Tests fail with 400/500 status codes**
- Solution: Check form validation by examining response content
- Add debugging: `response = client.post(...); print(response.content)` in shell

**Issue: URLs not found**
- Solution: Verify `ores/urls.py` exists and contains all CRUD routes:
  - `ore_list` → `OreListView`
  - `ore_detail` → `OreDetailView`
  - `ore_create` → `OreCreateView`
  - `ore_update` → `OreUpdateView`
  - `ore_delete` → `OreDeleteView`

## CI/CD Integration

**GitHub Actions Example:**
```yaml
- name: Run Integration Tests
  run: |
    uv run python scripts/tests/integration/run_integration_tests.py
  
- name: Upload Results
  uses: actions/upload-artifact@v3
  if: always()
  with:
    name: integration-test-results
    path: scripts/tests/testResults/
```

**GitLab CI Example:**
```yaml
integration_tests:
  script:
    - uv run python scripts/tests/integration/run_integration_tests.py
  artifacts:
    paths:
      - scripts/tests/testResults/
    expire_in: 30 days
    when: always
```

## Maintenance

- Test data is automatically cleaned up before and after each run
- Results files persist for documentation/audit purposes
- Old results files can be safely deleted to free space

## Related Documentation

- [ENH-0000005 Deployment Guide](../../../../docs/enhancementRequests/Phase2_views/ENH0000005/ENH-0000005-deployment-guide.md)
- [Ores App Structure](../../../../ores/)
- [Testing Best Practices](../../../../docs/projectPlan/phase4_testing.md)
