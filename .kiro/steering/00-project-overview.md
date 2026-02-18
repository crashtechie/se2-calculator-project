# SE2 Calculator Project - Overview

## Project Identity
- **Name**: Space Engineers 2 Calculator Project
- **Version**: 0.7.0-alpha
- **Framework**: Django 6.0.1
- **Python**: 3.13+
- **Status**: Active Development (Alpha)

## Core Purpose
Web-based calculator and resource management tool for Space Engineers 2 players, providing crafting calculations, build order planning, and resource optimization.

## Current Phase
- Phase 1 & 2: ✅ Complete (Models, Views, Templates)
- Phase 3: 🚧 In Progress (Build Order Calculator)
  - BuildOrder model complete
  - Views & Templates in progress

## Key Architecture Decisions
- **UUIDv7 Primary Keys**: All models use UUIDv7 for better performance and distributed compatibility
- **JSONField Storage**: Component/material requirements stored as JSON for flexibility
- **Resource Chain**: Ores → Components → Blocks → Build Orders
- **Caching Strategy**: 5-minute TTL for calculated results
- **Docker Stack**: nginx + Django + PostgreSQL for production-like local development

## Technology Stack
- Django 6.0.1
- PostgreSQL (production) / SQLite (dev fallback)
- Docker Compose
- UV package manager
- pytest-django
- python-dotenv

## Repository
https://github.com/crashtechie/se2-calculator-project
