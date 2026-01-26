# Docker Setup Guide for ENH-0000008

**Document Type:** Docker Usage & Setup Guide  
**Last Updated:** 2026-01-26  
**Status:** Ready for Implementation

---

## Overview

This guide provides instructions for building and running the SE2 Calculator project in a Docker environment. Option C (Django templates + nginx) creates a production-like environment for testing logging, error pages, security headers, and static file serving.

---

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Docker Compose installed (`docker-compose --version`)
- Project source code cloned
- Environment variables configured (.env file)

### Build and Run

```bash
# Build Docker image
docker-compose build

# Start all services in background
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser (optional)
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f

# Access application
# Web app: http://localhost
# Database: localhost:5432 (PostgreSQL)
```

### Stop Services

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Restart services
docker-compose restart
```

---

## Service Architecture

### Services

**1. database (PostgreSQL 17)**
- Port: 5432 (exposed for local connection)
- Volume: db_data (persistent storage)
- Purpose: Data persistence layer

**2. web (Django Application)**
- Port: 8000 (internal, not exposed)
- Volumes: project code, logs, static files
- Purpose: Django application server
- Depends on: database (with health check)

**3. nginx (Nginx Alpine)**
- Port: 80 (main HTTP access)
- Purpose: Reverse proxy, static file serving
- Depends on: web service

### Network

All services communicate via internal Docker network (`se2_network`). Database is accessed as `database:5432` from web service.

---

## Configuration

### Environment Variables (.env)

For Docker, ensure these are set:

```bash
# Standard Django settings
DEBUG=True  # Set to False for production testing
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (use 'database' service name, not localhost)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=se2_calculator_db
DB_USER=se2_user
DB_PASSWORD=your_password
DB_HOST=database  # Important: use service name for Docker
DB_PORT=5432

# Application settings
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
ENVIRONMENT=docker
```

### Volume Configuration

**db_data** - PostgreSQL data persistence  
**logs** - Application logs (logs/app.log, nginx logs)  
**static_files** - Django static files (served by nginx)

---

## Testing Production-like Environment

### Test 1: Error Pages in Production Mode

```bash
# Set DEBUG=False in .env
DEBUG=False

# Restart web service
docker-compose restart web

# Test 404 page
curl http://localhost/nonexistent-page/

# Test 500 page (optional - create error in view)

# Verify custom error pages display (not Django debug)
```

### Test 2: Static Files via Nginx

```bash
# Static files should be served by nginx (not Django)
curl -I http://localhost/static/css/main.css

# Should return:
# HTTP/1.1 200 OK
# Cache-Control: public, immutable
# Expires: ...
```

### Test 3: Security Headers

```bash
# Verify security headers are present
curl -I http://localhost/

# Should include:
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
```

### Test 4: Logging Persistence

```bash
# Create/update objects to generate logs
docker-compose exec web python manage.py shell
# >>> from ores.models import Ore
# >>> Ore.objects.create(name="Test", mass=100.0)

# Check logs are persisted
docker-compose exec web cat logs/app.log

# Restart containers (logs persist)
docker-compose restart
docker-compose exec web cat logs/app.log  # Should still contain previous logs
```

### Test 5: Database Connectivity

```bash
# Verify web service can reach database
docker-compose exec web python manage.py dbshell
# psql command prompt should appear

# List tables
\dt

# Exit
\q
```

---

## Common Tasks

### View Logs

```bash
# Django application logs
docker-compose logs -f web

# Nginx logs
docker-compose logs -f nginx

# Database logs
docker-compose logs -f database

# All services
docker-compose logs -f
```

### Execute Commands

```bash
# Run Django management commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py test core
docker-compose exec web python manage.py createsuperuser

# Access Django shell
docker-compose exec web python manage.py shell

# Access PostgreSQL
docker-compose exec database psql -U se2_user -d se2_calculator_db
```

### Rebuild Services

```bash
# Rebuild web service after code changes
docker-compose build web
docker-compose up -d web

# Rebuild all services
docker-compose build
docker-compose up -d
```

### Cleanup

```bash
# Remove stopped containers
docker-compose rm

# Remove unused images
docker image prune

# Remove all unused volumes
docker volume prune

# Full cleanup (careful!)
docker-compose down -v
docker system prune -a
```

---

## Troubleshooting

### Issue: Port 80 Already in Use

```bash
# Check what's using port 80
sudo lsof -i :80

# Change port in docker-compose.yml
# Change: "80:80"
# To: "8080:80"
# Then access: http://localhost:8080
```

### Issue: Database Connection Failed

```bash
# Check database health
docker-compose ps

# Restart database service
docker-compose restart database

# Check database logs
docker-compose logs database

# Verify DB_HOST is set to 'database', not 'localhost'
cat .env | grep DB_HOST
```

### Issue: Static Files Not Loading

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Verify nginx can access static files
docker-compose exec nginx ls -la /app/static/

# Check nginx configuration
docker-compose exec nginx cat /etc/nginx/conf.d/default.conf
```

### Issue: Migrations Not Applied

```bash
# Manually run migrations
docker-compose exec web python manage.py migrate

# Check migration status
docker-compose exec web python manage.py migrate --list
```

### Issue: Permission Denied on Logs

```bash
# Logs directory needs write permissions
docker-compose exec web chmod 755 /app/logs

# Or recreate logs volume
docker-compose down -v
docker-compose up -d
```

---

## Performance Optimization

### For Development

- Keep `DEBUG=True` for better error messages
- Use `runserver` (included in Dockerfile)
- Fast iteration: code changes auto-reload

### For Production

- Set `DEBUG=False` (more secure)
- Use `gunicorn` instead of `runserver`
- Enable gzip compression in nginx
- Add caching headers for static files
- Use environment-specific settings

---

## Security Considerations

### Current Configuration

✅ Security headers configured in nginx.conf  
✅ Static files served by nginx (not Django)  
✅ Database not exposed to public (only port 5432 for local)  
✅ Django debug disabled in production (DEBUG=False)  
✅ Environment variables not in image (loaded at runtime)

### Recommendations for Production

- Use HTTPS/SSL (add to nginx.conf)
- Use secret management system (not .env)
- Limit database access
- Use separate user for Django process
- Regular security updates for base images
- Use Docker registries for image storage

---

## Monitoring & Logs

### Log Locations

- **Django app logs:** /app/logs/app.log (inside container, mounted volume)
- **Nginx access logs:** /var/log/nginx/access.log (inside container)
- **Nginx error logs:** /var/log/nginx/error.log (inside container)
- **PostgreSQL logs:** stdout (docker-compose logs database)

### Volume Inspection

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect se2-calculator_logs

# Access volume data
docker run -v se2-calculator_logs:/mnt alpine ls -la /mnt/
```

---

## Development Workflow

### Typical Development Session

```bash
# 1. Start services
docker-compose up -d

# 2. Make code changes (auto-reload on runserver)

# 3. Run tests
docker-compose exec web python manage.py test

# 4. Check logs for issues
docker-compose logs -f web

# 5. Access Django shell for debugging
docker-compose exec web python manage.py shell

# 6. Stop when done
docker-compose down
```

### Debugging Tips

```bash
# Add print statements in code
# They appear in: docker-compose logs -f web

# Add breakpoints with pdb
# In code: import pdb; pdb.set_trace()
# In terminal: docker-compose exec web python -i manage.py runserver 0.0.0.0:8000

# Access Django shell
docker-compose exec web python manage.py shell
```

---

## Integration with ENH-0000008

This Docker setup supports ENH-0000008 testing:

✅ **Logging Configuration**
- Logs persisted in volume (survive restart)
- Can test logging in production (DEBUG=False)

✅ **Error Pages**
- Test 404/500 pages in DEBUG=False mode
- Verify custom templates display

✅ **Security Headers**
- Verify CSRF, X-Frame-Options, etc. in responses
- Test in production-like environment

✅ **Static Files**
- Nginx serves static files (production pattern)
- Test caching headers

✅ **API Endpoints**
- Test JSON responses via nginx reverse proxy
- Verify security in production mode

---

## Additional Resources

- Docker Documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Nginx Documentation: https://nginx.org/en/docs/
- Django Documentation: https://docs.djangoproject.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/

---

## Support & Troubleshooting

For issues during ENH-0000008 implementation:

1. Check logs: `docker-compose logs -f`
2. Verify .env configuration
3. Ensure all services are healthy: `docker-compose ps`
4. Check Docker disk space: `docker system df`
5. Review nginx.conf for proxy issues
6. Verify ports are not in use: `lsof -i :80`, `lsof -i :5432`

---

## Document Version

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-26 | Initial creation for ENH-0000008 |

