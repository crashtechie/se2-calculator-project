# Troubleshoot Docker

Use this prompt to diagnose and fix Docker-related issues.

## Quick Diagnostics

### Check Container Status
```bash
docker compose ps
```

**Expected**: All containers show "healthy" status

### View Logs
```bash
# All services
docker compose logs

# Specific service
docker compose logs web
docker compose logs nginx
docker compose logs database

# Follow logs in real-time
docker compose logs -f web
```

### Check Health Endpoints
```bash
# nginx health
curl http://localhost/health/

# Direct Django health (if port exposed)
curl http://localhost:8000/health/
```

## Common Issues & Solutions

### 1. Container Won't Start

**Symptoms**: Container exits immediately or shows "unhealthy"

**Diagnosis**:
```bash
docker compose logs web
docker compose ps
```

**Solutions**:
- Check environment variables in `.env`
- Verify `DB_HOST=database` for Docker
- Rebuild from scratch: `docker compose down -v && docker compose up -d --build`
- Check Dockerfile syntax
- Verify entrypoint script permissions

### 2. Database Connection Refused

**Symptoms**: "connection refused" or "could not connect to server"

**Diagnosis**:
```bash
docker compose ps database
docker compose logs database
docker compose exec database psql -U se2_user -d se2_calculator -c "SELECT 1;"
```

**Solutions**:
- Ensure database container is healthy
- Verify `DB_HOST=database` in `.env`
- Check database credentials match
- Wait for database to fully start (health check)
- Verify network connectivity: `docker compose exec web ping database`

### 3. Static Files Not Loading

**Symptoms**: CSS/JS not loading, 404 errors for static files

**Diagnosis**:
```bash
docker compose exec nginx ls -la /static/
docker compose exec web ls -la /app/staticfiles/
curl -I http://localhost/static/css/style.css
```

**Solutions**:
- Run collectstatic: `docker compose exec web python app/manage.py collectstatic --no-input`
- Check nginx volume mounts in `docker-compose.yml`
- Verify `STATIC_ROOT` in Django settings
- Check nginx configuration paths
- Rebuild web container: `docker compose up -d --build web`

### 4. Health Check Failing

**Symptoms**: Container shows "unhealthy" status

**Diagnosis**:
```bash
docker compose ps
docker inspect <container_id> | grep -A 10 Health
```

**Solutions**:
- Check health endpoint is accessible
- Verify `ALLOWED_HOSTS` includes container hostname
- Increase health check timeout/retries
- Check application logs for errors
- Test health endpoint manually: `docker compose exec web curl http://localhost:8000/health/`

### 5. Permission Denied Errors

**Symptoms**: "Permission denied" in logs

**Diagnosis**:
```bash
docker compose exec web ls -la /app/
docker compose exec web whoami
```

**Solutions**:
- Fix ownership: `docker compose exec web chown -R app:app /app/logs`
- Check Dockerfile USER directive
- Verify volume mount permissions
- Rebuild with `--no-cache`: `docker compose build --no-cache`

### 6. Port Already in Use

**Symptoms**: "port is already allocated" error

**Diagnosis**:
```bash
sudo lsof -i :80
sudo lsof -i :5432
```

**Solutions**:
- Stop conflicting service
- Change port in `docker-compose.yml`
- Kill process using port: `sudo kill -9 <PID>`

### 7. Volume Mount Issues

**Symptoms**: Files not syncing, old data persisting

**Diagnosis**:
```bash
docker volume ls
docker volume inspect se2-calculator-project_postgres_data
```

**Solutions**:
- Remove volumes: `docker compose down -v` (WARNING: destroys data)
- Recreate specific volume: `docker volume rm <volume_name>`
- Check volume paths in `docker-compose.yml`
- Verify file permissions on host

### 8. Migration Errors

**Symptoms**: "no such table" or migration conflicts

**Diagnosis**:
```bash
docker compose exec web python app/manage.py showmigrations
docker compose logs web | grep migration
```

**Solutions**:
- Run migrations: `docker compose exec web python app/manage.py migrate`
- Check migration files exist
- Fake migration if needed: `docker compose exec web python app/manage.py migrate --fake`
- Reset database: `docker compose down -v && docker compose up -d`

## Complete Reset Procedure

When all else fails:

```bash
# 1. Stop and remove everything
docker compose down -v

# 2. Remove dangling images
docker system prune -a

# 3. Rebuild from scratch
docker compose build --no-cache

# 4. Start services
docker compose up -d

# 5. Wait for health checks
sleep 30
docker compose ps

# 6. Run migrations
docker compose exec web python app/manage.py migrate

# 7. Load fixtures
docker compose exec web python app/manage.py loaddata sample_ores sample_components sample_blocks

# 8. Create superuser
docker compose exec web python app/manage.py createsuperuser

# 9. Verify health
curl http://localhost/health/
```

## Debugging Commands

```bash
# Enter container shell
docker compose exec web bash
docker compose exec database bash

# Check environment variables
docker compose exec web env

# Test database connection
docker compose exec web python app/manage.py dbshell

# Check Django configuration
docker compose exec web python app/manage.py check

# Run Django shell
docker compose exec web python app/manage.py shell

# View container resource usage
docker stats

# Inspect container details
docker inspect <container_name>

# View container processes
docker compose top
```

## Prevention Checklist

- [ ] `.env` file properly configured
- [ ] `DB_HOST=database` for Docker
- [ ] Secrets generated via `secrets_gen.py`
- [ ] Migrations applied before starting
- [ ] Static files collected
- [ ] Health checks configured
- [ ] Volumes properly mounted
- [ ] Network connectivity verified
