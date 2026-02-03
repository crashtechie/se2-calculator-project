# ISSUE-013: Nginx Static Files Path Mismatch in Docker Environment

**Status:** Resolved  
**Priority:** High  
**Created:** 2026-02-03  
**Resolved:** 2026-02-03  
**Component:** Docker Infrastructure / Nginx / Static Files  
**Affects Version:** 0.7.0-alpha

## Problem Description

The Docker build CI/CD workflow failed when testing static file serving through nginx. The test `curl -f http://localhost/static/css/main.css` returned a 404 error, indicating that nginx could not locate the static files despite them being collected by Django's `collectstatic` command.

## Error Output

```
Testing static files...
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
0   146    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (22) The requested URL returned error: 404
Error: Process completed with exit code 1.
```

## Root Cause

The issue was caused by **incorrect path mapping** between Docker volume mounts and nginx configuration:

1. **Project Structure:** The Django application is located in the `app/` subdirectory of the project root
2. **Volume Mount:** `docker-compose.yml` mounts the project root to `/app/` in containers (`.:/app`)
3. **Actual File Location:** This means Django files are at `/app/app/` inside containers
4. **Static Files Path:** Django's `collectstatic` copies files to `/app/app/staticfiles/`
5. **Nginx Configuration:** nginx was configured to serve from `/app/staticfiles/` ❌
6. **Volume Conflict:** A named volume `static_files` was mounted to `/app/staticfiles/`, creating an empty directory that shadowed the actual files

## Technical Details

**Affected Files:**
- `nginx.conf` (static file location path)
- `docker-compose.yml` (volume mounts)
- `.github/workflows/docker.yml` (CI/CD test)

**Django Settings:**
```python
BASE_DIR = Path(__file__).resolve().parent.parent  # /app/app/
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # /app/app/static/
STATIC_ROOT = BASE_DIR / "staticfiles"     # /app/app/staticfiles/
```

**Original Nginx Configuration (Broken):**
```nginx
location /static/ {
    alias /app/staticfiles/;  # Wrong path!
    expires 30d;
    add_header Cache-Control "public, immutable" always;
    access_log off;
}
```

**Original Docker Compose (Broken):**
```yaml
web:
  volumes:
    - .:/app
    - static_files:/app/staticfiles  # Conflicts with project mount

nginx:
  volumes:
    - static_files:/app/staticfiles:ro  # Empty volume
```

**Path Resolution Inside Container:**
- Project root mounted at: `/app/`
- Django BASE_DIR: `/app/app/`
- Static files collected to: `/app/app/staticfiles/`
- Nginx looking at: `/app/staticfiles/` (empty due to volume mount)

**Expected Behavior:**
- Static files accessible at `http://localhost/static/css/main.css`
- CI/CD test passes with 200 OK response
- Nginx serves files from correct location

**Actual Behavior:**
- Static files return 404 Not Found
- CI/CD workflow fails
- Empty directory at `/app/staticfiles/` due to volume mount

## Solution

### Step 1: Fix Nginx Path

Update `nginx.conf` to point to the correct nested path:

```nginx
location /static/ {
    alias /app/app/staticfiles/;  # Correct path!
    expires 30d;
    add_header Cache-Control "public, immutable" always;
    access_log off;
}
```

### Step 2: Remove Conflicting Volume Mount

Update `docker-compose.yml` to remove the `static_files` volume mount from the web service:

```yaml
web:
  volumes:
    - .:/app
    - logs:/app/logs
    # Removed: - static_files:/app/staticfiles
```

### Step 3: Update Nginx Volume Mount

Update nginx to use the same project mount instead of a separate volume:

```yaml
nginx:
  volumes:
    - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    - .:/app:ro  # Use project mount instead of separate volume
    - logs:/app/logs:ro
```

### Step 4: Remove Unused Volume

Remove the `static_files` volume definition:

```yaml
volumes:
  db_data:
    driver: local
  logs:
    driver: local
  # Removed: static_files
```

### Step 5: Add Explicit collectstatic Step to CI/CD

Update `.github/workflows/docker.yml` to ensure static files are collected:

```yaml
- name: Collect static files
  run: |
    docker compose exec -T web python app/manage.py collectstatic --noinput --clear
    echo "✓ Static files collected"
```

## Verification Checklist

- [x] Update nginx.conf with correct path `/app/app/staticfiles/`
- [x] Remove `static_files` volume mount from web service
- [x] Update nginx to use project mount
- [x] Remove unused `static_files` volume definition
- [x] Add collectstatic step to CI/CD workflow
- [x] Rebuild Docker containers with `docker compose down && docker compose up -d`
- [x] Verify files exist in container: `docker compose exec nginx ls -la /app/app/staticfiles/css/`
- [x] Test static file access: `curl -f http://localhost/static/css/main.css`
- [x] Verify 200 OK response
- [x] Check nginx logs for errors

## Resolution

**Date Resolved:** 2026-02-03

**Actions Taken:**
1. Updated `nginx.conf` to serve from `/app/app/staticfiles/` instead of `/app/staticfiles/`
2. Removed conflicting `static_files` volume mount from `docker-compose.yml`
3. Updated nginx service to use project mount (`.:/app:ro`)
4. Removed unused `static_files` volume definition
5. Added explicit `collectstatic` step to CI/CD workflow
6. Fixed Dockerfile permissions issue:
   - Create `appuser` before creating staticfiles directory
   - Set proper ownership (`appuser:appuser`) on `/app/app/staticfiles`
   - Run `collectstatic` as `appuser` instead of root
   - Prevents PermissionError when CI/CD runs collectstatic
7. Rebuilt containers and verified static files are accessible
8. Updated `.gitignore` to exclude `staticfiles/` directory

**Verification Results:**
```bash
# Check directory ownership
$ docker compose exec web ls -la /app/app/staticfiles/
total 20
drwxrwxr-x  5 appuser appuser 4096 Feb  3 06:16 .
drwxr-xr-x 11 appuser appuser 4096 Feb  3 06:16 ..
drwxrwxr-x  5 appuser appuser 4096 Feb  3 06:16 admin
drwxrwxr-x  2 appuser appuser 4096 Feb  3 06:45 css
drwxrwxr-x  2 appuser appuser 4096 Feb  3 06:45 js

# Test collectstatic as CI/CD does
$ docker compose exec -T web python app/manage.py collectstatic --noinput --clear
133 static files deleted, 133 static files copied to '/app/app/staticfiles'.

# Verify static file serving
$ curl -f -s -o /dev/null -w "%{http_code}" http://localhost/static/css/main.css
200

$ curl -f -s -o /dev/null -w "%{http_code}" http://localhost/
200
```

**Result:**
- Static files now serve correctly through nginx
- CI/CD workflow passes static file test
- No 404 errors in nginx logs
- All containers healthy and functioning

## Technical Explanation

### Why This Happened

This is a common issue when working with Docker volume mounts and nested project structures:

1. **Volume Mount Behavior:** When you mount a volume to a path, it creates a new filesystem at that mount point, potentially shadowing files that were copied during the Docker build
2. **Nested Structure:** Having the Django app in a subdirectory (`app/`) while mounting the project root creates nested paths inside containers
3. **Path Confusion:** It's easy to forget that paths inside containers differ from paths on the host

### Development vs Production

This configuration is optimized for **development** with live code reloading:

**Development (Current):**
- Mount entire project: `.:/app`
- Changes on host immediately reflected in container
- Static files served from mounted directory

**Production (Alternative):**
- Copy files during build (no volume mount)
- Static files baked into image
- Use `COPY . /app` in Dockerfile
- More efficient, no volume overhead

### Django Static Files Workflow

1. **Source Files:** Developers create CSS/JS in `app/static/`
2. **Collection:** `collectstatic` copies files from `STATICFILES_DIRS` to `STATIC_ROOT`
3. **Serving:** Nginx serves files from `STATIC_ROOT` location
4. **Git:** Only source files (`app/static/`) are committed; `staticfiles/` is ignored

## Related Issues

- ISSUE-007: Missing health endpoint (resolved)
- ISSUE-011: Health check Host header missing (resolved)
- ISSUE-012: Workflow YAML linting errors (resolved)

## Related Files

- `nginx.conf` - Static file location configuration
- `docker-compose.yml` - Volume mount configuration
- `.github/workflows/docker.yml` - CI/CD static file test
- `app/se2CalcProject/settings.py` - Django static files settings
- `.gitignore` - Excludes generated staticfiles directory
- `Dockerfile` - Collectstatic during build

## Notes

- The `app/static/` directory contains source files (committed to git)
- The `app/staticfiles/` directory contains collected files (ignored by git)
- Named volumes are useful for data persistence but can cause path conflicts
- Always verify paths inside containers match your configuration

## Best Practices

For Django + Nginx + Docker deployments:

1. **Understand Volume Mounts:** Know the difference between bind mounts and named volumes
2. **Verify Paths:** Use `docker compose exec` to check actual file locations in containers
3. **Consistent Paths:** Ensure nginx paths match where Django actually collects files
4. **Test Locally:** Run the same curl tests locally before pushing to CI/CD
5. **Document Structure:** Clearly document nested directory structures
6. **Separate Concerns:** Consider using different docker-compose files for dev vs prod
7. **Ignore Generated Files:** Always add `staticfiles/` to `.gitignore`

## Prevention

To prevent similar issues in the future:

1. Add integration tests that verify static file serving
2. Document the container path structure in README
3. Use environment variables for configurable paths
4. Consider flattening the project structure (move Django to root)
5. Add comments in nginx.conf explaining path mappings
