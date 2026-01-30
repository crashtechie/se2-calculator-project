# Docker Overview

**Project:** SE2 Calculator Project  
**Document Type:** Docker Documentation  
**Last Updated:** January 30, 2026  
**Status:** Active  

---

## Purpose

This document describes the Docker setup for the SE2 Calculator Project, including the container architecture, environment variables, and common workflows for local development and production-like usage.

---

## Container Architecture

The Docker setup defines three services:

- **database** (PostgreSQL)
- **web** (Django application)
- **nginx** (reverse proxy + static file serving)

```
Client → Nginx (80) → Django (8000) → PostgreSQL (5432)
```

---

## Files

- **Dockerfile**: builds the Django application image.
- **docker-compose.yml**: orchestrates web, database, and nginx.
- **nginx.conf**: reverse proxy configuration and static file handling.

---

## Service Details

### database (PostgreSQL)

- Image: `postgres:17`
- Port: `5432:5432`
- Data persistence: `db_data` volume
- Health check: `pg_isready`

### web (Django)

- Built from local Dockerfile
- Exposes port `8000` internally
- Runs migrations on startup
- Collects static files during image build
- Health check: `GET /health/`

### nginx

- Image: `nginx:alpine`
- Port: `80:80`
- Serves `/static/` from shared volume
- Proxies all other requests to Django

---

## Environment Variables

The Docker setup expects these variables (usually in a `.env` file):

| Variable | Required | Example | Description |
| --- | --- | --- | --- |
| `DEBUG` | Yes | `true` | Django debug flag |
| `SECRET_KEY` | Yes | `change_me` | Django secret key |
| `ALLOWED_HOSTS` | Yes | `localhost,127.0.0.1` | Allowed hosts |
| `DB_NAME` | Yes | `se2_calc` | Database name |
| `DB_USER` | Yes | `se2_user` | Database user |
| `DB_PASSWORD` | Yes | `change_me` | Database password |
| `DB_PORT` | No | `5432` | Database port |
| `DB_ENGINE` | No | `django.db.backends.postgresql` | Not used in settings but kept for consistency |

> `DB_HOST` is set to `database` in Docker to match the service name.

---

## Volumes

- `db_data`: persists PostgreSQL data
- `logs`: persists app logs
- `static_files`: shared static files for nginx

---

## Common Workflows

### Build and Run

```
docker compose up --build
```

### Stop

```
docker compose down
```

### Rebuild Only the Web Service

```
docker compose build web
```

---

## Health Checks

- Django health endpoint: `http://localhost/health/`
- Container health checks are defined for database and web services.

---

## Notes

- Django runs `migrate` on container startup.
- Static files are collected during image build and served by nginx.
- If `DEBUG` is enabled, you can still access Django error pages through nginx.

---

## Related Documentation

- Backend: [docs/wiki/backend/backend-overview.md](../backend/backend-overview.md)
- Database: [docs/wiki/database/database-overview.md](../database/database-overview.md)
