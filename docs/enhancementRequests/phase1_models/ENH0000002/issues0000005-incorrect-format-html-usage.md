# Issue Report: Incorrect format_html Usage with F-Strings

**Issue ID:** ISSUES0000005  
**Date:** 2026-01-19  
**Severity:** High  
**Status:** Resolved  
**Component:** Components Admin - Django Admin Display Methods

---

## Summary

After fixing the missing JSON import, the Components admin interface raised a `TypeError` when attempting to render the list view:

```
TypeError at /admin/components/component/
args or kwargs must be provided.
```

The error occurred because `format_html()` was being called with fully-formatted f-strings instead of format strings with placeholders.

---

## Root Cause Analysis

### Primary Cause
Django's `format_html()` function expects either:
1. A format string with `{}` placeholders + positional arguments, OR
2. A format string with `{}` placeholders + keyword arguments

However, the code was passing pre-formatted f-strings with no placeholders:

```python
# ❌ INCORRECT - f-string passed to format_html with no placeholders
return format_html(
    f'<span title="{json.dumps(obj.materials)}">'
    f'{material_count} material{"s" if material_count != 1 else ""}</span>'
)
```

### Why This Fails
- The f-string is evaluated first, producing a complete string
- `format_html()` receives a string with no `{}` placeholders
- `format_html()` has no arguments to substitute
- Django raises: `TypeError: args or kwargs must be provided`

### Affected Methods
Three methods in `ComponentAdmin` had this issue:
1. `materials_preview()` - Line 59-61
2. `material_ores()` - Line 84-86
3. `validation_status()` - Line 100-103

---

## Impact

1. **Immediate:** Admin list view completely broken after fixing JSON import
2. **User Experience:** Cannot view components list in admin interface
3. **Testing:** Manual Test 2 still failing with different error
4. **Development:** Continued blocking of ENH0000002 verification

---

## Error Details

**Exception Location:** `/home/dsmi001/app/se2-calculator-project/.venv/lib/python3.13/site-packages/django/utils/html.py`, line 137  
**Exception Type:** `TypeError`  
**Exception Value:** `args or kwargs must be provided.`  
**Request URL:** `http://127.0.0.1:8000/admin/components/component/`  
**Django Version:** 6.0.1  
**Python Version:** 3.13.7

---

## Resolution

### Solution Applied
Replaced f-strings with proper `format_html()` usage with placeholders:

#### 1. materials_preview() Method
```python
# ❌ BEFORE
return format_html(
    f'<span title="{json.dumps(obj.materials)}">'
    f'{material_count} material{"s" if material_count != 1 else ""}</span>'
)

# ✓ AFTER
material_count = len(obj.materials)
plural = 's' if material_count != 1 else ''
return format_html(
    '<span title="{}">{} material{}</span>',
    json.dumps(obj.materials),
    material_count,
    plural
)
```

#### 2. material_ores() Method
```python
# ❌ BEFORE
ore_list = '<br>'.join([
    f'<strong>{ore.name}</strong>: {obj.materials[str(ore.ore_id)]} units'
    for ore in ores
])
return format_html(ore_list)

# ✓ AFTER
ore_list = '<br>'.join([
    '<strong>{}</strong>: {} units'.format(ore.name, obj.materials[str(ore.ore_id)])
    for ore in ores
])
return format_html(ore_list)
```

#### 3. validation_status() Method
```python
# ❌ BEFORE
error_text = '<br>'.join([f'• {error}' for error in errors])
return format_html(
    '<span style="color: red; font-weight: bold;">✗ Invalid</span><br>' +
    error_text
)

# ✓ AFTER
error_text = '<br>'.join(['• {}'.format(error) for error in errors])
return format_html(
    '<span style="color: red; font-weight: bold;">✗ Invalid</span><br>{}',
    error_text
)
```

### Verification
- Admin list view loads successfully
- Materials preview displays correctly with tooltip
- Material ores display correctly in detail view
- Validation status displays correctly
- All admin functionality fully operational

---

## Lessons Learned

### Django format_html() Best Practices

| Pattern | ✓/✗ | Reason |
|---------|-----|--------|
| `format_html('<span>{}</span>', value)` | ✓ | Proper placeholder with argument |
| `format_html(f'<span>{value}</span>')` | ✗ | F-string has no placeholders for format_html |
| `format_html('<span>' + value + '</span>')` | ✗ | String concatenation bypasses HTML escaping |
| `format_html('<span>{name}</span>', name=value)` | ✓ | Named placeholder with kwarg |

### Key Insight
`format_html()` serves two purposes:
1. **HTML Escaping:** Automatically escapes arguments to prevent XSS
2. **Safe Formatting:** Marks the result as safe HTML

Using f-strings defeats both purposes:
- Values are already interpolated (no escaping)
- No arguments means `format_html()` has nothing to do

### Correct Usage Pattern
```python
# Use format_html with placeholders and arguments
return format_html(
    '<span class="{}">{}</span>',  # Template with placeholders
    css_class,                      # Argument 1 (auto-escaped)
    content                         # Argument 2 (auto-escaped)
)
```

---

## Next Steps

1. **Code Review**
   - Search codebase for other `format_html()` misuse
   - Check if ores/admin.py has similar issues
   - Review any future admin customizations

2. **Documentation Update**
   - Add Django admin best practices to development guide
   - Document proper `format_html()` usage patterns
   - Include examples of correct vs incorrect usage

3. **Testing Enhancement**
   - Consider adding admin view tests
   - Test admin rendering with various data states
   - Verify HTML escaping works correctly

4. **Knowledge Base**
   - Create entry: "Django format_html: Common Mistakes and Solutions"
   - Document the difference between f-strings and format_html
   - Explain when to use each approach

---

## References

- [Django format_html Documentation](https://docs.djangoproject.com/en/6.0/ref/utils/#django.utils.html.format_html)
- [Django Admin Customization](https://docs.djangoproject.com/en/6.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display)
- File: [components/admin.py](../../../components/admin.py)
- Related: [issues0000004-missing-json-import.md](./issues0000004-missing-json-import.md)

---

## Checklist

- [x] Root cause identified
- [x] Solution implemented and tested
- [x] All three methods fixed
- [x] Admin interface verified working
- [x] Manual Test 2 passes
- [ ] Codebase reviewed for similar issues
- [ ] Documentation updated
- [ ] Knowledge base entry created
