# Enhancement Request: Advanced Features (Comparison, Batch Ops, Drag-Drop)

**Enhancement ID:** ENH-0000015  
**Status:** Planned (Optional)  
**Priority:** Low  
**Estimated Effort:** 1.5 days

---

## Summary

Add advanced features for power users including build order comparison, batch operations, and drag-and-drop block ordering.

---

## Description

Collection of advanced features to enhance productivity:

### 1. Build Order Comparison
- Compare 2-4 build orders side-by-side
- Show differences in resource requirements
- Highlight most efficient option
- Export comparison results

### 2. Batch Operations
- Select multiple build orders
- Bulk delete
- Bulk export
- Bulk duplicate

### 3. Drag-and-Drop Ordering
- Reorder blocks within build order
- Visual drag handles
- Save block order preference
- Smooth animations

### 4. Build Order Duplication
- One-click duplicate
- Edit name on duplicate
- Preserve all blocks and quantities

---

## Acceptance Criteria

**Comparison:**
- [ ] Compare view accepts 2-4 order IDs
- [ ] Side-by-side table display
- [ ] Highlights differences
- [ ] Shows totals for each order
- [ ] Export comparison to CSV

**Batch Operations:**
- [ ] Checkboxes in list view
- [ ] "Select All" functionality
- [ ] Batch delete with confirmation
- [ ] Batch export to ZIP
- [ ] Batch duplicate

**Drag-Drop:**
- [ ] Drag handles on block rows
- [ ] Visual feedback during drag
- [ ] Order persists on save
- [ ] Works on touch devices

**Duplication:**
- [ ] Duplicate button in detail view
- [ ] Duplicate button in list view
- [ ] Name prompt on duplicate
- [ ] All data copied correctly

---

## Technical Details

**New Views:**
- CompareView
- BulkActionView
- DuplicateView

**New JavaScript:**
- `static/js/buildorder-comparison.js`
- `static/js/buildorder-bulk-actions.js`
- `static/js/buildorder-drag-drop.js` (using SortableJS)

**Dependencies:**
- SortableJS (for drag-drop)

---

## Implementation Notes

### Comparison View
```python
class BuildOrderCompareView(TemplateView):
    template_name = 'buildorders/compare.html'
    
    def get_context_data(self, **kwargs):
        order_ids = self.request.GET.getlist('orders')
        orders = BuildOrder.objects.filter(order_id__in=order_ids)
        
        comparisons = []
        for order in orders:
            comparisons.append({
                'order': order,
                'summary': order.get_calculation_summary()
            })
        
        return {'comparisons': comparisons}
```

### Batch Operations
```python
class BuildOrderBulkActionView(View):
    def post(self, request):
        action = request.POST.get('action')
        order_ids = request.POST.getlist('order_ids')
        
        if action == 'delete':
            BuildOrder.objects.filter(order_id__in=order_ids).delete()
        elif action == 'duplicate':
            for order_id in order_ids:
                original = BuildOrder.objects.get(order_id=order_id)
                BuildOrder.objects.create(
                    name=f"{original.name} (Copy)",
                    blocks=original.blocks.copy()
                )
        
        return redirect('buildorders:list')
```

### Drag-Drop
```javascript
import Sortable from 'sortablejs';

class BlockOrderManager {
    initSortable() {
        Sortable.create(this.container, {
            animation: 150,
            handle: '.drag-handle',
            onEnd: (evt) => this.updateBlockOrder()
        });
    }
}
```

---

## Testing Requirements

- [ ] Comparison view with 2 orders
- [ ] Comparison view with 4 orders
- [ ] Batch delete multiple orders
- [ ] Batch duplicate multiple orders
- [ ] Drag-drop reorders blocks
- [ ] Drag-drop persists on save
- [ ] Duplicate creates exact copy
- [ ] All features work on mobile

---

## Related Enhancements

- **Depends On:** ENH-0000010 (Build Order Views)
- **Optional:** Can be implemented anytime after Phase 3 core
- **Note:** These are power-user features, not essential for MVP

---

## Status

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Planned | Optional enhancement for Phase 3+ |
