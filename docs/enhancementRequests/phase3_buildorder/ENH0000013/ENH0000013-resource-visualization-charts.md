# Enhancement Request: Resource Visualization Charts

**Enhancement ID:** ENH-0000013  
**Status:** Planned (Optional)  
**Priority:** Medium  
**Estimated Effort:** 0.5 days

---

## Summary

Add interactive charts to build order detail view showing resource distribution using Chart.js, including pie charts for components and bar charts for fabrication times.

---

## Description

Enhance the detail view with visual representations of resource data:
- **Component Pie Chart:** Shows distribution of components by quantity
- **Ore Pie Chart:** Shows distribution of ores by mass
- **Fabricator Bar Chart:** Shows fabrication time by fabricator type
- **Mass Breakdown:** Stacked bar showing block mass contributions

---

## Acceptance Criteria

- [ ] Charts render in detail view
- [ ] Component pie chart shows all components
- [ ] Ore pie chart shows all ores
- [ ] Fabricator bar chart shows times
- [ ] Charts responsive on mobile
- [ ] Charts use consistent color scheme
- [ ] Tooltips show detailed information
- [ ] Charts update when order changes
- [ ] Tests for chart data generation
- [ ] Documentation updated

---

## Technical Details

**Dependencies:**
- Chart.js (CDN or npm)

**Modified Files:**
- `buildorders/templates/buildorders/buildorder_detail.html`

**New Files:**
- `static/js/buildorder-charts.js`

---

## Implementation Notes

```javascript
class ResourceCharts {
    renderComponentPieChart(canvasId, data) {
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.components.map(c => c.name),
                datasets: [{
                    data: data.components.map(c => c.quantity),
                    backgroundColor: this.generateColors(data.components.length)
                }]
            }
        });
    }
}
```

---

## Related Enhancements

- **Depends On:** ENH-0000010 (Build Order Views)
- **Optional:** Can be implemented anytime after Phase 3 core

---

## Status

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Planned | Optional enhancement for Phase 3+ |
