# Utility Scripts

This directory contains utility scripts for the SE2 Calculator project.

## Available Utilities

### generate_django_secret.py

**Description:** Generate a secure Django SECRET_KEY safe for .env files and Docker Compose.

**Usage:**
```bash
uv run python scripts/utils/generate_django_secret.py
```

**Output:** Generates a 50-character secret key using only safe characters (alphanumeric + `-_+.~`) and updates the SECRET_KEY in your .env file.

**Features:**
- No problematic special characters (avoids `$`, `!`, `` ` ``, etc.)
- Cryptographically secure (uses Python's `secrets` module)
- 301 bits of entropy (exceeds AES-256 security)
- No Django dependency required

**See:** [README_SECRET_GENERATION.md](./README_SECRET_GENERATION.md) for detailed documentation.

### generate_fixture_uuids.py

**Description:** Generate UUIDv7 values for fixture files.

**Usage:**
```bash
uv run python scripts/utils/generate_fixture_uuids.py
```

**Purpose:** Creates properly formatted UUIDv7 identifiers for use in JSON fixture files.

### generate_postgres_password.py

**Description:** Generate a secure PostgreSQL password safe for .env files and Docker Compose.

**Usage:**
```bash
uv run python scripts/utils/generate_postgres_password.py
```

**Output:** Generates a 24-character password using only safe characters (alphanumeric + `-_+.~`) and updates the DB_PASSWORD in your .env file.

**Features:**
- No problematic special characters (avoids `$`, `!`, `` ` ``, etc.)
- Cryptographically secure (uses Python's `secrets` module)
- 144 bits of entropy (exceeds security recommendations)

**See:** [README_SECRET_GENERATION.md](./README_SECRET_GENERATION.md) for detailed documentation.

### secrets_gen.py

**Description:** Convenience script that generates both Django SECRET_KEY and PostgreSQL DB_PASSWORD.

**Usage:**
```bash
uv run python scripts/utils/secrets_gen.py
```

**Purpose:** Runs both `generate_django_secret.py` and `generate_postgres_password.py` to set up all required secrets in one command.

**Recommended for:**
- Initial project setup
- Environment configuration
- Secret rotation

**See:** [README_SECRET_GENERATION.md](./README_SECRET_GENERATION.md) for detailed documentation.

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
# Copy .env.example to .env
cp .env.example .env

# Generate all secrets (Django SECRET_KEY + PostgreSQL DB_PASSWORD)
uv run python scripts/utils/secrets_gen.py

# Verify no Docker Compose warnings
docker compose config
```

### Regenerate Secrets

```bash
# Regenerate all secrets
uv run python scripts/utils/secrets_gen.py

# Or regenerate individually
uv run python scripts/utils/generate_django_secret.py
uv run python scripts/utils/generate_postgres_password.py
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

- [Secret Generation Details](./README_SECRET_GENERATION.md) - Comprehensive guide to secret generation
- [Main Scripts README](../README.md)
- [Test Scripts](../tests/README.md)
- [Integration Tests](../tests/integration/README.md)

## Troubleshooting

### Docker Compose Warning: "The 'variable_name' variable is not set"

**Cause:** Secret contains `$` character which Docker interprets as variable substitution.

**Solution:** Regenerate secrets using updated scripts:
```bash
uv run python scripts/utils/secrets_gen.py
```

See [README_SECRET_GENERATION.md](./README_SECRET_GENERATION.md) for more details.
