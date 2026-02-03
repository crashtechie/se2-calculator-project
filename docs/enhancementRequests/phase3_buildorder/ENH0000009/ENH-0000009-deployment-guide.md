# ENH-0000009 Deployment Guide

**Enhancement:** Build Order Model & Core Logic  
**Version:** 1.0  
**Date:** 2026-02-02  
**Status:** Ready for Deployment

---

## Overview

This guide provides step-by-step instructions for deploying the BuildOrder model and related functionality to production environments.

---

## Prerequisites

### Required
- ✅ Django 6.0.1 or higher
- ✅ Python 3.13 or higher
- ✅ PostgreSQL 13+ or SQLite 3.35+ (for development)
- ✅ uuid-utils package installed
- ✅ ENH-0000001 (Ores Model) deployed
- ✅ ENH-0000002 (Components Model) deployed
- ✅ ENH-0000003 (Blocks Model) deployed

### Optional
- Redis or Memcached (for production caching)
- Coverage.py (for test verification)

---

## Pre-Deployment Checklist

- [ ] All dependencies deployed (Ores, Components, Blocks)
- [ ] Database backup completed
- [ ] Test environment validated
- [ ] Code review completed
- [ ] All tests passing (52/52)
- [ ] Test coverage verified (≥90%)
- [ ] Documentation reviewed

---

## Deployment Steps

### Step 1: Verify Dependencies

Ensure all prerequisite enhancements are deployed:

```bash
# Check that required apps are in INSTALLED_APPS
cd app
uv run python manage.py shell -c "
from django.conf import settings
required = ['ores', 'components', 'blocks']
installed = [app for app in required if app in settings.INSTALLED_APPS]
print(f'Installed: {installed}')
print(f'Missing: {[app for app in required if app not in installed]}')
"
```

**Expected output:**
```
Installed: ['ores', 'components', 'blocks']
Missing: []
```

---

### Step 2: Update Settings

The buildorders app should already be registered in `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ores',        # ENH-0000001
    'components',  # ENH-0000002
    'blocks',      # ENH-0000003
    'buildorders', # ENH-0000009
]
```

**Verification:**
```bash
uv run python manage.py shell -c "
from django.conf import settings
print('buildorders' in settings.INSTALLED_APPS)
"
```

---

### Step 3: Run Tests

Verify all tests pass before deployment:

```bash
cd app

# Run buildorders tests
uv run pytest buildorders/tests.py -v

# Expected: 52 passed
```

**Verify test coverage:**
```bash
uv run coverage run -m pytest buildorders/tests.py -q
uv run coverage report --include="buildorders/*"

# Expected: ≥90% coverage
```

---

### Step 4: Create Database Migrations

Generate and review migrations:

```bash
cd app

# Create migrations
uv run python manage.py makemigrations buildorders

# Expected output:
# Migrations for 'buildorders':
#   buildorders/migrations/0001_initial.py
#     + Create model BuildOrder
```

**Review the migration file:**
```bash
cat buildorders/migrations/0001_initial.py
```

**Verify migration contents:**
- BuildOrder model with all fields
- UUIDField primary key
- JSONField for blocks
- Indexes on name and created_at
- Correct Meta options

---

### Step 5: Apply Migrations

**Development/Staging:**
```bash
cd app
uv run python manage.py migrate buildorders

# Expected output:
# Operations to perform:
#   Apply all migrations: buildorders
# Running migrations:
#   Applying buildorders.0001_initial... OK
```

**Production:**
```bash
# 1. Backup database first
pg_dump your_database > backup_before_enh0000009.sql

# 2. Apply migration
uv run python manage.py migrate buildorders

# 3. Verify migration
uv run python manage.py showmigrations buildorders
```

---

### Step 6: Verify Model

Test that the model is accessible:

```bash
cd app
uv run python manage.py shell
```

```python
from buildorders.models import BuildOrder
from blocks.models import Block

# Verify model is importable
print(f"BuildOrder model: {BuildOrder}")

# Verify fields
fields = [f.name for f in BuildOrder._meta.get_fields()]
print(f"Fields: {fields}")

# Expected: ['order_id', 'name', 'description', 'blocks', 'created_at', 'updated_at']

# Test basic creation (then delete)
test_order = BuildOrder.objects.create(
    name="Test Order",
    description="Deployment verification"
)
print(f"Created: {test_order}")
print(f"UUID: {test_order.order_id}")

# Clean up
test_order.delete()
print("Test order deleted")
```

---

### Step 7: Verify Admin Interface

1. Start development server:
```bash
cd app
uv run python manage.py runserver
```

2. Navigate to admin: `http://localhost:8000/admin/`

3. Verify BuildOrder appears in admin

4. Test admin features:
   - Create a build order
   - View list display (name, blocks_count, total_mass, dates)
   - View detail page with formatted JSON
   - View calculation summary
   - Verify validation works

---

### Step 8: Run Integration Tests

Create a test build order with real data:

```bash
cd app
uv run python manage.py shell
```

```python
from buildorders.models import BuildOrder
from blocks.models import Block

# Get some blocks
blocks = Block.objects.all()[:3]
print(f"Using blocks: {[b.name for b in blocks]}")

# Create build order
order = BuildOrder.objects.create(
    name="Integration Test Order",
    description="Testing deployment",
    blocks={
        str(blocks[0].block_id): 10,
        str(blocks[1].block_id): 5,
        str(blocks[2].block_id): 3
    }
)

# Test calculations
summary = order.get_calculation_summary()
print(f"Total mass: {summary['total_mass']} kg")
print(f"Components: {len(summary['required_components'])}")
print(f"Ores: {len(summary['required_ores'])}")
print(f"Fabricators: {len(summary['fabricator_times'])}")

# Test caching
import time
start = time.time()
summary1 = order.get_cached_calculation_summary()
time1 = time.time() - start

start = time.time()
summary2 = order.get_cached_calculation_summary()
time2 = time.time() - start

print(f"First call: {time1:.4f}s")
print(f"Cached call: {time2:.4f}s")
print(f"Cache speedup: {time1/time2:.1f}x")

# Clean up
order.delete()
print("Integration test complete")
```

---

### Step 9: Configure Production Caching (Optional)

For production environments, configure Redis or Memcached:

**Redis Configuration:**
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'se2calc',
        'TIMEOUT': 300,  # 5 minutes (matches BuildOrder cache TTL)
    }
}
```

**Memcached Configuration:**
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'se2calc',
        'TIMEOUT': 300,
    }
}
```

**Verify caching:**
```bash
uv run python manage.py shell -c "
from django.core.cache import cache
cache.set('test_key', 'test_value', 60)
print(f'Cache test: {cache.get(\"test_key\")}')
"
```

---

### Step 10: Performance Testing

Test with larger build orders:

```python
from buildorders.models import BuildOrder
from blocks.models import Block
import time

# Get all blocks
all_blocks = list(Block.objects.all())
print(f"Testing with {len(all_blocks)} blocks")

# Create large build order
blocks_dict = {str(b.block_id): 10 for b in all_blocks}
order = BuildOrder.objects.create(
    name="Performance Test",
    blocks=blocks_dict
)

# Time calculation
start = time.time()
summary = order.get_calculation_summary()
calc_time = time.time() - start

print(f"Calculation time: {calc_time:.3f}s")
print(f"Total mass: {summary['total_mass']:,.0f} kg")
print(f"Components: {len(summary['required_components'])}")
print(f"Ores: {len(summary['required_ores'])}")

# Clean up
order.delete()
```

**Performance Benchmarks:**
- Small orders (1-10 blocks): < 0.1s
- Medium orders (10-50 blocks): < 0.5s
- Large orders (50-100 blocks): < 2s

---

## Post-Deployment Verification

### Checklist

- [ ] All migrations applied successfully
- [ ] Model accessible in Django shell
- [ ] Admin interface working
- [ ] Calculations producing correct results
- [ ] Caching working (if configured)
- [ ] No errors in logs
- [ ] Performance acceptable
- [ ] Integration tests passing

### Verification Commands

```bash
# Check migrations
uv run python manage.py showmigrations buildorders

# Check model
uv run python manage.py shell -c "from buildorders.models import BuildOrder; print(BuildOrder.objects.count())"

# Run tests
uv run pytest buildorders/tests.py -v

# Check for errors
tail -f logs/django.log  # or your log location
```

---

## Rollback Procedure

If issues occur, follow these steps:

### Step 1: Stop Application
```bash
# Stop web server
sudo systemctl stop gunicorn  # or your web server
```

### Step 2: Rollback Migration
```bash
cd app
uv run python manage.py migrate buildorders zero
```

### Step 3: Restore Database (if needed)
```bash
# PostgreSQL
psql your_database < backup_before_enh0000009.sql
```

### Step 4: Remove from INSTALLED_APPS
```python
# settings.py
INSTALLED_APPS = [
    # ... other apps ...
    # 'buildorders',  # Commented out
]
```

### Step 5: Restart Application
```bash
sudo systemctl start gunicorn
```

---

## Troubleshooting

### Issue: Migration Fails

**Symptoms:** Migration command returns error

**Solutions:**
1. Check database connectivity
2. Verify all dependencies are migrated
3. Check for conflicting migrations
4. Review migration file for errors

```bash
# Check migration status
uv run python manage.py showmigrations

# Try fake migration (if already applied manually)
uv run python manage.py migrate buildorders --fake
```

### Issue: Import Errors

**Symptoms:** Cannot import BuildOrder model

**Solutions:**
1. Verify app is in INSTALLED_APPS
2. Check for syntax errors in models.py
3. Restart Django shell/server

```bash
# Verify installation
uv run python manage.py check buildorders
```

### Issue: Calculation Errors

**Symptoms:** Calculations return incorrect results

**Solutions:**
1. Verify test data is correct
2. Check for missing blocks/components/ores
3. Review calculation logic
4. Clear cache and retry

```bash
# Clear cache
uv run python manage.py shell -c "from django.core.cache import cache; cache.clear()"
```

### Issue: Performance Problems

**Symptoms:** Calculations are slow

**Solutions:**
1. Enable caching (Redis/Memcached)
2. Check database indexes
3. Optimize queries with select_related
4. Monitor database query count

```bash
# Check query count
uv run python manage.py shell
```
```python
from django.db import connection
from django.test.utils import override_settings

with override_settings(DEBUG=True):
    from buildorders.models import BuildOrder
    order = BuildOrder.objects.first()
    summary = order.get_calculation_summary()
    print(f"Queries: {len(connection.queries)}")
```

---

## Monitoring

### Key Metrics

Monitor these metrics post-deployment:

1. **Response Times:**
   - Calculation time per order
   - Cache hit rate
   - Database query count

2. **Error Rates:**
   - ValidationError frequency
   - Missing block/component errors
   - Cache failures

3. **Usage Patterns:**
   - Orders created per day
   - Average blocks per order
   - Most common block combinations

### Logging

Add logging to track issues:

```python
# In production settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/buildorders.log',
        },
    },
    'loggers': {
        'buildorders': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

---

## Support

### Documentation
- **Enhancement Doc:** `ENH0000009-buildorder-model-core-logic.md`
- **Calculation Algorithms:** `docs/design/calculation_algorithms.md`
- **Model Code:** `app/buildorders/models.py`
- **Tests:** `app/buildorders/tests.py`
- **Admin:** `app/buildorders/admin.py`

### Contact
- **Developer:** Dan Smith (crashtechie)
- **Enhancement ID:** ENH-0000009
- **Completion Date:** 2026-02-02

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-02 | Initial deployment guide |

---

## Appendix: Quick Reference

### Common Commands

```bash
# Run tests
uv run pytest buildorders/tests.py -v

# Check migrations
uv run python manage.py showmigrations buildorders

# Apply migrations
uv run python manage.py migrate buildorders

# Create superuser (if needed)
uv run python manage.py createsuperuser

# Collect static files
uv run python manage.py collectstatic --noinput

# Clear cache
uv run python manage.py shell -c "from django.core.cache import cache; cache.clear()"
```

### Model Quick Reference

```python
from buildorders.models import BuildOrder

# Create
order = BuildOrder.objects.create(
    name="My Order",
    blocks={'block_id': quantity}
)

# Calculate
summary = order.get_calculation_summary()

# With caching
summary = order.get_cached_calculation_summary()

# Validate
errors = order.validate_blocks()

# Get blocks
blocks = order.get_block_objects()
```
