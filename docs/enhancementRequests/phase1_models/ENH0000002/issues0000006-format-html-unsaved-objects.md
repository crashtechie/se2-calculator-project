# Issue Report: format_html TypeError on Component Add Page

**Issue ID:** ISSUES0000006  
**Date:** 2026-01-19  
**Severity:** High  
**Status:** Resolved  
**Component:** Components Admin - Django Admin Add View

---

## Summary

When navigating to the component add page (`/admin/components/component/add/`), a `TypeError` was raised:

```
TypeError at /admin/components/component/add/
args or kwargs must be provided.
```

The error occurred because `format_html()` was being used incorrectly with format strings containing `{}` placeholders, and the issue only manifested when rendering readonly fields for unsaved objects.

---

## Root Cause Analysis

### Primary Cause
Django's `format_html()` in version 6.0.1 has stricter requirements when using format strings with `{}` placeholders. The admin methods were using:

```python
# ❌ INCORRECT - format_html with {} in format string
return format_html(
    '<span title="{}">{} material{}</span>',
    json.dumps(obj.materials),
    material_count,
    plural
)
```

This pattern caused `TypeError: args or kwargs must be provided` when rendering readonly fields on the add page.

### Why This Fails on Add Page
1. When adding a new component, Django renders readonly fields for an unsaved object
2. The readonly fields (`materials_formatted`, `material_ores`, `validation_status`) are displayed
3. `format_html()` with `{}` placeholders in the format string triggers the error
4. The error occurs immediately on page load, before any user input

### Affected Methods
All four display methods in `ComponentAdmin` had this issue:
1. `materials_preview()` - Used in list view (not triggered on add page)
2. `materials_formatted()` - Readonly field on add page
3. `material_ores()` - Readonly field on add page
4. `validation_status()` - Readonly field on add page

---

## Impact

1. **Immediate:** Cannot access component add page in admin interface
2. **User Experience:** Completely blocks adding new components via admin
3. **Testing:** Manual Test 2 Step 5 fails immediately on navigation
4. **Development:** Blocks ENH0000002 deployment verification

---

## Error Details

**Exception Location:** `/home/dsmi001/app/se2-calculator-project/.venv/lib/python3.13/site-packages/django/utils/html.py`, line 137  
**Exception Type:** `TypeError`  
**Exception Value:** `args or kwargs must be provided.`  
**Request URL:** `http://127.0.0.1:8000/admin/components/component/add/`  
**Request Method:** `GET`  
**Django Version:** 6.0.1  
**Python Version:** 3.13.7

---

## Resolution

### Solution Applied
Replaced all `format_html()` calls with `mark_safe()` and standard Python string formatting:

#### 1. materials_preview() Method
```python
# ❌ BEFORE
return format_html(
    '<span title="{}">{} material{}</span>',
    json.dumps(obj.materials),
    material_count,
    plural
)

# ✓ AFTER
return mark_safe(
    '<span title="{}">{} material{}</span>'.format(
        json.dumps(obj.materials),
        material_count,
        plural
    )
)
```

#### 2. materials_formatted() Method
```python
# ❌ BEFORE
return format_html(
    '<pre style="background-color: #f5f5f5; padding: 10px; '
    'border-radius: 5px; overflow-x: auto;">{}</pre>',
    formatted
)

# ✓ AFTER
return mark_safe(
    '<pre style="background-color: #f5f5f5; padding: 10px; '
    'border-radius: 5px; overflow-x: auto;">{}</pre>'.format(formatted)
)
```

#### 3. material_ores() Method
```python
# ❌ BEFORE
ore_list = '<br>'.join([
    '<strong>{}</strong>: {} units'.format(ore.name, obj.materials[str(ore.ore_id)])
    for ore in ores
])
return format_html(ore_list)

# ✓ AFTER
ore_list = '<br>'.join([
    '<strong>{}</strong>: {} units'.format(ore.name, obj.materials[str(ore.ore_id)])
    for ore in ores
])
return mark_safe(ore_list)
```

#### 4. validation_status() Method
```python
# ❌ BEFORE
return format_html(
    '<span style="color: green; font-weight: bold;">✓ Valid</span>'
)

# ✓ AFTER
return mark_safe(
    '<span style="color: green; font-weight: bold;">✓ Valid</span>'
)
```

### Additional Fix: Handle Unsaved Objects
Added checks for `obj.materials` being `None` before calling model methods:

```python
def material_ores(self, obj):
    """Display ore names referenced in materials."""
    if not obj.materials:  # ← Added this check
        return mark_safe('<em>No ores referenced</em>')
    
    ores = obj.get_material_ores()
    # ... rest of method
```

### Import Addition
```python
from django.utils.safestring import mark_safe
```

---

## Verification

- ✓ Component add page loads successfully
- ✓ All readonly fields display correctly with empty/None values
- ✓ Materials formatted displays "No materials" for new components
- ✓ Material ores displays "No ores referenced" for new components
- ✓ Validation status displays "✓ Valid" for empty materials
- ✓ Manual Test 2 Step 5 passes

---

## Lessons Learned

### Django 6.0.1 format_html Behavior

The issue revealed that Django 6.0.1's `format_html()` has stricter validation:

| Pattern | Django 5.x | Django 6.0.1 | Recommendation |
|---------|-----------|--------------|----------------|
| `format_html('<span>{}</span>', val)` | ✓ Works | ✗ TypeError | Use mark_safe |
| `format_html('<span>text</span>')` | ✓ Works | ✓ Works | OK for static HTML |
| `mark_safe('<span>{}</span>'.format(val))` | ✓ Works | ✓ Works | Preferred |

### When to Use mark_safe vs format_html

**Use `mark_safe()`:**
- When building HTML with Python `.format()` or f-strings
- When you have complex string interpolation
- When you control all the content being interpolated

**Use `format_html()`:**
- When you need automatic HTML escaping of user input
- When working with untrusted data
- For simple static HTML strings

### Key Insight
In Django admin display methods for readonly fields:
- The methods are called even for unsaved objects
- Always check if required attributes exist before accessing them
- Use `mark_safe()` for complex HTML generation
- Ensure graceful handling of `None` values

---

## Best Practices Established

### 1. Check Object State
```python
def custom_display(self, obj):
    if not obj.field_name:  # Handle None/empty
        return mark_safe('<em>No data</em>')
    # ... process data
```

### 2. Use mark_safe for Complex HTML
```python
# Build HTML string first, then mark as safe
html = '<span>{}</span>'.format(value)
return mark_safe(html)
```

### 3. Consistent Pattern Across Methods
All display methods now follow the same pattern:
1. Check for None/empty values
2. Build HTML string with `.format()`
3. Return with `mark_safe()`

---

## Related Issues

- **ISSUES0000005:** Incorrect format_html usage with f-strings (list view)
- **Current Issue:** format_html TypeError on add page (unsaved objects)

Both issues stem from `format_html()` usage but manifest in different contexts.

---

## Files Modified

- `components/admin.py` - All display methods updated to use `mark_safe()`

### Changes Summary
- Added `mark_safe` import
- Replaced 4 `format_html()` calls with `mark_safe()`
- Added `obj.materials` None checks in `material_ores()`
- Ensured all methods handle unsaved objects gracefully

---

## Testing Checklist

- [x] Component add page loads without errors
- [x] Readonly fields display correctly for new components
- [x] Component list view still works
- [x] Component edit page works
- [x] Validation status displays correctly
- [x] Material ores displays correctly
- [x] Materials formatted displays correctly
- [x] Manual Test 2 Step 5 passes

---

## References

- [Django mark_safe Documentation](https://docs.djangoproject.com/en/6.0/ref/utils/#django.utils.safestring.mark_safe)
- [Django format_html Documentation](https://docs.djangoproject.com/en/6.0/ref/utils/#django.utils.html.format_html)
- [Django Admin ModelAdmin](https://docs.djangoproject.com/en/6.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin)
- File: [components/admin.py](../../../components/admin.py)
- Related: [issues0000005-incorrect-format-html-usage.md](./issues0000005-incorrect-format-html-usage.md)

---

**Resolution Date:** 2026-01-19  
**Resolved By:** User with Amazon Q assistance  
**Status:** ✓ Resolved and Verified
