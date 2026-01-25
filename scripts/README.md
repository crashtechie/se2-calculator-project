# Scripts Directory

This directory contains utility scripts and test scripts for the SE2 Calculator project.

## Directory Structure

```
scripts/
├── README.md
├── tests/
│   ├── README.md
│   ├── testResults/                    # Test result files (JSON)
│   │   └── integration_test_results_<timestamp>.json
│   └── integration/
│       ├── README.md
│       └── run_integration_tests.py
└── utils/
    ├── README.md
    ├── generate_django_secret.py
    ├── generate_fixture_uuids.py
    ├── generate_postgres_password.py
    ├── secrets_gen.py
    └── verify_fixtures.py
```

## Available Scripts

### Test Scripts

- **Integration Tests**: `scripts/tests/integration/run_integration_tests.py`
  - Runs CRUD workflow tests for the ores module
  - Saves results to `scripts/tests/testResults/`
  - Usage: `uv run python scripts/tests/integration/run_integration_tests.py`

See [scripts/tests/README.md](tests/README.md) for more test details.

### Utility Scripts

Located in `scripts/utils/`:

- **generate_django_secret.py**: Generate a secure Django SECRET_KEY
- **generate_fixture_uuids.py**: Generate UUIDv7 values for fixture files
- **generate_postgres_password.py**: Generate PostgreSQL password
- **secrets_gen.py**: General secret generation utility
- **verify_fixtures.py**: Validate fixture files for integrity

Usage:
```bash
# Generate Django secret
uv run python scripts/utils/generate_django_secret.py

# Generate fixture UUIDs
uv run python scripts/utils/generate_fixture_uuids.py

# Generate PostgreSQL password
uv run python scripts/utils/generate_postgres_password.py

# Verify fixtures
uv run python scripts/utils/verify_fixtures.py
```

See [scripts/utils/README.md](utils/README.md) for more utility details.

## Quick Start

```bash
# Run integration tests
uv run python scripts/tests/integration/run_integration_tests.py

# Generate Django secret
uv run python scripts/utils/generate_django_secret.py

# Verify fixtures
uv run python scripts/utils/verify_fixtures.py
```

## Exit Codes

Most scripts return:
- **0**: Success
- **1**: Failure

This allows them to be used in CI/CD pipelines.

## Adding New Scripts

When adding new scripts:

1. Choose the appropriate category:
   - **tests/**: Test and validation scripts
   - **utils/**: Utility and generation scripts

2. Create a subdirectory for related scripts (e.g., `tests/unit/`)

3. Include a docstring with usage instructions

4. Update the relevant README.md file

## CI/CD Integration

These scripts can be integrated into CI/CD pipelines:

**GitHub Actions:**
```yaml
- name: Run Integration Tests
  run: uv run python scripts/tests/integration/run_integration_tests.py
```

**GitLab CI:**
```yaml
integration_tests:
  script:
    - uv run python scripts/tests/integration/run_integration_tests.py
```

## Documentation

- [Test Scripts](tests/README.md)
- [Utility Scripts](utils/README.md)
- [Integration Test Details](tests/integration/README.md)
