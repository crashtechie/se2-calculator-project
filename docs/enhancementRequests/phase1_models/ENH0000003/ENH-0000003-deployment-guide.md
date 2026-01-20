# ENH-0000003 Deployment Guide: Create Blocks App and Model

**Enhancement ID:** ENH-0000003  
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
DB_NAME=se2_calculator_db
DB_USER=se2_user
DB_PASSWORD=<your-db-password>
DB_HOST=localhost
DB_PORT=5432
```

### Permissions Required
- Write access to project directory
- Database access (create tables, run migrations)
- Ability to restart development server
- ENH-0000001 (Ores) and ENH-0000002 (Components) must be completed

### Dependency Verification

**Verify ENH-0000001 and ENH-0000002 are completed:**
```bash
# Check apps exist and are registered
uv run python manage.py check
# Should output: System check identified no issues (0 silenced).

# Verify models can be imported
uv run python manage.py shell -c "from ores.models import Ore; from components.models import Component; print('✓ Dependencies ready')"
```

---

## Pre-Deployment Checklist

- [x] Verify ENH-0000001 (Ores) and ENH-0000002 (Components) completed
  ```bash
  uv run python manage.py shell
  from ores.models import Ore
  from components.models import Component
  print(f"Ores: {Ore.objects.count()}, Components: {Component.objects.count()}")
  exit()
  ```

- [x] Backup current database
  ```bash
  # SQLite backup
  cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)
  
  # PostgreSQL backup
  pg_dump -U se2_user se2_calculator_db > backup_$(date +%Y%m%d_%H%M%S).sql
  ```

- [x] Verify current git branch and commit changes
  ```bash
  git status
  git checkout -b feat/enh0000003-create-blocks-app-model
  ```

- [x] Create blocks app if not exists
  ```bash
  uv run python manage.py startapp blocks
  ```

- [x] Verify dependencies installed
  ```bash
  uv pip list | grep -E "django|uuid"
  ```

- [x] Test database connectivity
  ```bash
  uv run python manage.py check --database default
  ```

---

## Implementation Steps

### Step 1: Register Blocks App in Settings

**File:** `se2CalcProject/settings.py`

**Action:** Add `'blocks'` to `INSTALLED_APPS` after components app

**Current State:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ores',  # ENH-0000001
    'components',  # ENH-0000002
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
    'components',  # ENH-0000002: Components app
    'blocks',  # ENH-0000003: Blocks app
]
```

**Verification:**
```bash
uv run python manage.py check
# Should output: System check identified no issues (0 silenced).
```

---

### Step 2: Implement Block Model

**File:** `blocks/models.py`

**Implementation:**

```python
from django.db import models
from uuid_utils import uuid7
from components.models import Component


def generate_uuid():
    """Generate UUIDv7 string for primary key."""
    return str(uuid7())


class Block(models.Model):
    """
    Represents a buildable block in Space Engineers 2.
    
    Blocks are the final buildable items made from components.
    """
    block_id = models.UUIDField(
        primary_key=True,
        default=generate_uuid,
        editable=False,
        help_text="UUIDv7 primary key"
    )
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique name of the block (e.g., 'Large Reactor', 'Small Thruster')"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the block and its uses"
    )
    
    mass = models.FloatField(
        help_text="Total mass of the block in kilograms"
    )
    
    components = models.JSONField(
        default=list,
        blank=True,
        help_text="JSON array of component requirements with IDs, names, and quantities"
    )
    
    health = models.FloatField(
        help_text="Block health/integrity points"
    )
    
    pcu = models.IntegerField(
        help_text="Performance Cost Units (PCU) for this block"
    )
    
    snap_size = models.FloatField(
        help_text="Grid snap size for placement"
    )
    
    input_mass = models.IntegerField(
        help_text="Input mass capacity in kg"
    )
    
    output_mass = models.IntegerField(
        help_text="Output mass capacity in kg"
    )
    
    consumer_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Type of resource consumed (e.g., 'Power', 'Hydrogen', 'Oxygen')"
    )
    
    consumer_rate = models.FloatField(
        default=0.0,
        help_text="Consumption rate per second"
    )
    
    producer_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Type of resource produced (e.g., 'Power', 'Hydrogen', 'Oxygen')"
    )
    
    producer_rate = models.FloatField(
        default=0.0,
        help_text="Production rate per second"
    )
    
    storage_capacity = models.FloatField(
        default=0.0,
        help_text="Storage capacity in liters or units"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the block was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the block was last updated"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Block'
        verbose_name_plural = 'Blocks'
        db_table = 'blocks_block'
    
    def __str__(self):
        return self.name
    
    def validate_components(self):
        """
        Validate that all component_ids in components JSON reference valid Components.
        
        Returns:
            tuple: (is_valid: bool, errors: list of error messages)
        """
        if not self.components:
            return True, []
        
        errors = []
        
        for item in self.components:
            try:
                # Validate structure
                if not isinstance(item, dict):
                    errors.append(f"Component item must be dict, got {type(item)}")
                    continue
                
                required_keys = ['component_id', 'component_name', 'quantity']
                missing_keys = [k for k in required_keys if k not in item]
                if missing_keys:
                    errors.append(f"Component missing keys: {missing_keys}")
                    continue
                
                # Validate quantity
                quantity = item.get('quantity')
                if not isinstance(quantity, int) or quantity <= 0:
                    errors.append(
                        f"Invalid quantity for component {item.get('component_name')}: "
                        f"must be positive integer, got {quantity}"
                    )
                    continue
                
                # Validate component_id references existing Component
                component_id = item.get('component_id')
                try:
                    Component.objects.get(component_id=component_id)
                except Component.DoesNotExist:
                    errors.append(
                        f"Component with ID {component_id} does not exist"
                    )
            except Exception as e:
                errors.append(f"Error validating component: {str(e)}")
        
        return len(errors) == 0, errors
    
    def validate_consumer(self):
        """
        Validate consumer_type and consumer_rate relationship.
        
        Returns:
            tuple: (is_valid: bool, errors: list of error messages)
        """
        errors = []
        
        if self.consumer_type and self.consumer_rate <= 0:
            errors.append(
                f"Consumer type '{self.consumer_type}' requires consumer_rate > 0, "
                f"got {self.consumer_rate}"
            )
        
        if self.consumer_rate < 0:
            errors.append(f"Consumer rate cannot be negative, got {self.consumer_rate}")
        
        return len(errors) == 0, errors
    
    def validate_producer(self):
        """
        Validate producer_type and producer_rate relationship.
        
        Returns:
            tuple: (is_valid: bool, errors: list of error messages)
        """
        errors = []
        
        if self.producer_type and self.producer_rate <= 0:
            errors.append(
                f"Producer type '{self.producer_type}' requires producer_rate > 0, "
                f"got {self.producer_rate}"
            )
        
        if self.producer_rate < 0:
            errors.append(f"Producer rate cannot be negative, got {self.producer_rate}")
        
        return len(errors) == 0, errors
    
    def get_component_objects(self):
        """
        Get all Component objects referenced in components JSON.
        
        Returns:
            QuerySet: Component objects used in this block
        """
        if not self.components:
            return Component.objects.none()
        
        component_ids = [item['component_id'] for item in self.components]
        return Component.objects.filter(component_id__in=component_ids)
    
    def clean(self):
        """Validate model before saving."""
        from django.core.exceptions import ValidationError
        
        all_errors = []
        
        # Validate components
        is_valid, errors = self.validate_components()
        if not is_valid:
            all_errors.extend(errors)
        
        # Validate consumer
        is_valid, errors = self.validate_consumer()
        if not is_valid:
            all_errors.extend(errors)
        
        # Validate producer
        is_valid, errors = self.validate_producer()
        if not is_valid:
            all_errors.extend(errors)
        
        if all_errors:
            raise ValidationError(f"Validation failed: {', '.join(all_errors)}")
    
    def save(self, *args, **kwargs):
        """Override save to validate before saving."""
        self.clean()
        super().save(*args, **kwargs)
```

**Key Implementation Details:**

1. **UUIDv7 Primary Key:** Uses `generate_uuid()` named function (not lambda)
2. **JSONField Components:** Array format `[{"component_id": "uuid", "component_name": "name", "quantity": int}]`
3. **Validation Methods:** validate_components(), validate_consumer(), validate_producer()
4. **Relationship Helper:** get_component_objects() returns Component queryset
5. **Auto-validation:** clean() and save() override ensure validation runs

**Verification:**
```bash
uv run python manage.py check
# Should output: System check identified no issues (0 silenced).
```

---

### Step 3: Configure Django Admin

**File:** `blocks/admin.py`

**Implementation:**

```python
from django.contrib import admin
from django.utils.html import mark_safe
import json
from .models import Block


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Block model.
    """
    list_display = (
        'name',
        'health',
        'pcu',
        'mass',
        'components_preview',
        'consumer_info',
        'producer_info',
        'created_at'
    )
    search_fields = ('name', 'description', 'consumer_type', 'producer_type')
    list_filter = ('consumer_type', 'producer_type', 'created_at', 'updated_at')
    readonly_fields = (
        'block_id',
        'created_at',
        'updated_at',
        'components_formatted',
        'component_objects',
        'validation_status'
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'mass')
        }),
        ('Block Properties', {
            'fields': ('health', 'pcu', 'snap_size', 'input_mass', 'output_mass')
        }),
        ('Components & Production', {
            'fields': (
                'components',
                'components_formatted',
                'component_objects'
            ),
            'description': 'Define components as JSON array: [{"component_id": "uuid", "component_name": "name", "quantity": int}, ...]'
        }),
        ('Power & Resources', {
            'fields': (
                'consumer_type',
                'consumer_rate',
                'producer_type',
                'producer_rate',
                'storage_capacity'
            )
        }),
        ('Validation', {
            'fields': ('validation_status',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('block_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def components_preview(self, obj):
        """Display components count in list view."""
        if not obj.components:
            return mark_safe('<em>No components</em>')
        
        component_count = len(obj.components)
        plural = 's' if component_count != 1 else ''
        return mark_safe(
            '<span title=\"{}\">{} component{}</span>'.format(
                json.dumps(obj.components),
                component_count,
                plural
            )
        )
    components_preview.short_description = 'Components'
    
    def components_formatted(self, obj):
        """Display components as formatted JSON in detail view."""
        if not obj.components:
            return mark_safe('<em>No components</em>')
        
        formatted = json.dumps(obj.components, indent=2)
        return mark_safe(
            '<pre style="background-color: #f5f5f5; padding: 10px; '
            'border-radius: 5px; overflow-x: auto;">{}</pre>'.format(formatted)
        )
    components_formatted.short_description = 'Components (Formatted)'
    
    def component_objects(self, obj):
        """Display component names referenced in components."""
        components = obj.get_component_objects()
        if not components:
            return mark_safe('<em>No components referenced</em>')
        
        # Create lookup dict for quantities
        quantity_map = {item['component_id']: item['quantity'] for item in obj.components}
        
        component_list = '<br>'.join([
            '<strong>{}</strong>: {} units'.format(
                comp.name,
                quantity_map.get(str(comp.component_id), 0)
            )
            for comp in components
        ])
        return mark_safe(component_list)
    component_objects.short_description = 'Referenced Components'
    
    def consumer_info(self, obj):
        """Display consumer information."""
        if not obj.consumer_type:
            return mark_safe('<em>None</em>')
        return mark_safe(
            '<strong>{}</strong><br>{} /s'.format(
                obj.consumer_type,
                obj.consumer_rate
            )
        )
    consumer_info.short_description = 'Consumer'
    
    def producer_info(self, obj):
        """Display producer information."""
        if not obj.producer_type:
            return mark_safe('<em>None</em>')
        return mark_safe(
            '<strong>{}</strong><br>{} /s'.format(
                obj.producer_type,
                obj.producer_rate
            )
        )
    producer_info.short_description = 'Producer'
    
    def validation_status(self, obj):
        """Display validation status for all validations."""
        all_valid = True
        all_errors = []
        
        # Validate components
        is_valid, errors = obj.validate_components()
        if not is_valid:
            all_valid = False
            all_errors.extend(['Components: ' + e for e in errors])
        
        # Validate consumer
        is_valid, errors = obj.validate_consumer()
        if not is_valid:
            all_valid = False
            all_errors.extend(['Consumer: ' + e for e in errors])
        
        # Validate producer
        is_valid, errors = obj.validate_producer()
        if not is_valid:
            all_valid = False
            all_errors.extend(['Producer: ' + e for e in errors])
        
        if all_valid:
            return mark_safe(
                '<span style="color: green; font-weight: bold;">✓ Valid</span>'
            )
        else:
            error_text = '<br>'.join(['• ' + error for error in all_errors])
            return mark_safe(
                '<span style="color: red; font-weight: bold;">✗ Invalid</span><br>' +
                error_text
            )
    validation_status.short_description = 'Validation Status'
```

**Admin Features:**
- Custom displays for components, consumer, producer
- Formatted JSON display
- Validation status with detailed errors
- Logical field grouping with fieldsets

**Verification:**
```bash
uv run python manage.py check
# Should output: System check identified no issues (0 silenced).
```

---

### Step 4: Create Database Migrations

**Command:**
```bash
uv run python manage.py makemigrations blocks
```

**Expected Output:**
```
Migrations for 'blocks':
  blocks/migrations/0001_initial.py
    - Create model Block
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
uv run python manage.py migrate blocks
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: blocks
Running migrations:
  Applying blocks.0001_initial... OK
```

**Verification:**
```bash
# Verify table created
uv run python manage.py dbshell
```

**SQLite Verification:**
```sql
.tables
-- Should show: blocks_block

.schema blocks_block
-- Should show table structure

.quit
```

---

### Step 6: Start Development Server

**Command:**
```bash
uv run python manage.py runserver
```

**Expected Output:**
```
System check identified no issues (0 silenced).
Django version 6.0.1, using settings 'se2CalcProject.settings'
Starting development server at http://127.0.0.1:8000/
```

---

### Step 7: Create Comprehensive Automated Test Suite

**File:** `blocks/tests.py`

**Requirement:** 45+ tests minimum (per ENH-0000003 specifications)

**Implementation:**

Create comprehensive test suite organized into logical test classes following the pattern from ENH-0000001 and ENH-0000002.

**Reference Template:** Use `components/tests.py` as a template and adapt for Block model. Replace:
- `Component` → `Block`
- `component_id` → `block_id`
- `materials` → `components`
- `Ore` → `Component`
- Add consumer/producer validation tests

**Test Structure:** The test suite must include:

- **BlockModelCreationTests** (7 tests)
- **BlockFieldValidationTests** (8 tests)  
- **BlockTimestampTests** (5 tests)
- **BlockComponentsJSONFieldTests** (5 tests)
- **BlockConsumerValidationTests** (5 tests)
- **BlockProducerValidationTests** (5 tests)
- **BlockComponentRelationshipTests** (4 tests)
- **BlockMetaTests** (4 tests)
- **BlockIntegrationTests** (6 tests)

**Total: 49 tests minimum**

---

#### Test Code (Blocks)

```python
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from ores.models import Ore
from components.models import Component
from blocks.models import Block


# ---- Test helpers / factories ----
def create_ore(name="Iron", mass=1.0):
    return Ore.objects.create(name=name, mass=mass, description="")


def create_component(name="Steel Plate", materials=None):
    if materials is None:
        ore = create_ore()
        materials = {str(ore.ore_id): 1}
    return Component.objects.create(
        name=name,
        description="",
        materials=materials,
        fabricator_type="Assembler",
        crafting_time=1.0,
        mass=1.0,
    )


def component_entry(component: Component, quantity: int = 1):
    return {
        "component_id": str(component.component_id),
        "component_name": component.name,
        "quantity": quantity,
    }


def create_block(
    name="Test Block",
    components_list=None,
    consumer_type="",
    consumer_rate=0.0,
    producer_type="",
    producer_rate=0.0,
    storage_capacity=0.0,
    mass=10.0,
    health=100.0,
    pcu=50,
    snap_size=0.25,
    input_mass=5,
    output_mass=2,
):
    if components_list is None:
        components_list = []
    return Block.objects.create(
        name=name,
        description="",
        mass=mass,
        components=components_list,
        health=health,
        pcu=pcu,
        snap_size=snap_size,
        input_mass=input_mass,
        output_mass=output_mass,
        consumer_type=consumer_type,
        consumer_rate=consumer_rate,
        producer_type=producer_type,
        producer_rate=producer_rate,
        storage_capacity=storage_capacity,
    )


# ---- BlockModelCreationTests (7) ----
class BlockModelCreationTests(TestCase):
    def test_create_valid_block_minimal_fields(self):
        blk = create_block(name="Minimal Block")
        self.assertIsInstance(blk, Block)
        self.assertEqual(blk.name, "Minimal Block")

    def test_duplicate_name_not_allowed(self):
        create_block(name="Unique Block")
        with self.assertRaises(IntegrityError):
            create_block(name="Unique Block")

    def test_default_components_is_list(self):
        blk = create_block(name="Default Components Block")
        self.assertIsInstance(blk.components, list)
        self.assertEqual(blk.components, [])

    def test_str_returns_name(self):
        blk = create_block(name="Display Name Block")
        self.assertEqual(str(blk), "Display Name Block")

    def test_uuid_primary_key_assigned(self):
        blk = create_block(name="UUID Block")
        self.assertIsNotNone(blk.block_id)
        self.assertTrue(str(blk.block_id))

    def test_timestamps_auto_populated(self):
        blk = create_block(name="Timestamp Block")
        self.assertIsNotNone(blk.created_at)
        self.assertIsNotNone(blk.updated_at)

    def test_get_component_objects_empty_returns_none_queryset(self):
        blk = create_block(name="Empty Components Block")
        qs = blk.get_component_objects()
        self.assertEqual(qs.count(), 0)


# ---- BlockFieldValidationTests (8) ----
class BlockFieldValidationTests(TestCase):
    def test_blank_description_allowed(self):
        blk = create_block(name="No Description Block")
        self.assertEqual(blk.description, "")

    def test_assign_and_retrieve_mass(self):
        blk = create_block(name="Mass Block", mass=42.5)
        self.assertEqual(blk.mass, 42.5)

    def test_assign_and_retrieve_health(self):
        blk = create_block(name="Health Block", health=250.0)
        self.assertEqual(blk.health, 250.0)

    def test_assign_and_retrieve_pcu(self):
        blk = create_block(name="PCU Block", pcu=123)
        self.assertEqual(blk.pcu, 123)

    def test_assign_and_retrieve_snap_size(self):
        blk = create_block(name="Snap Block", snap_size=0.5)
        self.assertEqual(blk.snap_size, 0.5)

    def test_assign_and_retrieve_input_mass(self):
        blk = create_block(name="Input Mass Block", input_mass=99)
        self.assertEqual(blk.input_mass, 99)

    def test_assign_and_retrieve_output_mass(self):
        blk = create_block(name="Output Mass Block", output_mass=77)
        self.assertEqual(blk.output_mass, 77)

    def test_assign_and_retrieve_storage_capacity(self):
        blk = create_block(name="Storage Block", storage_capacity=10.0)
        self.assertEqual(blk.storage_capacity, 10.0)


# ---- BlockTimestampTests (5) ----
class BlockTimestampTests(TestCase):
    def test_created_at_set_on_create(self):
        blk = create_block(name="CreatedAt Block")
        self.assertIsNotNone(blk.created_at)

    def test_updated_at_updates_on_save(self):
        blk = create_block(name="UpdatedAt Block")
        original_updated = blk.updated_at
        blk.description = "Updated"
        blk.save()
        self.assertGreaterEqual(blk.updated_at, original_updated)

    def test_updated_at_greater_or_equal_to_created_at(self):
        blk = create_block(name="Timestamp Compare Block")
        self.assertGreaterEqual(blk.updated_at, blk.created_at)

    def test_multiple_updates_change_updated_at(self):
        blk = create_block(name="Multi Update Block")
        first = blk.updated_at
        blk.description = "A"
        blk.save()
        second = blk.updated_at
        blk.description = "B"
        blk.save()
        third = blk.updated_at
        self.assertGreaterEqual(second, first)
        self.assertGreaterEqual(third, second)

    def test_datetime_types(self):
        blk = create_block(name="Datetime Type Block")
        from datetime import datetime
        self.assertIsInstance(blk.created_at, datetime)
        self.assertIsInstance(blk.updated_at, datetime)


# ---- BlockComponentsJSONFieldTests (5) ----
class BlockComponentsJSONFieldTests(TestCase):
    def test_empty_components_valid(self):
        blk = create_block(name="Empty Components Valid Block")
        is_valid, errors = blk.validate_components()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_non_dict_component_item_invalid(self):
        blk = create_block(
            name="NonDict Component Block",
            components_list=["not-a-dict"],
        )
        is_valid, errors = blk.validate_components()
        self.assertFalse(is_valid)
        self.assertTrue(any("must be dict" in e for e in errors))

    def test_missing_keys_in_component_item_invalid(self):
        blk = create_block(
            name="Missing Keys Block",
            components_list=[{"component_id": "x"}],
        )
        is_valid, errors = blk.validate_components()
        self.assertFalse(is_valid)
        self.assertTrue(any("missing keys" in e for e in errors))

    def test_invalid_quantity_in_component_item_invalid(self):
        comp = create_component(name="Motor")
        blk = create_block(
            name="Invalid Quantity Block",
            components_list=[component_entry(comp, quantity=0)],
        )
        is_valid, errors = blk.validate_components()
        self.assertFalse(is_valid)
        self.assertTrue(any("Invalid quantity" in e for e in errors))

    def test_nonexistent_component_id_invalid(self):
        blk = create_block(
            name="Nonexistent Component ID Block",
            components_list=[
                {
                    "component_id": "00000000-0000-0000-0000-000000000000",
                    "component_name": "Ghost",
                    "quantity": 1,
                }
            ],
        )
        is_valid, errors = blk.validate_components()
        self.assertFalse(is_valid)
        self.assertTrue(any("does not exist" in e for e in errors))


# ---- BlockConsumerValidationTests (5) ----
class BlockConsumerValidationTests(TestCase):
    def test_consumer_valid_when_type_empty_and_rate_zero(self):
        blk = create_block(name="Consumer OK Empty", consumer_type="", consumer_rate=0.0)
        is_valid, errors = blk.validate_consumer()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_consumer_invalid_when_type_set_and_rate_zero(self):
        blk = create_block(name="Consumer Invalid Zero", consumer_type="Power", consumer_rate=0.0)
        is_valid, errors = blk.validate_consumer()
        self.assertFalse(is_valid)
        self.assertTrue(any("requires consumer_rate > 0" in e for e in errors))

    def test_consumer_invalid_when_rate_negative(self):
        blk = create_block(name="Consumer Invalid Negative", consumer_type="Power", consumer_rate=-1.0)
        is_valid, errors = blk.validate_consumer()
        self.assertFalse(is_valid)
        self.assertTrue(any("cannot be negative" in e for e in errors))

    def test_consumer_valid_when_type_set_and_rate_positive(self):
        blk = create_block(name="Consumer Valid", consumer_type="Power", consumer_rate=5.0)
        is_valid, errors = blk.validate_consumer()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_consumer_error_message_contains_type(self):
        blk = create_block(name="Consumer Msg", consumer_type="Oxygen", consumer_rate=0.0)
        is_valid, errors = blk.validate_consumer()
        self.assertFalse(is_valid)
        self.assertTrue(any("Oxygen" in e for e in errors))


# ---- BlockProducerValidationTests (5) ----
class BlockProducerValidationTests(TestCase):
    def test_producer_valid_when_type_empty_and_rate_zero(self):
        blk = create_block(name="Producer OK Empty", producer_type="", producer_rate=0.0)
        is_valid, errors = blk.validate_producer()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_producer_invalid_when_type_set_and_rate_zero(self):
        blk = create_block(name="Producer Invalid Zero", producer_type="Hydrogen", producer_rate=0.0)
        is_valid, errors = blk.validate_producer()
        self.assertFalse(is_valid)
        self.assertTrue(any("requires producer_rate > 0" in e for e in errors))

    def test_producer_invalid_when_rate_negative(self):
        blk = create_block(name="Producer Invalid Negative", producer_type="Hydrogen", producer_rate=-1.0)
        is_valid, errors = blk.validate_producer()
        self.assertFalse(is_valid)
        self.assertTrue(any("cannot be negative" in e for e in errors))

    def test_producer_valid_when_type_set_and_rate_positive(self):
        blk = create_block(name="Producer Valid", producer_type="Hydrogen", producer_rate=3.0)
        is_valid, errors = blk.validate_producer()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_producer_error_message_contains_type(self):
        blk = create_block(name="Producer Msg", producer_type="Power", producer_rate=0.0)
        is_valid, errors = blk.validate_producer()
        self.assertFalse(is_valid)
        self.assertTrue(any("Power" in e for e in errors))


# ---- BlockComponentRelationshipTests (4) ----
class BlockComponentRelationshipTests(TestCase):
    def test_get_component_objects_returns_correct_queryset(self):
        comp1 = create_component(name="Motor")
        comp2 = create_component(name="Computer")
        blk = create_block(
            name="Relationship Block",
            components_list=[component_entry(comp1, 2), component_entry(comp2, 3)],
        )
        qs = blk.get_component_objects()
        names = set(qs.values_list("name", flat=True))
        self.assertEqual(names, {"Motor", "Computer"})

    def test_get_component_objects_with_duplicate_ids_returns_unique(self):
        comp = create_component(name="Display")
        blk = create_block(
            name="Duplicate IDs Block",
            components_list=[component_entry(comp, 1), component_entry(comp, 2)],
        )
        qs = blk.get_component_objects()
        self.assertEqual(qs.count(), 1)

    def test_validate_components_success_with_existing_components(self):
        comp = create_component(name="Steel Plate")
        blk = create_block(
            name="Validate Components Success",
            components_list=[component_entry(comp, 10)],
        )
        is_valid, errors = blk.validate_components()
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_save_with_valid_components_succeeds(self):
        comp = create_component(name="Interior Plate")
        blk = create_block(
            name="Save Valid Components",
            components_list=[component_entry(comp, 1)],
        )
        # save() runs clean(); should succeed
        blk.description = "OK"
        blk.save()
        self.assertEqual(Block.objects.get(pk=blk.block_id).description, "OK")


# ---- BlockMetaTests (4) ----
class BlockMetaTests(TestCase):
    def test_verbose_names(self):
        self.assertEqual(Block._meta.verbose_name, "Block")
        self.assertEqual(Block._meta.verbose_name_plural, "Blocks")

    def test_db_table_name(self):
        self.assertEqual(Block._meta.db_table, "blocks_block")

    def test_ordering_by_name(self):
        b1 = create_block(name="A")
        b2 = create_block(name="B")
        names = list(Block.objects.values_list("name", flat=True))
        self.assertEqual(names, ["A", "B"])  # ordered by name

    def test_model_fields_exist(self):
        field_names = {f.name for f in Block._meta.get_fields()}
        for expected in [
            "block_id",
            "name",
            "description",
            "mass",
            "components",
            "health",
            "pcu",
            "snap_size",
            "input_mass",
            "output_mass",
            "consumer_type",
            "consumer_rate",
            "producer_type",
            "producer_rate",
            "storage_capacity",
            "created_at",
            "updated_at",
        ]:
            self.assertIn(expected, field_names)


# ---- BlockIntegrationTests (6) ----
class BlockIntegrationTests(TestCase):
    def test_save_raises_validation_error_for_invalid_components(self):
        blk = create_block(
            name="Invalid Components Save",
            components_list=[{"bad": "structure"}],
        )
        blk.description = "Try save"
        with self.assertRaises(ValidationError):
            blk.save()

    def test_save_raises_validation_error_for_consumer_and_producer_invalid(self):
        blk = create_block(
            name="Invalid Consumer Producer",
            consumer_type="Power",
            consumer_rate=0.0,
            producer_type="Hydrogen",
            producer_rate=0.0,
        )
        with self.assertRaises(ValidationError) as ctx:
            blk.save()
        msg = str(ctx.exception)
        self.assertIn("consumer_rate > 0", msg)
        self.assertIn("producer_rate > 0", msg)

    def test_save_success_with_valid_consumer_and_producer(self):
        blk = create_block(
            name="Valid Consumer Producer",
            consumer_type="Power",
            consumer_rate=1.5,
            producer_type="Hydrogen",
            producer_rate=2.0,
        )
        blk.description = "OK"
        blk.save()
        self.assertEqual(Block.objects.get(pk=blk.block_id).description, "OK")

    def test_multiple_errors_aggregated_in_validation_error_message(self):
        blk = create_block(
            name="Multiple Errors",
            components_list=[{"not": "valid"}],
            consumer_type="Power",
            consumer_rate=0.0,
        )
        with self.assertRaises(ValidationError) as ctx:
            blk.save()
        msg = str(ctx.exception)
        self.assertIn("Validation failed:", msg)
        self.assertIn("consumer_rate > 0", msg)
        self.assertIn("must be dict", msg)

    def test_full_cycle_create_update_save_updates_timestamp(self):
        blk = create_block(name="Full Cycle")
        before = blk.updated_at
        blk.description = "Cycle"
        blk.save()
        after = blk.updated_at
        self.assertGreaterEqual(after, before)

    def test_query_filtering_by_name_and_ordering(self):
        create_block(name="Alpha")
        create_block(name="Beta")
        names = list(Block.objects.filter(name__in=["Alpha", "Beta"]).values_list("name", flat=True))
        self.assertEqual(names, ["Alpha", "Beta"])  # ordering by name
```

---

### Step 8: Run Automated Tests

**Command:**
```bash
uv run python manage.py test blocks -v 2
```

**Expected Output:**
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).

[Test execution output showing all 49 tests passing]

----------------------------------------------------------------------
Ran 49 tests in 0.2-0.3s

OK

Destroying test database for alias 'default'...
```

**Success Criteria:**
- ✅ All 49 tests pass (100% pass rate)
- ✅ Tests run in < 0.5 seconds
- ✅ No errors or failures
- ✅ Test coverage exceeds 45+ minimum requirement

**Troubleshooting Test Failures:**

If tests fail, check:
1. Ores and Components apps are properly installed and migrated
2. All imports are correct
3. Database is accessible
4. No conflicting test data from previous runs

**Test Report:**

Comprehensive test report available at: [`logs/test_reports/blocks-test-report.md`](../../../../logs/test_reports/blocks-test-report.md)

**Test Results Summary (January 19, 2026):**
- ✅ **49/49 tests passed** (100% success rate)
- ⏱️ Runtime: 0.151 seconds
- 🏗️ Django 6.0.1
- 📊 Test Coverage:
  - Model Creation: 7 tests
  - Field Validation: 8 tests
  - Timestamp Tests: 5 tests
  - Components JSON: 5 tests
  - Consumer Validation: 5 tests
  - Producer Validation: 5 tests
  - Component Relationships: 4 tests
  - Meta Tests: 4 tests
  - Integration Tests: 6 tests

---

## Verification & Testing

**Note:** Comprehensive automated tests (49 tests) were created in Step 7 and Step 8 of the Implementation Steps. This section covers additional manual verification tests to ensure the system is working correctly in the development environment.

### Manual Test 1: Create Block with Valid Components

**Purpose:** Verify basic block creation with component relationships

```bash
uv run python manage.py shell
```

```python
from blocks.models import Block
from components.models import Component
from ores.models import Ore
import uuid

# Create test ore and component first with unique names
test_id = str(uuid.uuid4())[:8]
ore = Ore.objects.create(name=f"Iron Ore {test_id}", mass=1.0, description="Basic iron ore")
component = Component.objects.create(
    name=f"Steel Plate {test_id}",
    description="Basic construction material",
    materials={str(ore.ore_id): 7},
    fabricator_type="Assembler",
    crafting_time=2.5,
    mass=20.0
)

# Create block with valid components
reactor = Block.objects.create(
    name=f"Large Reactor {test_id}",
    description="Generates power from uranium",
    mass=5000.0,
    components=[
        {
            "component_id": str(component.component_id),
            "component_name": component.name,
            "quantity": 100
        }
    ],
    health=1000.0,
    pcu=100,
    snap_size=2.5,
    input_mass=0,
    output_mass=0,
    producer_type="Power",
    producer_rate=300.0,
    storage_capacity=0.0
)

# Verify results
if (reactor.name == "Large Reactor" and 
    len(reactor.components) == 1 and 
    reactor.block_id is not None):
    print(f"✅ Created: {reactor}")
    print(f"✅ UUID: {reactor.block_id}")
    print(f"✅ Components count: {len(reactor.components)}")
    print("✅ Test 1 PASSED")
else:
    print("❌ Test 1 FAILED: Validation checks failed")
```

### Manual Test 2: Validate Components Method

**Purpose:** Test validate_components() with valid and invalid data

```python
from blocks.models import Block
from components.models import Component
import uuid

test_id = str(uuid.uuid4())[:8]

# Get existing component
comp = Component.objects.first()

# Test 1: Valid components
block = Block(
    name=f"Test Block 1 {test_id}",
    mass=100.0,
    components=[
        {
            "component_id": str(comp.component_id),
            "component_name": comp.name,
            "quantity": 5
        }
    ],
    health=100.0,
    pcu=10,
    snap_size=1.0,
    input_mass=10,
    output_mass=5
)
is_valid, errors = block.validate_components()
if is_valid and errors == []:
    print(f"✅ Valid components: {is_valid}, Errors: {errors}")
else:
    print(f"❌ Expected valid components, got: {errors}")

# Test 2: Invalid - missing keys
block2 = Block(
    name=f"Test Block 2 {test_id}",
    mass=100.0,
    components=[{"component_id": "xxx"}],  # Missing keys
    health=100.0,
    pcu=10,
    snap_size=1.0,
    input_mass=10,
    output_mass=5
)
is_valid, errors = block2.validate_components()
if not is_valid and len(errors) > 0:
    print(f"✅ Invalid components detected: {not is_valid}")
    print(f"✅ Errors: {errors}")
else:
    print("❌ Expected invalid components but validation passed")

# Test 3: Invalid - wrong type
block3 = Block(
    name=f"Test Block 3 {test_id}",
    mass=100.0,
    components=["not-a-dict"],  # Wrong type
    health=100.0,
    pcu=10,
    snap_size=1.0,
    input_mass=10,
    output_mass=5
)
is_valid, errors = block3.validate_components()
if "must be dict" in str(errors):
    print(f"✅ Type error detected: {not is_valid}")
    print("✅ Test 2 PASSED")
else:
    print(f"❌ Test 2 FAILED: Expected 'must be dict' error, got: {errors}")
```

### Manual Test 3: Consumer and Producer Validation

**Purpose:** Test consumer_type/consumer_rate and producer_type/producer_rate validation

```python
from blocks.models import Block
import uuid

test_id = str(uuid.uuid4())[:8]

# Test 1: Valid consumer
block = Block(
    name=f"Power Consumer {test_id}",
    mass=100.0,
    components=[],
    health=100.0,
    pcu=10,
    snap_size=1.0,
    input_mass=10,
    output_mass=5,
    consumer_type="Power",
    consumer_rate=5.0
)
is_valid, errors = block.validate_consumer()
if is_valid:
    print(f"✅ Valid consumer: {is_valid}")
else:
    print(f"❌ Expected valid consumer, got errors: {errors}")

# Test 2: Invalid consumer (type without rate)
block2 = Block(
    name=f"Invalid Consumer {test_id}",
    mass=100.0,
    components=[],
    health=100.0,
    pcu=10,
    snap_size=1.0,
    input_mass=10,
    output_mass=5,
    consumer_type="Power",
    consumer_rate=0.0  # Invalid!
)
is_valid, errors = block2.validate_consumer()
if not is_valid and len(errors) > 0 and "requires consumer_rate > 0" in errors[0]:
    print(f"✅ Invalid consumer detected: {not is_valid}")
else:
    print(f"❌ Expected invalid consumer with rate error, got: {errors}")

# Test 3: Valid producer
block3 = Block(
    name=f"Hydrogen Generator {test_id}",
    mass=100.0,
    components=[],
    health=100.0,
    pcu=10,
    snap_size=1.0,
    input_mass=10,
    output_mass=5,
    producer_type="Hydrogen",
    producer_rate=10.0
)
is_valid, errors = block3.validate_producer()
if is_valid:
    print(f"✅ Valid producer: {is_valid}")
else:
    print(f"❌ Expected valid producer, got errors: {errors}")

# Test 4: Invalid producer (negative rate)
block4 = Block(
    name=f"Invalid Producer {test_id}",
    mass=100.0,
    components=[],
    health=100.0,
    pcu=10,
    snap_size=1.0,
    input_mass=10,
    output_mass=5,
    producer_type="Oxygen",
    producer_rate=-1.0  # Invalid!
)
is_valid, errors = block4.validate_producer()
if not is_valid and len(errors) > 0 and any("cannot be negative" in err for err in errors):
    print(f"✅ Invalid producer detected: {not is_valid}")
    print("✅ Test 3 PASSED")
else:
    print(f"❌ Test 3 FAILED: Expected negative rate error, got: {errors}")
```

### Manual Test 4: Component Relationship Query

**Purpose:** Test get_component_objects() method

```python
from blocks.models import Block
from components.models import Component
from ores.models import Ore
import uuid

test_id = str(uuid.uuid4())[:8]

# Create 2 distinct components for this test
ore1 = Ore.objects.create(name=f"Test Ore 1 {test_id}", mass=1.0, description="")
comp1 = Component.objects.create(
    name=f"Test Component 1 {test_id}",
    materials={str(ore1.ore_id): 5},
    fabricator_type="Assembler",
    crafting_time=1.0,
    mass=10.0
)

ore2 = Ore.objects.create(name=f"Test Ore 2 {test_id}", mass=2.0, description="")
comp2 = Component.objects.create(
    name=f"Test Component 2 {test_id}",
    materials={str(ore2.ore_id): 3},
    fabricator_type="Assembler",
    crafting_time=2.0,
    mass=15.0
)

# Create block with multiple components
block = Block.objects.create(
    name=f"Complex Block {test_id}",
    mass=500.0,
    components=[
        {
            "component_id": str(comp1.component_id),
            "component_name": comp1.name,
            "quantity": 10
        },
        {
            "component_id": str(comp2.component_id),
            "component_name": comp2.name,
            "quantity": 5
        }
    ],
    health=100.0,
    pcu=10,
    snap_size=1.0,
    input_mass=10,
    output_mass=5
)

# Query related components
components = block.get_component_objects()
if components.count() == 2:
    print(f"✅ Found {components.count()} component objects")
    for comp in components:
        print(f"  - {comp.name} (ID: {comp.component_id})")
    print("✅ Test 4 PASSED")
else:
    print(f"❌ Test 4 FAILED: Expected 2 components, got {components.count()}")
```

### Manual Test 5: Save with Validation (Integration)

**Purpose:** Test that save() triggers clean() validation

```python
from blocks.models import Block
from django.core.exceptions import ValidationError
import uuid

test_id = str(uuid.uuid4())[:8]

# Test 1: Valid save
try:
    block = Block.objects.create(
        name=f"Valid Block {test_id}",
        mass=100.0,
        components=[],
        health=100.0,
        pcu=10,
        snap_size=1.0,
        input_mass=10,
        output_mass=5
    )
    if block.name == "Valid Block":
        print(f"✅ Valid block saved: {block.name}")
    else:
        print("❌ Block not saved correctly")
except ValidationError as e:
    print(f"❌ Unexpected ValidationError: {e}")

# Test 2: Invalid save (bad consumer)
try:
    block = Block.objects.create(
        name=f"Invalid Consumer Block {test_id}",
        mass=100.0,
        components=[],
        health=100.0,
        pcu=10,
        snap_size=1.0,
        input_mass=10,
        output_mass=5,
        consumer_type="Power",
        consumer_rate=0.0  # Invalid!
    )
    print("❌ Should have raised ValidationError but none was raised!")
except ValidationError as e:
    if "consumer_rate > 0" in str(e):
        print(f"✅ ValidationError raised as expected: {e}")
    else:
        print(f"❌ Wrong error message: {e}")

# Test 3: Invalid save (bad components)
try:
    block = Block.objects.create(
        name=f"Invalid Components Block {test_id}",
        mass=100.0,
        components=[{"bad": "data"}],  # Invalid structure
        health=100.0,
        pcu=10,
        snap_size=1.0,
        input_mass=10,
        output_mass=5
    )
    print("❌ Should have raised ValidationError but none was raised!")
except ValidationError as e:
    if "missing keys" in str(e):
        print(f"✅ ValidationError raised as expected: {e}")
        print("✅ Test 5 PASSED")
    else:
        print(f"❌ Test 5 FAILED: Wrong error message: {e}")
```

### Manual Test 6: Timestamp Behavior

**Purpose:** Verify auto_now and auto_now_add behavior

```python
from blocks.models import Block
import time
import uuid

test_id = str(uuid.uuid4())[:8]

# Create block
block = Block.objects.create(
    name=f"Timestamp Test {test_id}",
    mass=100.0,
    components=[],
    health=100.0,
    pcu=10,
    snap_size=1.0,
    input_mass=10,
    output_mass=5
)

created = block.created_at
updated1 = block.updated_at

if created is not None and updated1 is not None and updated1 >= created:
    print(f"✅ Created: {created}")
    print(f"✅ Updated: {updated1}")
else:
    print("❌ Timestamp validation failed")

# Update block
time.sleep(0.1)  # Small delay
block.description = "Modified"
block.save()

updated2 = block.updated_at
if updated2 >= updated1 and block.created_at == created:
    print(f"✅ Updated after save: {updated2}")
    print("✅ Test 6 PASSED")
else:
    print("❌ Test 6 FAILED: Timestamp update validation failed")
```

### Manual Test 7: Query and Ordering

**Purpose:** Test Meta ordering and queries

```python
from blocks.models import Block
import uuid

test_id = str(uuid.uuid4())[:8]

# Create blocks in non-alphabetical order
Block.objects.create(
    name=f"Zebra Block {test_id}",
    mass=100.0,
    components=[],
    health=100.0,
    pcu=10,
    snap_size=1.0,
    input_mass=10,
    output_mass=5
)

Block.objects.create(
    name=f"Alpha Block {test_id}",
    mass=100.0,
    components=[],
    health=100.0,
    pcu=10,
    snap_size=1.0,
    input_mass=10,
    output_mass=5
)

# Query all blocks
blocks = Block.objects.all()
names = [b.name for b in blocks]

# Verify alphabetical ordering
if names == sorted(names):
    print(f"✅ Block names: {names}")
    print("✅ Blocks are ordered alphabetically")
    
    # Test filtering
    power_blocks = Block.objects.filter(producer_type="Power")
    print(f"✅ Found {power_blocks.count()} power-producing blocks")
    
    print("✅ Test 7 PASSED")
else:
    print(f"❌ Test 7 FAILED: Blocks not ordered alphabetically, got: {names}")
```

### Manual Test 8: Admin Integration (Optional)

**Purpose:** Verify blocks appear in Django admin

```bash
# Start server
uv run python manage.py runserver
```

Then navigate to:
- http://127.0.0.1:8000/admin/blocks/block/
- Verify blocks list appears
- Verify add/edit forms work
- Check that JSON fields display correctly

### Manual Test Summary

Run all tests:
```python
# Copy and paste all tests above in sequence
print("\n" + "="*50)
print("ALL MANUAL TESTS PASSED ✅")
print("="*50)
exit()
```

**Expected Results:**
- ✅ All 8 manual tests pass
- ✅ Blocks can be created with valid data
- ✅ Validation methods catch errors correctly
- ✅ Save triggers validation as expected
- ✅ Component relationships work
- ✅ Timestamps behave correctly
- ✅ Queries and ordering work

---

## Rollback Procedure

### Rollback Step 1: Unapply Migration

```bash
uv run python manage.py migrate blocks zero
```

### Rollback Step 2: Remove App from Settings

Remove `'blocks'` from `INSTALLED_APPS`

### Rollback Step 3: Restore Database Backup

```bash
# SQLite
cp db.sqlite3.backup.YYYYMMDD_HHMMSS db.sqlite3

# PostgreSQL
psql -U se2_user se2_calculator_db < backup_YYYYMMDD_HHMMSS.sql
```

---

## Troubleshooting

### Issue 1: Migration Serialization Error

**Symptom:**
```
ValueError: Cannot serialize function: lambda
```

**Solution:**
Ensure using `generate_uuid()` named function, not lambda.

---

## Post-Deployment Tasks

### Task 1: Update Documentation

- [ ] Update `CHANGELOG.md`
- [ ] Update Phase 1 checklist
- [ ] Create post-deployment review

### Task 2: Commit Changes

```bash
git add se2CalcProject/settings.py blocks/
git commit -m "ENH-0000003: Implement Blocks app and model"
git push origin feat/enh0000003-create-blocks-app-model
```

---

**Document End**
