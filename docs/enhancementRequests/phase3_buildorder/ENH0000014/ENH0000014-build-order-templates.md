# Enhancement Request: Build Order Templates

**Enhancement ID:** ENH-0000014  
**Status:** Planned (Optional)  
**Priority:** Low  
**Estimated Effort:** 1 day

---

## Summary

Allow users to save build orders as reusable templates and create new orders from templates, enabling quick setup of common builds.

---

## Description

Add template functionality to build orders:
- Save existing build order as template
- Create new build order from template
- Public/private template sharing
- Template library view
- Template management (edit, delete)

---

## Acceptance Criteria

- [ ] BuildOrderTemplate model created
- [ ] "Save as Template" button in detail view
- [ ] Template library view lists all templates
- [ ] "Create from Template" button in list view
- [ ] Templates can be public or private
- [ ] Template CRUD operations work
- [ ] Templates include blocks configuration
- [ ] New order inherits blocks from template
- [ ] Tests for template functionality
- [ ] Documentation updated

---

## Technical Details

**New Model:**
```python
class BuildOrderTemplate(models.Model):
    template_id = models.UUIDField(primary_key=True, default=generate_uuid)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    blocks = models.JSONField(default=dict)
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def create_build_order(self, name=None):
        return BuildOrder.objects.create(
            name=name or f"{self.name} (from template)",
            blocks=self.blocks.copy()
        )
```

**New Views:**
- TemplateListView
- TemplateDetailView
- TemplateCreateView (from existing order)
- BuildOrderFromTemplateView

---

## Related Enhancements

- **Depends On:** ENH-0000010 (Build Order Views)
- **Optional:** Can be implemented anytime after Phase 3 core
- **Note:** Requires user authentication for private templates

---

## Status

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Planned | Optional enhancement for Phase 3+ |
