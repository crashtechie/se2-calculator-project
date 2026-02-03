# ISSUE-010: Database Credentials Mismatch in Docker Volume

**Status:** Resolved  
**Priority:** High  
**Created:** 2026-02-02  
**Resolved:** 2026-02-02  
**Component:** Docker Infrastructure  
**Affects Version:** 0.6.0-alpha

## Problem Description

The Docker web container fails to connect to the PostgreSQL database with error "password authentication failed for user 'se2_user'". This occurs because the database volume was initialized with different credentials than those currently in the `.env` file.

## Error Output

```
django.db.utils.OperationalError: connection to server at "database" (172.18.0.2), 
port 5432 failed: FATAL: password authentication failed for user "se2_user"
```

## Root Cause

PostgreSQL only initializes the database (including user credentials) when the data volume is first created. If the volume already exists from a previous run with different credentials, PostgreSQL will not update the credentials even if the environment variables change. The existing volume had old credentials that didn't match the current `.env` file.

## Technical Details

**Affected Files:**
- `.env` (database credentials)
- `docker-compose.yml` (volume configuration)

**PostgreSQL Initialization Behavior:**
- First run: Creates database, user, and password from environment variables
- Subsequent runs: Uses existing database, ignores environment variables
- Volume persistence: Data survives container restarts and rebuilds

**Environment Variables:**
```bash
DB_NAME=se2_calc
DB_USER=se2_user
DB_PASSWORD=Sb4msxRfbT4r+8T5kkDp9uEp
DB_HOST=database
DB_PORT=5432
```

**Expected Behavior:**
- Web container connects to database successfully
- Migrations run without errors
- Django application starts normally

**Actual Behavior:**
- Web container fails to connect to database
- Authentication error prevents migrations
- Container enters restart loop

## Solution

Remove all Docker volumes to force PostgreSQL to reinitialize with current credentials:

```bash
docker-compose down -v
docker-compose up -d --build
```

The `-v` flag removes all named volumes, including:
- `se2-calculator_db_data` (PostgreSQL data)
- `se2-calculator_logs` (application logs)
- `se2-calculator_static_files` (static files)

## Verification Checklist

- [x] Stop all containers with `docker-compose down -v`
- [x] Verify volumes removed with `docker volume ls`
- [x] Rebuild and start containers with `docker-compose up -d --build`
- [x] Check web container logs for successful database connection
- [x] Verify migrations run successfully
- [x] Verify Django server starts without errors
- [x] Test database connectivity from web container

## Resolution

**Date Resolved:** 2026-02-02

**Actions Taken:**
1. Executed `docker-compose down -v` to remove all volumes
2. Rebuilt containers with `docker-compose up -d --build`
3. Verified database initialized with correct credentials
4. Confirmed web container connects successfully
5. Verified migrations run without errors

**Result:**
- Database volume recreated with correct credentials
- Web container connects to database successfully
- All migrations applied successfully
- Application fully operational

## Prevention

To avoid this issue in the future:

1. **Document credential changes:** When updating database credentials in `.env`, document that volumes must be recreated
2. **Use consistent credentials:** Avoid changing database credentials unless necessary
3. **Backup before changes:** Before removing volumes, backup any important data
4. **Environment-specific configs:** Consider using different `.env` files for different environments

## Related Issues

- ISSUE-009: Dockerfile manage.py path incorrect (resolved)
- ISSUE-011: Health check Host header missing (resolved)

## Related Files

- `.env`
- `docker-compose.yml`
- `app/se2CalcProject/settings.py`

## Notes

- This is a common Docker + PostgreSQL issue
- Volume removal is destructive - all database data is lost
- In production, use proper database migration procedures
- Consider adding volume backup scripts for development

## Alternative Solutions

If you need to preserve data while changing credentials:

1. **Export data:**
   ```bash
   docker-compose exec database pg_dump -U se2_user se2_calc > backup.sql
   ```

2. **Remove volumes and recreate:**
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

3. **Import data:**
   ```bash
   docker-compose exec -T database psql -U se2_user se2_calc < backup.sql
   ```

