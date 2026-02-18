# ENH-0000011: Dynamic Block Selector

**Status:** Planned  
**Phase:** 3 - Build Order Calculator  
**Priority:** High  
**Dependencies:** ENH-0000010

## Full Documentation

📄 **Main ENH Doc**: `docs/enhancementRequests/phase3_buildorder/ENH0000011/ENH0000011-dynamic-block-selector-live-preview.md`

## Related Files

- Views: `#[[file:app/buildorders/views.py]]`
- Forms: `#[[file:app/buildorders/forms.py]]`
- Templates: `#[[file:app/buildorders/templates/buildorders/buildorder_form.html]]`
- Static JS: `#[[file:app/static/js/block_selector.js]]`
- Blocks Model: `#[[file:app/blocks/models.py]]`

## Requirements

### Functional Requirements
1. Search/filter blocks by name
2. Add blocks to build order with quantity input
3. Remove blocks from selection
4. Update quantities dynamically
5. Display selected blocks with totals
6. Validate quantities (positive integers)

### Non-Functional Requirements
1. Responsive design (mobile-friendly)
2. Real-time validation feedback
3. Accessible keyboard navigation
4. No page reloads (AJAX)
5. Graceful degradation without JavaScript

## Implementation Tasks

### 1. Backend API
- [ ] Create API endpoint: `/api/blocks/search/`
- [ ] Return JSON: `[{id, name, mass, components}]`
- [ ] Support query parameter: `?q=search_term`
- [ ] Add pagination for large result sets
- [ ] Implement rate limiting

### 2. JavaScript Component
- [ ] Create `app/static/js/block_selector.js`
- [ ] Implement search with debouncing (300ms)
- [ ] Add block to selection list
- [ ] Remove block from selection
- [ ] Update quantity with validation
- [ ] Serialize to hidden JSON field
- [ ] Handle errors gracefully

### 3. Form Widget
- [ ] Custom Django widget for block selection
- [ ] Render search input + results container
- [ ] Render selected blocks list
- [ ] Hidden input for JSON data
- [ ] Include required JavaScript/CSS

### 4. Template Updates
- [ ] Add block selector to form template
- [ ] Include JavaScript dependencies
- [ ] Add CSS for styling
- [ ] Provide fallback for no-JS users

### 5. Styling
- [ ] Create `app/static/css/block_selector.css`
- [ ] Style search input and results
- [ ] Style selected blocks list
- [ ] Add loading indicators
- [ ] Responsive breakpoints

### 6. Testing
- [ ] Unit tests for API endpoint
- [ ] JavaScript tests (if using test framework)
- [ ] Integration tests for form submission
- [ ] Accessibility tests
- [ ] Cross-browser testing

## Acceptance Criteria

- [ ] Users can search blocks by name
- [ ] Blocks can be added/removed dynamically
- [ ] Quantities can be updated in real-time
- [ ] Form validates before submission
- [ ] Works on mobile devices
- [ ] Accessible via keyboard
- [ ] Tests pass with >80% coverage

## UI Mockup

```
┌─────────────────────────────────────────┐
│ Search Blocks: [____________] 🔍        │
├─────────────────────────────────────────┤
│ Results:                                │
│ • Small Reactor [Add]                   │
│ • Large Reactor [Add]                   │
│ • Battery [Add]                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Selected Blocks:                        │
├─────────────────────────────────────────┤
│ Small Reactor    Qty: [5] [Remove]     │
│ Battery          Qty: [10] [Remove]    │
└─────────────────────────────────────────┘
```

## JavaScript API

```javascript
// Initialize block selector
const selector = new BlockSelector({
  searchUrl: '/api/blocks/search/',
  container: '#block-selector',
  hiddenInput: '#id_blocks',
  debounceMs: 300
});

// Events
selector.on('blockAdded', (block) => {...});
selector.on('blockRemoved', (blockId) => {...});
selector.on('quantityChanged', (blockId, qty) => {...});
```

## API Endpoint Specification

### GET /api/blocks/search/

**Query Parameters:**
- `q` (string, optional): Search term
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Results per page (default: 20)

**Response:**
```json
{
  "results": [
    {
      "id": "uuid-here",
      "name": "Small Reactor",
      "mass": 1000.0,
      "components": {"comp-uuid": 5}
    }
  ],
  "count": 42,
  "next": "/api/blocks/search/?q=reactor&page=2",
  "previous": null
}
```

## Implementation Notes

- Use `fetch()` API for AJAX requests
- Debounce search to reduce server load
- Cache search results client-side
- Validate quantities: positive integers only
- Provide clear error messages
- Support keyboard shortcuts (Enter to add, Escape to clear)

## References

- Django REST Framework: https://www.django-rest-framework.org/
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- Accessibility: `#[[file:.kiro/steering/05-code-style.md]]`
