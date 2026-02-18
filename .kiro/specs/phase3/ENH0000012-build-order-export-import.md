# ENH-0000012: Build Order Export/Import

**Status:** Planned  
**Phase:** 3 - Build Order Calculator  
**Priority:** Medium  
**Dependencies:** ENH-0000010

## Full Documentation

📄 **Main ENH Doc**: `docs/enhancementRequests/phase3_buildorder/ENH0000012/ENH0000012-export-functionality.md`

## Related Files

- Views: `#[[file:app/buildorders/views.py]]`
- Models: `#[[file:app/buildorders/models.py]]`
- Templates: `#[[file:app/buildorders/templates/buildorders/buildorder_detail.html]]`
- Steering: `#[[file:.kiro/steering/07-security-secrets.md]]`

## Requirements

### Functional Requirements
1. Export build order to JSON file
2. Import build order from JSON file
3. Validate imported data
4. Handle version compatibility
5. Preserve UUIDs or generate new ones (user choice)

### Non-Functional Requirements
1. Secure file upload validation
2. File size limits (max 1MB)
3. Format validation before import
4. Error handling with user feedback
5. Audit logging for imports/exports

## Implementation Tasks

### 1. Export Functionality
- [ ] Add export button to detail view
- [ ] Create `BuildOrderExportView`
- [ ] Generate JSON with metadata
- [ ] Include version information
- [ ] Set appropriate Content-Type headers
- [ ] Filename: `buildorder_{name}_{date}.json`

### 2. Import Functionality
- [ ] Create import form with file upload
- [ ] Create `BuildOrderImportView`
- [ ] Validate JSON structure
- [ ] Check version compatibility
- [ ] Validate all referenced UUIDs exist
- [ ] Option to preserve or regenerate UUIDs

### 3. Data Format
- [ ] Define JSON schema
- [ ] Include format version
- [ ] Include export timestamp
- [ ] Include block references with names
- [ ] Include calculated totals (for verification)

### 4. Validation
- [ ] File type validation (JSON only)
- [ ] File size validation (<1MB)
- [ ] Schema validation
- [ ] UUID existence validation
- [ ] Quantity validation

### 5. Error Handling
- [ ] Invalid file format errors
- [ ] Missing block references
- [ ] Version mismatch warnings
- [ ] Duplicate name handling
- [ ] Rollback on import failure

### 6. Testing
- [ ] Export generates valid JSON
- [ ] Import validates correctly
- [ ] Round-trip test (export → import)
- [ ] Invalid file rejection
- [ ] Security tests (malicious files)

## Acceptance Criteria

- [ ] Users can export build orders as JSON
- [ ] Users can import valid JSON files
- [ ] Invalid files are rejected with clear errors
- [ ] Imported build orders function correctly
- [ ] No security vulnerabilities
- [ ] Tests pass with >80% coverage

## JSON Format Specification

```json
{
  "format_version": "1.0",
  "exported_at": "2026-02-18T12:00:00Z",
  "buildorder": {
    "name": "My Build Order",
    "description": "Description here",
    "blocks": {
      "block-uuid-1": 5,
      "block-uuid-2": 10
    },
    "metadata": {
      "block_names": {
        "block-uuid-1": "Small Reactor",
        "block-uuid-2": "Battery"
      },
      "total_components": 42,
      "total_ores": 1000
    }
  }
}
```

## Import Options

```
┌─────────────────────────────────────────┐
│ Import Build Order                      │
├─────────────────────────────────────────┤
│ File: [Choose File] buildorder.json    │
│                                         │
│ Options:                                │
│ ☐ Preserve original UUIDs              │
│ ☑ Generate new UUIDs                   │
│ ☑ Validate block references             │
│                                         │
│ [Cancel] [Import]                       │
└─────────────────────────────────────────┘
```

## Security Considerations

- Validate file MIME type
- Limit file size to prevent DoS
- Sanitize all input data
- Use Django's file upload validation
- Log all import attempts
- Rate limit import operations
- Scan for malicious content

## Implementation Notes

- Use `JsonResponse` for export
- Use `FileField` for import form
- Validate with `json.loads()` and schema
- Use transactions for import (rollback on error)
- Provide detailed error messages
- Support batch import (future enhancement)

## Error Messages

```python
ERRORS = {
    'invalid_format': 'Invalid JSON format',
    'version_mismatch': 'Incompatible format version',
    'missing_blocks': 'Referenced blocks not found: {blocks}',
    'invalid_quantities': 'Invalid quantities detected',
    'file_too_large': 'File exceeds 1MB limit',
}
```

## References

- File Upload Security: https://docs.djangoproject.com/en/6.0/topics/security/
- JSON Schema: https://json-schema.org/
- Security Guidelines: `#[[file:.kiro/steering/07-security-secrets.md]]`
