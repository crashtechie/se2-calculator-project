# Data Migration & Transformation

## When to Activate This Skill

- Migrating data between schema versions
- Transforming existing data in the database
- Importing data from external sources
- Performing bulk data updates
- Cleaning up or normalizing data
- Backfilling new fields with calculated values

## Django Data Migrations

### Creating Data Migrations
```python
# Generate empty migration
python manage.py makemigrations --empty myapp --name populate_default_values

# migrations/0005_populate_default_values.py
from django.db import migrations

def populate_defaults(apps, schema_editor):
    """Forward migration: populate default values"""
    Block = apps.get_model('blocks', 'Block')
    for block in Block.objects.filter(efficiency__isnull=True):
        if block.input_mass and block.output_mass:
            block.efficiency = (block.output_mass / block.input_mass) * 100
            block.save()

def reverse_populate(apps, schema_editor):
    """Reverse migration: clear values"""
    Block = apps.get_model('blocks', 'Block')
    Block.objects.all().update(efficiency=None)

class Migration(migrations.Migration):
    dependencies = [
        ('blocks', '0004_add_efficiency_field'),
    ]
    
    operations = [
        migrations.RunPython(populate_defaults, reverse_populate),
    ]
```

### Safe Data Migration Pattern
```python
from django.db import migrations, transaction

def migrate_component_data(apps, schema_editor):
    """Migrate component data with error handling"""
    Component = apps.get_model('components', 'Component')
    
    # Process in batches to avoid memory issues
    batch_size = 1000
    total = Component.objects.count()
    
    for offset in range(0, total, batch_size):
        with transaction.atomic():
            components = Component.objects.all()[offset:offset + batch_size]
            for component in components:
                try:
                    # Transform data
                    component.normalized_name = component.name.lower().strip()
                    component.save(update_fields=['normalized_name'])
                except Exception as e:
                    # Log error but continue
                    print(f"Error migrating component {component.id}: {e}")

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(migrate_component_data, migrations.RunPython.noop),
    ]
```

### Conditional Data Migration
```python
def conditional_migration(apps, schema_editor):
    """Only migrate if conditions are met"""
    Block = apps.get_model('blocks', 'Block')
    
    # Check if migration is needed
    if not Block.objects.filter(status='legacy').exists():
        print("No legacy blocks found, skipping migration")
        return
    
    # Perform migration
    legacy_blocks = Block.objects.filter(status='legacy')
    for block in legacy_blocks:
        block.status = 'active'
        block.migrated_at = timezone.now()
        block.save()
    
    print(f"Migrated {legacy_blocks.count()} legacy blocks")
```

## Bulk Data Operations

### Bulk Update with bulk_update()
```python
from django.db import transaction

def update_block_masses():
    """Bulk update block masses"""
    blocks = Block.objects.all()
    
    # Modify objects in memory
    for block in blocks:
        block.total_mass = block.input_mass + block.output_mass
        block.updated_at = timezone.now()
    
    # Single database operation
    Block.objects.bulk_update(
        blocks,
        ['total_mass', 'updated_at'],
        batch_size=500
    )
```

### Bulk Create with bulk_create()
```python
def import_components_from_csv(csv_file):
    """Import components from CSV file"""
    import csv
    
    components = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            components.append(Component(
                name=row['name'],
                mass=float(row['mass']),
                volume=float(row['volume']),
            ))
    
    # Bulk insert
    Component.objects.bulk_create(components, batch_size=1000)
    print(f"Imported {len(components)} components")
```

### Update with F() Expressions
```python
from django.db.models import F

def increment_usage_counts():
    """Update fields based on existing values"""
    # Single query, no race conditions
    Block.objects.filter(is_active=True).update(
        usage_count=F('usage_count') + 1,
        last_used=timezone.now()
    )

def calculate_efficiency():
    """Calculate field from other fields"""
    Block.objects.update(
        efficiency=(F('output_mass') / F('input_mass')) * 100
    )
```

## Data Transformation

### JSON Field Transformation
```python
def transform_json_structure(apps, schema_editor):
    """Transform JSON field structure"""
    Block = apps.get_model('blocks', 'Block')
    
    for block in Block.objects.all():
        if block.components:
            # Old format: {"iron": 10, "steel": 5}
            # New format: [{"name": "iron", "quantity": 10}, ...]
            old_data = block.components
            new_data = [
                {"name": name, "quantity": qty}
                for name, qty in old_data.items()
            ]
            block.components = new_data
            block.save(update_fields=['components'])
```

### String Normalization
```python
def normalize_names(apps, schema_editor):
    """Normalize string fields"""
    Component = apps.get_model('components', 'Component')
    
    for component in Component.objects.all():
        # Normalize name
        normalized = component.name.strip().title()
        
        # Remove extra whitespace
        normalized = ' '.join(normalized.split())
        
        if normalized != component.name:
            component.name = normalized
            component.save(update_fields=['name'])
```

### Data Deduplication
```python
from django.db.models import Count

def remove_duplicate_components(apps, schema_editor):
    """Remove duplicate components, keeping the oldest"""
    Component = apps.get_model('components', 'Component')
    
    # Find duplicates
    duplicates = (
        Component.objects
        .values('name')
        .annotate(count=Count('id'))
        .filter(count__gt=1)
    )
    
    for dup in duplicates:
        # Get all instances with this name
        components = Component.objects.filter(name=dup['name']).order_by('created_at')
        
        # Keep first, delete rest
        keep = components.first()
        to_delete = components.exclude(id=keep.id)
        
        # Update foreign keys to point to kept instance
        Block.objects.filter(component__in=to_delete).update(component=keep)
        
        # Delete duplicates
        to_delete.delete()
```

## External Data Import

### CSV Import
```python
import csv
from django.db import transaction

def import_from_csv(file_path):
    """Import data from CSV with validation"""
    imported = 0
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row_num, row in enumerate(reader, start=2):
            try:
                with transaction.atomic():
                    # Validate data
                    if not row.get('name'):
                        raise ValueError("Name is required")
                    
                    mass = float(row.get('mass', 0))
                    if mass <= 0:
                        raise ValueError("Mass must be positive")
                    
                    # Create object
                    Component.objects.create(
                        name=row['name'],
                        mass=mass,
                        volume=float(row.get('volume', 0)),
                        description=row.get('description', '')
                    )
                    imported += 1
            
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
    
    return {
        'imported': imported,
        'errors': errors
    }
```

### JSON Import
```python
import json

def import_from_json(file_path):
    """Import data from JSON file"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    blocks = []
    for item in data['blocks']:
        # Get or create related objects
        component, _ = Component.objects.get_or_create(
            name=item['component_name'],
            defaults={'mass': item.get('component_mass', 0)}
        )
        
        blocks.append(Block(
            name=item['name'],
            component=component,
            input_mass=item['input_mass'],
            output_mass=item['output_mass']
        ))
    
    Block.objects.bulk_create(blocks, ignore_conflicts=True)
```

### API Data Import
```python
import requests
from django.core.cache import cache

def import_from_api(api_url):
    """Import data from external API"""
    # Check cache first
    cache_key = f'api_import_{api_url}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        data = cached_data
    else:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        cache.set(cache_key, data, timeout=3600)
    
    # Process data
    components = []
    for item in data['components']:
        components.append(Component(
            name=item['name'],
            mass=item['mass'],
            external_id=item['id']
        ))
    
    # Use update_or_create for idempotency
    for comp_data in data['components']:
        Component.objects.update_or_create(
            external_id=comp_data['id'],
            defaults={
                'name': comp_data['name'],
                'mass': comp_data['mass']
            }
        )
```

## Data Export

### CSV Export
```python
import csv
from django.http import HttpResponse

def export_to_csv(request):
    """Export data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="blocks.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Component', 'Input Mass', 'Output Mass'])
    
    blocks = Block.objects.select_related('component').all()
    for block in blocks:
        writer.writerow([
            block.id,
            block.name,
            block.component.name if block.component else '',
            block.input_mass,
            block.output_mass
        ])
    
    return response
```

### JSON Export
```python
from django.core.serializers import serialize
from django.http import JsonResponse

def export_to_json(request):
    """Export data to JSON"""
    blocks = Block.objects.select_related('component').all()
    
    data = []
    for block in blocks:
        data.append({
            'id': block.id,
            'name': block.name,
            'component': {
                'id': block.component.id,
                'name': block.component.name
            } if block.component else None,
            'input_mass': float(block.input_mass),
            'output_mass': float(block.output_mass),
        })
    
    return JsonResponse({'blocks': data})
```

## Data Validation and Cleanup

### Validate Existing Data
```python
def validate_block_data():
    """Find and report data inconsistencies"""
    issues = []
    
    # Check for negative masses
    invalid_mass = Block.objects.filter(
        models.Q(input_mass__lt=0) | models.Q(output_mass__lt=0)
    )
    if invalid_mass.exists():
        issues.append(f"Found {invalid_mass.count()} blocks with negative mass")
    
    # Check for orphaned records
    orphaned = Block.objects.filter(component__isnull=True)
    if orphaned.exists():
        issues.append(f"Found {orphaned.count()} blocks without components")
    
    # Check for efficiency > 100%
    inefficient = Block.objects.filter(output_mass__gt=F('input_mass'))
    if inefficient.exists():
        issues.append(f"Found {inefficient.count()} blocks with output > input")
    
    return issues
```

### Clean Up Data
```python
def cleanup_invalid_data():
    """Remove or fix invalid data"""
    # Delete blocks with invalid data
    Block.objects.filter(
        input_mass__lte=0,
        output_mass__lte=0
    ).delete()
    
    # Fix blocks with missing components
    default_component = Component.objects.get(name='Default')
    Block.objects.filter(component__isnull=True).update(
        component=default_component
    )
    
    # Cap efficiency at 100%
    Block.objects.filter(
        output_mass__gt=F('input_mass')
    ).update(
        output_mass=F('input_mass')
    )
```


## Advanced Migration Patterns

### Multi-Step Migration
```python
# Step 1: Add new field (0010_add_new_field.py)
class Migration(migrations.Migration):
    operations = [
        migrations.AddField('Block', 'new_field', models.CharField(null=True)),
    ]

# Step 2: Populate new field (0011_populate_new_field.py)
def populate_new_field(apps, schema_editor):
    Block = apps.get_model('blocks', 'Block')
    Block.objects.all().update(new_field='default_value')

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(populate_new_field),
    ]

# Step 3: Make field non-nullable (0012_make_field_required.py)
class Migration(migrations.Migration):
    operations = [
        migrations.AlterField('Block', 'new_field', models.CharField(null=False)),
    ]
```

### Reversible Complex Migration
```python
def forward_migration(apps, schema_editor):
    """Split full_name into first_name and last_name"""
    User = apps.get_model('auth', 'User')
    for user in User.objects.all():
        if user.full_name:
            parts = user.full_name.split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''
            user.save(update_fields=['first_name', 'last_name'])

def reverse_migration(apps, schema_editor):
    """Combine first_name and last_name back to full_name"""
    User = apps.get_model('auth', 'User')
    for user in User.objects.all():
        user.full_name = f"{user.first_name} {user.last_name}".strip()
        user.save(update_fields=['full_name'])

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(forward_migration, reverse_migration),
    ]
```

### Migration with External Dependencies
```python
def migrate_with_api_data(apps, schema_editor):
    """Migrate data using external API"""
    import requests
    
    Component = apps.get_model('components', 'Component')
    
    # Fetch reference data from API
    response = requests.get('https://api.example.com/components')
    api_data = {item['name']: item for item in response.json()}
    
    for component in Component.objects.all():
        if component.name in api_data:
            api_item = api_data[component.name]
            component.external_id = api_item['id']
            component.category = api_item['category']
            component.save(update_fields=['external_id', 'category'])
```

## Performance Optimization

### Batch Processing
```python
from django.db import transaction

def process_large_dataset():
    """Process large dataset in batches"""
    batch_size = 1000
    queryset = Block.objects.all()
    total = queryset.count()
    
    for offset in range(0, total, batch_size):
        batch = queryset[offset:offset + batch_size]
        
        with transaction.atomic():
            for block in batch:
                # Process each block
                block.processed = True
                block.save(update_fields=['processed'])
        
        print(f"Processed {min(offset + batch_size, total)}/{total}")
```

### Iterator for Memory Efficiency
```python
def process_with_iterator():
    """Use iterator to avoid loading all objects into memory"""
    for block in Block.objects.iterator(chunk_size=500):
        # Process one at a time
        block.calculate_efficiency()
        block.save()
```

### Raw SQL for Complex Operations
```python
from django.db import connection

def complex_data_transformation():
    """Use raw SQL for complex transformations"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE blocks_block
            SET efficiency = (output_mass / NULLIF(input_mass, 0)) * 100
            WHERE input_mass > 0
        """)
        
        rows_updated = cursor.rowcount
        print(f"Updated {rows_updated} rows")
```

## Testing Data Migrations

### Testing Migration Functions
```python
from django.test import TestCase
from django.apps import apps
from django.db import connection
from django.db.migrations.executor import MigrationExecutor

class MigrationTest(TestCase):
    """Test data migration"""
    
    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name
    
    migrate_from = [('blocks', '0004_add_efficiency_field')]
    migrate_to = [('blocks', '0005_populate_efficiency')]
    
    def setUp(self):
        # Migrate to state before data migration
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        
        # Create test data in old state
        Block = apps.get_model('blocks', 'Block')
        self.block = Block.objects.create(
            name='Test Block',
            input_mass=100,
            output_mass=90
        )
    
    def test_migration(self):
        # Run migration
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_to)
        
        # Check results
        Block = apps.get_model('blocks', 'Block')
        block = Block.objects.get(id=self.block.id)
        self.assertEqual(block.efficiency, 90.0)
```

### Testing Import Functions
```python
import tempfile
import csv

class ImportTest(TestCase):
    def test_csv_import(self):
        """Test CSV import function"""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'mass', 'volume'])
            writer.writerow(['Component 1', '10.5', '5.0'])
            writer.writerow(['Component 2', '20.0', '10.0'])
            temp_file = f.name
        
        # Import data
        result = import_from_csv(temp_file)
        
        # Verify
        self.assertEqual(result['imported'], 2)
        self.assertEqual(Component.objects.count(), 2)
        
        # Cleanup
        os.unlink(temp_file)
```

## Best Practices

### Data Migration Guidelines
- Always provide reverse migrations when possible
- Test migrations on a copy of production data
- Process large datasets in batches
- Use transactions for data consistency
- Log progress for long-running migrations
- Handle errors gracefully
- Make migrations idempotent when possible

### Import/Export Guidelines
- Validate data before importing
- Use transactions for atomicity
- Provide detailed error messages
- Handle encoding issues (UTF-8)
- Sanitize user input
- Use bulk operations for performance
- Implement progress tracking for large imports

### Performance Considerations
- Use bulk_create() and bulk_update() for multiple records
- Process large datasets in batches
- Use select_related() and prefetch_related()
- Consider using raw SQL for complex operations
- Use database indexes for frequently queried fields
- Monitor memory usage with large datasets

### Safety Measures
- Always backup data before migrations
- Test migrations in development first
- Use staging environment for final testing
- Have rollback plan ready
- Monitor migration progress
- Set timeouts for long operations
- Validate data after migration

## Common Pitfalls

### Not Using Transactions
```python
# Bad: No transaction, partial updates on error
for block in Block.objects.all():
    block.efficiency = calculate_efficiency(block)
    block.save()  # If this fails, previous saves are committed

# Good: Use transaction
from django.db import transaction

with transaction.atomic():
    for block in Block.objects.all():
        block.efficiency = calculate_efficiency(block)
        block.save()
```

### Loading Too Much Data
```python
# Bad: Loads all objects into memory
blocks = Block.objects.all()
for block in blocks:
    process(block)

# Good: Use iterator
for block in Block.objects.iterator(chunk_size=500):
    process(block)
```

### Not Handling Duplicates
```python
# Bad: Fails on duplicate key
Component.objects.create(name='Iron Ore')

# Good: Handle duplicates
Component.objects.get_or_create(
    name='Iron Ore',
    defaults={'mass': 1.0}
)

# Or use update_or_create
Component.objects.update_or_create(
    name='Iron Ore',
    defaults={'mass': 1.0, 'volume': 0.5}
)
```

### Ignoring Data Validation
```python
# Bad: No validation
for row in csv_data:
    Component.objects.create(**row)

# Good: Validate before creating
for row in csv_data:
    try:
        mass = float(row['mass'])
        if mass <= 0:
            raise ValueError("Mass must be positive")
        
        Component.objects.create(
            name=row['name'],
            mass=mass
        )
    except (ValueError, KeyError) as e:
        logger.error(f"Invalid row: {row}, error: {e}")
```

## Monitoring and Logging

### Progress Tracking
```python
import logging

logger = logging.getLogger(__name__)

def migrate_with_progress():
    """Migration with progress logging"""
    total = Block.objects.count()
    processed = 0
    batch_size = 1000
    
    logger.info(f"Starting migration of {total} blocks")
    
    for offset in range(0, total, batch_size):
        batch = Block.objects.all()[offset:offset + batch_size]
        
        for block in batch:
            # Process block
            processed += 1
            
            if processed % 100 == 0:
                logger.info(f"Progress: {processed}/{total} ({processed/total*100:.1f}%)")
    
    logger.info(f"Migration complete: {processed} blocks processed")
```

### Error Tracking
```python
def import_with_error_tracking(file_path):
    """Import with detailed error tracking"""
    stats = {
        'total': 0,
        'success': 0,
        'errors': []
    }
    
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        
        for row_num, row in enumerate(reader, start=2):
            stats['total'] += 1
            
            try:
                Component.objects.create(**row)
                stats['success'] += 1
            except Exception as e:
                error_msg = f"Row {row_num}: {str(e)}"
                stats['errors'].append(error_msg)
                logger.error(error_msg)
    
    logger.info(f"Import complete: {stats['success']}/{stats['total']} successful")
    return stats
```

## Resources

- [Django Migrations Documentation](https://docs.djangoproject.com/en/stable/topics/migrations/)
- [Django Data Migration Guide](https://docs.djangoproject.com/en/stable/topics/migrations/#data-migrations)
- [Bulk Operations](https://docs.djangoproject.com/en/stable/ref/models/querysets/#bulk-create)
- [Django Import/Export](https://django-import-export.readthedocs.io/)
