# Enhancement Request: Export Functionality (CSV/JSON/PDF)

**Enhancement ID:** ENH-0000012  
**Status:** Planned (Optional)  
**Priority:** Medium  
**Estimated Effort:** 0.5 days

---

## Summary

Add export functionality to build orders, allowing users to download resource calculations in CSV, JSON, and PDF formats for external analysis and sharing.

---

## Description

Implement export views that generate downloadable files containing build order data and calculations. Supports three formats:
- **CSV:** For spreadsheet analysis
- **JSON:** For programmatic access
- **PDF:** For printing and sharing

---

## Acceptance Criteria

- [ ] Export button in detail view with format dropdown
- [ ] CSV export includes all blocks, components, ores
- [ ] JSON export includes complete calculation summary
- [ ] PDF export formatted for printing
- [ ] Filename includes order name and date
- [ ] All formats include calculation results
- [ ] Tests for each export format
- [ ] Documentation updated

---

## Technical Details

**New Files:**
- `buildorders/export_views.py`
- `buildorders/test_exports.py`

**Dependencies:**
- reportlab (for PDF generation)

**URL Pattern:**
```python
path('<uuid:order_id>/export/', ExportView.as_view(), name='export'),
```

---

## Implementation Notes

- Use Django's HttpResponse with appropriate content types
- CSV: Use Python's csv module
- JSON: Use Django's JsonResponse
- PDF: Use reportlab library
- Add export button to detail view template
- Test with large build orders (100+ blocks)

---

## Related Enhancements

- **Depends On:** ENH-0000010 (Build Order Views)
- **Optional:** Can be implemented anytime after Phase 3 core

---

## Status

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Planned | Optional enhancement for Phase 3+ |
