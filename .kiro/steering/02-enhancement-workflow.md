# Enhancement Request Workflow

## Creating Enhancement Requests

### File Location
Place all ENH documents in `docs/enhancementRequests/` organized by phase:
- `Phase1_models/` - Database models and schema
- `Phase2_views/` - Views, templates, and CRUD operations
- `Phase3_buildorder/` - Build order calculator features
- `Phase4_testing/` - Testing, documentation, infrastructure

### Naming Convention
`ENH{7-digit-number}-{brief-description}.md`

Example: `ENH0000010-build-order-views.md`

### Required Sections

1. **Header**
   - Enhancement ID
   - Title
   - Status (Proposed/In Progress/Complete/Deferred)
   - Priority (Critical/High/Medium/Low)
   - Phase
   - Estimated Effort

2. **Overview**
   - Brief description
   - Business value
   - Dependencies

3. **Requirements**
   - Functional requirements
   - Non-functional requirements
   - Acceptance criteria

4. **Technical Design**
   - Implementation approach
   - Data structures
   - API endpoints (if applicable)
   - Database changes

5. **Testing Strategy**
   - Test scenarios
   - Coverage targets
   - Edge cases

6. **Documentation**
   - User-facing documentation
   - Developer documentation
   - API documentation (if applicable)

7. **Implementation Checklist**
   - [ ] Code implementation
   - [ ] Tests written and passing
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated
   - [ ] README.md updated (if needed)
   - [ ] Code review completed

## Implementation Process

1. **Create ENH document** with detailed requirements
2. **Get approval** (if working with team)
3. **Create feature branch** (optional): `feature/ENH{number}-description`
4. **Implement** following Django standards
5. **Write tests** achieving >80% coverage
6. **Update documentation** (ENH doc, CHANGELOG, README)
7. **Submit for review** (if applicable)
8. **Merge and deploy**

## Status Updates

Update ENH document status as work progresses:
- **Proposed**: Initial draft, awaiting approval
- **In Progress**: Active development
- **Complete**: Implemented, tested, documented
- **Deferred**: Postponed to future release
- **Cancelled**: No longer needed

## CHANGELOG Updates

When completing an ENH, add entry to CHANGELOG.md:

```markdown
### Added
- ENH-{number}: Brief description of feature

### Changed
- ENH-{number}: Description of changes

### Fixed
- ENH-{number}: Description of bug fix
```

## Cross-References

- Link related ENH documents
- Reference GitHub issues
- Note dependencies between features
- Document breaking changes
