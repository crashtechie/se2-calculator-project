# Backend Overview

**Project:** SE2 Calculator Project  
**Document Type:** Backend Documentation  
**Last Updated:** January 30, 2026  
**Status:** Active  

---

## Purpose

This document describes the backend architecture, core apps, and key workflows for the SE2 Calculator Project. The backend is a Django application that exposes CRUD views for ores, components, and blocks, with validation rules enforced in the model layer.

---

## Technology Stack

- **Framework:** Django 6.0.1
- **Language:** Python
- **Templating:** Django Templates
- **Database:** PostgreSQL (production) / SQLite (local)
- **Static Assets:** Served via Django staticfiles

---

## Project Layout

```
app/
├── manage.py
├── se2CalcProject/        # Project settings and URLs
├── ores/                  # Ores app
├── components/            # Components app
└── blocks/                # Blocks app
```

---

## Installed Apps

Backend apps are registered in Django settings:

- `ores`
- `components`
- `blocks`

---

## Core Domain Apps

### Ores

**Purpose:** Store raw ore definitions and properties.

**Key model:** `Ore`
- UUIDv7 primary key (`ore_id`)
- Unique name
- Mass and description
- Automatic timestamps

### Components

**Purpose:** Store buildable components and their ore requirements.

**Key model:** `Component`
- UUIDv7 primary key (`component_id`)
- Materials JSON mapping (`ore_id -> quantity`)
- Validation ensures referenced ores exist

### Blocks

**Purpose:** Store final buildable blocks and their component requirements.

**Key model:** `Block`
- UUIDv7 primary key (`block_id`)
- Components JSON mapping (`component_id -> quantity`)
- Consumer/producer validation rules

---

## Validation Strategy

The backend enforces referential integrity and business rules in model `clean()` methods before saving:

- **Component materials:** every `ore_id` must exist and quantities must be positive.
- **Block components:** every `component_id` must exist and quantities must be positive.
- **Block consumer/producer:** if type is set, rate must be > 0.

---

## Request Flow (High-Level)

```
HTTP Request
   ↓
URL Routing (app/urls.py)
   ↓
View (views.py)
   ↓
Form Validation (forms.py)
   ↓
Model Save (models.py)
   ↓
Database
```

---

## Management Commands

Common Django commands:

```bash
# Run the development server
uv run python manage.py runserver

# Apply migrations
uv run python manage.py migrate

# Create an app migration
uv run python manage.py makemigrations
```

---

## Fixtures and Test Data

Fixtures are provided under each app:

- `app/ores/fixtures/`
- `app/components/fixtures/`
- `app/blocks/fixtures/`

Load fixtures with:

```bash
uv run python manage.py loaddata <fixture-file>
```

---

## Error Handling

- Validation errors raise `ValidationError` during model `clean()`.
- Views and forms surface errors to the UI.

---

## Related Documentation

- Database: [docs/wiki/database/database-overview.md](../database/database-overview.md)
- QA: [docs/wiki/qualityAssurance](../qualityAssurance)
