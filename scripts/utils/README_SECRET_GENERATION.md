# Secret Generation Scripts - Documentation

**Last Updated:** 2026-02-02  
**Purpose:** Generate secure secrets safe for use in .env files and Docker Compose

---

## Overview

This directory contains scripts to generate cryptographically secure secrets for the Django application and PostgreSQL database. The scripts have been updated to avoid special characters that cause issues with shell and Docker Compose variable substitution.

---

## Problem Solved

### Original Issue

Django's default `get_random_secret_key()` and some password generators can produce special characters that conflict with:

- **Shell variable substitution**: `$`, `!`, `` ` ``, `\`
- **Docker Compose variable substitution**: `$`
- **YAML parsing**: `:`, `{`, `}`, `[`, `]`, `,`, `&`, `*`, `#`, `?`, `|`, `-`, `<`, `>`, `=`, `!`, `%`, `@`, `` ` ``

**Example Error**:
```
WARN[0000] The "bum_" variable is not set. Defaulting to a blank string.
```

This occurs when a secret contains `$bum_` which Docker interprets as a variable reference.

### Solution

Generate secrets using only **safe characters**:
- Alphanumeric: `A-Z`, `a-z`, `0-9`
- Safe special characters: `-`, `_`, `+`, `.`, `~`

This provides sufficient entropy (62+ character options) while avoiding shell/Docker conflicts.

---

## Scripts

### 1. `generate_django_secret.py`

Generates a Django SECRET_KEY safe for .env files.

**Usage**:
```bash
# From project root
python scripts/utils/generate_django_secret.py

# Or using UV
uv run python scripts/utils/generate_django_secret.py
```

**Output**:
```
New secret key generated and updated in /path/to/.env successfully.
Secret key length: 50 characters
Character set: alphanumeric + safe special characters (-_+.~)
```

**Features**:
- Generates 50-character secret key
- Uses cryptographically secure random generation (`secrets` module)
- Only uses safe characters: `A-Z a-z 0-9 - _ + . ~`
- Updates SECRET_KEY in .env file
- No Django dependency required

### 2. `generate_postgres_password.py`

Generates a PostgreSQL database password safe for .env files.

**Usage**:
```bash
# From project root
python scripts/utils/generate_postgres_password.py

# Or using UV
uv run python scripts/utils/generate_postgres_password.py
```

**Output**:
```
New Postgres password generated and updated in /path/to/.env successfully.
Password length: 24 characters
Character set: alphanumeric + safe special characters (-_+.~)
```

**Features**:
- Generates 24-character password
- Uses cryptographically secure random generation (`secrets` module)
- Only uses safe characters: `A-Z a-z 0-9 - _ + . ~`
- Updates DB_PASSWORD in .env file

### 3. `secrets_gen.py`

Convenience script that runs both generators.

**Usage**:
```bash
# From project root
python scripts/utils/secrets_gen.py

# Or using UV
uv run python scripts/utils/secrets_gen.py
```

**What it does**:
1. Generates new Django SECRET_KEY
2. Generates new PostgreSQL DB_PASSWORD
3. Updates both in .env file

---

## Security Considerations

### Entropy Analysis

**Character Set Size**: 62 characters (26 uppercase + 26 lowercase + 10 digits)
- With safe special characters: 67 characters (62 + 5 special chars: `-_+.~`)

**Entropy Calculation**:
- 50-character secret key: log₂(67⁵⁰) ≈ 301 bits of entropy
- 24-character password: log₂(67²⁴) ≈ 144 bits of entropy

**Security Level**:
- 301 bits: Exceeds all current security standards (AES-256 is 256 bits)
- 144 bits: Exceeds recommended minimum for passwords (128 bits)

### Comparison to Django Default

Django's `get_random_secret_key()` uses:
- Character set: 62 characters (alphanumeric) + special characters
- Length: 50 characters
- Entropy: ~300 bits

**Our implementation**:
- Character set: 67 characters (alphanumeric + 5 safe special chars)
- Length: 50 characters (SECRET_KEY), 24 characters (password)
- Entropy: ~301 bits (SECRET_KEY), ~144 bits (password)

**Conclusion**: Our implementation provides equivalent or better security while avoiding shell/Docker conflicts.

---

## Character Set Details

### Included Characters (67 total)

```python
# Uppercase letters (26)
ABCDEFGHIJKLMNOPQRSTUVWXYZ

# Lowercase letters (26)
abcdefghijklmnopqrstuvwxyz

# Digits (10)
0123456789

# Safe special characters (5)
- _ + . ~
```

### Excluded Characters

**Shell/Docker problematic**:
- `$` - Variable substitution
- `!` - History expansion (bash)
- `` ` `` - Command substitution
- `\` - Escape character

**YAML problematic**:
- `:` - Key-value separator
- `{` `}` - Flow mapping
- `[` `]` - Flow sequence
- `,` - Flow separator
- `&` - Anchor
- `*` - Alias
- `#` - Comment
- `?` - Key indicator
- `|` - Literal block scalar
- `>` - Folded block scalar
- `=` - Can cause issues in some contexts
- `%` - Can cause issues in some contexts
- `@` - Can cause issues in some contexts

---

## Usage Examples

### Initial Setup

```bash
# 1. Copy .env.example to .env
cp .env.example .env

# 2. Generate all secrets
uv run python scripts/utils/secrets_gen.py
```

### Regenerate Secrets

```bash
# Regenerate both secrets
uv run python scripts/utils/secrets_gen.py

# Or regenerate individually
uv run python scripts/utils/generate_django_secret.py
uv run python scripts/utils/generate_postgres_password.py
```

### Verify No Docker Warnings

```bash
# Check Docker Compose configuration
docker compose config

# Should show no warnings about undefined variables
```

---

## Testing

### Test Secret Generation

```python
# Test the safe secret key generator
from scripts.utils.generate_django_secret import generate_safe_secret_key

# Generate a test key
test_key = generate_safe_secret_key(50)
print(f"Length: {len(test_key)}")
print(f"Key: {test_key}")

# Verify no problematic characters
problematic = ['$', '!', '`', '\\', ':', '{', '}', '[', ']', ',', '&', '*', '#', '?', '|', '<', '>', '=', '%', '@']
has_problematic = any(char in test_key for char in problematic)
print(f"Has problematic chars: {has_problematic}")  # Should be False
```

### Test Password Generation

```python
# Test the safe password generator
from scripts.utils.generate_postgres_password import generate_safe_password

# Generate a test password
test_password = generate_safe_password(24)
print(f"Length: {len(test_password)}")
print(f"Password: {test_password}")

# Verify no problematic characters
problematic = ['$', '!', '`', '\\', ':', '{', '}', '[', ']', ',', '&', '*', '#', '?', '|', '<', '>', '=', '%', '@']
has_problematic = any(char in test_password for char in problematic)
print(f"Has problematic chars: {has_problematic}")  # Should be False
```

---

## Troubleshooting

### Issue: "The 'variable_name' variable is not set"

**Cause**: Secret contains `$` character which Docker interprets as variable substitution.

**Solution**: Regenerate secrets using the updated scripts:
```bash
uv run python scripts/utils/secrets_gen.py
```

### Issue: Script says ".env file not found"

**Cause**: .env file doesn't exist in project root.

**Solution**: Copy from example:
```bash
cp .env.example .env
uv run python scripts/utils/secrets_gen.py
```

### Issue: Permission denied

**Cause**: .env file is read-only or insufficient permissions.

**Solution**: Make .env writable:
```bash
chmod 644 .env
uv run python scripts/utils/secrets_gen.py
```

---

## Best Practices

1. **Always regenerate secrets** when:
   - Setting up a new environment
   - Secrets may have been compromised
   - Moving from development to production

2. **Never commit .env** to version control:
   - .env is in .gitignore
   - Only commit .env.example

3. **Use different secrets** for different environments:
   - Development: Generate once, can be shared in team
   - Staging: Different secrets from development
   - Production: Unique secrets, never shared

4. **Rotate secrets periodically**:
   - Production: Every 90 days recommended
   - Development: When team members change

5. **Backup secrets securely**:
   - Use password manager for production secrets
   - Never store in plain text files
   - Never send via email or chat

---

## Migration Guide

### From Old Secret Generation

If you have existing secrets with problematic characters:

```bash
# 1. Backup current .env
cp .env .env.backup

# 2. Regenerate secrets
uv run python scripts/utils/secrets_gen.py

# 3. Verify Docker Compose works
docker compose config

# 4. Test application
docker compose up -d
docker compose exec web python manage.py check

# 5. If everything works, remove backup
rm .env.backup
```

### From Django's get_random_secret_key()

The new implementation is a drop-in replacement:

**Before**:
```python
from django.core.management.utils import get_random_secret_key
secret = get_random_secret_key()
```

**After**:
```python
from scripts.utils.generate_django_secret import generate_safe_secret_key
secret = generate_safe_secret_key()
```

---

## References

- **Python secrets module**: https://docs.python.org/3/library/secrets.html
- **Django SECRET_KEY**: https://docs.djangoproject.com/en/stable/ref/settings/#secret-key
- **Docker Compose variable substitution**: https://docs.docker.com/compose/environment-variables/
- **OWASP Password Guidelines**: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

---

## Changelog

### 2026-02-02 - Version 2.0
- **BREAKING**: Removed Django dependency from generate_django_secret.py
- **BREAKING**: Changed character set to exclude problematic special characters
- Added `generate_safe_secret_key()` function with custom implementation
- Added `generate_safe_password()` function for consistency
- Increased password length from 16 to 24 characters
- Added detailed output showing character set and length
- Added comprehensive documentation

### Previous - Version 1.0
- Initial implementation using Django's get_random_secret_key()
- Used secrets.token_urlsafe() for passwords

---

**Maintained By:** Development Team  
**Questions?** Open an issue on GitHub
