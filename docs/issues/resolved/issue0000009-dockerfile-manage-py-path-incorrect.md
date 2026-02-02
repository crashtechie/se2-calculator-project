# ISSUE-009: Dockerfile manage.py Path Incorrect

**Status:** Resolved  
**Priority:** High  
**Created:** 2026-02-02  
**Resolved:** 2026-02-02  
**Component:** Docker Infrastructure  
**Affects Version:** 0.6.0-alpha

## Problem Description

The Docker web container fails to start with error "python: can't open file '/app/manage.py': [Errno 2] No such file or directory". The Dockerfile references `manage.py` at the root level, but the actual file is located at `app/manage.py` in the project structure.

## Error Output

```
python: can't open file '/app/manage.py': [Errno 2] No such file or directory
```

## Root Cause

The Django project structure has `manage.py` inside the `app/` subdirectory, but the Dockerfile was written assuming `manage.py` would be at the root level after `COPY . .`. This results in the file being located at `/app/app/manage.py` inside the container, not `/app/manage.py`.

## Technical Details

**Affected Files:**
- `Dockerfile` (lines 28, 48)

**Project Structure:**
```
/
├── app/
│   ├── manage.py          # Actual location
│   ├── se2CalcProject/
│   └── ...
├── Dockerfile
└── docker-compose.yml
```

**Container Structure After COPY:**
```
/app/
├── app/
│   ├── manage.py          # Actual location in container
│   └── ...
├── Dockerfile
└── ...
```

**Expected Behavior:**
- Container starts successfully
- Migrations run automatically
- Django development server starts

**Actual Behavior:**
- Container fails to start
- Error: manage.py not found at expected path

## Solution

Update all references to `manage.py` in the Dockerfile to use `app/manage.py`:

### Changes Made

**Line 28 - collectstatic command:**
```dockerfile
# Before:
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# After:
RUN python app/manage.py collectstatic --noinput --clear 2>/dev/null || true
```

**Line 48 - CMD startup command:**
```dockerfile
# Before:
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]

# After:
CMD ["sh", "-c", "python app/manage.py migrate --noinput && python app/manage.py runserver 0.0.0.0:8000"]
```

## Verification Checklist

- [x] Update collectstatic command to use `app/manage.py`
- [x] Update CMD startup command to use `app/manage.py`
- [x] Rebuild Docker image with `docker-compose build --no-cache`
- [x] Start containers with `docker-compose up`
- [x] Verify web container starts successfully
- [x] Verify migrations run automatically
- [x] Verify Django server is accessible

## Resolution

**Date Resolved:** 2026-02-02

**Actions Taken:**
1. Updated Dockerfile line 28 to use `python app/manage.py collectstatic`
2. Updated Dockerfile line 48 to use `python app/manage.py migrate` and `python app/manage.py runserver`
3. Rebuilt Docker image with `docker-compose build --no-cache`
4. Started containers with `docker-compose up`

**Result:**
- Web container now starts successfully
- Migrations run automatically on startup
- Django development server accessible at http://localhost/
- All three containers (database, web, nginx) running and healthy

## Related Issues

- ISSUE-010: Database credentials mismatch (resolved)
- ISSUE-011: Health check Host header missing (resolved)

## Related Files

- `Dockerfile`
- `docker-compose.yml`
- `app/manage.py`

## Notes

- Alternative solution would be to restructure project to have `manage.py` at root
- Current solution maintains existing project structure
- Consider documenting project structure in README.md

