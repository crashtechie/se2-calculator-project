# Phase 3: Build Order Calculator - Enhancement Requests

**Phase:** 3 - Build Order Calculator  
**Status:** Planned  
**Start Date:** TBD  
**Target Completion:** TBD

---

## Overview

Phase 3 implements the Build Order Calculator feature, allowing users to select multiple blocks, specify quantities, and calculate total resource requirements including components, ores, and fabrication times.

---

## Enhancement Structure

### Core Enhancements (Required)

| ID | Title | Priority | Status | Estimated Effort |
|----|-------|----------|--------|------------------|
| ENH-0000009 | Build Order Model & Core Logic | High | Planned | 1 day |
| ENH-0000010 | Build Order CRUD Views & Templates | High | Planned | 1.5 days |
| ENH-0000011 | Dynamic Block Selector & Live Preview | High | Planned | 1 day |

### Optional Enhancements (Phase 3+)

| ID | Title | Priority | Status | Estimated Effort |
|----|-------|----------|--------|------------------|
| ENH-0000012 | Export Functionality (CSV/JSON/PDF) | Medium | Planned | 0.5 days |
| ENH-0000013 | Resource Visualization Charts | Medium | Planned | 0.5 days |
| ENH-0000014 | Build Order Templates | Low | Planned | 1 day |
| ENH-0000015 | Advanced Features (Comparison, Batch Ops) | Low | Planned | 1.5 days |

---

## Dependencies

### Phase 1 & 2 Prerequisites (All Complete ✅)
- ENH-0000001: Ores Model ✅
- ENH-0000002: Components Model ✅
- ENH-0000003: Blocks Model ✅
- ENH-0000005: Ores Views ✅
- ENH-0000006: Components Views ✅
- ENH-0000007: Blocks Views ✅
- ENH-0000008: Core Infrastructure (Docker) ✅

### Phase 3 Dependencies
- ENH-0000009 must be completed before ENH-0000010
- ENH-0000010 must be completed before ENH-0000011
- Optional enhancements (ENH-0000012-0000015) can be implemented in any order after core enhancements

---

## Implementation Strategy

### Stage 1: Model & Core Logic (Day 1)
**Enhancement:** ENH-0000009
- Create BuildOrder model with UUIDv7 pattern
- Implement calculation methods (mass, components, ores, fabrication times)
- Add validation methods
- Write comprehensive unit tests
- Add property-based tests for calculations

**Deliverables:**
- Working BuildOrder model
- All calculation methods tested
- Admin interface configured
- 50+ tests passing

### Stage 2: CRUD Interface (Day 2)
**Enhancement:** ENH-0000010
- Implement CRUD views following Phase 2 patterns
- Create templates with Bootstrap 5 styling
- Add URL configuration
- Implement detail view with full calculation display
- Write view and integration tests

**Deliverables:**
- Complete CRUD interface
- Calculation summary display
- 30+ tests passing
- Documentation updated

### Stage 3: Dynamic UI & Polish (Day 3)
**Enhancement:** ENH-0000011
- Implement dynamic block selector JavaScript
- Add live calculation preview
- Add autocomplete for block search
- Polish UI/UX
- Integration testing

**Deliverables:**
- Dynamic block selection working
- Live preview functional
- Smooth user experience
- 20+ tests passing

### Stage 4: Optional Enhancements (Post-Phase 3)
**Enhancements:** ENH-0000012 through ENH-0000015
- Implement based on priority and user feedback
- Can be done incrementally
- Each enhancement is independent

---

## Testing Strategy

### Test Coverage Goals
- Overall coverage: ≥85%
- BuildOrder model: ≥90%
- Calculation methods: 100%
- Views: ≥85%
- Forms: ≥90%

### Test Types
1. **Unit Tests:** Model methods, calculations, validation
2. **Property-Based Tests:** Calculation properties across all inputs
3. **Integration Tests:** Full workflow (create → calculate → display)
4. **View Tests:** CRUD operations, context data
5. **Form Tests:** Validation, JSON conversion
6. **JavaScript Tests:** Manual testing of dynamic features

### Test Data
- Use existing fixtures from Phase 1 (15 ores, 15 components, 15 blocks)
- Create additional test build orders for edge cases
- Test with 1 block, 10 blocks, 50 blocks, 100 blocks

---

## Documentation Requirements

Each enhancement must include:
1. **Main Enhancement Document:** `ENH-XXXXXXX-<description>.md`
2. **Deployment Guide:** `ENH-XXXXXXX-deployment-guide.md`
3. **Post-Deployment Report:** `ENH-XXXXXXX-POST-DEPLOYMENT-REPORT.md`
4. **README.md:** Summary and quick reference

Additional documentation:
- Calculation algorithm documentation
- API documentation (if implementing API endpoints)
- User guide for build order calculator
- Phase 3 completion report

---

## Success Criteria

Phase 3 will be considered complete when:
- ✅ All core enhancements (ENH-0000009-0000011) completed
- ✅ All tests passing (100+ new tests)
- ✅ Test coverage ≥85%
- ✅ Calculations accurate for complex scenarios
- ✅ UI responsive and intuitive
- ✅ Documentation complete
- ✅ No performance issues with 100+ blocks
- ✅ Phase 3 post-deployment report completed

---

## Risk Management

### Technical Risks
1. **Calculation Complexity:** Mitigated by comprehensive testing
2. **Performance:** Mitigated by caching and query optimization
3. **UI Complexity:** Mitigated by reusing Phase 2 patterns

### Schedule Risks
1. **Scope Creep:** Keep optional features separate
2. **Testing Time:** Allocate sufficient time for edge cases
3. **Integration Issues:** Test early and often

---

## Phase 3 Timeline

**Estimated Duration:** 3-4 days (core enhancements only)

| Day | Focus | Enhancements | Deliverables |
|-----|-------|--------------|--------------|
| 1 | Model & Logic | ENH-0000009 | Model, calculations, tests |
| 2 | CRUD Interface | ENH-0000010 | Views, templates, tests |
| 3 | Dynamic UI | ENH-0000011 | JavaScript, live preview |
| 4 | Testing & Docs | All | Documentation, polish |

**Optional Enhancements:** 2-3 additional days (can be done post-Phase 3)

---

## Related Documentation

- [Phase 3 Project Plan](../../projectPlan/phase3_buildorder.md)
- [Phase 1 & 2 Validation Report](../../projectPlan/PHASE_1_2_VALIDATION_REPORT.md)
- [Enhancement Request Template](../enhancementRequestTemplate.md)

---

## Notes

- Follow patterns established in Phase 1 & 2
- Reuse JavaScript patterns from component-selector.js
- Use UUIDv7 for consistency
- Implement caching for performance
- Document calculation algorithms thoroughly
- Consider user feedback for optional enhancements

---

## Status Updates

| Date | Update |
|------|--------|
| 2026-02-01 | Phase 3 enhancement structure created |
| TBD | Phase 3 implementation started |
| TBD | Phase 3 completed |
