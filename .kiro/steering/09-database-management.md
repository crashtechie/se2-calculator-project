# Database Management

## Migration Best Practices

### Creating Migrations
```bash
# Generate migrations for all apps
uv run python app/manage.py makemigrations

# Generate for specific app
uv run python app/manage.py makemigrations ores

# Dry run to preview SQL
uv run python app/manage.py sqlmigrate ores 0001

# Check for migration issues
uv run python app/manage.py makemigrations --check
```

### Migration Guidelines
- **One logical change per migration**: Don't mix schema changes with data migrations
- **Review generated SQL**: Use `sqlmigrate` before applying
- **Test rollback**: Ensure migrations are reversible with `reverse_sql`
- **Avoid direct SQL**: Use Django ORM operations when possible
- **Document complex migrations**: Add comments explaining non-obvious changes

### Migration Dependencies
```python
class Migration(migrations.Migration):
    dependencies = [
        ('ores', '0001_initial'),
        ('components', '0002_add_materials_field'),
    ]
```

### Data Migrations
```python
# Example: Populate default values
def populate_defaults(apps, schema_editor):
    Ore = apps.get_model('ores', 'Ore')
    for ore in Ore.objects.filter(mass__isnull=True):
        ore.mass = 1.0
        ore.save()

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(populate_defaults, reverse_code=migrations.RunPython.noop),
    ]
```

## Fixture Management

### Creating Fixtures
```bash
# Export all data from an app
uv run python app/manage.py dumpdata ores --indent 2 > app/ores/fixtures/sample_ores.json

# Export specific models
uv run python app/manage.py dumpdata ores.Ore --indent 2 > app/ores/fixtures/ores_only.json

# Exclude certain fields
uv run python app/manage.py dumpdata ores --exclude ores.created_at --indent 2
```

### Loading Fixtures
```bash
# Load in dependency order
uv run python app/manage.py loaddata sample_ores
uv run python app/manage.py loaddata sample_components
uv run python app/manage.py loaddata sample_blocks
uv run python app/manage.py loaddata sample_buildorders

# Load all fixtures at once (if dependencies are correct)
uv run python app/manage.py loaddata sample_ores sample_components sample_blocks
```

### Fixture Best Practices
- **Respect dependencies**: Load Ores before Components before Blocks
- **Use UUIDv7**: Ensure all IDs are valid UUIDv7 format
- **Validate relationships**: All foreign key UUIDs must exist
- **Keep fixtures small**: 10-20 records per fixture for testing
- **Version control**: Commit fixtures to repository
- **Document purpose**: Add README explaining fixture contents

### Fixture Validation
```python
# Validate UUIDs in fixtures
import json
from uuid_utils import uuid7

with open('app/ores/fixtures/sample_ores.json') as f:
    data = json.load(f)
    for item in data:
        try:
            uuid7(item['pk'])
        except ValueError:
            print(f"Invalid UUID: {item['pk']}")
```

## Database Backup & Restore

### PostgreSQL Backup
```bash
# Full database backup
docker compose exec database pg_dump -U se2_user se2_calculator > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup specific tables
docker compose exec database pg_dump -U se2_user -t ores_ore -t components_component se2_calculator > partial_backup.sql

# Compressed backup
docker compose exec database pg_dump -U se2_user se2_calculator | gzip > backup.sql.gz
```

### PostgreSQL Restore
```bash
# Restore from backup
docker compose exec -T database psql -U se2_user se2_calculator < backup.sql

# Restore compressed backup
gunzip -c backup.sql.gz | docker compose exec -T database psql -U se2_user se2_calculator

# Drop and recreate database before restore
docker compose exec database psql -U se2_user -c "DROP DATABASE se2_calculator;"
docker compose exec database psql -U se2_user -c "CREATE DATABASE se2_calculator;"
docker compose exec -T database psql -U se2_user se2_calculator < backup.sql
```

### Backup Schedule
- **Development**: Manual backups before major changes
- **Staging**: Daily automated backups (retain 7 days)
- **Production**: Hourly backups (retain 24 hours), daily backups (retain 30 days)

## Data Seeding Strategies

### Initial Data
```python
# Use fixtures for static reference data
# Example: Game-defined ores and components
uv run python app/manage.py loaddata game_ores game_components
```

### Test Data
```python
# Use factories or fixtures for test data
# Example: pytest fixtures
@pytest.fixture
def sample_ore():
    return Ore.objects.create(
        name="Test Ore",
        mass=1.0,
        description="Test description"
    )
```

### Development Data
```bash
# Create management command for dev data
# app/ores/management/commands/seed_dev_data.py
uv run python app/manage.py seed_dev_data
```

## PostgreSQL-Specific Optimizations

### Indexes
```python
class Meta:
    indexes = [
        models.Index(fields=['name']),
        models.Index(fields=['created_at']),
        models.Index(fields=['name', 'mass']),  # Composite index
    ]
```

### Query Optimization
```python
# Use select_related for foreign keys
blocks = Block.objects.select_related('category').all()

# Use prefetch_related for many-to-many or reverse foreign keys
components = Component.objects.prefetch_related('blocks').all()

# Use only() to limit fields
ores = Ore.objects.only('id', 'name', 'mass')

# Use values() for dictionaries (faster than model instances)
ore_names = Ore.objects.values('id', 'name')
```

### JSONField Queries
```python
# Query JSONField data
components_with_iron = Component.objects.filter(
    materials__has_key='<iron_ore_uuid>'
)

# Query nested JSON
blocks_with_steel = Block.objects.filter(
    components__<steel_component_uuid>__gt=5
)
```

### Connection Pooling
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Keep connections alive for 10 minutes
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

## Database Maintenance

### Vacuum and Analyze
```bash
# Vacuum database (reclaim storage)
docker compose exec database psql -U se2_user -d se2_calculator -c "VACUUM ANALYZE;"

# Vacuum specific table
docker compose exec database psql -U se2_user -d se2_calculator -c "VACUUM ANALYZE ores_ore;"
```

### Check Database Size
```bash
# Database size
docker compose exec database psql -U se2_user -d se2_calculator -c "SELECT pg_size_pretty(pg_database_size('se2_calculator'));"

# Table sizes
docker compose exec database psql -U se2_user -d se2_calculator -c "SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) FROM pg_tables WHERE schemaname = 'public' ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;"
```

### Monitor Connections
```bash
# Active connections
docker compose exec database psql -U se2_user -d se2_calculator -c "SELECT count(*) FROM pg_stat_activity;"

# Connection details
docker compose exec database psql -U se2_user -d se2_calculator -c "SELECT pid, usename, application_name, client_addr, state FROM pg_stat_activity;"
```

## Database Reset Procedures

### Development Reset
```bash
# Complete reset (destroys all data)
docker compose down -v
docker compose up -d
docker compose exec web python app/manage.py migrate
docker compose exec web python app/manage.py loaddata sample_ores sample_components sample_blocks
```

### Partial Reset
```bash
# Reset specific app data
uv run python app/manage.py flush --no-input
uv run python app/manage.py migrate
uv run python app/manage.py loaddata sample_ores sample_components sample_blocks
```

## Troubleshooting

### Migration Conflicts
```bash
# Show migration status
uv run python app/manage.py showmigrations

# Fake a migration (if already applied manually)
uv run python app/manage.py migrate --fake ores 0001

# Rollback to specific migration
uv run python app/manage.py migrate ores 0001
```

### Database Connection Issues
```bash
# Check database is running
docker compose ps database

# Check database logs
docker compose logs database

# Test connection
docker compose exec database psql -U se2_user -d se2_calculator -c "SELECT 1;"
```

### Performance Issues
```bash
# Identify slow queries
docker compose exec database psql -U se2_user -d se2_calculator -c "SELECT query, calls, total_time, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"

# Enable query logging (temporarily)
# Add to docker-compose.yml database service:
# command: postgres -c log_statement=all
```

## Database Checklist

### Before Deployment
- [ ] All migrations applied and tested
- [ ] Fixtures validated and loaded
- [ ] Backup procedures tested
- [ ] Indexes created for frequently queried fields
- [ ] Connection pooling configured
- [ ] Database credentials rotated

### Regular Maintenance
- [ ] Run VACUUM ANALYZE weekly
- [ ] Review slow queries monthly
- [ ] Test backup restoration quarterly
- [ ] Update PostgreSQL version annually
- [ ] Monitor database size growth
