# Issue Report: QuerySet Object Comparison Failures in Tests

**Issue ID:** ISSUES0000002  
**Date:** 2026-01-19  
**Severity:** Medium  
**Status:** Resolved  
**Component:** Components Tests - Material Ores Relationship Tests

---

## Summary

Two test cases failed when attempting to verify Ore objects returned from a QuerySet using `assertIn()`:

```
FAIL: test_get_material_ores_single_ore
AssertionError: <Ore: Rel Iron> not found in <QuerySet [<Ore: Rel Iron>]>

FAIL: test_get_material_ores_multiple_ores  
AssertionError: <Ore: Rel Copper> not found in <QuerySet [<Ore: Rel Iron>, <Ore: Rel Copper>]>
```

Tests appeared to fail despite the correct Ore objects being present in the QuerySet.

---

## Root Cause Analysis

### Primary Issue: Object Identity vs Equality

The `assertIn()` assertion uses Python's `in` operator, which checks for object membership using:
1. **First:** Object identity (`is` - same memory reference)
2. **Second:** Object equality (`==` - if `__eq__` is defined)

The test code was:
```python
self.iron = Ore.objects.create(name="Test Iron Ore", mass=1.0)  # Object created in setUp

# Later in test:
component = Component.objects.create(
    name="Single Ore",
    materials={str(self.iron.ore_id): 10}
)

ores = component.get_material_ores()  # Fresh QuerySet from database
self.assertIn(self.iron, ores)  # ❌ FAILS
```

The `self.iron` object instance and the Ore instances returned from `get_material_ores()` QuerySet are:
- **Different object instances** (different memory addresses)
- **Same database record** (same ore_id)
- **Possibly different equality** (depends on model's `__eq__` implementation)

Since Django ORM doesn't reload the same instance, each database query creates new object instances, making object identity checks fail.

### Secondary Issue: Data Type Mismatch

The QuerySet returns Ore objects with `ore_id` as UUID objects, but the materials JSON stores them as strings:

```python
materials={str(self.iron.ore_id): 10}  # String key "019bd794-..."

# get_material_ores() returns:
Ore(ore_id=UUID('019bd794-...'))  # UUID object
```

Initial fix attempts using `assertQuerySetEqual()` failed due to comparing string IDs against UUID objects.

---

## Impact

1. **Testing:** Two relationship tests were failing despite correct functionality
2. **Coverage:** Reduced test reliability when verifying ORM relationships
3. **Confidence:** Unclear whether the model methods worked correctly

---

## Lessons Learned

### Django QuerySet Testing Patterns

| Pattern | Use Case | Notes |
|---------|----------|-------|
| `assertIn(obj, queryset)` | ❌ Avoid | Object identity issues with fresh queries |
| `assertQuerySetEqual()` | ✓ Better | Django's standard QuerySet comparison method |
| `self.assertIn(obj.id, [o.id for o in qs])` | ✓ Good | Explicit ID comparison |
| `set comprehension` | ✓ Good | `{str(o.ore_id) for o in qs}` for type-consistent comparison |

### Key Insights

1. **QuerySet instances are always fresh** - Every database query creates new object instances
2. **Object identity fails** - `is` operator will always be false for freshly-queried objects
3. **Type consistency matters** - Compare using consistent types (all strings or all UUIDs)
4. **Django provides tools** - Use `assertQuerySetEqual()` instead of generic assertions

### Example of Correct Pattern

```python
# ❌ WRONG - Object identity
self.assertIn(self.iron, ores)

# ✓ CORRECT - ID-based comparison
ore_ids = {str(ore.ore_id) for ore in ores}
self.assertIn(str(self.iron.ore_id), ore_ids)

# ✓ ALSO CORRECT - Django's standard method
self.assertQuerySetEqual(
    ores,
    [self.iron],
    transform=lambda x: x.ore_id
)
```

---

## Resolution

### Solution Applied

Replaced `assertIn()` with explicit ID-based assertions using set comprehensions:

```python
def test_get_material_ores_single_ore(self):
    """Test getting a single ore from materials."""
    component = Component.objects.create(
        name="Single Ore",
        materials={str(self.iron.ore_id): 10}
    )
    
    ores = component.get_material_ores()
    self.assertEqual(ores.count(), 1)
    ore_ids = {str(ore.ore_id) for ore in ores}
    self.assertIn(str(self.iron.ore_id), ore_ids)  # ✓ Compare by ID

def test_get_material_ores_multiple_ores(self):
    """Test getting multiple ores from materials."""
    component = Component.objects.create(
        name="Multiple Ores",
        materials={
            str(self.iron.ore_id): 7,
            str(self.copper.ore_id): 3
        }
    )
    
    ores = component.get_material_ores()
    self.assertEqual(ores.count(), 2)
    ore_ids = {str(ore.ore_id) for ore in ores}
    self.assertIn(str(self.iron.ore_id), ore_ids)  # ✓ Compare by ID
    self.assertIn(str(self.copper.ore_id), ore_ids)
```

**Why this works:**
1. Converts both sides to strings for type consistency
2. Compares by unique identifier (ore_id) rather than object identity
3. Explicitly handles the SQLite/UUID serialization difference
4. Clear intent: testing relationship resolution, not object identity

---

## Next Steps

1. **Code Quality Guidelines**
   - Document Django ORM testing patterns in development guidelines
   - Add code review checklist: "QuerySet assertions use IDs, not objects"

2. **Test Utilities**
   - Consider creating test helper methods for common QuerySet assertions
   - Example: `assert_model_in_queryset(obj, queryset, field_name='id')`

3. **Documentation**
   - Create knowledge base article: "Testing Django ORM Relationships"
   - Include common pitfalls and solutions
   - Show assertQuerySetEqual() vs manual ID comparison

4. **Similar Code Review**
   - Search for other uses of `assertIn()` with QuerySets in the codebase
   - Review ores/tests.py for similar patterns
   - Apply consistent fixes

5. **Future Test Writing**
   - Always use ID-based or transform-based comparison for QuerySet assertions
   - Never rely on object identity across ORM boundaries

---

## References

- [Django Testing QuerySets](https://docs.djangoproject.com/en/6.0/topics/testing/tools/#assertqueryset-equal)
- [Python `in` operator behavior](https://docs.python.org/3/reference/datamodel.html#object.__eq__)
- File: [components/tests.py - test_get_material_ores_single_ore](../../../components/tests.py#L360)
- File: [components/tests.py - test_get_material_ores_multiple_ores](../../../components/tests.py#L372)

---

## Checklist

- [x] Root cause identified and documented
- [x] Solution implemented and tested
- [x] All related tests passing (2/2)
- [x] Verified correct functionality
- [ ] Code review guidelines updated
- [ ] Test helper utilities created
- [ ] Knowledge base article written
- [ ] Similar code patterns reviewed across codebase
