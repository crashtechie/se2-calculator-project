# Manual Testing Overview

**Project:** SE2 Calculator Project  
**Document Type:** Quality Assurance - Manual Testing Guide  
**Last Updated:** January 30, 2026  
**Status:** Active  

---

## Purpose

This document provides an overview of manual testing procedures for the SE2 Calculator Project. Manual testing complements automated test suites to ensure complete quality assurance coverage for functionality, usability, and user experience.

---

## Manual Testing Strategy

### When to Perform Manual Testing

1. **After Feature Implementation** - Verify new features work as expected in real-world scenarios
2. **Before Releases** - Final verification before production deployment
3. **UI/UX Changes** - Validate visual elements and user interactions
4. **Cross-Browser Testing** - Ensure compatibility across different browsers
5. **Integration Points** - Verify complex workflows that span multiple apps
6. **Exploratory Testing** - Discover edge cases not covered by automated tests

### Manual Testing Types

- **Functional Testing** - Verify features work according to specifications
- **UI/UX Testing** - Evaluate visual design, layout, and user experience
- **Browser Compatibility** - Test across different browsers and devices
- **Exploratory Testing** - Ad-hoc testing to discover unexpected issues
- **User Acceptance Testing (UAT)** - Validate with end-user perspective
- **Regression Testing** - Verify existing functionality after changes

---

## Test Environment Setup

### Prerequisites

1. **Development Environment**
   ```bash
   # Ensure all dependencies are installed
   cd /home/dsmi001/app/se2-calculator-project
   uv sync
   ```

2. **Database Setup**
   ```bash
   # Start PostgreSQL container
   docker-compose up -d database
   
   # Apply migrations
   cd app
   uv run python manage.py migrate
   ```

3. **Load Sample Data**
   ```bash
   # Load fixture data for testing
   uv run python manage.py loaddata sample_ores sample_components sample_blocks
   ```

4. **Start Development Server**
   ```bash
   uv run python manage.py runserver
   ```

5. **Access Application**
   - Navigate to: http://localhost:8000/
   - Admin interface: http://localhost:8000/admin/

### Test User Accounts

- **Admin User:** Create via `python manage.py createsuperuser`
- **Regular User:** Create via admin interface or registration (if implemented)

---

## Testing Workflow

### 1. Pre-Testing Checklist

- [ ] Development server is running
- [ ] Database has sample data loaded
- [ ] Browser developer tools are open (F12)
- [ ] Test scenario/checklist is prepared
- [ ] Issue tracking document is ready

### 2. During Testing

- [ ] Follow test scenarios step-by-step
- [ ] Document unexpected behavior immediately
- [ ] Take screenshots of issues
- [ ] Note browser console errors
- [ ] Record steps to reproduce issues
- [ ] Test both success and failure paths

### 3. Post-Testing

- [ ] Create issue reports for bugs found
- [ ] Update test documentation with new findings
- [ ] Report results to development team
- [ ] Archive test results with timestamp

---

## Test Coverage Areas

### Application Areas to Test

1. **Ores Management**
   - CRUD operations (Create, Read, Update, Delete)
   - List view with pagination, search, sorting
   - Form validation
   - Detail views

2. **Components Management**
   - CRUD operations
   - Material (ore) selection and relationships
   - JSON data handling for materials
   - Component-ore relationships

3. **Blocks Management**
   - CRUD operations
   - Component selection and relationships
   - Consumer/producer validation
   - Resource chain display

4. **Navigation & UI**
   - Menu links and routing
   - Breadcrumbs
   - Page layouts and responsiveness
   - Error pages (404, 500)

5. **Forms & Validation**
   - Required field validation
   - Data type validation
   - Error message display
   - Success message display

---

## Test Documentation

### Related Documents

- [CRUD Operations Testing](./manual-testing-crud-operations.md) - Test procedures for Create, Read, Update, Delete
- [UI Navigation Testing](./manual-testing-ui-navigation.md) - Navigation and interface testing
- [Form Validation Testing](./manual-testing-form-validation.md) - Form input and validation testing
- [Browser Compatibility Testing](./manual-testing-browser-compatibility.md) - Cross-browser testing procedures

### Issue Tracking

- **Open Issues:** `/docs/issues/open/`
- **Resolved Issues:** `/docs/issues/resolved/`
- **Issue Template:** Use consistent format as shown in existing issues

---

## Best Practices

### DO

✅ Test both success and failure scenarios  
✅ Document exact steps to reproduce issues  
✅ Clear browser cache between test sessions  
✅ Test with realistic data volumes  
✅ Verify error messages are user-friendly  
✅ Test keyboard navigation and accessibility  
✅ Check console for JavaScript errors  
✅ Verify responsive design on different screen sizes  

### DON'T

❌ Skip steps in test procedures  
❌ Assume functionality works without testing  
❌ Test on outdated code/database  
❌ Ignore minor visual issues  
❌ Fail to document discovered issues  
❌ Test without fresh sample data  
❌ Rush through test scenarios  

---

## Reporting Issues

### Issue Report Requirements

When creating issue reports in `docs/issues/open/`, include:

1. **Clear Title** - Descriptive and specific
2. **Summary** - Brief description of the issue
3. **Impact** - How it affects users/functionality
4. **Environment** - OS, browser, app version
5. **Steps to Reproduce** - Detailed, numbered steps
6. **Expected Behavior** - What should happen
7. **Actual Behavior** - What actually happens
8. **Screenshots** - Visual evidence if applicable
9. **Console Errors** - Any JavaScript/network errors
10. **Date Reported** - When the issue was discovered

### Issue Filename Convention

```
issue{NUMBER}-{brief-description}.md
```

Example: `issue0000004-components-link-redirects-to-blocks.md`

---

## Test Metrics

### Tracking Manual Testing

- **Test Coverage** - Percentage of features manually tested
- **Pass Rate** - Percentage of tests passed
- **Issues Found** - Number of new issues discovered
- **Critical Issues** - Number of high-priority issues
- **Regression Issues** - Previously working features now broken
- **Testing Time** - Time spent on manual testing

### Quality Goals

- **Feature Coverage:** 100% of user-facing features
- **Pass Rate:** >95% for stable features
- **Critical Issues:** 0 before release
- **Response Time:** Issues documented within 24 hours

---

## Resources

### Tools

- **Browser DevTools** - Chrome/Firefox developer tools
- **Screenshot Tools** - Built-in browser screenshot or external tools
- **Screen Recording** - For complex interaction issues
- **Responsive Design Mode** - Test different device sizes

### Reference Materials

- **Enhancement Requests** - `/docs/enhancementRequests/` for feature specifications
- **Deployment Guides** - Step-by-step implementation details
- **API Documentation** - For testing API endpoints
- **Database Schema** - Understanding data relationships

---

## Review & Updates

This document should be reviewed and updated:

- After each major feature implementation
- When testing procedures change
- After discovering new testing approaches
- Quarterly for general maintenance

---

**Document Owner:** QA Team  
**Contributors:** Development Team  
**Approval Required:** Yes (for major changes)  

---

## Sign-Off

| Role | Name | Date |
|------|------|------|
| QA Lead | TBD | TBD |
| Development Lead | TBD | TBD |
| Project Manager | TBD | TBD |
