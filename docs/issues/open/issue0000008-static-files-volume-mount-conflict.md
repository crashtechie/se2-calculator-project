# ISSUE-008: Static Files Collected During Build Overwritten by Volume Mount

**Status:** Open  
**Priority:** Low  
**Created:** 2026-01-30  
**Component:** Docker Infrastructure  
**Affects Version:** 0.4.2-alpha

## Problem Description

The Dockerfile runs `collectstatic` during image build, but docker-compose.yml mounts the local directory (`. :/app`), which overwrites the collected static files with the local directory contents.

## Root Cause

Conflicting static file management strategy between build-time collection and runtime volume mounting.

## Technical Details

**Affected Files:**
- `Dockerfile` (line 32)
- `docker-compose.yml` (web service volumes)

**Current Configuration:**

Dockerfile:
```dockerfile
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true
```

docker-compose.yml:
```yaml
volumes:
  - .:/app  # Overwrites /app including static files
  - static_files:/app/static
```

**Expected Behavior:**
- Static files available for nginx to serve
- Consistent static file location

**Actual Behavior:**
- Build-time collected files overwritten by volume mount
- Static files may be missing or inconsistent

## Solution

### Option 1: Remove collectstatic from Dockerfile (recommended for dev)

Remove line 32 from Dockerfile since development uses volume mount.

### Option 2: Run collectstatic in entrypoint

Move collectstatic to container startup:
```dockerfile
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
```

### Option 3: Separate dev/prod Dockerfiles

Create `Dockerfile.dev` without collectstatic and `Dockerfile.prod` with it.

## Verification Checklist

- [ ] Choose solution approach
- [ ] Implement changes to Dockerfile or docker-compose.yml
- [ ] Rebuild Docker image
- [ ] Verify static files accessible at /static/
- [ ] Test nginx serves static files correctly
- [ ] Verify no 404 errors for CSS/JS

## Related Files

- `Dockerfile`
- `docker-compose.yml`
- `nginx.conf`

## Notes

- Current setup works because static_files volume persists
- Consider documenting static file strategy in deployment guide
- Low priority as functionality not currently broken
