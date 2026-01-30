# ISSUE-007: Missing Health Endpoint for Docker Health Check

**Status:** Open  
**Priority:** Medium  
**Created:** 2026-01-30  
**Component:** Docker Infrastructure  
**Affects Version:** 0.4.2-alpha

## Problem Description

The Dockerfile includes a health check that attempts to access `/health/` endpoint, but this endpoint does not exist in the Django application, causing container health checks to fail.

## Error Output

```
HEALTHCHECK failed: urllib.error.HTTPError: HTTP Error 404: Not Found
```

## Root Cause

Dockerfile health check references a `/health/` endpoint that was never implemented in Django URL configuration.

## Technical Details

**Affected Files:**
- `Dockerfile` (line 44-45)
- Django URL configuration (missing endpoint)

**Current Health Check:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/', timeout=5)" || exit 1
```

**Expected Behavior:**
- Health check successfully verifies Django is running
- Container reports healthy status

**Actual Behavior:**
- Health check fails with 404 error
- Container may be marked unhealthy

## Solution

### Option 1: Remove health check (simplest)

Remove HEALTHCHECK from Dockerfile.

### Option 2: Create health endpoint (recommended)

Create minimal health view in Django:

```python
# se2CalcProject/views.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "healthy"})
```

Add to `se2CalcProject/urls.py`:
```python
from .views import health_check

urlpatterns = [
    path('health/', health_check, name='health_check'),
    # ... existing patterns
]
```

### Option 3: Modify health check

Change Dockerfile to verify Django without endpoint:
```dockerfile
HEALTHCHECK CMD python manage.py check --deploy || exit 1
```

## Verification Checklist

- [ ] Choose solution approach
- [ ] Implement health endpoint or modify check
- [ ] Rebuild Docker image
- [ ] Verify health check passes
- [ ] Test with `docker inspect <container>` shows healthy
- [ ] Update nginx.conf if needed (already has /health/ location)

## Related Files

- `Dockerfile`
- `se2CalcProject/urls.py`
- `se2CalcProject/views.py` (to be created)
- `nginx.conf` (already configured for /health/)

## Notes

- nginx.conf already has `/health/` location configured
- Recommended: Implement Option 2 for production monitoring
