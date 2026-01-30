# Database Overview

**Project:** SE2 Calculator Project  
**Document Type:** Database Documentation  
**Last Updated:** January 30, 2026  
**Status:** Active  

---

## Purpose

This document describes the database setup, configuration, and core schema for the SE2 Calculator Project. It covers the supported database engines, environment variables, schema structure, and common data workflows.

---

## Supported Database Engines

The application supports two database backends via Django:

- **PostgreSQL (preferred for production):** enabled when `DB_NAME` is set.
- **SQLite (default for local development):** used when no database environment variables are provided.

### Selection Logic

- If `DB_NAME` is present, Django uses PostgreSQL.
- Otherwise, Django uses SQLite at `db.sqlite3` in the project root.

---

## Configuration

### Environment Variables (PostgreSQL)

| Variable | Required | Example | Description |
| --- | --- | --- | --- |
| `DB_NAME` | Yes | `se2_calc` | Database name |
| `DB_USER` | Yes | `se2_user` | Database user |
| `DB_PASSWORD` | Yes | `change_me` | Database password |
| `DB_HOST` | No | `localhost` | Database host (default: `localhost`) |
| `DB_PORT` | No | `5432` | Database port (default: `5432`) |

### SQLite

When no PostgreSQL variables are set, Django uses:

- **File:** `db.sqlite3`
- **Path:** `<project-root>/db.sqlite3`

---

## Schema Overview

The database is centered around three core models:

- **Ore** (`ores_ore`)
- **Component** (`components_component`)
- **Block** (`blocks_block`)

### Entity Relationships (Logical)

```
Ore ──┐
      ├──(materials JSON)──> Component ──┐
      │                                  ├──(components JSON)──> Block
      └──────────────────────────────────┘
```

> Note: Relationships are stored in JSON fields (not foreign keys). Validation is enforced in application logic.

---

## Table Details

### `ores_ore`

Stores raw ore definitions.

**Key fields:**
- `ore_id` (UUIDv7, primary key)
- `name` (unique)
- `description`
- `mass`
- `created_at`, `updated_at`

### `components_component`

Stores buildable components and their ore requirements.

**Key fields:**
- `component_id` (UUIDv7, primary key)
- `name` (unique)
- `description`
- `materials` (JSON: `ore_id -> quantity`)
- `fabricator_type`
- `crafting_time`
- `mass`
- `created_at`, `updated_at`

**Validation rules:**
- All `materials` keys must reference existing `ore_id` values.
- Each material quantity must be a positive number.

### `blocks_block`

Stores final buildable blocks and their component requirements.

**Key fields:**
- `block_id` (UUIDv7, primary key)
- `name` (unique)
- `description`
- `mass`
- `components` (JSON: `component_id -> quantity`)
- `health`, `pcu`, `snap_size`
- `consumer_type`, `consumer_rate`
- `producer_type`, `producer_rate`
- `storage_capacity`
- `created_at`, `updated_at`

**Validation rules:**
- All `components` keys must reference existing `component_id` values.
- Each component quantity must be a positive number.
- If `consumer_type` is set, `consumer_rate` must be > 0.
- If `producer_type` is set, `producer_rate` must be > 0.

---

## Migrations

Django migrations define and evolve the schema.

Common commands:

```bash
# Create new migrations
uv run python manage.py makemigrations

# Apply migrations
uv run python manage.py migrate
```

---

## Fixtures and Seed Data

Each app includes fixtures for test and development data:

- `app/ores/fixtures/`
- `app/components/fixtures/`
- `app/blocks/fixtures/`

Load fixtures using:

```bash
uv run python manage.py loaddata <fixture-file>
```

---

## Data Integrity Notes

- Primary keys are UUIDv7 strings, generated in the model layer.
- Referential integrity is validated in application logic (not enforced by the database engine).
- JSON fields are used for flexible material and component maps.

---

## Troubleshooting

### PostgreSQL not being used

Ensure `DB_NAME` is set. Without it, the app defaults to SQLite.

### Missing related items

If validation errors mention missing `ore_id` or `component_id`, confirm that fixture data has been loaded in the correct order:

1. Ores
2. Components
3. Blocks
