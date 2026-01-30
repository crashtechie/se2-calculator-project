# Enhancement Request: Core Infrastructure & Best Practices

**Filename:** `inProgress-enh0000008-core-infrastructure.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000008  
**Status:** Partially Complete (Docker Only)  
**Priority:** High  
**Created Date:** 2026-01-24  
**Updated Date:** 2026-01-27  
**Completion Date:** 2026-01-26 (Docker infrastructure only)  
**Assigned To:** Development Team  
**Estimated Effort:** 1.5-2 days  
**Actual Effort:** 0.5 days (Docker only)

---

## Summary

ENH-0000008 originally planned comprehensive core infrastructure including Docker deployment, shared utilities, API endpoints, validation mixins, logging, and error handling. As of v0.4.0-alpha, only the Docker infrastructure has been implemented. Application-level features (core app, APIs, logging, error pages) are deferred to Phase 4.

### Completed in v0.4.0-alpha:
- ✅ Docker infrastructure (Dockerfile, docker-compose.yml, nginx.conf)
- ✅ nginx reverse proxy with security headers
- ✅ Static file serving via nginx
- ✅ PostgreSQL with health checks and volumes
- ✅ Production-like environment for testing

### Deferred to Phase 4:
- ⏳ Core app with validation mixins
- ⏳ API endpoints for AJAX functionality
- ⏳ Structured logging configuration
- ⏳ Custom error pages (404/500)
- ⏳ CSRF token JavaScript utilities
- ⏳ Input sanitization utilities

---

## Description

Establish foundational infrastructure that all Phase 2+ apps will use. This includes reusable validation mixins (DRY principle), API endpoints for AJAX functionality, structured logging, custom error pages, input sanitization, and security headers. Implementation will leverage lessons learned from ENH-0000005 (Ores), ENH-0000006 (Components), and ENH-0000007 (Blocks) successful deployments.

**Benefits:**
- Eliminates code duplication across apps (form validation, views)
- Establishes security best practices
- Enables AJAX functionality for dynamic forms
- Improves debugging with structured logging
- Better error handling and user feedback
- Foundation for Phase 3 build order calculator
- Foundation for Phase 4 testing infrastructure
- Supports future enhancements (authentication, bulk operations, REST API)

---

## Current Behavior (Post ENH-0000005/006/007, v0.4.0-alpha)

### Implemented:
- ✅ Docker Compose stack (web + nginx + PostgreSQL)
- ✅ nginx reverse proxy with security headers
- ✅ Static files served by nginx with caching
- ✅ Health checks for database service
- ✅ Persistent volumes for database, logs, and static files
- ✅ Production-like environment capability

### Not Implemented (Deferred):
- Form validation logic duplicated across apps (forms.py clean methods)
- No API endpoints for AJAX (all interactions via form submission)
- Basic logging to console only (no structured file logging)
- Generic Django error pages
- No input sanitization beyond form validation
- No structured error handling in views
- No reusable view mixins
- No core app

---

## Proposed Behavior

- `core` app with reusable utilities, mixins, and helpers
- RESTful API endpoints for ores/components (JSON responses)
- Validation mixins that reuse model validation (reduce duplication in forms)
- Structured logging for all view operations (creation, update, delete, errors)
- Custom 404/500 error pages (user-friendly messaging)
- HTML sanitization utility for user input (prevent XSS)
- Security headers configured (CSRF, XFrame, CSP)
- CSRF token handling for AJAX requests
- API request/response logging for debugging- Production-like Docker environment with nginx reverse proxy
- Proper static file serving and caching
- DEBUG=False testing to verify error pages and security headers
---

## Acceptance Criteria

### Lessons from ENH-0000005/006/007

Based on successful deployments of prior enhancements, the following patterns should be leveraged:

1. **Form Validation Pattern** (from ENH-0000006/0000007)
   - Hidden JSON fields for complex data (materials_json, components_json)
   - Client-side JavaScript manages data assembly
   - Server-side validation via form clean() methods
   - Reuse of model validation helpers (validate_materials(), validate_components())
   - **Action:** Refactor into reusable JSONFieldValidationMixin to eliminate duplication

2. **Template Tag Helpers** (from ENH-0000007)
   - Custom template tags for data resolution (get_component_name, get_component_mass)
   - Error handling for invalid UUIDs and missing data
   - **Action:** Create core.templatetags.core_filters with reusable helpers

3. **Exception Handling** (issues found in ENH-0000007)
   - Must use get_object_or_404() instead of custom get_object()
   - Must catch ValidationError in template filters
   - Must handle invalid UUID strings gracefully
   - **Action:** Create standardized error handling utilities

4. **Context Variable Naming** (from ENH-0000007)
   - Consistent naming conventions across views (e.g., available_components)
   - Test assertions match actual implementation
   - **Action:** Document naming conventions in code comments

5. **Test Data Completeness** (from ENH-0000007)
   - All required form fields must be present in test data
   - Optional fields with defaults clearly marked
   - **Action:** Create test fixtures in core app for reuse across tests

### Core Infrastructure Acceptance Criteria

**Docker Infrastructure (COMPLETED v0.4.0-alpha)**
- [x] Dockerfile created with Python 3.13, uv dependency management
- [x] docker-compose.yml with web service (Django), nginx, database
- [x] nginx.conf for reverse proxy and static file serving
- [x] .dockerignore created to exclude unnecessary files
- [x] logs volume mounted for persistent logging
- [x] static files volume for nginx serving
- [x] Docker build successful and services start without errors
- [x] Web service accessible via nginx on port 80
- [x] Database accessible via service name (database:5432)
- [x] Static files served by nginx (not Django development server)
- [x] Security headers configured in nginx (X-Frame-Options, X-Content-Type-Options, X-XSS-Protection)

**Core App & Utilities (DEFERRED TO PHASE 4)**
- [ ] Core app created with proper Django structure (apps.py, __init__.py)
- [ ] Utilities module with helper functions (sanitization, etc.)
- [ ] Mixins module with reusable form/view mixins
- [ ] All utilities have comprehensive docstrings
- [ ] All functions are unit tested

**Validation Mixin (DEFERRED TO PHASE 4)**
- [ ] JSONFieldValidationMixin reuses model.validate_materials()
- [ ] JSONFieldValidationMixin reuses model.validate_components()
- [ ] Mixin catches ValidationError and converts to form errors
- [ ] Mixin eliminates duplicate validation code in ComponentForm and BlockForm
- [ ] Tests verify mixin works for both materials and components

**API Endpoints (DEFERRED TO PHASE 4 / ENH-0000009)**
- [ ] OreAPIListView returns JSON list of ores (id, name, mass)
- [ ] ComponentAPIListView returns JSON list of components (id, name, mass)
- [ ] API endpoints at /ores/api/ and /components/api/
- [ ] API returns 405 for POST/DELETE (read-only)
- [ ] API documentation in code comments

**Error Handling (DEFERRED TO PHASE 4)**
- [ ] Custom 404.html page (user-friendly, with home link)
- [ ] Custom 500.html page (user-friendly, with error ID)
- [ ] Error pages use base.html template
- [ ] 404 handler in se2CalcProject.urls
- [ ] 500 handler in se2CalcProject.urls

**Logging (DEFERRED TO PHASE 4)**
- [ ] LOGGING config in settings.py with file + console handlers
- [ ] Loggers for each app (ores, components, blocks, core)
- [ ] View operations logged (CREATE, UPDATE, DELETE with object identifier)
- [ ] API requests logged with endpoint and response status
- [ ] Error stack traces logged for debugging
- [ ] Structured format: timestamp, level, module, message

**Security (PARTIALLY COMPLETE)**
- [x] X_FRAME_OPTIONS = 'DENY' (nginx.conf)
- [x] X-Content-Type-Options: nosniff (nginx.conf)
- [x] X-XSS-Protection: 1; mode=block (nginx.conf)
- [ ] SECURE_BROWSER_XSS_FILTER = True (Django settings - deferred)
- [ ] SECURE_CONTENT_TYPE_NOSNIFF = True (Django settings - deferred)
- [ ] CSRF_COOKIE_HTTPONLY = True (deferred)
- [ ] SESSION_COOKIE_HTTPONLY = True (deferred)
- [ ] Production settings enable HTTPS/SSL (deferred)
- [ ] CSRF tokens handled in static/js/csrf.js (deferred)

**Input Sanitization (DEFERRED - Optional)**
- [ ] Sanitization utility with bleach library
- [ ] Used in views/forms to prevent XSS
- [ ] Tests verify script tags are removed
- [ ] Safe HTML tags allowed (p, br, strong, em, ul, ol, li)

**Automated Tests**
- [x] Docker infrastructure tested manually (deployment verification)
- [ ] Core app tests (deferred - no core app exists)
- [ ] API tests (deferred - no APIs exist)
- [ ] Error page tests (deferred - no custom error pages)
- [ ] Logging tests (deferred - no structured logging)

**Documentation (COMPLETED for Docker)**
- [x] ENH0000008_DEPLOYMENT_GUIDE.md (comprehensive deployment guide)
- [x] DOCKER_SETUP_GUIDE.md (setup, testing, troubleshooting)
- [x] DOCKER_CONFIGURATION_SUMMARY.md (quick reference)
- [x] README.md updated with Docker Quick Start
- [x] CHANGELOG.md updated with v0.4.0-alpha Docker features
- [ ] API endpoint documentation (deferred)
- [ ] Mixin usage guide (deferred)
- [ ] Logging configuration documentation (deferred)
- [ ] Error handling strategy documentation (deferred)

---

## Technical Details

### Dependencies

**Existing (no new packages required for core functionality):**
- Django 6.0.1 (already installed)
- Python 3.13+ (already used)

**Optional (for input sanitization):**
```toml
dependencies = [
    "bleach>=6.1.0",  # HTML sanitization (optional, can implement without)
]

[project.optional-dependencies]
dev = [
    "django-debug-toolbar>=4.2.0",  # Query debugging (optional)
]
```

### Affected Components
- New `core` app (no models, just utilities and mixins)
- Updated `ores/forms.py`, `ores/views.py` (optional - can refactor after core created)
- Updated `components/forms.py`, `components/views.py` (optional)
- Updated `blocks/forms.py`, `blocks/views.py` (optional)
- Settings configuration (logging, security, error handlers)
- URL routing (error handlers, API routes)

### Files to Create

**Core App Structure:**
- `core/__init__.py` - Empty module init
- `core/apps.py` - CoreConfig class
- `core/mixins.py` - JSONFieldValidationMixin, other mixins
- `core/utils.py` - Helper functions (sanitization, etc.)
- `core/templatetags/__init__.py` - Template tag module init
- `core/templatetags/core_filters.py` - Reusable template filters/tags
- `core/tests.py` - Comprehensive test suite (20+ tests)

**Error Pages:**
- `templates/404.html` - Custom 404 page
- `templates/500.html` - Custom 500 page

**API Endpoints:**
- `ores/api.py` - Ore API views (can be in views.py)
- `components/api.py` - Component API views (can be in views.py)
- Update `ores/urls.py` - Add API routes
- Update `components/urls.py` - Add API routes

**Frontend Assets:**
- `static/js/csrf.js` - CSRF token handling for AJAX

**Docker & Infrastructure (Option C: Django templates + nginx):**
- `Dockerfile` - Multi-stage build with Python 3.13, uv package manager
- `docker-compose.yml` - Web (Django), nginx (reverse proxy), database services
- `nginx.conf` - Nginx configuration for reverse proxy and static file serving
- `.dockerignore` - Files to exclude from Docker build

### Files to Modify
- `se2CalcProject/settings.py` - Add core app, logging, security headers, error handlers
- `se2CalcProject/urls.py` - Add 404/500 handlers, error pages config
- `.env` - Add DB_HOST=database for container networking
- `.env.example` - Document Docker environment variables
- `components/forms.py` - (Optional) Inherit from JSONFieldValidationMixin
- `blocks/forms.py` - (Optional) Inherit from JSONFieldValidationMixin

### Database Changes
- [ ] No migrations required
- [ ] No new models
- [ ] No schema changes

---

## Implementation Plan

**NOTE:** As of v0.4.0-alpha, only Phase 9-10 (Docker Infrastructure) has been implemented. Phases 1-8 (Core App, APIs, Logging, Error Pages) are deferred to Phase 4 and documented here for future reference.

### Phase 9: Docker & Infrastructure (Option C) - ✅ COMPLETED (v0.4.0-alpha)

**Step 9.1: Create Dockerfile** - ✅ COMPLETE

**Step 9.2: Create nginx.conf** - ✅ COMPLETE

**Step 9.3: Update docker-compose.yml** - ✅ COMPLETE

**Step 9.4: Create .dockerignore** - ✅ COMPLETE

**Step 9.5: Update .env for Docker** - ✅ COMPLETE

**Step 9.6: Build and test Docker environment** - ✅ COMPLETE

**Step 9.7: Test production-like environment** - ✅ COMPLETE

### Phase 10: Deployment Verification - ✅ COMPLETED (v0.4.0-alpha)

**Step 10.1: Verify all components** - ✅ COMPLETE

**Step 10.2: Test rollback** - ✅ COMPLETE

---

### Phases 1-8: Core App Infrastructure - ⏳ DEFERRED TO PHASE 4

The following phases were originally planned but not implemented in v0.4.0-alpha. They are documented below for future reference and will be addressed in Phase 4 enhancements.

### Phase 1: Core App Setup (Deferred)

**Step 1.1: Create core app**
```bash
cd /home/dsmi001/app/se2-calculator-project
uv run python manage.py startapp core
```
Based on ENH-0000006/007 pattern - consolidate validation logic:
```python
# core/mixins.py
from django.core.exceptions import ValidationError

class JSONFieldValidationMixin:
    """
    Reusable mixin for forms with JSONField that requires model validation.
    
    Uses model's validate_materials() or validate_components() methods
    to provide server-side validation of JSON data.
    """
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate materials if model has validate_materials
        if hasattr(self.instance, 'validate_materials'):
            is_valid, errors = self.instance.validate_materials()
            if not is_valid:
                raise ValidationError({
                    'materials_json': errors
                })
        
        # Validate components if model has validate_components
        if hasattr(self.instance, 'validate_components'):
            is_valid, errors = self.instance.validate_components()
            if not is_valid:
                raise ValidationError({
                    'components_json': errors
                })
        
        return cleaned_data
```

**Step 1.3: Create utils.py with helper functions**
```python
# core/utils.py
import uuid
from django.core.exceptions import ValidationError

def validate_uuid(value):
    """Validate UUID string format."""
    try:
        return uuid.UUID(value)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid UUID format: {value}")

def sanitize_html(text, allowed_tags=['p', 'br', 'strong', 'em', 'ul', 'ol', 'li']):
    """
    Sanitize HTML to prevent XSS attacks.
    Optional: requires bleach package.
    """
    try:
        import bleach
        return bleach.clean(text, tags=allowed_tags, strip=True)
    except ImportError:
        # Fallback: return text as-is if bleach not installed
        return text
```

**Step 1.4: Create core/tests.py with comprehensive tests**
```python
# core/tests.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from core.mixins import JSONFieldValidationMixin
from core.utils import validate_uuid, sanitize_html

class JSONFieldValidationMixinTestCase(TestCase):
    """Test JSONFieldValidationMixin functionality."""
    # Tests for validation logic
    
class UtilsTestCase(TestCase):
    """Test utility functions."""
    # Tests for sanitization, UUID validation, etc.
```

### Phase 2: API Endpoints (Day 1, 1-2 hours)

**Step 2.1: Create ores/api.py**
```python
# ores/api.py
from django.http import JsonResponse
from django.views import View
from .models import Ore

class OreListAPIView(View):
    """
    API endpoint returning list of ores as JSON.
    
    GET /ores/api/ returns:
    [
        {"ore_id": "uuid", "name": "Iron Ore", "mass": 125.5},
        ...
    ]
    """
    
    def get(self, request):
        ores = Ore.objects.values('ore_id', 'name', 'mass').order_by('name')
        return JsonResponse(list(ores), safe=False)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Method not allowed'}, status=405)
```

**Step 2.2: Update ores/urls.py**
```python
# ores/urls.py
from django.urls import path
from . import views, api

app_name = 'ores'

urlpatterns = [
    # Existing patterns...
    path('api/', api.OreListAPIView.as_view(), name='api_list'),
]
```

**Step 2.3: Create components/api.py (similar pattern)**

**Step 2.4: Add tests for API endpoints (2 tests minimum)**

### Phase 3: Logging Configuration (Day 1, 1 hour)

**Step 3.1: Update se2CalcProject/settings.py**
Add LOGGING configuration:
```python
import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'app.log',
            'formatter': 'verbose',
            'level': 'INFO',
        },
    },
    'loggers': {
        'ores': {'handlers': ['console', 'file'], 'level': 'INFO'},
        'components': {'handlers': ['console', 'file'], 'level': 'INFO'},
        'blocks': {'handlers': ['console', 'file'], 'level': 'INFO'},
        'core': {'handlers': ['console', 'file'], 'level': 'INFO'},
    },
}
```

**Step 3.2: Add logging to views (ores/views.py, etc.)**
```python
import logging
logger = logging.getLogger(__name__)

class OreCreateView(SuccessMessageMixin, CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Created ore: {self.object.name} (ID: {self.object.ore_id})")
        return response
```

### Phase 4: Error Pages (Day 1, 30 minutes)

**Step 4.1: Create templates/404.html**
```html
{% extends "base.html" %}
{% block content %}
<div class="alert alert-warning" role="alert">
    <h1>404 - Page Not Found</h1>
    <p>The page you requested does not exist.</p>
    <a href="{% url 'home' %}" class="btn btn-primary">Return Home</a>
</div>
{% endblock %}
```

**Step 4.2: Create templates/500.html**

**Step 4.3: Update se2CalcProject/urls.py**
```python
handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
```

**Step 4.4: Create core/views.py with error handlers**
```python
from django.shortcuts import render

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)
```

### Phase 5: Security Configuration (Day 1, 30 minutes)

**Step 5.1: Update se2CalcProject/settings.py with security headers**
```python
# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

# Production settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    HSTS_SECONDS = 31536000
    HSTS_INCLUDE_SUBDOMAINS = True
```

### Phase 6: CSRF Token JavaScript (Day 1, 30 minutes)

**Step 6.1: Create static/js/csrf.js**
```javascript
// static/js/csrf.js
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Use in AJAX calls:
// headers: {'X-CSRFToken': csrftoken}
```

**Step 6.2: Include in base.html**
```html
<script src="{% static 'js/csrf.js' %}"></script>
```

### Phase 7: Testing & Integration (Day 2, 2-3 hours)

**Step 7.1: Run full test suite**
```bash
uv run python manage.py test core -v 2
uv run python manage.py test ores components blocks core -v 2
```

**Step 7.2: Verify coverage**
```bash
uv run coverage run --source='core' manage.py test core
uv run coverage report
```

**Step 7.3: Manual testing**
- Test API endpoints: /ores/api/, /components/api/
- Test error pages: visit nonexistent URL for 404
- Test logging: create/update/delete object, check logs/app.log
- Test security: verify headers in response

### Phase 8: Documentation (Day 2, 1-2 hours)

**Step 8.1: Document API endpoints** (in code comments)
**Step 8.2: Document mixin usage** (in docstrings)
**Step 8.3: Create deployment guide**
**Step 8.4: Update README.md**
**Step 8.5: Update CHANGELOG.md**

### Phase 9: Docker & Infrastructure (Option C) (Day 2, 2-3 hours)

**Step 9.1: Create Dockerfile**
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN pip install uv && uv pip install --system

# Copy project code
COPY . .

# Collect static files (needed for production)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && gunicorn se2CalcProject.wsgi:application --bind 0.0.0.0:8000"]
```

**Step 9.2: Create nginx.conf**
```nginx
upstream django_app {
    server web:8000;
}

server {
    listen 80;
    server_name _;
    client_max_body_size 10M;

    # Serve static files directly from nginx
    location /static/ {
        alias /app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy all other requests to Django
    location / {
        proxy_pass http://django_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check endpoint
    location /health/ {
        access_log off;
        proxy_pass http://django_app;
    }
}
```

**Step 9.3: Update docker-compose.yml**
```yaml
name: se2-calculator
services:
  database:
    image: postgres:17
    restart: always
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    restart: always
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - DB_ENGINE=${DB_ENGINE}
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=database
      - DB_PORT=${DB_PORT}
    volumes:
      - .:/app
      - logs:/app/logs
      - static_files:/app/static
    depends_on:
      database:
        condition: service_healthy
    expose:
      - "8000"

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - static_files:/app/static:ro
      - logs:/app/logs:ro
    depends_on:
      - web

volumes:
  db_data:
  logs:
  static_files:
```

**Step 9.4: Create .dockerignore**
```
.git
.gitignore
.env
db.sqlite3
htmlcov
.coverage
__pycache__
*.pyc
.venv
.vscode
.idea
*.log
node_modules
.DS_Store
```

**Step 9.5: Update .env for Docker**
```dotenv
# Existing settings...
DB_HOST=database  # Use service name instead of localhost

# Docker-specific settings
DOCKER_ENV=true
```

**Step 9.6: Build and test Docker environment**
```bash
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
# Visit http://localhost:80 in browser
docker-compose logs -f
```

**Step 9.7: Test production-like environment**
- Verify DEBUG=False doesn't expose debug info
- Test custom 404/500 pages display correctly
- Verify static files served by nginx (not Django)
- Check logging output in logs/app.log
- Verify security headers present in response
- Test database connectivity via service name

### Phase 10: Deployment Verification (Day 3, 1-2 hours)

**Step 10.1: Verify all components**
- [ ] Docker image builds successfully
- [ ] All services start without errors
- [ ] Web app accessible on port 80
- [ ] Database migrates successfully
- [ ] Static files served by nginx
- [ ] Logs persist across restarts
- [ ] Error pages work in production mode (DEBUG=False)
- [ ] Security headers present
- [ ] API endpoints functional
- [ ] Performance acceptable

**Step 10.2: Test rollback**
- [ ] Can restart individual services
- [ ] Can stop/start containers
- [ ] Data persists in volumes
- [ ] No data loss on restart

### Step 5: Logging Configuration
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/app.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'ores': {'handlers': ['file', 'console'], 'level': 'INFO'},
        'components': {'handlers': ['file', 'console'], 'level': 'INFO'},
        'blocks': {'handlers': ['file', 'console'], 'level': 'INFO'},
        'core': {'handlers': ['file', 'console'], 'level': 'INFO'},
    },
}
```

### Step 6: Error Pages
```html
<!-- templates/404.html -->
{% extends "base.html" %}
{% block content %}
<div class="error-page">
    <h1>404 - Not Found</h1>
    <p>The resource you requested does not exist.</p>
    <a href="{% url 'home' %}">Return to Home</a>
</div>
{% endblock %}
```

### Step 7: Security Configuration
```python
# settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

# In production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### Step 8: CSRF Token JavaScript
```javascript
// static/js/csrf.js
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
```

### Step 9: Testing
- Create `core/tests.py` with 15+ tests
- Test sanitization functions
- Test API endpoints
- Test validation mixins
- Test error pages
- Test CSRF token handling

### Step 10: Documentation
- Document all utilities with docstrings
- Create API endpoint documentation
- Update README with core app info
- Add security best practices guide

---

## Testing Requirements

### Unit Tests (Minimum 15)

**Sanitization Tests (3):**
- [ ] sanitize_html removes script tags
- [ ] sanitize_html allows safe tags
- [ ] sanitize_html handles None/empty strings

**API Tests (6):**
- [ ] OreAPIListView returns JSON
- [ ] OreAPIListView returns all ores
- [ ] ComponentAPIListView returns JSON
- [ ] ComponentAPIListView returns all components
- [ ] API endpoints require GET method
- [ ] API endpoints return 405 for POST

**Validation Mixin Tests (4):**
- [ ] JSONFieldValidationMixin calls model validation
- [ ] Mixin raises ValidationError for invalid data
- [ ] Mixin passes for valid data
- [ ] Mixin works with both materials and components

**Error Page Tests (2):**
- [ ] 404 page renders correctly
- [ ] 500 page renders correctly

### Integration Tests (Minimum 5)
- [ ] API endpoint integrates with views
- [ ] Sanitization works in forms
- [ ] Validation mixin works in ComponentForm
- [ ] Validation mixin works in BlockForm
- [ ] Logging captures view operations

### Security Tests (Minimum 5)
- [ ] XSS prevention works
- [ ] CSRF token required for POST
- [ ] Security headers present in response
- [ ] API endpoints don't expose sensitive data
- [ ] Error pages don't leak debug info

---

## Deliverables

### Completed (v0.4.0-alpha):
- [x] Docker infrastructure (Dockerfile, docker-compose.yml, nginx.conf)
- [x] Security headers configured (nginx)
- [x] Static file serving via nginx
- [x] Deployment guide (ENH0000008_DEPLOYMENT_GUIDE.md)
- [x] Docker setup guide (DOCKER_SETUP_GUIDE.md)
- [x] Docker configuration summary (DOCKER_CONFIGURATION_SUMMARY.md)
- [x] CHANGELOG.md updated
- [x] README.md updated with Docker Quick Start

### Deferred to Phase 4:
- [ ] Core app with utilities and mixins
- [ ] API endpoints for ores and components
- [ ] Logging configuration
- [ ] Custom error pages
- [ ] Input sanitization
- [ ] Additional Django security settings
- [ ] CSRF token JavaScript
- [ ] Automated test suite for core app
- [ ] Documentation for utilities and APIs

---

## Documentation Updates

- [ ] README.md - Add core app section
- [ ] CHANGELOG.md - Add ENH-0000008 entry
- [ ] Create API endpoint documentation
- [ ] Create security best practices guide
- [ ] Document validation mixin usage
- [ ] Add docstrings to all utilities
- [ ] Create deployment guide

---

## Risks and Considerations

**Risk 1: Breaking Changes to Existing Code**
- **Impact:** Medium
- **Mitigation:** Implement alongside ENH-0000005, test thoroughly

**Risk 2: Performance Overhead from Logging**
- **Impact:** Low
- **Mitigation:** Use INFO level, log to file not console in production

**Risk 3: Sanitization Too Aggressive**
- **Impact:** Low
- **Mitigation:** Allow safe HTML tags, test with real content

**Risk 4: API Endpoints Expose Too Much Data**
- **Impact:** Medium
- **Mitigation:** Only return needed fields (id, name, mass)

---

## Timeline & Effort

**Original Estimated Effort:** 1.5-2 days (12-16 hours) with Docker support (Option C)
**Actual Effort (Docker Only):** 0.5 days (4 hours)

**Completed Work (v0.4.0-alpha):**
- Docker infrastructure setup: 2 hours
- nginx configuration: 1 hour
- Documentation (deployment guides): 1 hour
- Testing and verification: Manual testing only

**Deferred Work (Phase 4):**
- Core app setup: 2-3 hours
- API endpoints: 1-2 hours  
- Logging configuration: 1 hour
- Error pages: 1 hour
- Additional security settings: 1 hour
- CSRF handling: 30 minutes
- Tests (20+): 2-3 hours
- Additional documentation: 1-2 hours

**Estimated Remaining Effort:** 10-14 hours (Phase 4)

---

## Alternatives Considered

### Alternative 1: Skip Core App, Put Utilities in Each App
**Rejected:** Violates DRY principle, harder to maintain across 3+ apps.

### Alternative 2: Use Django REST Framework
**Deferred (not rejected):** Over-engineering for simple JSON endpoints. Can add later if needed.

### Alternative 3: Third-Party Error Tracking (Sentry)
**Deferred:** Good for production, but overkill for alpha. Add in Phase 4.

### Alternative 4: Implement Mixins by Refactoring Existing Apps
**Not Recommended (for this iteration):** Risks breaking ENH-0000005/006/007. Better to create core app first.

---

## Related Issues/Enhancements

**Depends On:**
- Phase 1 (ENH-0000001/002/003) - Models complete ✅
- Phase 2 (ENH-0000005/006/007) - Views deployed ✅

**Enables:**
- ENH-0000009 (Build Order Calculator) - Can use API endpoints, logging
- ENH-0000010+ (Authentication, Bulk Operations) - Can reuse mixins

**Complements:**
- Phase 4 (Testing & Polish) - Better logging for debugging
- Future REST API endpoint expansion

---

## Lessons Learned from Recent Deployments

### From ENH-0000005 (Ores Views):
- Clean, simple view implementations work well
- Standard Django CBVs sufficient for CRUD
- Form validation via clean() methods effective
- Pagination at 25 items/page is good default

### From ENH-0000006 (Components Views):
- Hidden JSON fields (materials_json) elegant solution for complex data
- JavaScript client-side assembly + server-side validation good pattern
- Template filters for data resolution (ore name lookup) useful
- Reuse model validation helpers (validate_materials()) in forms

### From ENH-0000007 (Blocks Views):
- **Exception Handling:** Must use get_object_or_404(), not custom get_object()
- **Template Filters:** Must catch ValidationError for invalid UUIDs  
- **Error Messages:** "Unknown Component" display important for robustness
- **Test Data:** All required fields must be in fixtures
- **Context Variables:** Consistent naming across views (e.g., available_components)
- **Performance:** Caching resource chain data reduces queries

### Recommendations for ENH-0000008:
1. Create core app as "utility foundation" without breaking changes
2. Implement mixins for use in Phase 3+, don't force refactoring existing code
3. API endpoints should be read-only (GET only) for now
4. Logging should be comprehensive but not verbose
5. Error pages should be user-friendly without exposing stack traces
6. Security headers should follow OWASP recommendations
7. All utilities should be thoroughly tested before use

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-24 | inReview | Initial creation based on infrastructure planning |
| 2026-01-26 | inProgress | Updated after ENH-0000005/006/007 deployment review |
| 2026-01-26 | inProgress | Added Docker infrastructure (Option C) - nginx + Django templates + PostgreSQL |
| 2026-01-26 | Partially Complete | Docker infrastructure deployed in v0.4.0-alpha |
| 2026-01-27 | Partially Complete | Documentation updated to reflect actual implementation scope |

---

## Sign-off

**Design Review:** Approved (Docker infrastructure only)  
**Technical Review:** Approved (Docker infrastructure only)  
**QA Approval:** Manual testing passed  
**Deployment Date:** 2026-01-26 (v0.4.0-alpha - Docker only)

**Note:** Core app features (APIs, logging, error pages, mixins) deferred to Phase 4. Separate enhancement request will be created for application-level infrastructure.
