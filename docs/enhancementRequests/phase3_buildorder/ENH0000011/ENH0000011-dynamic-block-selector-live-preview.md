# Enhancement Request: Dynamic Block Selector & Live Preview

**Filename:** `ENH0000011-dynamic-block-selector-live-preview.md`

---

## Enhancement Information

**Enhancement ID:** ENH-0000011  
**Status:** Planned  
**Priority:** High  
**Created Date:** 2026-02-01  
**Updated Date:** 2026-02-01  
**Completion Date:** (pending)  
**Assigned To:** (pending)  
**Estimated Effort:** 1 day  
**Actual Effort:** (pending)

---

## Summary

Implement dynamic JavaScript block selector with autocomplete search and live calculation preview for Build Order create/update forms.

---

## Description

Add interactive block selection interface to Build Order forms, allowing users to search, add, and remove blocks with quantities. Includes live AJAX preview of resource calculations as blocks are added/removed.

**Key Features:**
- Dynamic block selector (adapted from block-component-selector.js)
- Autocomplete search for blocks
- Add/remove blocks with quantity inputs
- Live calculation preview via AJAX
- Client-side validation
- Smooth animations and UX polish

**Benefits:**
- Intuitive block selection
- Immediate feedback on resource requirements
- Reduced errors
- Better user experience
- No page reloads needed

---

## Current Behavior

- Build Order forms have hidden blocks_json field
- No way to select blocks in UI
- No live preview of calculations
- Must manually enter JSON (poor UX)

---

## Proposed Behavior

- Search box with autocomplete for blocks
- Click to add block to order
- Quantity input for each block
- Remove button for each block
- Live preview panel showing:
  - Total mass
  - Component count
  - Ore count
  - Fabrication time
- Preview updates as blocks added/removed
- Form validates before submission
- Smooth animations

---

## Acceptance Criteria

- [ ] Block search with autocomplete works
- [ ] Autocomplete shows block name, mass, PCU
- [ ] Click adds block to selected list
- [ ] Quantity input for each block
- [ ] Remove button removes block
- [ ] Selected blocks display in cart-style list
- [ ] Live preview panel displays calculations
- [ ] Preview updates on add/remove/quantity change
- [ ] AJAX endpoint returns calculation data
- [ ] Client-side validation prevents negative quantities
- [ ] Form submission converts to JSON
- [ ] Hidden blocks_json field populated
- [ ] Works on mobile devices
- [ ] Smooth animations
- [ ] Loading indicators during AJAX
- [ ] Error handling for AJAX failures
- [ ] Minimum 20 automated tests
- [ ] JavaScript tests (manual)
- [ ] Documentation updated

---

## Technical Details

### Dependencies
- ENH-0000010 (Build Order Views) must be completed first
- No new packages required
- Reuse patterns from block-component-selector.js

### Affected Components
- `buildorders` app (views, templates)
- Static JavaScript files

### Files to Modify/Create

**New Files:**
- `static/js/buildorder-selector.js` (main selector logic)
- `static/js/buildorder-calculator.js` (live preview)
- `buildorders/api_views.py` (AJAX endpoints)
- `buildorders/test_api.py` (API tests)

**Modified Files:**
- `buildorders/urls.py` (add API endpoints)
- `buildorders/templates/buildorders/buildorder_form.html` (add JavaScript)
- `buildorders/views.py` (add context for block list)

---

## Implementation Plan

### Step 1: Block Autocomplete
```javascript
// static/js/buildorder-selector.js
class BlockAutocomplete {
    constructor(inputElement, resultsElement) {
        this.input = inputElement;
        this.results = resultsElement;
        this.blocks = [];
        this.init();
    }
    
    async init() {
        this.blocks = await this.fetchBlocks();
        this.setupEventListeners();
    }
    
    async fetchBlocks() {
        const response = await fetch('/api/blocks/');
        return await response.json();
    }
    
    handleInput(e) {
        const query = e.target.value.toLowerCase();
        const matches = this.blocks.filter(block => 
            block.name.toLowerCase().includes(query)
        );
        this.showResults(matches);
    }
}
```

### Step 2: Block Selector
```javascript
class BuildOrderSelector {
    constructor() {
        this.selectedBlocks = {};
        this.calculator = new BuildOrderCalculator();
        this.init();
    }
    
    addBlock(blockId, quantity = 1) {
        this.selectedBlocks[blockId] = quantity;
        this.updateDisplay();
        this.updateHiddenField();
        this.calculator.updatePreview(this.selectedBlocks);
    }
    
    removeBlock(blockId) {
        delete this.selectedBlocks[blockId];
        this.updateDisplay();
        this.updateHiddenField();
        this.calculator.updatePreview(this.selectedBlocks);
    }
}
```

### Step 3: Live Calculator
```javascript
class BuildOrderCalculator {
    async updatePreview(blocks) {
        if (Object.keys(blocks).length === 0) {
            this.showEmptyState();
            return;
        }
        
        try {
            const response = await fetch('/api/buildorder/calculate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ blocks: blocks })
            });
            
            const data = await response.json();
            this.renderPreview(data);
        } catch (error) {
            this.showError();
        }
    }
}
```

### Step 4: API Endpoints
```python
# buildorders/api_views.py
from django.http import JsonResponse
from django.views import View
from blocks.models import Block
from .models import BuildOrder

class BlockListAPIView(View):
    def get(self, request):
        blocks = Block.objects.all().values(
            'block_id', 'name', 'mass', 'pcu', 'description'
        )
        return JsonResponse(list(blocks), safe=False)

class CalculateAPIView(View):
    def post(self, request):
        import json
        data = json.loads(request.body)
        blocks = data.get('blocks', {})
        
        # Create temporary BuildOrder for calculation
        temp_order = BuildOrder(blocks=blocks)
        summary = temp_order.get_calculation_summary(use_cache=False)
        
        return JsonResponse({
            'total_mass': summary['total_mass'],
            'component_count': len(summary['components']),
            'ore_count': len(summary['ores']),
            'total_fabrication_time': sum(summary['fabricators'].values())
        })
```

### Step 5: Template Integration
Update `buildorder_form.html`:
```django
{% block extra_js %}
<script src="{% static 'js/buildorder-selector.js' %}"></script>
<script src="{% static 'js/buildorder-calculator.js' %}"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    new BuildOrderSelector();
});
</script>
{% endblock %}
```

### Step 6: Testing
- JavaScript unit tests (manual)
- API endpoint tests
- Integration tests
- Mobile testing

---

## Testing Requirements

### API Tests (10 tests)
- [ ] Block list API returns all blocks
- [ ] Block list API returns correct format
- [ ] Calculate API accepts valid blocks
- [ ] Calculate API rejects invalid blocks
- [ ] Calculate API returns correct calculations
- [ ] Calculate API handles empty blocks
- [ ] Calculate API requires POST
- [ ] Calculate API validates CSRF token
- [ ] Calculate API handles errors gracefully
- [ ] Calculate API performance <500ms

### JavaScript Tests (Manual - 10 tests)
- [ ] Autocomplete shows results
- [ ] Autocomplete filters correctly
- [ ] Add block button works
- [ ] Remove block button works
- [ ] Quantity input updates
- [ ] Live preview updates
- [ ] Hidden field populates
- [ ] Form validates before submit
- [ ] Works on mobile
- [ ] Animations smooth

### Integration Tests (5 tests)
- [ ] Full workflow: search → add → preview → submit
- [ ] Multiple blocks → correct calculations
- [ ] Update existing order → blocks pre-populate
- [ ] Remove all blocks → empty state
- [ ] AJAX failure → error message

---

## Deliverables

- [ ] Working block selector with autocomplete
- [ ] Live calculation preview
- [ ] API endpoints functional
- [ ] Mobile responsive
- [ ] Automated tests (20+ tests)
- [ ] JavaScript documented
- [ ] Deployment guide
- [ ] User guide

---

## Documentation Updates

- [ ] JavaScript API documentation
- [ ] User guide for block selection
- [ ] API endpoint documentation
- [ ] Deployment guide
- [ ] CHANGELOG.md

---

## Risks and Considerations

**Risk 1: JavaScript Complexity**
- **Mitigation:** Reuse patterns from Phase 2, keep code modular

**Risk 2: AJAX Performance**
- **Mitigation:** Debounce preview updates, cache block list

**Risk 3: Mobile UX**
- **Mitigation:** Test on mobile devices, use touch-friendly controls

---

## Related Issues/Enhancements

- **Depends On:** ENH-0000010 (Build Order Views)
- **Enables:** ENH-0000012 (Export)
- **Enables:** ENH-0000013 (Charts)

---

## Status History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Planned | Initial creation for Phase 3 |

---

## Sign-off

**Reviewed By:** (pending)  
**Approved By:** (pending)  
**Completed By:** (pending)  
**Completion Date:** (pending)
