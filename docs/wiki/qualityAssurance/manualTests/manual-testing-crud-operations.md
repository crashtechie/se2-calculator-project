# Manual Testing: CRUD Operations

**Project:** SE2 Calculator Project  
**Document Type:** Quality Assurance - CRUD Testing Procedures  
**Last Updated:** January 30, 2026  
**Status:** Active  

---

## Purpose

This document provides detailed test procedures for manual testing of CRUD (Create, Read, Update, Delete) operations across all apps in the SE2 Calculator Project.

---

## Prerequisites

- Development server running: `uv run python manage.py runserver`
- Database with sample data loaded
- Browser with developer tools open
- Test data ready for creation

---

## Ores App - CRUD Testing

### Test 1: Create New Ore

**Objective:** Verify ore creation with valid data

**Steps:**
1. Navigate to http://localhost:8000/ores/
2. Click "Create New Ore" or "Add Ore" button
3. Fill in the form:
   - **Name:** "Test Ore Manual"
   - **Mass:** 150.5
   - **Description:** "This is a test ore created during manual testing"
4. Click "Save" or "Submit" button
5. Verify redirect to ore detail page or list page
6. Verify success message displays: "Ore created successfully" (or similar)
7. Verify new ore appears in the list
8. Verify all entered data is saved correctly

**Expected Results:**
- ✅ Form submits without errors
- ✅ Success message displays
- ✅ New ore appears in database
- ✅ All field values are correct
- ✅ Timestamps are generated (created_at, updated_at)

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 2: Read Ore (List View)

**Objective:** Verify ore list displays correctly

**Steps:**
1. Navigate to http://localhost:8000/ores/
2. Verify page loads without errors
3. Verify list displays all ores from database
4. Check pagination (if >25 ores exist)
5. Verify each ore shows:
   - Name
   - Mass
   - Description (truncated or full)
   - Action buttons (View, Edit, Delete)
6. Test search functionality (if available)
7. Test sorting by columns (if available)
8. Test filtering options (if available)

**Expected Results:**
- ✅ Page loads in <2 seconds
- ✅ All ores are displayed
- ✅ Data is accurate and formatted properly
- ✅ Pagination works (if applicable)
- ✅ Search/sort/filter work correctly
- ✅ No console errors

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 3: Read Ore (Detail View)

**Objective:** Verify individual ore detail page displays correctly

**Steps:**
1. Navigate to http://localhost:8000/ores/
2. Click on an ore name or "View Details" button
3. Verify detail page loads
4. Verify all ore information displays:
   - Name
   - Mass (with unit)
   - Description (full text)
   - UUID
   - Created timestamp
   - Updated timestamp
5. Verify action buttons present (Edit, Delete, Back)
6. Verify formatting is clean and readable

**Expected Results:**
- ✅ Detail page loads successfully
- ✅ All data fields are visible
- ✅ Data is accurate
- ✅ UUIDs are properly formatted
- ✅ Timestamps are human-readable
- ✅ Navigation buttons work

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 4: Update Ore

**Objective:** Verify ore can be updated successfully

**Steps:**
1. Navigate to an ore detail page
2. Click "Edit" button
3. Verify form pre-populates with existing data
4. Modify the ore:
   - **Name:** Add " - Modified" to the end
   - **Mass:** Change to a different value
   - **Description:** Add " Updated during testing."
5. Click "Save" or "Update" button
6. Verify redirect to detail or list page
7. Verify success message: "Ore updated successfully"
8. Verify changes are saved correctly
9. Verify updated_at timestamp changed
10. Verify created_at timestamp unchanged

**Expected Results:**
- ✅ Edit form pre-populates correctly
- ✅ Changes save without errors
- ✅ Success message displays
- ✅ Updated data is correct
- ✅ Timestamps update appropriately

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 5: Delete Ore (with Confirmation)

**Objective:** Verify ore can be deleted with confirmation

**Steps:**
1. Navigate to ore list or detail page
2. Click "Delete" button on an ore
3. Verify confirmation page displays
4. Verify confirmation message: "Are you sure you want to delete [Ore Name]?"
5. Verify ore details are shown on confirmation page
6. Click "Cancel" button
7. Verify redirected back without deletion
8. Verify ore still exists
9. Click "Delete" again
10. Click "Confirm" or "Yes, Delete" button
11. Verify redirect to list page
12. Verify success message: "Ore deleted successfully"
13. Verify ore no longer appears in list
14. Try to access deleted ore's detail page directly (should 404)

**Expected Results:**
- ✅ Confirmation page appears before deletion
- ✅ Cancel works without deleting
- ✅ Confirm deletes the ore
- ✅ Success message displays
- ✅ Ore is removed from database
- ✅ Related data handled correctly (cascade/prevent)

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## Components App - CRUD Testing

### Test 6: Create New Component with Materials

**Objective:** Verify component creation with ore materials

**Steps:**
1. Navigate to http://localhost:8000/components/
2. Click "Create New Component" button
3. Fill in basic information:
   - **Name:** "Test Component Manual"
   - **Description:** "Component for manual testing"
4. Add materials (ores):
   - Click "Add Material" button
   - Select an ore from dropdown
   - Enter quantity: 5
   - Click "Add Material" again
   - Select different ore
   - Enter quantity: 10
5. Click "Save" button
6. Verify redirect to component detail page
7. Verify success message displays
8. Verify component appears in list
9. Verify materials are saved and displayed correctly

**Expected Results:**
- ✅ Form allows adding multiple materials
- ✅ JavaScript material selector works
- ✅ Materials save as JSON in database
- ✅ Component and materials relationship is correct
- ✅ Success message displays

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 7: Read Component (with Materials Display)

**Objective:** Verify component detail shows materials correctly

**Steps:**
1. Navigate to http://localhost:8000/components/
2. Click on a component that has materials
3. Verify detail page displays:
   - Component name
   - Component description
   - UUID
   - Created/Updated timestamps
   - List of materials (ores) with quantities
4. Verify materials are formatted as:
   - Ore name: quantity
   - Or table format with ore and quantity columns
5. Verify ore names are clickable links to ore details (if implemented)

**Expected Results:**
- ✅ Component details display correctly
- ✅ Materials list is visible and formatted
- ✅ Quantities are accurate
- ✅ Ore relationships resolve correctly

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 8: Update Component Materials

**Objective:** Verify component materials can be modified

**Steps:**
1. Navigate to a component detail page
2. Click "Edit" button
3. Verify existing materials display in form
4. Modify materials:
   - Change quantity of existing material
   - Remove one material
   - Add a new material
5. Click "Save" button
6. Verify success message
7. Verify materials are updated correctly
8. Verify removed material is gone
9. Verify new material appears

**Expected Results:**
- ✅ Edit form shows existing materials
- ✅ Can modify, add, and remove materials
- ✅ Changes save correctly
- ✅ JSON data updates properly

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 9: Delete Component

**Objective:** Verify component deletion

**Steps:**
1. Navigate to component list or detail
2. Click "Delete" on a component
3. Verify confirmation page
4. Confirm deletion
5. Verify success message
6. Verify component removed from list
7. Verify materials data is cleaned up

**Expected Results:**
- ✅ Confirmation required before deletion
- ✅ Component deletes successfully
- ✅ Associated data handled correctly

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## Blocks App - CRUD Testing

### Test 10: Create New Block with Components

**Objective:** Verify block creation with component selection

**Steps:**
1. Navigate to http://localhost:8000/blocks/
2. Click "Create New Block" button
3. Fill in form:
   - **Name:** "Test Block Manual"
   - **Description:** "Block for manual testing"
   - **Consumer Components:** Select 1-3 components (input materials)
   - **Producer Components:** Select 1-2 components (output products)
4. Click "Save" button
5. Verify consumer/producer validation (at least one of each)
6. Verify success message
7. Verify block appears in list
8. Verify component relationships are correct

**Expected Results:**
- ✅ Form validates consumer/producer requirements
- ✅ Component selection works
- ✅ Block saves successfully
- ✅ Relationships are created correctly

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 11: Read Block (with Resource Chain)

**Objective:** Verify block detail shows complete resource chain

**Steps:**
1. Navigate to a block detail page
2. Verify display includes:
   - Block name and description
   - Consumer components (inputs)
   - Producer components (outputs)
   - Resource chain: Ores → Components → Block
3. Verify resource chain traces back to base ores
4. Verify all component relationships resolve
5. Verify quantities/materials display correctly

**Expected Results:**
- ✅ Block details are complete
- ✅ Consumer/producer components listed
- ✅ Resource chain displays correctly
- ✅ Can trace from block to base ores

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 12: Update Block Components

**Objective:** Verify block components can be updated

**Steps:**
1. Navigate to a block detail page
2. Click "Edit" button
3. Modify components:
   - Change a consumer component
   - Change a producer component
4. Verify validation still enforces consumer/producer rules
5. Save changes
6. Verify success message
7. Verify component relationships updated
8. Verify resource chain updates correctly

**Expected Results:**
- ✅ Can modify component selections
- ✅ Validation enforced on update
- ✅ Changes save correctly
- ✅ Relationships update properly

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

### Test 13: Delete Block

**Objective:** Verify block deletion

**Steps:**
1. Navigate to block list or detail
2. Click "Delete" button
3. Verify confirmation page
4. Confirm deletion
5. Verify success message
6. Verify block removed from list
7. Verify component relationships cleaned up
8. Verify components themselves are NOT deleted

**Expected Results:**
- ✅ Confirmation required
- ✅ Block deletes successfully
- ✅ Components remain in database
- ✅ Only relationships are removed

**Test Result:** ☐ PASS ☐ FAIL

**Notes:**
_______________________________________________

---

## Summary & Reporting

### Test Session Information

**Date:** _______________________  
**Tester:** _______________________  
**Environment:** _______________________  
**Browser:** _______________________  
**Test Duration:** _______________________  

### Results Summary

| Test # | Test Name | Result | Issues Found |
|--------|-----------|--------|--------------|
| 1 | Create Ore | ☐ PASS ☐ FAIL | |
| 2 | Read Ore List | ☐ PASS ☐ FAIL | |
| 3 | Read Ore Detail | ☐ PASS ☐ FAIL | |
| 4 | Update Ore | ☐ PASS ☐ FAIL | |
| 5 | Delete Ore | ☐ PASS ☐ FAIL | |
| 6 | Create Component | ☐ PASS ☐ FAIL | |
| 7 | Read Component | ☐ PASS ☐ FAIL | |
| 8 | Update Component | ☐ PASS ☐ FAIL | |
| 9 | Delete Component | ☐ PASS ☐ FAIL | |
| 10 | Create Block | ☐ PASS ☐ FAIL | |
| 11 | Read Block | ☐ PASS ☐ FAIL | |
| 12 | Update Block | ☐ PASS ☐ FAIL | |
| 13 | Delete Block | ☐ PASS ☐ FAIL | |

**Total Tests:** 13  
**Passed:** _______  
**Failed:** _______  
**Pass Rate:** _______ %  

### Issues Found

List any issues discovered during testing:

1. _______________________________________________________
2. _______________________________________________________
3. _______________________________________________________

### Recommendations

_____________________________________________________________________________
_____________________________________________________________________________
_____________________________________________________________________________

---

**Tester Signature:** _______________________  
**Date:** _______________________
