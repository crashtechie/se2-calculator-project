# ENH-0000010: Build Order Views & Templates

**Status:** Planned  
**Phase:** 3 - Build Order Calculator  
**Priority:** High  
**Dependencies:** ENH-0000009 (Complete)

## Full Documentation

📄 **Main ENH Doc**: `docs/enhancementRequests/phase3_buildorder/ENH0000010/ENH0000010-buildorder-crud-views-templates.md`

## Related Files

- Model: `#[[file:app/buildorders/models.py]]`
- Admin: `#[[file:app/buildorders/admin.py]]`
- Tests: `#[[file:app/buildorders/tests.py]]`
- Steering: `#[[file:.kiro/steering/01-django-standards.md]]`

## Requirements

### Functional Requirements
1. List view with pagination (10 items per page)
2. Detail view showing full resource chain (Blocks → Components → Ores)
3. Create view with dynamic block selector
4. Update view with existing data pre-populated
5. Delete view with confirmation
6. Search and filtering capabilities

### Non-Functional Requirements
1. Responsive Bootstrap 5 design
2. Consistent with existing Ores/Components/Blocks views
3. >80% test coverage
4. Performance: <500ms page load for lists
5. Accessibility: WCAG 2.1 AA compliance

## Implementation Tasks

### 1. URL Configuration
- [ ] Create `app/buildorders/urls.py`
- [ ] Define URL patterns for all CRUD operations
- [ ] Add namespace: `app_name = 'buildorders'`
- [ ] Include in main `urls.py`

### 2. Views
- [ ] `BuildOrderListView` - Paginated list with search
- [ ] `BuildOrderDetailView` - Full resource chain display
- [ ] `BuildOrderCreateView` - Form with block selector
- [ ] `BuildOrderUpdateView` - Edit existing build order
- [ ] `BuildOrderDeleteView` - Confirmation and deletion

### 3. Forms
- [ ] Create `app/buildorders/forms.py`
- [ ] `BuildOrderForm` with JSONField validation
- [ ] Custom widgets for block selection
- [ ] Validation for positive quantities
- [ ] Clean method for UUID validation

### 4. Templates
- [ ] `app/buildorders/templates/buildorders/buildorder_list.html`
- [ ] `app/buildorders/templates/buildorders/buildorder_detail.html`
- [ ] `app/buildorders/templates/buildorders/buildorder_form.html`
- [ ] `app/buildorders/templates/buildorders/buildorder_confirm_delete.html`
- [ ] Extend `base.html` for consistency

### 5. Testing
- [ ] View tests for all CRUD operations
- [ ] Form validation tests
- [ ] Template rendering tests
- [ ] Integration tests for resource calculations
- [ ] Achieve >80% coverage

### 6. Documentation
- [ ] Update README.md with BuildOrder features
- [ ] Add docstrings to all views
- [ ] Update CHANGELOG.md
- [ ] Create user guide in docs/

## Acceptance Criteria

- [ ] All CRUD operations functional via web interface
- [ ] Resource chain calculations display correctly
- [ ] Forms validate input properly
- [ ] Tests pass with >80% coverage
- [ ] UI matches existing app design
- [ ] No performance regressions
- [ ] Documentation complete

## Testing Strategy

### Unit Tests
```python
# Test view responses
def test_buildorder_list_view(client):
    response = client.get(reverse('buildorders:list'))
    assert response.status_code == 200

# Test form validation
def test_buildorder_form_invalid_quantity():
    form = BuildOrderForm(data={'blocks': {'uuid': -1}})
    assert not form.is_valid()
```

### Integration Tests
```python
# Test full CRUD workflow
def test_buildorder_crud_workflow(client, sample_blocks):
    # Create
    response = client.post(reverse('buildorders:create'), data={...})
    # Read
    # Update
    # Delete
```

## Implementation Notes

- Follow Django class-based view patterns
- Use `get_context_data()` for additional context
- Implement pagination with `paginate_by = 10`
- Cache resource calculations (5-minute TTL)
- Use Bootstrap 5 for styling
- Add CSRF protection to all forms

## References

- Django CBV Documentation: https://docs.djangoproject.com/en/6.0/topics/class-based-views/
- Bootstrap 5 Forms: https://getbootstrap.com/docs/5.0/forms/overview/
- Testing Guidelines: `#[[file:.kiro/steering/03-testing-guidelines.md]]`
