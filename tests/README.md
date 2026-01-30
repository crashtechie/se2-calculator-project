# Test Scripts

This directory contains test scripts for the SE2 Calculator project.

## Available Test Suites

### Integration Tests

**Location:** `scripts/tests/integration/`

**Description:** Comprehensive integration tests for the ores module CRUD workflow.

**Usage:**
```bash
uv run python scripts/tests/integration/run_integration_tests.py
```

**Tests Included:**
- Create ore via view
- Read ore detail page
- Update ore data
- Read ore list page
- Delete ore via view
- Verify deletion in database
- Verify deletion in list view

**Results:** Test results are saved to `ores/testResults/integration_test_results_<timestamp>.json`

**Exit Code:** 
- 0 = All tests passed
- 1 = One or more tests failed

See [Integration Test README](integration/README.md) for detailed documentation.

## Test Organization

```
tests/
├── integration/           # Integration tests
│   ├── run_integration_tests.py
│   └── README.md
└── README.md            # This file
```

## Future Test Types

As the project grows, additional test categories can be added:

- `unit/` - Unit tests for specific components
- `e2e/` - End-to-end tests for complete workflows
- `performance/` - Performance and load tests
- `fixtures/` - Fixture validation and generation
- `api/` - API endpoint tests

## Running Tests

### All Integration Tests
```bash
uv run python scripts/tests/integration/run_integration_tests.py
```

### With Exit Code Check
```bash
uv run python scripts/tests/integration/run_integration_tests.py && echo "Tests passed!" || echo "Tests failed!"
```

### Capturing Output
```bash
uv run python scripts/tests/integration/run_integration_tests.py | tee test_output.log
```

## Viewing Results

Integration test results are stored in JSON format:

```bash
# View latest results
python -m json.tool scripts/tests/testResults/integration_test_results_*.json | tail -60

# Get pass rate
python -c "
import json
import glob
from pathlib import Path
result = json.loads(Path(sorted(glob.glob('scripts/tests/testResults/*.json'))[-1]).read_text())
print(f\"Pass Rate: {(result['summary']['passed'] / result['summary']['total']) * 100:.1f}%\")
"
```

## Prerequisites

- Python 3.13+
- Django 6.0.1+
- UV package manager
- All dependencies from `pyproject.toml`

## CI/CD Integration

### GitHub Actions
```yaml
- name: Run Integration Tests
  run: uv run python scripts/tests/integration/run_integration_tests.py
  
- name: Upload Test Results
  uses: actions/upload-artifact@v3
  if: always()
  with:
    name: test-results
    path: scripts/tests/testResults/
```

### GitLab CI
```yaml
integration_tests:
  script:
    - uv run python scripts/tests/integration/run_integration_tests.py
  artifacts:
    paths:
      - ores/testResults/
    expire_in: 30 days
    when: always
```

## Documentation

- [Main Scripts README](../README.md)
- [Integration Test Details](integration/README.md)
- [Utility Scripts](../utils/README.md)
