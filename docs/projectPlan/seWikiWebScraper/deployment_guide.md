# Deployment Guide

## Initial Setup

### 1. Create Project Directory

```bash
mkdir se2-wiki-scraper
cd se2-wiki-scraper
```

### 2. Create Directory Structure

```bash
mkdir -p scraper/parsers scraper/utils data logs
touch scraper/__init__.py
touch scraper/parsers/__init__.py
touch scraper/utils/__init__.py
```

### 3. Create Docker Files

Create Dockerfile, docker-compose.yml, and requirements.txt as specified in Phase 1.

### 4. Build Container

```bash
docker compose build
```

## Running the Scraper

### First Run

```bash
docker compose up
```

### Subsequent Runs

```bash
docker compose up
```

### Run in Background

```bash
docker compose up -d
```

### View Logs

```bash
docker compose logs -f
```

## Output Files

After successful run, check:

```bash
ls -lh data/
# Should show:
# - ores.json
# - components.json
# - blocks.json
```

## Integration with Django Project

### 1. Copy Files to Django Fixtures

```bash
cp data/ores.json ../se2-calculator-project/ores/fixtures/
cp data/components.json ../se2-calculator-project/components/fixtures/
cp data/blocks.json ../se2-calculator-project/blocks/fixtures/
```

### 2. Load into Django

```bash
cd ../se2-calculator-project
uv run python manage.py loaddata ores.json
uv run python manage.py loaddata components.json
uv run python manage.py loaddata blocks.json
```

## Updating Data

When wiki data changes:

```bash
cd se2-wiki-scraper
docker compose up
# Wait for completion
# Copy new files to Django
# Reload fixtures
```

## Troubleshooting

### Container Won't Start

```bash
docker compose down
docker compose build --no-cache
docker compose up
```

### Network Errors

Check logs for specific errors:
```bash
docker compose logs
```

### Invalid JSON Output

Run validation:
```bash
python -m json.tool data/ores.json
```

## Maintenance

### Update Dependencies

Edit requirements.txt, then:
```bash
docker compose build --no-cache
```

### Update Scraper Code

Code changes are reflected immediately due to volume mount. Just restart:
```bash
docker compose restart
```
