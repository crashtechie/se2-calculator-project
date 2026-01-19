# ENH-0000001 Deployment Guide: Create Ores App and Model

**Enhancement ID:** ENH-0000001  
**Document Version:** 1.0  
**Last Updated:** 2026-01-20  
**Deployment Status:** Ready for Implementation

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [Implementation Steps](#implementation-steps)
4. [Verification & Testing](#verification--testing)
5. [Rollback Procedure](#rollback-procedure)
6. [Troubleshooting](#troubleshooting)
7. [Post-Deployment Tasks](#post-deployment-tasks)

---

## Prerequisites

### System Requirements
- Python 3.13+
- UV package manager installed
- Django 6.0.1
- PostgreSQL 13+ (optional) or SQLite3
- Git for version control

### Required Dependencies
All dependencies are already in `pyproject.toml`:
- `django>=6.0.1`
- `uuid-utils>=0.13.0`
- `uuid7>=0.1.0`

### Environment Setup
Ensure `.env` file exists with required variables:
```bash
DEBUG=true
SECRET_KEY=<your-secret-key>
# Optional PostgreSQL settings
DB_NAME=se2_calculator
DB_USER=se2_user
DB_PASSWORD=<your-db-password>
DB_HOST=localhost
DB_PORT=5432
```

### Permissions Required
- Write access to project directory
- Database access (create tables, run migrations)
- Ability to restart development server

---

## Pre-Deployment Checklist

- [ ] Backup current database
  ```bash
  # SQLite backup
  cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)
  
  # PostgreSQL backup
  pg_dump -U se2_user se2_calculator > backup_$(date +%Y%m%d_%H%M%S).sql
  ```

- [ ] Verify current git branch and commit changes
  ```bash
  git status
  git checkout -b feature/enh-0000001-ores-model
  ```

- [ ] Confirm ores app exists
  ```bash
  ls -la ores/
  ```

- [ ] Verify dependencies installed
  ```bash
  uv pip list | grep -E "django|uuid"
  ```

- [ ] Test database connectivity
  ```bash
  uv run python manage.py check --database default
  ```

---

## Implementation Steps

### Step 1: Register Ores App in Settings

**File:** `se2CalcProject/settings.py`

**Action:** Add `'ores'` to `INSTALLED_APPS`

**Current State:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

**New State:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ores',  # ENH-0000001: Ores app
]
```

**Verification:**
```bash
uv run python manage.py check
# Should output: System check identified no issues (0 silenced).
```

---

### Step 2: Implement Ore Model

**File:** `ores/models.py`

**Implementation:**

```python
from django.db import models
from uuid_utils import uuid7


class Ore(models.Model):
    """
    Represents a raw ore resource in Space Engineers 2.
    
    Ores are the base materials that are refined and used to craft components.
    """
    object_id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
        help_text="UUIDv7 primary key"
    )
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique name of the ore (e.g., 'Iron Ore', 'Silicon')"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the ore and its uses"
    )
    
    mass = models.FloatField(
        help_text="Mass per unit in kilograms"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the ore was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the ore was last updated"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Ore'
        verbose_name_plural = 'Ores'
        db_table = 'ores_ore'
    
    def __str__(self):
        return self.name
```

**Key Implementation Details:**

1. **UUIDv7 Primary Key:**
   - Uses `uuid_utils.uuid7` for time-ordered UUIDs
   - `editable=False` prevents manual editing in admin
   - Provides better database indexing than UUID4

2. **Field Constraints:**
   - `name`: Unique constraint ensures no duplicate ore names
   - `description`: Optional field (blank=True)
   - `mass`: Required float for calculations

3. **Timestamps:**
   - `created_at`: Auto-populated on creation
   - `updated_at`: Auto-updated on every save

4. **Meta Options:**
   - Ordered alphabetically by name
   - Custom table name for clarity

**Verification:**
```bash
uv run python manage.py check
# Should output: System check identified no issues (0 silenced).
```

---

### Step 3: Configure Django Admin

**File:** `ores/admin.py`

**Implementation:**

```python
from django.contrib import admin
from .models import Ore


@admin.register(Ore)
class OreAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Ore model.
    """
    list_display = ('name', 'mass', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('object_id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'mass')
        }),
        ('System Information', {
            'fields': ('object_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

**Admin Features:**

1. **list_display:** Shows key fields in list view
2. **search_fields:** Enables search by name and description
3. **list_filter:** Adds date filters in sidebar
4. **readonly_fields:** Prevents editing system fields
5. **fieldsets:** Groups fields logically with collapsible system info

**Verification:**
```bash
uv run python manage.py check
# Should output: System check identified no issues (0 silenced).
```

---

### Step 4: Create Database Migrations

**Command:**
```bash
uv run python manage.py makemigrations ores
```

**Expected Output:**
```
Migrations for 'ores':
  ores/migrations/0001_initial.py
    - Create model Ore
```

**Generated Migration File:** `ores/migrations/0001_initial.py`

**Review Migration:**
```bash
cat ores/migrations/0001_initial.py
```

**Expected Content:**
```python
# Generated by Django 6.0.1 on YYYY-MM-DD HH:MM

from django.db import migrations, models
import uuid_utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ore',
            fields=[
                ('object_id', models.UUIDField(default=uuid_utils.uuid7, editable=False, help_text='UUIDv7 primary key', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text="Unique name of the ore (e.g., 'Iron Ore', 'Silicon')", max_length=100, unique=True)),
                ('description', models.TextField(blank=True, help_text='Detailed description of the ore and its uses')),
                ('mass', models.FloatField(help_text='Mass per unit in kilograms')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the ore was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the ore was last updated')),
            ],
            options={
                'verbose_name': 'Ore',
                'verbose_name_plural': 'Ores',
                'db_table': 'ores_ore',
                'ordering': ['name'],
            },
        ),
    ]
```

**Verification:**
```bash
# Check migration without applying
uv run python manage.py migrate --plan
```

---

### Step 5: Apply Database Migrations

**Command:**
```bash
uv run python manage.py migrate ores
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: ores
Running migrations:
  Applying ores.0001_initial... OK
```

**Verification:**
```bash
# Verify table created
uv run python manage.py dbshell
```

**SQLite Verification:**
```sql
.tables
-- Should show: ores_ore

.schema ores_ore
-- Should show table structure

.quit
```

**PostgreSQL Verification:**
```sql
\dt
-- Should show: ores_ore

\d ores_ore
-- Should show table structure

\q
```

---

### Step 6: Create Superuser (if needed)

**Command:**
```bash
uv run python manage.py createsuperuser
```

**Follow prompts:**
```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

---

### Step 7: Start Development Server

**Command:**
```bash
uv run python manage.py runserver
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 20, 2026 - 12:00:00
Django version 6.0.1, using settings 'se2CalcProject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## Verification & Testing

### Test 1: Django Shell - Create Ore

```bash
uv run python manage.py shell
```

```python
from ores.models import Ore

# Create an ore
iron = Ore.objects.create(
    name="Iron Ore",
    description="Common ore used for steel production",
    mass=1.0
)

print(f"Created: {iron}")
print(f"UUID: {iron.object_id}")
print(f"Created at: {iron.created_at}")

# Verify it exists
ores = Ore.objects.all()
print(f"Total ores: {ores.count()}")

# Test __str__ method
print(f"String representation: {str(iron)}")

# Exit shell
exit()
```

**Expected Output:**
```
Created: Iron Ore
UUID: 01933e7a-8b2c-7890-abcd-ef1234567890
Created at: 2026-01-20 12:00:00.123456+00:00
Total ores: 1
String representation: Iron Ore
```

---

### Test 2: Admin Interface

1. **Navigate to admin:**
   ```
   http://127.0.0.1:8000/admin/
   ```

2. **Login with superuser credentials**

3. **Verify Ores section appears:**
   - Should see "ORES" section
   - Should see "Ores" link

4. **Click "Ores" and verify:**
   - List view shows: name, mass, created_at, updated_at
   - Search box present
   - Filter sidebar shows date filters

5. **Click "Add Ore":**
   - Form shows: name, description, mass fields
   - System Information section collapsed
   - object_id, created_at, updated_at are readonly

6. **Create test ore:**
   ```
   Name: Silicon
   Description: Used for electronics and solar panels
   Mass: 0.8
   ```

7. **Save and verify:**
   - Redirects to list view
   - New ore appears in list
   - Sorted alphabetically

---

### Test 3: UUIDv7 Validation

```bash
uv run python manage.py shell
```

```python
from ores.models import Ore
import uuid

# Create multiple ores
ores = []
for i in range(5):
    ore = Ore.objects.create(
        name=f"Test Ore {i}",
        mass=1.0
    )
    ores.append(ore)
    print(f"Created: {ore.name} - UUID: {ore.object_id}")

# Verify UUIDs are time-ordered (UUIDv7 property)
uuids = [ore.object_id for ore in ores]
print(f"\nUUIDs are sequential: {uuids == sorted(uuids)}")

# Cleanup
Ore.objects.filter(name__startswith="Test Ore").delete()
print("\nTest ores deleted")

exit()
```

**Expected Output:**
```
Created: Test Ore 0 - UUID: 01933e7a-8b2c-7890-abcd-ef1234567890
Created: Test Ore 1 - UUID: 01933e7a-8b2c-7891-abcd-ef1234567891
Created: Test Ore 2 - UUID: 01933e7a-8b2c-7892-abcd-ef1234567892
Created: Test Ore 3 - UUID: 01933e7a-8b2c-7893-abcd-ef1234567893
Created: Test Ore 4 - UUID: 01933e7a-8b2c-7894-abcd-ef1234567894

UUIDs are sequential: True

Test ores deleted
```

---

### Test 4: Timestamp Auto-Population

```bash
uv run python manage.py shell
```

```python
from ores.models import Ore
import time

# Create ore
ore = Ore.objects.create(name="Timestamp Test", mass=1.0)
created = ore.created_at
updated = ore.updated_at

print(f"Created: {created}")
print(f"Updated: {updated}")
print(f"Timestamps match: {created == updated}")

# Wait and update
time.sleep(2)
ore.mass = 2.0
ore.save()

ore.refresh_from_db()
print(f"\nAfter update:")
print(f"Created: {ore.created_at}")
print(f"Updated: {ore.updated_at}")
print(f"Updated timestamp changed: {ore.updated_at > created}")
print(f"Created timestamp unchanged: {ore.created_at == created}")

# Cleanup
ore.delete()

exit()
```

**Expected Output:**
```
Created: 2026-01-20 12:00:00.123456+00:00
Updated: 2026-01-20 12:00:00.123456+00:00
Timestamps match: True

After update:
Created: 2026-01-20 12:00:00.123456+00:00
Updated: 2026-01-20 12:00:02.654321+00:00
Updated timestamp changed: True
Created timestamp unchanged: True
```

---

### Test 5: Unique Constraint

```bash
uv run python manage.py shell
```

```python
from ores.models import Ore
from django.db import IntegrityError

# Create ore
Ore.objects.create(name="Unique Test", mass=1.0)

# Try to create duplicate
try:
    Ore.objects.create(name="Unique Test", mass=2.0)
    print("ERROR: Duplicate allowed!")
except IntegrityError as e:
    print(f"SUCCESS: Duplicate prevented - {e}")

# Cleanup
Ore.objects.filter(name="Unique Test").delete()

exit()
```

**Expected Output:**
```
SUCCESS: Duplicate prevented - UNIQUE constraint failed: ores_ore.name
```

---

## Rollback Procedure

### If Issues Occur During Deployment

#### Rollback Step 1: Unapply Migration

```bash
# Revert to zero state (removes table)
uv run python manage.py migrate ores zero
```

**Expected Output:**
```
Operations to perform:
  Unapply all migrations: ores
Running migrations:
  Rendering model states... DONE
  Unapplying ores.0001_initial... OK
```

#### Rollback Step 2: Remove App from Settings

**File:** `se2CalcProject/settings.py`

Remove `'ores'` from `INSTALLED_APPS`

#### Rollback Step 3: Restore Database Backup

**SQLite:**
```bash
cp db.sqlite3.backup.YYYYMMDD_HHMMSS db.sqlite3
```

**PostgreSQL:**
```bash
psql -U se2_user se2_calculator < backup_YYYYMMDD_HHMMSS.sql
```

#### Rollback Step 4: Revert Code Changes

```bash
git checkout se2CalcProject/settings.py
git checkout ores/models.py
git checkout ores/admin.py
```

#### Rollback Step 5: Verify System

```bash
uv run python manage.py check
uv run python manage.py runserver
```

---

## Troubleshooting

### Issue 1: ImportError: cannot import name 'uuid7'

**Symptom:**
```
ImportError: cannot import name 'uuid7' from 'uuid_utils'
```

**Solution:**
```bash
# Reinstall uuid-utils
uv pip install --force-reinstall uuid-utils

# Verify installation
uv pip show uuid-utils
```

---

### Issue 2: Migration Already Exists

**Symptom:**
```
CommandError: Conflicting migrations detected
```

**Solution:**
```bash
# Remove existing migration
rm ores/migrations/0001_initial.py

# Recreate migration
uv run python manage.py makemigrations ores
```

---

### Issue 3: Table Already Exists

**Symptom:**
```
django.db.utils.OperationalError: table "ores_ore" already exists
```

**Solution:**
```bash
# Fake the migration (if table structure matches)
uv run python manage.py migrate ores --fake

# OR drop table and recreate
uv run python manage.py dbshell
DROP TABLE ores_ore;
.quit

uv run python manage.py migrate ores
```

---

### Issue 4: Admin Not Showing Ores

**Symptom:**
Ores section doesn't appear in admin interface

**Solution:**
1. Verify app registered in settings
2. Verify admin.py has @admin.register decorator
3. Clear browser cache
4. Restart development server
5. Check for Python syntax errors:
   ```bash
   python -m py_compile ores/admin.py
   ```

---

### Issue 5: UUIDv7 Not Sequential

**Symptom:**
UUIDs appear random, not time-ordered

**Solution:**
```bash
# Verify uuid-utils version
uv pip show uuid-utils

# Should be >= 0.13.0
# If not, upgrade:
uv pip install --upgrade uuid-utils
```

---

## Post-Deployment Tasks

### Task 1: Update Documentation

- [ ] Update `CHANGELOG.md`:
  ```markdown
  ## [0.2.0-alpha] - 2026-01-20
  
  ### Added
  - ENH-0000001: Created Ores app with Ore model
  - UUIDv7 primary keys for ores
  - Django admin interface for ore management
  ```

- [ ] Update `docs/projectPlan/phase1_models.md`:
  - Check off completed tasks in section 1.1 and 1.2

---

### Task 2: Commit Changes

```bash
# Stage changes
git add se2CalcProject/settings.py
git add ores/models.py
git add ores/admin.py
git add ores/migrations/0001_initial.py
git add CHANGELOG.md
git add docs/projectPlan/phase1_models.md

# Commit
git commit -m "ENH-0000001: Implement Ores app and model

- Register ores app in INSTALLED_APPS
- Create Ore model with UUIDv7 primary key
- Configure Django admin interface
- Create and apply initial migration
- Add comprehensive field help text
- Implement Meta class with ordering

Closes ENH-0000001"

# Push to remote
git push origin feature/enh-0000001-ores-model
```

---

### Task 3: Create Pull Request

**PR Title:** `ENH-0000001: Implement Ores App and Model`

**PR Description:**
```markdown
## Enhancement
Implements ENH-0000001: Create Ores App and Model

## Changes
- ✅ Registered ores app in settings
- ✅ Created Ore model with UUIDv7 primary keys
- ✅ Configured Django admin interface
- ✅ Created and applied migrations
- ✅ All tests passing

## Testing
- [x] Model creation via Django shell
- [x] Admin interface CRUD operations
- [x] UUIDv7 generation verified
- [x] Timestamp auto-population verified
- [x] Unique constraint verified

## Documentation
- [x] CHANGELOG.md updated
- [x] Phase 1 checklist updated
- [x] Deployment guide created

## Related
- Part of Phase 1: Models & Database Setup
- Blocks ENH-0000002 (Components) and ENH-0000003 (Blocks)
```

---

### Task 4: Update Enhancement Status

**File:** `docs/enhancementRequests/phase1_models/inReview-enh0000001-create-ores-app-model.md`

1. Rename file:
   ```bash
   git mv docs/enhancementRequests/phase1_models/inReview-enh0000001-create-ores-app-model.md \
          docs/enhancementRequests/phase1_models/completed-enh0000001-create-ores-app-model.md
   ```

2. Update status in document:
   ```markdown
   **Status:** completed
   ```

3. Update Status History table:
   ```markdown
   | Date | Status | Notes |
   |------|--------|-------|
   | 2026-01-20 | inReview | Initial creation |
   | 2026-01-20 | inProgress | Started implementation |
   | 2026-01-20 | completed | Merged to main |
   ```

4. Update Sign-off section:
   ```markdown
   **Completed By:** [Your Name]
   **Completion Date:** 2026-01-20
   ```

---

### Task 5: Notify Team

Send notification with:
- Enhancement ID and description
- Link to merged PR
- Link to deployment guide
- Next steps (ENH-0000002: Components)

---

## Deployment Checklist Summary

### Pre-Deployment
- [ ] Database backed up
- [ ] Git branch created
- [ ] Dependencies verified
- [ ] Database connectivity tested

### Implementation
- [ ] App registered in settings
- [ ] Ore model implemented
- [ ] Admin interface configured
- [ ] Migrations created
- [ ] Migrations applied

### Verification
- [ ] Django shell tests passed
- [ ] Admin interface tests passed
- [ ] UUIDv7 validation passed
- [ ] Timestamp tests passed
- [ ] Unique constraint tests passed

### Post-Deployment
- [ ] Documentation updated
- [ ] Changes committed
- [ ] Pull request created
- [ ] Enhancement status updated
- [ ] Team notified

---

## Success Criteria

Deployment is successful when:

1. ✅ Ores app registered in INSTALLED_APPS
2. ✅ Ore model created with all required fields
3. ✅ UUIDv7 primary keys generating correctly
4. ✅ Admin interface displays ores
5. ✅ Migrations applied without errors
6. ✅ All verification tests pass
7. ✅ No system check warnings
8. ✅ Development server runs without errors

---

## Support & References

### Documentation
- Django Models: https://docs.djangoproject.com/en/6.0/topics/db/models/
- Django Admin: https://docs.djangoproject.com/en/6.0/ref/contrib/admin/
- Django Migrations: https://docs.djangoproject.com/en/6.0/topics/migrations/
- uuid-utils: https://pypi.org/project/uuid-utils/

### Project Files
- Enhancement Request: `docs/enhancementRequests/phase1_models/inReview-enh0000001-create-ores-app-model.md`
- Phase 1 Plan: `docs/projectPlan/phase1_models.md`
- Settings: `se2CalcProject/settings.py`

### Contact
For issues or questions, open an issue on GitHub or contact the development team.

---

**Document End**
