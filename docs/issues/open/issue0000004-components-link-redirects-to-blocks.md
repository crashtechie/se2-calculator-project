# ISSUE-004: Components Link Redirects to Blocks Page

**Status:** Open  
**Priority:** Medium  
**Created:** 2026-01-30  
**Component:** UI Navigation  
**Affects Version:** 0.4.1-alpha

## Problem Description

The "components" link in the title bar navigation incorrectly directs users to the blocks page instead of the components page.

## Error Output

- Clicking "components" link navigates to `/blocks/`
- Expected: Navigate to `/components/`

## Root Cause

Incorrect URL configuration in the navigation template or URL routing mismatch in the title bar component.

## Technical Details

**Affected Files:**
- `app/templates/base.html` (likely)
- Navigation template/component

**Expected Behavior:**
- Components link → `/components/` → Components list page

**Actual Behavior:**
- Components link → `/blocks/` → Blocks list page

## Solution

### Step 1: Identify navigation template

```bash
grep -r "components" app/templates/
```

### Step 2: Verify URL configuration

Check the href attribute for the components link in the navigation.

### Step 3: Update the link

Correct the URL to point to `{% url 'components:component_list' %}` or equivalent.

### Step 4: Test navigation

```bash
uv run python manage.py runserver
# Click components link in browser
```

## Verification Checklist

- [ ] Identify template file with navigation
- [ ] Verify components URL configuration
- [ ] Update link to correct URL
- [ ] Test components link navigates correctly
- [ ] Test blocks link still works
- [ ] Test all other navigation links

## Related Files

- `app/templates/base.html`
- `app/components/urls.py`
- `app/blocks/urls.py`

## Notes

- Review all navigation links for consistency
- Consider adding automated navigation tests
