# Issue: Components link in title bar redirects to blocks page

## Summary
The "components" link in the title bar of the UI incorrectly directs users to the "blocks" page instead of the "components" page.

## Impact
- Users clicking on the "components" link in the navigation cannot access the components page
- Navigation confusion between blocks and components functionality
- UI inconsistency and poor user experience

## Environment
- Project: se2-calculator-project
- Branch: develop
- Affected area: Title bar navigation

## Symptoms
- Clicking the "components" link in the title bar navigates to `/blocks/` or the blocks page
- Expected behavior: Should navigate to `/components/` or the components page

## Root Cause
Likely incorrect URL configuration in the navigation template or URL routing mismatch in the title bar/navigation component.

## Resolution
- [ ] Identify the template file containing the title bar navigation
- [ ] Verify the URL configuration for the components link
- [ ] Update the link to point to the correct components URL/route
- [ ] Test navigation to confirm both blocks and components links work correctly

## Verification
After fix, verify:
- Components link navigates to the components page
- Blocks link still navigates to the blocks page
- No other navigation links are affected

## Notes / Follow-ups
- Review all navigation links to ensure consistency
- Consider adding automated tests for navigation routing

## Date Reported
January 30, 2026
