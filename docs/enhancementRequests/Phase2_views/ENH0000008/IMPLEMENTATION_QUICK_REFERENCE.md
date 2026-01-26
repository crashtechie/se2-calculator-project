# ENH-0000008 Implementation Quick Reference

**Last Updated:** 2026-01-26  
**Status:** In Progress

---

## Key Lessons from Prior Deployments

### 1. Exception Handling (From ENH-0000007)
**DO:**
```python
from django.shortcuts import get_object_or_404

def get(self, request, pk):
    obj = get_object_or_404(Model, pk=pk)  # ✅ Correct
```

**DON'T:**
```python
try:
    obj = Model.objects.get(pk=pk)  # ❌ Don't do this
except Model.DoesNotExist:
    raise Http404()
```

### 2. Template Filter Error Handling (From ENH-0000007)
**DO:**
```python
@register.filter
def get_component_name(component_id):
    try:
        component = Component.objects.get(component_id=component_id)
        return component.name
    except (ValidationError, Component.DoesNotExist):  # ✅ Catch both
        return "Unknown Component"
```

**DON'T:**
```python
@register.filter
def get_component_name(component_id):
    return Component.objects.get(component_id=component_id).name  # ❌ Will crash
```

### 3. Form Validation (From ENH-0000006/007)
**Pattern:**
```python
class ComponentForm(forms.ModelForm):
    materials_json = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Component
        fields = ['name', 'mass', 'crafting_time']
    
    def clean(self):
        cleaned_data = super().clean()
        # Validate JSON from hidden field
        materials = self._parse_materials_json(cleaned_data)
        # Call model validation helper
        is_valid, errors = self.instance.validate_materials()
        if not is_valid:
            raise ValidationError(errors)
        return cleaned_data
```

### 4. Context Variables (From ENH-0000007)
**Convention:** Use consistent names across similar views
- List view context: Include filters, sort options, search query
- Detail view context: Include related objects, calculations
- Create/Update view context: Include `available_[items]` for selectors

**Example:**
```python
class BlockCreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_components'] = Component.objects.all()  # Consistent naming
        return context
```

### 5. Test Fixtures (From ENH-0000007)
**Requirement:** All required model fields must be in fixtures

**DO:**
```python
# blocks/tests_fixtures.py - Complete test data
BLOCK_DATA = {
    'name': 'Light Armor Block',
    'description': 'Lightweight armor block',
    'mass': 250.5,
    'health': 100,
    'pcu': 160,
    'snap_size': 0.5,
    'input_mass': None,  # Optional field
    'output_mass': None,  # Optional field
    'consumer_type': '',
    'consumer_rate': 0,
    'producer_type': '',
    'producer_rate': 0,
    'storage_capacity': 0,
}
```

**DON'T:**
```python
# ❌ Missing required fields - tests will fail
BLOCK_DATA = {
    'name': 'Light Armor Block',
    'mass': 250.5,
    'health': 100,
}
```

---

## Core Infrastructure Priorities

### Priority 1: Foundation (Required for Phase 3)

#### 1.1 JSONFieldValidationMixin
```python
# core/mixins.py
class JSONFieldValidationMixin:
    """
    Reuse model validation in forms with JSONField.
    Calls model.validate_materials() or validate_components() helpers.
    """
    def clean(self):
        # Implementation...
        pass
```

**Tests needed:** 4 tests (materials valid/invalid, components valid/invalid)

#### 1.2 Exception Handling Utilities
```python
# core/utils.py
def get_object_or_404_with_logging(Model, **kwargs):
    """Log object lookups and handle 404 gracefully."""
    pass

def safe_uuid_lookup(uuid_string):
    """Convert UUID string to UUID object, handle ValidationError."""
    pass
```

**Tests needed:** 3 tests (valid UUID, invalid UUID, None handling)

#### 1.3 Template Filter Helpers
```python
# core/templatetags/core_filters.py
@register.filter
def resolve_uuid_to_name(uuid_value, model_class):
    """Generic UUID→name resolution with error handling."""
    pass
```

**Tests needed:** 4 tests (valid, invalid, not found, None)

### Priority 2: User Experience (Improves Deployment)

#### 2.1 Error Pages (404/500)
- Custom templates that use base.html
- Friendly messaging
- Home/back navigation

**Tests needed:** 2 tests (404 rendering, 500 rendering)

#### 2.2 Logging Configuration
```python
# se2CalcProject/settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {message}',
        },
    },
    # ... handlers and loggers
}
```

**Integration:** Add logging to view post_save() methods
**Tests needed:** 4 tests (handler config, level config, format verification)

### Priority 3: Future-Ready (For Phase 3+)

#### 3.1 API Endpoints
```python
# ores/api.py
class OreListAPIView(View):
    def get(self, request):
        ores = Ore.objects.values('ore_id', 'name', 'mass')
        return JsonResponse(list(ores), safe=False)
```

**Tests needed:** 2 tests (GET returns JSON, POST returns 405)

#### 3.2 Security Headers
```python
# se2CalcProject/settings.py
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
```

**Tests needed:** Can verify in integration tests

#### 3.3 CSRF Token JavaScript
```javascript
// static/js/csrf.js
function getCookie(name) { /* ... */ }
const csrftoken = getCookie('csrftoken');
```

**Tests needed:** Include in template, verify script loads

---

## Test Coverage Checklist

- [ ] JSONFieldValidationMixin tests (4)
- [ ] Exception handling utility tests (3)
- [ ] Template filter helper tests (4)
- [ ] Error page tests (2)
- [ ] Logging tests (4)
- [ ] API endpoint tests (2)
- [ ] CSRF token tests (1)

**Total: 20 tests minimum**  
**Coverage target: 80%+**  
**Command:** `uv run coverage run --source='core' manage.py test core && uv run coverage report`

---

## Files to Create

```
core/
├── __init__.py
├── apps.py
├── mixins.py              # JSONFieldValidationMixin
├── utils.py               # Helper functions
├── views.py               # Error handlers
├── tests.py               # 20+ tests
├── templatetags/
│   ├── __init__.py
│   └── core_filters.py    # Reusable template filters
└── fixtures/
    └── test_data.json     # Shared test fixtures

templates/
├── 404.html               # Custom 404 page
└── 500.html               # Custom 500 page

static/js/
└── csrf.js                # CSRF token utility
```

---

## Files to Modify

```
se2CalcProject/
├── settings.py            # Add LOGGING, security headers
├── urls.py                # Add error handlers
└── apps.py                # Register core app

ores/
├── urls.py                # Add API routes (optional)
└── api.py                 # Create API views (optional)

components/
├── urls.py                # Add API routes (optional)
└── api.py                 # Create API views (optional)
```

---

## Common Patterns to Implement

### Pattern 1: List View with Search/Sort/Pagination
```python
class BaseListView(ListView):
    paginate_by = 25
    
    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        sort_by = self.request.GET.get('sort', 'name')
        if sort_by in self.allowed_sorts:
            qs = qs.order_by(sort_by)
        return qs
```

### Pattern 2: Detail View with Resource Chain
```python
class BaseDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate resource chain
        context['resource_chain'] = self.object.calculate_resources()
        # Resolve related object names
        context['component_names'] = self._get_component_names()
        return context
```

### Pattern 3: Form with JSONField
```python
class BaseForm(forms.ModelForm):
    data_json = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        # Parse and validate JSON
        data = json.loads(cleaned_data.get('data_json', '[]'))
        # Call model validator
        is_valid, errors = self.instance.validate_data()
        if not is_valid:
            raise ValidationError(errors)
        return cleaned_data
```

---

## Performance Considerations

### Caching (Phase 3+)
- Cache component name lookups: 5 min TTL
- Cache component mass lookups: 5 min TTL
- Cache resource chain: 1 hour TTL
- Expected cache hit rate: 85%+

### Query Optimization
- Use select_related() for foreign keys
- Use prefetch_related() for reverse relations
- Use values() for API endpoints
- Avoid N+1 queries in detail views

### Monitoring
- Track view response times
- Monitor cache hit rates
- Track error page visits
- Monitor log file size

---

## Deployment Checklist

Before deploying ENH-0000008:

### Code Quality
- [ ] All 20+ tests passing
- [ ] 80%+ code coverage
- [ ] No linting errors
- [ ] All docstrings present
- [ ] No TODO comments

### Documentation
- [ ] API endpoint documented
- [ ] Mixin usage documented
- [ ] Logging setup documented
- [ ] Error handling documented
- [ ] CHANGELOG.md updated

### Testing
- [ ] Run full test suite: `uv run python manage.py test`
- [ ] Check coverage: `uv run coverage report`
- [ ] Test error pages manually (404, 500)
- [ ] Test API endpoints manually
- [ ] Verify logging output

### Deployment
- [ ] Create deployment guide
- [ ] Test migrations (if any)
- [ ] Verify static files
- [ ] Test in DEBUG=False mode
- [ ] Verify error pages in production mode

---

## Recommended Reading

Before implementing ENH-0000008, review:

1. [ENH-0000005 Post-Deployment Report](ENH-0000005/ENH-0000005-POST-DEPLOYMENT-REPORT.md) - Basic patterns
2. [ENH-0000006 Post-Deployment Report](ENH-0000006/ENH-0000006-POST-DEPLOYMENT-REPORT.md) - JSONField patterns
3. [ENH-0000007 Post-Deployment Report](ENH-0000007/ENH-0000007-post-deployment-report.md) - Exception handling
4. [DEPLOYMENT_REVIEW_SUMMARY.md](DEPLOYMENT_REVIEW_SUMMARY.md) - This analysis

---

## Quick Answers

**Q: Should we use Django REST Framework?**  
A: No, not yet. Vanilla View + JsonResponse sufficient for now. Can add DRF in Phase 5 if mobile client needed.

**Q: Should we refactor existing forms to use JSONFieldValidationMixin?**  
A: No, create core app standalone. Optionally refactor after ENH-0000008 deployed.

**Q: How many tests do we need?**  
A: Minimum 20 (must exceed 15 from original spec). Target 25+ for 80%+ coverage.

**Q: Should we implement input sanitization with bleach?**  
A: Optional. Can skip for now if low priority. Add in Phase 4+ if needed.

**Q: What about caching?**  
A: Document strategy in core/utils.py. Implement selectively in Phase 3 for expensive lookups.

**Q: Error pages in both DEBUG=True and DEBUG=False?**  
A: Yes, test both modes. Default error pages show in DEBUG=True, custom pages show in DEBUG=False.

---

## Success Criteria

ENH-0000008 is successfully deployed when:

✅ Core app created with utilities, mixins, template tags  
✅ 20+ automated tests all passing (100% pass rate)  
✅ 80%+ code coverage for core app  
✅ Error pages (404, 500) custom templates deployed  
✅ Logging configuration added to settings  
✅ CSRF token JavaScript included in base.html  
✅ API endpoints (read-only) functional  
✅ Security headers configured  
✅ All code has comprehensive docstrings  
✅ Deployment guide and documentation complete  
✅ Zero critical issues post-deployment  

---

End of Quick Reference Guide
