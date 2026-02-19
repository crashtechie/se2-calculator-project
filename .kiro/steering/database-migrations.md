---
inclusion: auto
fileMatchPattern: '**/migrations/*.py'
description: Database migration best practices including creation, review, testing, and deployment strategies
---

# Database Migrations Best Practices

## Project Context

Space Engineers 2 Calculator uses:
- **PostgreSQL** in production (Docker)
- **SQLite** for development fallback
- **UUIDv7** primary keys across all models
- **JSONField** for flexible relationships
- **Explicit table names** (e.g., `blocks_block`, `components_component`)

## Migration Workflow

### Creating Migrations

```bash
# Check for model changes
python manage.py makemigrations --dry-run --verbosity 3

# Create migrations
python manage.py makemigrations

# Create migration for specific app
python manage.py makemigrations blocks

# Create empty migration for data migration
python manage.py makemigrations --empty blocks --name migrate_component_format
```

### Reviewing Migrations

**ALWAYS review generated migrations before applying!**

```bash
# View SQL that will be executed
python manage.py sqlmigrate blocks 0001

# Check migration status
python manage.py showmigrations

# Check for migration conflicts
python manage.py makemigrations --check
```

### Applying Migrations

```bash
# Apply all migrations
python manage.py migrate

# Apply specific app migrations
python manage.py migrate blocks

# Apply up to specific migration
python manage.py migrate blocks 0003

# Fake migration (mark as applied without running)
python manage.py migrate blocks 0001 --fake

# Rollback to previous migration
python manage.py migrate blocks 0002
```

## Migration Best Practices

### 1. One Logical Change Per Migration

```python
# GOOD: Single focused change
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='block',
            name='tier',
            field=models.IntegerField(default=1),
        ),
    ]

# BAD: Multiple unrelated changes
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(model_name='block', name='tier', ...),
        migrations.AddField(model_name='component', name='rarity', ...),
        migrations.AlterField(model_name='ore', name='mass', ...),
    ]
```

### 2. Provide Default Values

```python
# GOOD: Provide default for new non-nullable field
migrations.AddField(
    model_name='block',
    name='tier',
    field=models.IntegerField(default=1),
)

# GOOD: Make field nullable initially
migrations.AddField(
    model_name='block',
    name='category',
    field=models.CharField(max_length=50, null=True, blank=True),
)
```

### 3. Use Explicit Table Names

```python
# Project standard: Explicit db_table in Meta
class Block(models.Model):
    class Meta:
        db_table = 'blocks_block'  # Explicit table name

# Migration will use this table name
migrations.CreateModel(
    name='Block',
    options={
        'db_table': 'blocks_block',
    },
)
```

### 4. Handle JSONField Defaults Carefully

```python
# GOOD: Use dict for JSONField default
components = models.JSONField(
    default=dict,  # Callable, not dict()
    blank=True,
)

# BAD: Mutable default
components = models.JSONField(
    default={},  # Shared across instances!
)

# In migration
migrations.AddField(
    model_name='block',
    name='components',
    field=models.JSONField(default=dict, blank=True),
)
```

## Data Migrations

### Creating Data Migrations

```python
# Create empty migration
python manage.py makemigrations --empty blocks --name migrate_component_format

# Edit migration file
from django.db import migrations

def migrate_component_format(apps, schema_editor):
    """Convert component format from list to dict."""
    Block = apps.get_model('blocks', 'Block')
    
    for block in Block.objects.all():
        if isinstance(block.components, list):
            # Convert list to dict format
            new_components = {}
            for item in block.components:
                comp_id = item.get('component_id')
                quantity = item.get('quantity', 1)
                new_components[comp_id] = quantity
            
            block.components = new_components
            block.save(update_fields=['components'])

def reverse_migration(apps, schema_editor):
    """Reverse the migration."""
    Block = apps.get_model('blocks', 'Block')
    
    for block in Block.objects.all():
        if isinstance(block.components, dict):
            # Convert dict back to list
            new_components = []
            for comp_id, quantity in block.components.items():
                new_components.append({
                    'component_id': comp_id,
                    'quantity': quantity
                })
            
            block.components = new_components
            block.save(update_fields=['components'])

class Migration(migrations.Migration):
    dependencies = [
        ('blocks', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(migrate_component_format, reverse_migration),
    ]
```

### Data Migration Best Practices

```python
# GOOD: Use apps.get_model() not direct imports
def migrate_data(apps, schema_editor):
    Block = apps.get_model('blocks', 'Block')  # Historical model
    # Work with Block

# BAD: Direct import
from blocks.models import Block  # Don't do this!

# GOOD: Provide reverse migration
migrations.RunPython(forward_func, reverse_func)

# GOOD: Handle large datasets in batches
def migrate_large_dataset(apps, schema_editor):
    Block = apps.get_model('blocks', 'Block')
    
    batch_size = 1000
    blocks = Block.objects.all()
    total = blocks.count()
    
    for i in range(0, total, batch_size):
        batch = blocks[i:i + batch_size]
        for block in batch:
            # Process block
            block.save(update_fields=['field_name'])
```

## Migration Patterns

### Adding Fields

```python
# Add nullable field
migrations.AddField(
    model_name='block',
    name='category',
    field=models.CharField(max_length=50, null=True, blank=True),
)

# Add field with default
migrations.AddField(
    model_name='block',
    name='tier',
    field=models.IntegerField(default=1),
)

# Add field then populate
class Migration(migrations.Migration):
    operations = [
        # Step 1: Add nullable field
        migrations.AddField(
            model_name='block',
            name='category',
            field=models.CharField(max_length=50, null=True),
        ),
        # Step 2: Populate data
        migrations.RunPython(populate_categories),
        # Step 3: Make non-nullable
        migrations.AlterField(
            model_name='block',
            name='category',
            field=models.CharField(max_length=50),
        ),
    ]
```

### Removing Fields

```python
# Safe removal in steps
class Migration(migrations.Migration):
    operations = [
        # Step 1: Make field nullable (deploy this first)
        migrations.AlterField(
            model_name='block',
            name='old_field',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

# Later migration after code deployed
class Migration(migrations.Migration):
    operations = [
        # Step 2: Remove field (deploy after code updated)
        migrations.RemoveField(
            model_name='block',
            name='old_field',
        ),
    ]
```

### Renaming Fields

```python
# Use RenameField for simple renames
migrations.RenameField(
    model_name='block',
    old_name='pcu_cost',
    new_name='pcu',
)

# For complex renames, use multi-step approach
class Migration(migrations.Migration):
    operations = [
        # Step 1: Add new field
        migrations.AddField(
            model_name='block',
            name='new_name',
            field=models.IntegerField(null=True),
        ),
        # Step 2: Copy data
        migrations.RunPython(copy_field_data),
        # Step 3: Remove old field (in next migration)
    ]
```

### Adding Indexes

```python
# Add index to existing field
migrations.AddIndex(
    model_name='block',
    index=models.Index(fields=['name'], name='blocks_name_idx'),
)

# Add composite index
migrations.AddIndex(
    model_name='buildorder',
    index=models.Index(fields=['name', '-created_at'], name='buildorder_name_created_idx'),
)

# Project uses Meta.indexes
class Meta:
    indexes = [
        models.Index(fields=['name']),
        models.Index(fields=['-created_at']),
    ]
```

## Testing Migrations

### Test Migration Forward and Backward

```bash
# Apply migration
python manage.py migrate blocks 0003

# Test the change
python manage.py shell
# ... test functionality

# Rollback
python manage.py migrate blocks 0002

# Test rollback worked
python manage.py shell
# ... verify data intact
```

### Test with Production-Like Data

```python
# Create test data
python manage.py loaddata sample_ores sample_components sample_blocks

# Apply migration
python manage.py migrate

# Verify data integrity
python manage.py shell
>>> from blocks.models import Block
>>> Block.objects.all().count()
>>> # Check data looks correct
```

### Automated Migration Tests

```python
# tests/test_migrations.py
from django.test import TestCase
from django.core.management import call_command

class MigrationTestCase(TestCase):
    def test_migration_0002_component_format(self):
        """Test component format migration."""
        # Load initial data
        call_command('loaddata', 'test_blocks.json')
        
        # Apply migration
        call_command('migrate', 'blocks', '0002')
        
        # Verify migration worked
        from blocks.models import Block
        block = Block.objects.first()
        assert isinstance(block.components, dict)
```

## Migration Deployment

### Deployment Checklist

```bash
# 1. Review migration SQL
python manage.py sqlmigrate blocks 0003

# 2. Backup database
pg_dump se2calc > backup_$(date +%Y%m%d_%H%M%S).sql

# 3. Test migration on staging
python manage.py migrate --plan
python manage.py migrate

# 4. Verify application works
python manage.py check
python manage.py test

# 5. Deploy to production
# - Apply migrations before deploying code
# - Monitor for errors
# - Have rollback plan ready
```

### Zero-Downtime Migrations

```python
# Phase 1: Add new field (nullable)
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='block',
            name='new_field',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
# Deploy code that writes to both old and new fields

# Phase 2: Backfill data
class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(backfill_new_field),
    ]
# Deploy and run migration

# Phase 3: Make field non-nullable
class Migration(migrations.Migration):
    operations = [
        migrations.AlterField(
            model_name='block',
            name='new_field',
            field=models.CharField(max_length=100),
        ),
    ]
# Deploy code that only uses new field

# Phase 4: Remove old field
class Migration(migrations.Migration):
    operations = [
        migrations.RemoveField(
            model_name='block',
            name='old_field',
        ),
    ]
```

## Troubleshooting Migrations

### Fake Migrations

```bash
# Mark migration as applied without running
python manage.py migrate blocks 0001 --fake

# Fake initial migration (when table already exists)
python manage.py migrate blocks 0001_initial --fake-initial
```

### Reset Migrations (Development Only!)

```bash
# WARNING: Destroys data!

# 1. Delete migration files (keep __init__.py)
rm blocks/migrations/0*.py

# 2. Drop tables
python manage.py dbshell
DROP TABLE blocks_block;

# 3. Recreate migrations
python manage.py makemigrations

# 4. Apply migrations
python manage.py migrate
```

### Squash Migrations

```bash
# Combine multiple migrations into one
python manage.py squashmigrations blocks 0001 0005

# Review squashed migration
# Test thoroughly
# Delete old migrations after deploying
```

## Migration Checklist

### Before Creating Migration
- [ ] Review model changes
- [ ] Consider backward compatibility
- [ ] Plan for data migration if needed
- [ ] Check for default values

### After Creating Migration
- [ ] Review generated migration file
- [ ] Check SQL with sqlmigrate
- [ ] Test migration forward
- [ ] Test migration backward (if reversible)
- [ ] Test with realistic data
- [ ] Document breaking changes

### Before Deploying
- [ ] Backup production database
- [ ] Test on staging environment
- [ ] Review deployment plan
- [ ] Prepare rollback plan
- [ ] Schedule maintenance window if needed

### After Deploying
- [ ] Verify migration applied successfully
- [ ] Check application functionality
- [ ] Monitor for errors
- [ ] Verify data integrity
- [ ] Update documentation

## Common Migration Issues

### Issue: Migration Conflicts

```bash
# Check for conflicts
python manage.py makemigrations --check

# Merge migrations
python manage.py makemigrations --merge
```

### Issue: Circular Dependencies

```python
# Use string references for foreign keys
class Block(models.Model):
    category = models.ForeignKey(
        'categories.Category',  # String reference
        on_delete=models.CASCADE
    )
```

### Issue: Large Table Migrations

```python
# For large tables, consider:
# 1. Add index concurrently (PostgreSQL)
migrations.RunSQL(
    "CREATE INDEX CONCURRENTLY blocks_name_idx ON blocks_block (name);",
    reverse_sql="DROP INDEX blocks_name_idx;"
)

# 2. Batch data migrations
def migrate_in_batches(apps, schema_editor):
    Block = apps.get_model('blocks', 'Block')
    batch_size = 1000
    
    for i in range(0, Block.objects.count(), batch_size):
        blocks = Block.objects.all()[i:i + batch_size]
        for block in blocks:
            # Process
            pass
```

## Project-Specific Patterns

### UUIDv7 Primary Keys

```python
# Always use generate_uuid function
import blocks.models

migrations.CreateModel(
    name='Block',
    fields=[
        ('block_id', models.UUIDField(
            primary_key=True,
            default=blocks.models.generate_uuid,
            editable=False,
        )),
    ],
)
```

### JSONField Migrations

```python
# Changing JSONField structure requires data migration
class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(
            migrate_json_structure,
            reverse_migrate_json_structure
        ),
    ]
```

### Explicit Table Names

```python
# Always specify db_table in Meta
class Meta:
    db_table = 'app_modelname'  # Prevents migration issues
```
