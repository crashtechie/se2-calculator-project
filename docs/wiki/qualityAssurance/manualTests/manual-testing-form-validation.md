# Manual Testing: Form Validation

**Project:** SE2 Calculator Project  
**Document Type:** Quality Assurance - Form Validation Testing  
**Last Updated:** January 30, 2026  
**Status:** Active  

---

## Purpose

This document provides test procedures for manual testing of form validation, error handling, and user input across all forms in the SE2 Calculator Project.

---

## Prerequisites

- Development server running
- Browser with developer tools open
- Understanding of validation rules for each form

---

## Ores Form Validation

### Test 1: Required Fields - Ore Form

**Objective:** Verify required field validation works

**Steps:**
1. Navigate to http://localhost:8000/ores/create/
2. Leave all fields blank
3. Click "Submit" button
4. Verify validation errors display
5. Verify required fields are indicated:
   - Name (required)
   - Mass (required)
6. Verify form does not submit
7. Verify user stays on form page
8. Verify error messages are clear and helpful

**Expected Results:**
- ✅ Form does not submit with missing required fields
- ✅ Error messages display for each required field
- ✅ Error messages are clear: "This field is required"
- ✅ Required fields marked with asterisk or label
- ✅ Focus moves to first error field

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 2: Data Type Validation - Ore Mass

**Objective:** Verify mass field only accepts valid numeric input

**Steps:**
1. Navigate to ore create form
2. Enter valid name: "Test Ore"
3. Test invalid mass values:
   - Text: "abc" → Should show error
   - Empty: "" → Should show error (required)
   - Special chars: "!@#" → Should show error
4. Test edge case mass values:
   - Zero: "0" → Should work (valid)
   - Negative: "-10" → Should show error
   - Decimal: "123.45" → Should work
   - Large number: "999999.99" → Should work
5. Verify error messages are descriptive

**Expected Results:**
- ✅ Non-numeric input rejected
- ✅ Negative numbers rejected
- ✅ Positive numbers and zero accepted
- ✅ Decimal numbers accepted
- ✅ Error message: "Enter a valid number"

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 3: Field Length Validation - Ore Name

**Objective:** Verify name field respects max length

**Steps:**
1. Navigate to ore create form
2. Enter name exceeding max length (if max_length=100):
   - Enter 101+ characters
   - Verify validation error or truncation
3. Enter valid length name:
   - Enter 50 characters → Should work
   - Enter exactly 100 characters → Should work
4. Test minimum length (if applicable)
5. Verify character counter (if implemented)

**Expected Results:**
- ✅ Max length enforced (100 characters)
- ✅ Error message if exceeded
- ✅ Valid lengths accepted
- ✅ Clear indication of limits

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 4: Unique Constraint Validation - Ore Name

**Objective:** Verify duplicate ore names are prevented

**Steps:**
1. Create an ore with name "Duplicate Test Ore"
2. Navigate to create new ore
3. Enter same name: "Duplicate Test Ore"
4. Enter valid mass: 100
5. Click "Submit"
6. Verify validation error displays
7. Verify error message mentions duplicate/existing ore
8. Verify form does not submit
9. Test case sensitivity:
   - Try "duplicate test ore" (lowercase)
   - Verify if duplicate check is case-insensitive

**Expected Results:**
- ✅ Duplicate names prevented
- ✅ Clear error message: "Ore with this name already exists"
- ✅ Case-insensitive duplicate checking
- ✅ Form does not submit

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## Components Form Validation

### Test 5: Required Fields - Component Form

**Objective:** Verify component required fields

**Steps:**
1. Navigate to http://localhost:8000/components/create/
2. Leave all fields blank
3. Click "Submit"
4. Verify errors for:
   - Name (required)
   - Materials/Ores (may be optional or required)
5. Fill in name only, submit
6. Verify behavior based on requirements

**Expected Results:**
- ✅ Required fields validated
- ✅ Clear error messages
- ✅ Form behavior matches requirements

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 6: Material Validation - Component Form

**Objective:** Verify component materials validation

**Steps:**
1. Navigate to component create form
2. Add a material row
3. Test invalid material inputs:
   - Select ore but leave quantity blank → Error
   - Enter quantity but don't select ore → Error
   - Enter negative quantity: -5 → Error
   - Enter zero quantity: 0 → Error or valid (check requirements)
   - Enter decimal quantity: 2.5 → Valid or error (check requirements)
4. Test valid material:
   - Select ore
   - Enter quantity: 10
   - Verify no errors
5. Test multiple materials with same ore:
   - Add 2 rows with same ore
   - Verify if duplicates allowed or prevented

**Expected Results:**
- ✅ Ore selection required when quantity entered
- ✅ Quantity required when ore selected
- ✅ Negative quantities rejected
- ✅ Valid materials accepted
- ✅ Duplicate ore handling is correct

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 7: Dynamic Form Behavior - Component Materials

**Objective:** Verify add/remove material rows works correctly

**Steps:**
1. Navigate to component create form
2. Click "Add Material" button
   - Verify new material row appears
   - Verify ore dropdown populates correctly
3. Click "Add Material" multiple times
   - Verify multiple rows can be added
4. Fill in some material rows
5. Click "Remove" button on a row
   - Verify row is removed
   - Verify data in other rows persists
6. Remove all material rows
   - Verify form still works (if materials optional)
7. Test validation with dynamic rows:
   - Add row, leave it blank
   - Submit form
   - Verify appropriate validation

**Expected Results:**
- ✅ Add material button works
- ✅ Remove material button works
- ✅ Multiple rows can be added
- ✅ Removing rows doesn't affect other data
- ✅ Validation works on dynamic rows

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## Blocks Form Validation

### Test 8: Required Fields - Block Form

**Objective:** Verify block required fields

**Steps:**
1. Navigate to http://localhost:8000/blocks/create/
2. Leave all fields blank
3. Click "Submit"
4. Verify errors for:
   - Name (required)
   - Consumer components (may be required)
   - Producer components (may be required)

**Expected Results:**
- ✅ Required fields validated
- ✅ Clear error messages
- ✅ Form does not submit

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 9: Business Rule Validation - Consumer/Producer

**Objective:** Verify block requires at least one consumer and producer

**Steps:**
1. Navigate to block create form
2. Fill in name: "Test Block"
3. Select only consumer components (no producers)
4. Click "Submit"
5. Verify error: "Must have at least one producer component"
6. Clear form, try reverse:
   - Select only producer components (no consumers)
   - Verify error: "Must have at least one consumer component"
7. Select at least one consumer AND one producer
8. Verify form submits successfully

**Expected Results:**
- ✅ At least one consumer required
- ✅ At least one producer required
- ✅ Clear error messages for violations
- ✅ Valid combinations accepted

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 10: Component Selection Validation - Blocks

**Objective:** Verify component selection works correctly

**Steps:**
1. Navigate to block create form
2. Test component selection:
   - Verify consumer component dropdown populates
   - Verify producer component dropdown populates
3. Select multiple consumers
   - Verify multiple selection works
4. Select multiple producers
   - Verify multiple selection works
5. Test selecting same component as both consumer and producer:
   - Verify if allowed or prevented
   - If allowed, verify it works correctly
   - If prevented, verify error message

**Expected Results:**
- ✅ Component dropdowns populate correctly
- ✅ Multiple selections work
- ✅ Business rules enforced correctly
- ✅ Clear feedback on selections

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## General Form Validation

### Test 11: Client-Side vs Server-Side Validation

**Objective:** Verify both client and server validation work

**Steps:**
1. Navigate to any create form
2. Test with browser JavaScript enabled:
   - Enter invalid data
   - Verify client-side validation catches it before submit
   - Verify immediate feedback (no page reload)
3. Disable JavaScript in browser
4. Enter same invalid data
5. Submit form
6. Verify server-side validation catches it
7. Verify error messages display on page reload

**Expected Results:**
- ✅ Client-side validation works (with JS)
- ✅ Server-side validation works (without JS)
- ✅ Error messages display in both cases
- ✅ Form does not submit invalid data in either case

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 12: Error Message Display

**Objective:** Verify error messages are clear and well-positioned

**Steps:**
1. Trigger various validation errors
2. For each error, verify:
   - Error message displays near the relevant field
   - Error message is in red or highlighted color
   - Field with error is highlighted/outlined
   - Error icon displays (if implemented)
3. Verify multiple errors:
   - Trigger errors on multiple fields
   - Verify all errors display simultaneously
   - Verify summary error message at top (if implemented)
4. Verify error messages:
   - Use clear, non-technical language
   - Provide actionable guidance
   - Are concise but informative

**Expected Results:**
- ✅ Error messages clearly visible
- ✅ Positioned near relevant fields
- ✅ Multiple errors all display
- ✅ Error styling is clear
- ✅ Messages are user-friendly

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 13: Success Message Display

**Objective:** Verify success messages display after form submission

**Steps:**
1. Navigate to any create form
2. Fill in valid data
3. Submit form
4. Verify success message displays:
   - Message appears at top of page or near form
   - Message is in green or success color
   - Message is clear: "[Object] created successfully"
5. Test success messages for different actions:
   - Create
   - Update
   - Delete
6. Verify message disappears after:
   - Page navigation
   - Timeout (if auto-dismiss is implemented)

**Expected Results:**
- ✅ Success messages display
- ✅ Messages are positive and clear
- ✅ Success styling is distinct from errors
- ✅ Messages appear for all success actions

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 14: Form Persistence on Error

**Objective:** Verify form data persists when validation fails

**Steps:**
1. Navigate to any create form
2. Fill in most fields with valid data
3. Leave one required field blank or enter invalid data
4. Submit form
5. Verify validation error displays
6. Verify all valid data you entered is still in the form
7. Verify you don't have to re-enter everything
8. Correct the error
9. Verify form now submits successfully

**Expected Results:**
- ✅ Valid form data persists on error
- ✅ User doesn't lose their work
- ✅ Only need to fix the specific error
- ✅ Form submission works after correction

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 15: Cancel/Back Functionality

**Objective:** Verify cancel button works and handles unsaved data

**Steps:**
1. Navigate to any create form
2. Fill in some data (don't submit)
3. Click "Cancel" or "Back" button
4. Verify behavior:
   - Option A: Immediately returns to previous page (data lost)
   - Option B: Shows confirmation dialog: "Unsaved changes will be lost"
5. If confirmation dialog:
   - Click "Cancel" in dialog → Stay on form with data
   - Click "OK" or "Leave" → Return to previous page
6. Test from edit form as well
7. Verify no data is saved if user cancels

**Expected Results:**
- ✅ Cancel button works
- ✅ User is warned about unsaved data (optional)
- ✅ No partial saves occur
- ✅ Returns to appropriate page

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 16: XSS Prevention in Forms

**Objective:** Verify forms prevent cross-site scripting attacks

**Steps:**
1. Navigate to any create form
2. Enter potentially malicious input in text fields:
   ```
   <script>alert('XSS')</script>
   ```
3. Submit form
4. Navigate to detail page for created object
5. Verify script does not execute
6. Verify script is displayed as text or sanitized
7. Test other XSS vectors:
   ```html
   <img src=x onerror="alert('XSS')">
   ```
8. Verify all HTML is escaped or sanitized

**Expected Results:**
- ✅ Scripts do not execute
- ✅ HTML is escaped/sanitized
- ✅ Data is safely displayed
- ✅ No security vulnerabilities

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## Summary & Reporting

### Test Session Information

**Date:** _______________________  
**Tester:** _______________________  
**Browser:** _______________________  
**Test Duration:** _______________________  

### Results Summary

| Test # | Test Name | Result | Issues Found |
|--------|-----------|--------|--------------|
| 1 | Ore Required Fields | ☐ PASS ☐ FAIL | |
| 2 | Ore Mass Validation | ☐ PASS ☐ FAIL | |
| 3 | Ore Name Length | ☐ PASS ☐ FAIL | |
| 4 | Ore Name Unique | ☐ PASS ☐ FAIL | |
| 5 | Component Required | ☐ PASS ☐ FAIL | |
| 6 | Component Materials | ☐ PASS ☐ FAIL | |
| 7 | Dynamic Materials | ☐ PASS ☐ FAIL | |
| 8 | Block Required Fields | ☐ PASS ☐ FAIL | |
| 9 | Consumer/Producer | ☐ PASS ☐ FAIL | |
| 10 | Component Selection | ☐ PASS ☐ FAIL | |
| 11 | Client/Server Validation | ☐ PASS ☐ FAIL | |
| 12 | Error Messages | ☐ PASS ☐ FAIL | |
| 13 | Success Messages | ☐ PASS ☐ FAIL | |
| 14 | Form Persistence | ☐ PASS ☐ FAIL | |
| 15 | Cancel Button | ☐ PASS ☐ FAIL | |
| 16 | XSS Prevention | ☐ PASS ☐ FAIL | |

**Total Tests:** 16  
**Passed:** _______  
**Failed:** _______  
**Pass Rate:** _______ %  

### Critical Validation Issues

List any critical validation bypasses or security issues:

1. _______________________________________________________
2. _______________________________________________________

### Recommendations

_____________________________________________________________________________
_____________________________________________________________________________

---

**Tester Signature:** _______________________  
**Date:** _______________________
