# ISSUE-011: Health Check Host Header Missing in Nginx Configuration

**Status:** Resolved  
**Priority:** Medium  
**Created:** 2026-02-02  
**Resolved:** 2026-02-02  
**Component:** Docker Infrastructure / Nginx  
**Affects Version:** 0.6.0-alpha

## Problem Description

The `/health/` endpoint returns a Django error page (400 Bad Request) when accessed through nginx, despite the endpoint being correctly implemented in Django. The issue is caused by nginx not passing the `Host` header to Django, which triggers Django's `ALLOWED_HOSTS` security check.

## Error Output

```
django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'django_app'. 
The domain name provided is not valid according to RFC 1034/1035.
```

**HTTP Response:**
- Status: 400 Bad Request
- Body: Django debug error page (HTML)

## Root Cause

The nginx configuration for the `/health/` location block did not include the `proxy_set_header Host $host;` directive. Without this header, nginx passes the upstream name (`django_app`) as the Host header, which is not in Django's `ALLOWED_HOSTS` list and violates RFC 1034/1035 domain name requirements.

## Technical Details

**Affected Files:**
- `nginx.conf` (health check location block)

**Nginx Upstream Configuration:**
```nginx
upstream django_app {
    server web:8000;
}
```

**Original Health Check Location (Broken):**
```nginx
location /health/ {
    access_log off;
    proxy_pass http://django_app;
}
```

**Django ALLOWED_HOSTS:**
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

**Request Flow:**
1. Client → `http://localhost/health/`
2. Nginx → Django with Host: `django_app` (upstream name)
3. Django → Rejects request (django_app not in ALLOWED_HOSTS)
4. Client ← 400 Bad Request

**Expected Behavior:**
- Health check returns `{"status": "ok"}` with 200 status
- Docker health check passes
- Container marked as healthy

**Actual Behavior:**
- Health check returns Django error page with 400 status
- Docker health check may fail
- Confusing error messages in logs

## Solution

Add the `proxy_set_header Host $host;` directive to the `/health/` location block in nginx.conf:

```nginx
location /health/ {
    access_log off;
    proxy_pass http://django_app;
    proxy_set_header Host $host;
}
```

This ensures nginx passes the original Host header (`localhost`) to Django, which is in the `ALLOWED_HOSTS` list.

## Verification Checklist

- [x] Update nginx.conf to include Host header in health check location
- [x] Restart nginx container with `docker-compose restart nginx`
- [x] Test health check with `curl http://localhost/health/`
- [x] Verify response is `{"status": "ok"}`
- [x] Verify HTTP status is 200
- [x] Check Docker health check status with `docker-compose ps`
- [x] Verify container shows as healthy

## Resolution

**Date Resolved:** 2026-02-02

**Actions Taken:**
1. Updated `nginx.conf` to add `proxy_set_header Host $host;` to `/health/` location
2. Restarted nginx container with `docker-compose restart nginx`
3. Tested health check endpoint with curl
4. Verified correct JSON response

**Result:**
- Health check now returns `{"status": "ok"}` with 200 status
- Docker health check passes successfully
- All containers marked as healthy
- No more DisallowedHost errors in logs

## Technical Explanation

### Why This Matters

Django's `ALLOWED_HOSTS` setting is a security feature that prevents HTTP Host header attacks. When a request comes in, Django checks if the Host header matches one of the allowed hosts. If not, it rejects the request with a 400 error.

### Nginx Proxy Headers

When nginx proxies requests, it needs to pass certain headers to the backend:

- `Host`: The original hostname from the client request
- `X-Real-IP`: The client's IP address
- `X-Forwarded-For`: Chain of proxy IPs
- `X-Forwarded-Proto`: Original protocol (http/https)

The main `/` location block already had these headers configured correctly, but the `/health/` location block was missing them.

### Why It Worked for Main Location

The main location block includes:
```nginx
location / {
    proxy_pass http://django_app;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

This is why the main application worked fine, but the health check failed.

## Related Issues

- ISSUE-007: Missing health endpoint (open - now resolved by this fix)
- ISSUE-009: Dockerfile manage.py path incorrect (resolved)
- ISSUE-010: Database credentials mismatch (resolved)

## Related Files

- `nginx.conf`
- `app/se2CalcProject/urls.py` (health check endpoint)
- `app/se2CalcProject/settings.py` (ALLOWED_HOSTS)
- `Dockerfile` (HEALTHCHECK directive)

## Notes

- Consider adding all proxy headers to health check location for consistency
- Health check endpoint already existed in Django (was not missing)
- Issue-007 can be marked as resolved since health endpoint works correctly
- This is a common nginx + Django configuration issue

## Best Practices

For nginx + Django deployments:

1. **Always pass Host header:** Include `proxy_set_header Host $host;` in all proxy locations
2. **Consistent headers:** Use the same proxy headers across all locations
3. **Test health checks:** Verify health endpoints work through the proxy
4. **Document ALLOWED_HOSTS:** Keep track of which hosts need to be allowed
5. **Use variables:** Consider using nginx variables for common header sets

