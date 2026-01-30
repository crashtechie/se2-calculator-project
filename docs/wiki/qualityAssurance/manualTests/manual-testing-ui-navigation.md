# Manual Testing: UI Navigation

**Project:** SE2 Calculator Project  
**Document Type:** Quality Assurance - UI Navigation Testing  
**Last Updated:** January 30, 2026  
**Status:** Active  

---

## Purpose

This document provides test procedures for manual testing of user interface navigation, menu functionality, and overall user experience in the SE2 Calculator Project.

---

## Prerequisites

- Development server running
- Sample data loaded in database
- Browser with developer tools open

---

## Navigation Testing

### Test 1: Main Navigation Menu

**Objective:** Verify all main navigation links work correctly

**Steps:**
1. Navigate to http://localhost:8000/
2. Identify main navigation menu (typically in header/title bar)
3. Click "Home" or site logo
   - Verify redirects to home page
4. Click "Ores" link
   - Verify redirects to http://localhost:8000/ores/
   - Verify ores list displays
5. Click "Components" link
   - Verify redirects to http://localhost:8000/components/
   - Verify components list displays
   - **CRITICAL:** Verify does NOT redirect to blocks page
6. Click "Blocks" link
   - Verify redirects to http://localhost:8000/blocks/
   - Verify blocks list displays
7. Click "Admin" link (if visible)
   - Verify redirects to admin interface
8. Test each link from different pages (not just home)

**Expected Results:**
- ✅ All navigation links work correctly
- ✅ Each link goes to the correct destination
- ✅ No broken links (404 errors)
- ✅ Active page highlighted in navigation (if implemented)
- ✅ Navigation visible on all pages

**Known Issues:**
- ⚠️ Components link redirects to blocks page (Issue #0000004)

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 2: Breadcrumb Navigation

**Objective:** Verify breadcrumb navigation displays and works correctly

**Steps:**
1. Navigate to home page
2. Click through to a detail page: Home → Ores → [Specific Ore]
3. Verify breadcrumb displays: `Home > Ores > [Ore Name]`
4. Click "Ores" in breadcrumb
   - Verify returns to ores list
5. Click "Home" in breadcrumb
   - Verify returns to home page
6. Test breadcrumbs from different page depths:
   - List pages
   - Detail pages
   - Edit pages
   - Create pages
7. Verify breadcrumb updates with page navigation

**Expected Results:**
- ✅ Breadcrumbs display on all pages
- ✅ Breadcrumb links work correctly
- ✅ Current page shown in breadcrumb (not linked)
- ✅ Breadcrumb reflects actual page hierarchy

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 3: Back Button Navigation

**Objective:** Verify browser back button works correctly

**Steps:**
1. Navigate through several pages:
   - Home → Ores List → Ore Detail → Edit Ore
2. Click browser back button
   - Verify returns to Ore Detail (not edit mode)
3. Click back button again
   - Verify returns to Ores List
4. Click back button again
   - Verify returns to Home
5. Click forward button
   - Verify moves forward through history
6. Test back button after form submission
   - Create a new ore
   - Click back button
   - Verify doesn't re-submit form
   - Verify shows appropriate page

**Expected Results:**
- ✅ Back button navigates correctly
- ✅ No form re-submission warnings
- ✅ Page state is preserved
- ✅ No JavaScript errors on back navigation

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 4: Footer Navigation

**Objective:** Verify footer links work correctly

**Steps:**
1. Scroll to bottom of any page
2. Identify footer section
3. Test all footer links:
   - About
   - Contact
   - Documentation
   - GitHub repository (if linked)
   - License information
4. Verify external links open in new tab
5. Verify internal links stay in same tab

**Expected Results:**
- ✅ All footer links work
- ✅ External links open in new tab
- ✅ Internal links work correctly
- ✅ Footer displays on all pages

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## Page Layout Testing

### Test 5: Responsive Design - Mobile View

**Objective:** Verify UI adapts to mobile screen sizes

**Steps:**
1. Open browser developer tools (F12)
2. Enable responsive design mode / device toolbar
3. Set viewport to mobile size (e.g., iPhone 12: 390x844)
4. Navigate through all main pages:
   - Home
   - Ores list
   - Ore detail
   - Components list
   - Blocks list
5. Verify for each page:
   - Content is readable (no horizontal scroll)
   - Navigation menu adapts (hamburger menu?)
   - Buttons are touchable (not too small)
   - Tables adapt or scroll horizontally
   - Forms are usable
   - Images/graphics scale appropriately

**Expected Results:**
- ✅ All pages are mobile-friendly
- ✅ No content cut off
- ✅ Navigation accessible on mobile
- ✅ Forms functional on mobile
- ✅ Touch targets adequate size (min 44x44px)

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 6: Responsive Design - Tablet View

**Objective:** Verify UI adapts to tablet screen sizes

**Steps:**
1. Set viewport to tablet size (e.g., iPad: 768x1024)
2. Test both portrait and landscape orientations
3. Navigate through main pages
4. Verify layout uses screen space efficiently
5. Verify navigation is appropriate for tablet
6. Test touch interactions

**Expected Results:**
- ✅ Layout optimized for tablet
- ✅ Both orientations work well
- ✅ Touch-friendly interface
- ✅ Efficient use of screen space

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 7: Responsive Design - Desktop View

**Objective:** Verify UI works well on desktop screens

**Steps:**
1. Test at various desktop resolutions:
   - 1920x1080 (Full HD)
   - 1366x768 (Common laptop)
   - 2560x1440 (2K)
2. Verify content scales appropriately
3. Verify no excessive white space
4. Verify content centered or well-distributed
5. Test window resizing behavior

**Expected Results:**
- ✅ Works well at all common resolutions
- ✅ Content readable at all sizes
- ✅ Layout adapts to window resize
- ✅ No layout breaking

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## UI Elements Testing

### Test 8: Button Functionality

**Objective:** Verify all buttons work and provide feedback

**Steps:**
1. Identify all button types in the application:
   - Primary action buttons (Save, Submit, Create)
   - Secondary action buttons (Cancel, Back)
   - Destructive action buttons (Delete)
   - Navigation buttons
2. For each button type, verify:
   - Hover state changes appearance
   - Click triggers correct action
   - Disabled state (if applicable) prevents action
   - Loading state (if applicable) shows feedback
3. Test keyboard navigation (Tab to button, Enter to activate)
4. Verify button labels are clear and descriptive

**Expected Results:**
- ✅ All buttons function correctly
- ✅ Visual feedback on hover/click
- ✅ Disabled buttons don't trigger actions
- ✅ Keyboard navigation works
- ✅ Button labels are clear

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 9: Link Styling and Behavior

**Objective:** Verify links are styled and function correctly

**Steps:**
1. Identify different link types:
   - Navigation links
   - Content links (e.g., ore name in component detail)
   - Action links (Edit, Delete as links vs buttons)
2. Verify link styling:
   - Clearly identifiable as links (color, underline)
   - Hover state shows interactivity
   - Visited state (if applicable)
3. Verify all links:
   - Navigate to correct destination
   - Open in appropriate target (same/new tab)
   - Work with keyboard (Tab + Enter)
4. Test link behavior with Ctrl+Click (open in new tab)

**Expected Results:**
- ✅ Links clearly identifiable
- ✅ All links functional
- ✅ Consistent styling throughout app
- ✅ Keyboard accessible

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 10: Search Functionality

**Objective:** Verify search features work correctly

**Steps:**
1. Navigate to a list page with search (e.g., Ores)
2. Locate search box/field
3. Enter search term matching existing data
   - Verify results filter correctly
4. Enter search term with no matches
   - Verify "no results" message displays
5. Enter partial search term
   - Verify partial matching works (if implemented)
6. Test case sensitivity
   - Search for "iron" vs "IRON"
   - Verify behavior is consistent
7. Clear search and verify full list returns
8. Test search with special characters

**Expected Results:**
- ✅ Search filters results correctly
- ✅ Partial matching works (if implemented)
- ✅ No results message displays appropriately
- ✅ Search can be cleared
- ✅ Case sensitivity is appropriate

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 11: Sorting Functionality

**Objective:** Verify data sorting works correctly

**Steps:**
1. Navigate to a list page with sortable columns
2. Click column header to sort ascending
   - Verify data sorts correctly (A-Z or 1-10)
3. Click same column header again to sort descending
   - Verify data sorts correctly (Z-A or 10-1)
4. Test sorting on different column types:
   - Text columns (Name)
   - Numeric columns (Mass)
   - Date columns (Created At)
5. Verify sort indicator displays (arrow up/down)
6. Verify sorting persists with pagination

**Expected Results:**
- ✅ Sorting works on all sortable columns
- ✅ Sort direction indicator clear
- ✅ Data sorts correctly by type
- ✅ Sorting works with pagination

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 12: Pagination

**Objective:** Verify pagination works correctly

**Steps:**
1. Navigate to a list page with >25 items (or pagination threshold)
2. Verify pagination controls display
3. Click "Next" button
   - Verify next page loads
   - Verify page number updates
4. Click "Previous" button
   - Verify previous page loads
5. Click specific page number
   - Verify that page loads
6. Navigate to last page
   - Verify "Next" button disabled
7. Navigate to first page
   - Verify "Previous" button disabled
8. Test pagination with filters/search active
9. Verify page count is accurate

**Expected Results:**
- ✅ Pagination displays when needed
- ✅ Page navigation works correctly
- ✅ Page numbers accurate
- ✅ Disabled states work correctly
- ✅ Works with filters/search

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## Error Handling Testing

### Test 13: 404 Page Not Found

**Objective:** Verify 404 error page displays correctly

**Steps:**
1. Navigate to a non-existent URL: http://localhost:8000/does-not-exist/
2. Verify custom 404 page displays (not default Django error)
3. Verify 404 page includes:
   - Clear error message
   - Navigation back to home or main sections
   - Site header/footer
4. Test 404 for various non-existent URLs:
   - /ores/invalid-uuid/
   - /components/99999/
   - /random-page/

**Expected Results:**
- ✅ Custom 404 page displays
- ✅ User-friendly error message
- ✅ Navigation options available
- ✅ Consistent with site design

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 14: Permission/Access Denied

**Objective:** Verify access control and error messages

**Steps:**
1. If authentication is implemented:
   - Log out
   - Try to access protected pages
   - Verify redirect to login or access denied message
2. If admin-only sections exist:
   - Access as regular user
   - Verify appropriate error or redirect
3. Test unauthorized actions (if applicable)

**Expected Results:**
- ✅ Access control enforced
- ✅ Clear error messages
- ✅ Appropriate redirects
- ✅ No sensitive info leaked in errors

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## Accessibility Testing

### Test 15: Keyboard Navigation

**Objective:** Verify site is fully navigable with keyboard only

**Steps:**
1. Do not use mouse - keyboard only
2. Use Tab key to navigate through page elements
3. Verify all interactive elements are accessible:
   - Links
   - Buttons
   - Form fields
   - Navigation menus
4. Use Enter/Space to activate elements
5. Use Shift+Tab to navigate backwards
6. Verify focus indicator is visible on all elements
7. Test form submission with keyboard
8. Test dropdown/select with keyboard (arrow keys)

**Expected Results:**
- ✅ All interactive elements accessible via keyboard
- ✅ Focus indicator visible
- ✅ Logical tab order
- ✅ All functionality works without mouse

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 16: Screen Reader Compatibility (Basic)

**Objective:** Verify basic screen reader compatibility

**Steps:**
1. Enable screen reader (NVDA on Windows, VoiceOver on Mac)
2. Navigate through home page
3. Verify screen reader announces:
   - Page title
   - Headings
   - Links with descriptive text
   - Form labels
   - Button purposes
4. Verify images have alt text
5. Verify form fields have associated labels
6. Check for hidden elements that shouldn't be announced

**Expected Results:**
- ✅ Semantic HTML used correctly
- ✅ All content has text alternatives
- ✅ Form labels associated properly
- ✅ Navigation makes sense via screen reader

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## Summary & Reporting

### Test Session Information

**Date:** _______________________  
**Tester:** _______________________  
**Browser:** _______________________  
**Screen Resolution:** _______________________  
**Test Duration:** _______________________  

### Results Summary

| Test # | Test Name | Result | Issues Found |
|--------|-----------|--------|--------------|
| 1 | Main Navigation | ☐ PASS ☐ FAIL | |
| 2 | Breadcrumbs | ☐ PASS ☐ FAIL | |
| 3 | Back Button | ☐ PASS ☐ FAIL | |
| 4 | Footer Navigation | ☐ PASS ☐ FAIL | |
| 5 | Mobile Responsive | ☐ PASS ☐ FAIL | |
| 6 | Tablet Responsive | ☐ PASS ☐ FAIL | |
| 7 | Desktop Responsive | ☐ PASS ☐ FAIL | |
| 8 | Button Functionality | ☐ PASS ☐ FAIL | |
| 9 | Link Behavior | ☐ PASS ☐ FAIL | |
| 10 | Search Functionality | ☐ PASS ☐ FAIL | |
| 11 | Sorting | ☐ PASS ☐ FAIL | |
| 12 | Pagination | ☐ PASS ☐ FAIL | |
| 13 | 404 Error Page | ☐ PASS ☐ FAIL | |
| 14 | Access Control | ☐ PASS ☐ FAIL | |
| 15 | Keyboard Navigation | ☐ PASS ☐ FAIL | |
| 16 | Screen Reader | ☐ PASS ☐ FAIL | |

**Total Tests:** 16  
**Passed:** _______  
**Failed:** _______  
**Pass Rate:** _______ %  

### Issues Found

1. Components link redirects to blocks page (Issue #0000004)
2. _______________________________________________________
3. _______________________________________________________

### Recommendations

_____________________________________________________________________________
_____________________________________________________________________________

---

**Tester Signature:** _______________________  
**Date:** _______________________
