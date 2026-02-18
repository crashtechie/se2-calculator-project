# Docker & Deployment Guidelines

## Docker Stack Overview

The project uses a three-container stack:
- **nginx**: Reverse proxy, static file serving, security headers
- **web**: Django application (Python 3.13)
- **database**: PostgreSQL 17

## Environment Configuration

### Required Variables
```bash
# Django
DEBUG=false
SECRET_KEY=<generated-by-secrets_gen.py>
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=se2_calculator
DB_USER=se2_user
DB_PASSWORD=<generated-by-secrets_gen.py>
DB_HOST=database  # Use 'database' for Docker, 'localhost' for local dev
DB_PORT=5432
```

### Generating Secrets
```bash
uv run python scripts/secrets_gen.py
```

## Common Docker Commands

### Starting Services
```bash
# Build and start all services
docker compose up -d --build

# Start without rebuilding
docker compose up -d

# View logs
docker compose logs -f web
docker compose logs -f nginx
docker compose logs -f database
```

### Database Operations
```bash
# Run migrations
docker compose exec web python app/manage.py migrate

# Create superuser
docker compose exec web python app/manage.py createsuperuser

# Load fixtures
docker compose exec web python app/manage.py loaddata sample_ores sample_components sample_blocks

# Access PostgreSQL shell
docker compose exec database psql -U se2_user -d se2_calculator
```

### Maintenance
```bash
# Stop services
docker compose down

# Stop and remove volumes (WARNING: destroys data)
docker compose down -v

# Restart specific service
docker compose restart web

# View container status
docker compose ps

# Check health status
curl http://localhost/health/
```

## Health Checks

All containers include health checks:
- **nginx**: HTTP check on port 80
- **web**: Django health endpoint at `/health/`
- **database**: PostgreSQL connection check

Containers show as "healthy" when ready.

## Volume Management

### Named Volumes
- `postgres_data`: Database persistence
- `static_files`: Collected static files
- `logs`: Application logs

### Backup Database
```bash
# Create backup
docker compose exec database pg_dump -U se2_user se2_calculator > backup.sql

# Restore backup
docker compose exec -T database psql -U se2_user se2_calculator < backup.sql
```

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker compose logs web

# Rebuild from scratch
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

### Database Connection Issues
- Verify `DB_HOST=database` in `.env`
- Check database container is healthy: `docker compose ps`
- Ensure migrations are applied

### Static Files Not Loading
```bash
# Collect static files
docker compose exec web python app/manage.py collectstatic --no-input

# Verify nginx volume mount
docker compose exec nginx ls -la /static/
```

### Permission Issues
```bash
# Fix ownership (if needed)
docker compose exec web chown -R app:app /app/logs
```

## Local Development vs Docker

### Local Development
- Use SQLite: Comment out PostgreSQL settings in `settings.py`
- Set `DB_HOST=localhost` in `.env`
- Run: `uv run python manage.py runserver`

### Docker Development
- Use PostgreSQL: Set `DB_HOST=database`
- Access via nginx: http://localhost/
- Django runs internally on port 8000

## Production Considerations

### Security
- Set `DEBUG=false`
- Use strong `SECRET_KEY` and `DB_PASSWORD`
- Configure `ALLOWED_HOSTS` appropriately
- Enable HTTPS in nginx configuration
- Use environment-specific `.env` files

### Performance
- Enable Django caching
- Configure nginx caching headers
- Use connection pooling for database
- Monitor container resource usage

### Monitoring
- Check health endpoints regularly
- Monitor container logs
- Set up log aggregation (e.g., ELK stack)
- Configure alerts for container failures
