# Phase 1: Models & Database Setup

**Duration:** 2-3 days  
**Priority:** High (Blocking)

## Objectives
- Create three Django apps: ores, components, blocks
- Define models with all required fields
- Create and run migrations
- Set up Django admin interface

## Tasks

### 1.1 Create Django Apps
```bash
uv run python manage.py startapp ores
uv run python manage.py startapp components
uv run python manage.py startapp blocks
```

- [ ] Create ores app
- [ ] Create components app
- [ ] Create blocks app
- [ ] Register apps in `se2CalcProject/settings.py` INSTALLED_APPS

### 1.2 Implement Ores Model
**File:** `ores/models.py`

Fields:
- object_id (UUIDv7, primary key)
- name (CharField, unique, required)
- description (TextField)
- mass (FloatField, required)
- created_at (DateTimeField, auto_now_add)
- updated_at (DateTimeField, auto_now)

- [ ] Define Ore model
- [ ] Add __str__ method
- [ ] Add Meta class (ordering, verbose_name)

### 1.3 Implement Components Model
**File:** `components/models.py`

Fields (includes all base fields plus):
- material (JSONField) - Format: [{"ore_id": "uuid", "quantity": float}]
- fabricator (CharField)
- crafting_time (FloatField)

- [ ] Define Component model
- [ ] Add foreign key validation helper methods
- [ ] Add __str__ method
- [ ] Add Meta class

### 1.4 Implement Blocks Model
**File:** `blocks/models.py`

Fields (includes all base fields plus):
- components (JSONField) - Format: [{"component_id": "uuid", "quantity": int}]
- health (FloatField)
- pcu (IntegerField)
- snap_size (FloatField)
- input_mass (IntegerField)
- output_mass (IntegerField)
- consumer_type (CharField, optional)
- consumer_rate (FloatField, default=0)
- producer_type (CharField, optional)
- producer_rate (FloatField, default=0)
- storage_capacity (FloatField, optional)

- [ ] Define Block model
- [ ] Add validation for consumer/producer logic
- [ ] Add __str__ method
- [ ] Add Meta class

### 1.5 Create Migrations
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

- [ ] Generate migrations for all three apps
- [ ] Review migration files
- [ ] Apply migrations to database

### 1.6 Django Admin Setup
**Files:** `ores/admin.py`, `components/admin.py`, `blocks/admin.py`

- [ ] Register Ore model with admin
- [ ] Register Component model with admin (add JSONField display)
- [ ] Register Block model with admin (add JSONField display)
- [ ] Configure list_display, search_fields, list_filter
- [ ] Test admin interface

### 1.7 Create Fixtures (Optional)
**Files:** `ores/fixtures/`, `components/fixtures/`, `blocks/fixtures/`

- [ ] Create sample ore data
- [ ] Create sample component data
- [ ] Create sample block data
- [ ] Load fixtures for testing

## Deliverables
- Three functional Django apps
- All models defined with proper fields and validation
- Migrations created and applied
- Admin interface configured and tested
- Sample data loaded (optional)

## Testing Checklist
- [ ] Models can be created via Django shell
- [ ] Admin interface displays all fields correctly
- [ ] JSONField data saves and retrieves properly
- [ ] UUIDv7 primary keys generate correctly
- [ ] Timestamps auto-populate on create/update

## Notes
- Use uuid_utils library for UUIDv7 support: `pip install uuid-utils`
- JSONField format must be documented for frontend integration
- Consider adding model validators for JSONField structure
