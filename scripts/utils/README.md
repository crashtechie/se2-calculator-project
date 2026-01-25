# Utility Scripts

This directory contains utility scripts for the SE2 Calculator project.

## Available Utilities

### generate_django_secret.py

**Description:** Generate a secure Django SECRET_KEY for use in settings.

**Usage:**
```bash
uv run python scripts/utils/generate_django_secret.py
```

**Output:** Prints a secure random string suitable for Django's SECRET_KEY setting.

### generate_fixture_uuids.py

**Description:** Generate UUIDv7 values for fixture files.

**Usage:**
```bash
uv run python scripts/utils/generate_fixture_uuids.py
```

**Purpose:** Creates properly formatted UUIDv7 identifiers for use in JSON fixture files.

### generate_postgres_password.py

**Description:** Generate a secure PostgreSQL password.

**Usage:**
```bash
uv run python scripts/utils/generate_postgres_password.py
```

**Output:** Prints a secure random password suitable for PostgreSQL authentication.

### secrets_gen.py

**Description:** General secret generation utility for various purposes.

**Usage:**
```bash
uv run python scripts/utils/secrets_gen.py
```

**Purpose:** Generates secure random values for configuration and setup.

### verify_fixtures.py

**Description:** Validate fixture files for integrity and relationships.

**Usage:**
```bash
uv run python scripts/utils/verify_fixtures.py
```

**Validation Includes:**
- JSON syntax validation
- UUID format verification (UUIDv7)
- Uniqueness checks
- Relationship integrity (foreign key references)
- Minimum count requirements

## Utility Organization

```
utils/
├── generate_django_secret.py
├── generate_fixture_uuids.py
├── generate_postgres_password.py
├── secrets_gen.py
├── verify_fixtures.py
└── README.md              # This file
```

## Quick Reference

| Script | Purpose | Output |
|--------|---------|--------|
| generate_django_secret.py | Django SECRET_KEY | Random secure string |
| generate_fixture_uuids.py | Fixture UUID generation | UUIDv7 values |
| generate_postgres_password.py | PostgreSQL password | Random secure password |
| secrets_gen.py | General secret generation | Secure random value |
| verify_fixtures.py | Fixture validation | Validation report |

## Common Tasks

### Setup New Environment

```bash
# Generate Django secret
SECRET=$(uv run python scripts/utils/generate_django_secret.py)
echo "SECRET_KEY=$SECRET" >> .env

# Generate PostgreSQL password
DB_PASS=$(uv run python scripts/utils/generate_postgres_password.py)
echo "DB_PASSWORD=$DB_PASS" >> .env
```

### Validate Fixtures Before Deployment

```bash
uv run python scripts/utils/verify_fixtures.py
```

### Generate Fixture Data

```bash
uv run python scripts/utils/generate_fixture_uuids.py
```

## Exit Codes

Most utilities return:
- **0**: Success
- **1**: Failure

## Integration with Setup Process

These utilities are typically used during:
1. Initial project setup
2. Docker image building
3. CI/CD pipeline configuration
4. Environment configuration
5. Fixture validation

## Documentation

- [Main Scripts README](../README.md)
- [Test Scripts](../tests/README.md)
- [Integration Tests](../tests/integration/README.md)
