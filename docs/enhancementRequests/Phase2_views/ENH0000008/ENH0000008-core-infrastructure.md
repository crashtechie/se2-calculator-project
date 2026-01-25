# Enhancement Request: Core Infrastructure & Best Practices

**Filename:** `inReview-enh0000008-core-infrastructure.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000008  
**Status:** inReview  
**Priority:** High  
**Created Date:** 2026-01-24  
**Updated Date:** 2026-01-24  
**Completion Date:** (pending)  
**Assigned To:** (pending)  
**Estimated Effort:** 1 day  
**Actual Effort:** (pending)

---

## Summary

Create core infrastructure app with shared utilities, API endpoints, validation mixins, logging, error handling, and security improvements to support Phase 2 views.

---

## Description

Establish foundational infrastructure that all Phase 2 apps will use. This includes reusable validation mixins (DRY principle), API endpoints for AJAX functionality, structured logging, custom error pages, input sanitization, and security headers. This enhancement should be completed before or alongside ENH-0000005/006/007.

**Benefits:**
- Eliminates code duplication across apps
- Establishes security best practices
- Enables AJAX functionality for dynamic forms
- Improves debugging with structured logging
- Better error handling and user feedback
- Foundation for Phase 3+ features

---

## Current Behavior

- No shared utilities or mixins
- No API endpoints for AJAX
- No structured logging
- Generic Django error pages
- No input sanitization
- Basic security configuration

---

## Proposed Behavior

- `core` app with reusable utilities
- RESTful API endpoints for ores/components
- Validation mixins that reuse model validation
- Structured logging for all operations
- Custom 404/500 error pages
- HTML sanitization for user input
- Security headers configured
- CSRF token handling for AJAX

---

## Acceptance Criteria

- [ ] Core app created with proper structure
- [ ] API endpoints return JSON for ores and components
- [ ] JSONFieldValidationMixin reuses model validation
- [ ] Logging configured for all apps
- [ ] Custom error pages (404, 500) created
- [ ] Input sanitization prevents XSS
- [ ] CSRF tokens work with AJAX requests
- [ ] Security headers configured in settings
- [ ] All utilities have docstrings
- [ ] Minimum 15 automated tests
- [ ] All tests pass with 100% pass rate
- [ ] Documentation updated
- [ ] Code reviewed

---

## Technical Details

### Dependencies

**New packages:**
```toml
dependencies = [
    "bleach>=6.1.0",           # HTML sanitization
    "whitenoise>=6.6.0",       # Static file serving
]

[project.optional-dependencies]
dev = [
    "django-debug-toolbar>=4.2.0",  # Query debugging
]
```

### Affected Components
- New `core` app
- All existing apps (ores, components, blocks)
- Settings configuration
- URL routing

### Files to Create

**Core App:**
- `core/__init__.py`
- `core/apps.py`
- `core/mixins.py` - Validation and permission mixins
- `core/utils.py` - Sanitization and helpers
- `core/views.py` - Error pages and API base classes
- `core/logging.py` - Logging configuration
- `core/tests.py` - Core utility tests
- `templates/404.html` - Custom 404 page
- `templates/500.html` - Custom 500 page
- `static/js/csrf.js` - CSRF token handling

**API Endpoints:**
- `ores/api.py` - Ore API views
- `components/api.py` - Component API views
- `ores/urls.py` - Add API routes
- `components/urls.py` - Add API routes

### Files to Modify
- `se2CalcProject/settings.py` - Add core app, logging, security
- `se2CalcProject/urls.py` - Add error handlers

### Database Changes
- [ ] No migrations required
- [ ] No new models
- [ ] No schema changes

---

## Implementation Plan

### Step 1: Create Core App
```bash
uv run python manage.py startapp core
```

### Step 2: Validation Mixins
```python
# core/mixins.py
from django.core.exceptions import ValidationError

class JSONFieldValidationMixin:
    """Reuse model validation in forms."""
    
    def clean(self):
        cleaned_data = super().clean()
        temp_obj = self.Meta.model(**cleaned_data)
        
        if hasattr(temp_obj, 'validate_materials'):
            is_valid, errors = temp_obj.validate_materials()
            if not is_valid:
                raise ValidationError(errors)
        
        if hasattr(temp_obj, 'validate_components'):
            is_valid, errors = temp_obj.validate_components()
            if not is_valid:
                raise ValidationError(errors)
        
        return cleaned_data
```

### Step 3: Input Sanitization
```python
# core/utils.py
import bleach

ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li']

def sanitize_html(text):
    """Sanitize user input to prevent XSS."""
    if not text:
        return text
    return bleach.clean(text, tags=ALLOWED_TAGS, strip=True)
```

### Step 4: API Endpoints
```python
# ores/api.py
from django.http import JsonResponse
from django.views import View
from .models import Ore

class OreAPIListView(View):
    def get(self, request):
        ores = Ore.objects.values('ore_id', 'name', 'mass')
        return JsonResponse(list(ores), safe=False)

# ores/urls.py - Add API routes
urlpatterns = [
    # ... existing patterns
    path('api/', OreAPIListView.as_view(), name='api_list'),
]
```

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

- [ ] Core app with utilities and mixins
- [ ] API endpoints for ores and components
- [ ] Logging configuration
- [ ] Custom error pages
- [ ] Input sanitization
- [ ] Security headers configured
- [ ] CSRF token JavaScript
- [ ] Automated test suite (15+ tests, all passing)
- [ ] Documentation for all utilities
- [ ] Deployment guide
- [ ] CHANGELOG.md updated

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

## Alternatives Considered

### Alternative 1: Skip Core App, Put Utilities in Each App
**Rejected:** Violates DRY principle, harder to maintain.

### Alternative 2: Use Django REST Framework
**Rejected:** Over-engineering for simple JSON endpoints. Can add later if needed.

### Alternative 3: Third-Party Error Tracking (Sentry)
**Deferred:** Good for production, but overkill for alpha. Add in Phase 4.

---

## Related Issues/Enhancements

- **Enables:** ENH-0000005 (Ores Views) - Provides API and mixins
- **Enables:** ENH-0000006 (Components Views) - Provides validation mixins
- **Enables:** ENH-0000007 (Blocks Views) - Provides validation mixins
- **Foundation For:** Phase 3 (Build Order Calculator)
- **Foundation For:** Phase 5 (User Authentication)

---

## Notes

- Should be implemented before or alongside ENH-0000005
- API endpoints enable AJAX functionality in forms
- Validation mixins eliminate code duplication
- Security configuration follows OWASP best practices
- Logging helps with debugging and monitoring
- All utilities are reusable across apps
- Consider this the "infrastructure" enhancement

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-24 | inReview | Initial creation based on best practices review |

---

## Sign-off

**Reviewed By:** (pending)  
**Approved By:** (pending)  
**Completed By:** (pending)  
**Completion Date:** (pending)
