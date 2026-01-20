# Issue Report: Lambda Function Migration Serialization Error

**Issue ID:** ISSUES0000001  
**Date:** 2026-01-19  
**Severity:** High  
**Status:** Resolved  
**Component:** Components Model - UUID Generation

---

## Summary

Django's migration system was unable to serialize a lambda function used as the default value for the `component_id` UUIDField. This prevented the creation of database migrations with the error:

```
ValueError: Cannot serialize function: lambda
```

---

## Root Cause Analysis

### Primary Cause
The `Component` model was defined with:
```python
component_id = models.UUIDField(
    primary_key=True,
    default=lambda: str(uuid7()),  # ❌ Lambda not serializable
    editable=False,
    help_text="Unique identifier for the component",
)
```

Django's migration writer cannot serialize lambda functions because:
1. Lambda functions have no importable name
2. They cannot be reconstructed from a string representation
3. The migration system needs to store the default as importable Python code

### Secondary Issue
Even after the lambda was initially replaced with `default=generate_uuid()`, the migration captured a **hardcoded UUID string** instead of the function reference:
```python
default='019bd780-94f5-7843-b709-141a5f13842d'  # ❌ Static value, not callable
```

This occurred because `generate_uuid()` was called at model definition time rather than referenced as a callable.

---

## Impact

1. **Immediate:** Unable to create or apply migrations
2. **Database:** Every Component would receive the same UUID, violating primary key constraints
3. **Development:** Blocked progress on ENH0000002 implementation

---

## Lessons Learned

### Best Practices for Django Defaults

| Pattern | ✓/✗ | Reason |
|---------|-----|--------|
| `default=function_ref` | ✓ | Function is called at instance creation; serializable |
| `default=lambda: value()` | ✗ | Lambdas are not serializable by Django migrations |
| `default=function_call()` | ✗ | Captures static value at definition time |
| `default=callable_class` | ✓ | Classes can be serialized if importable |

### Key Insight
When using `default=` in Django models, always provide:
- A named, module-level function (not a lambda)
- A reference to the function (not a function call)
- A function that Django can import from the model module

### Documentation Gap
The ENH0000002 deployment guide specified `default=lambda: str(uuid7())` which is incorrect for Django migrations. This should have been `default=generate_uuid` with a module-level function definition.

---

## Resolution

### Solution Applied
1. Created a named function at module level:
   ```python
   def generate_uuid():
       return str(uuid7())
   ```

2. Changed the model field to reference the function without calling it:
   ```python
   component_id = models.UUIDField(
       primary_key=True,
       default=generate_uuid,  # ✓ Function reference (no parentheses)
       editable=False,
       help_text="Unique identifier for the component",
   )
   ```

3. Deleted the broken migration and regenerated it
4. New migration correctly references: `default=components.models.generate_uuid`

---

## Next Steps

1. **Documentation Update**
   - Correct ENH0000002 deployment guide to show `default=generate_uuid` pattern
   - Add best practices section for Django field defaults
   - Include example of callable vs non-callable defaults

2. **Code Review Process**
   - Add migration serialization check to development checklist
   - Review any other models using similar patterns (ores/models.py)

3. **Testing**
   - Verify migrations are reproducible from scratch
   - Add test to ensure migration can be applied to fresh database

4. **Knowledge Base**
   - Create knowledge base entry: "Django Model Field Defaults: Serialization Requirements"
   - Document common serialization issues and solutions

---

## References

- [Django Migration Serialization](https://docs.djangoproject.com/en/6.0/howto/writing-migrations/#serializing-values)
- [Django Model Field default Parameter](https://docs.djangoproject.com/en/6.0/ref/models/fields/#default)
- File: [components/models.py](../../../components/models.py)
- File: [components/migrations/0001_initial.py](../../../components/migrations/0001_initial.py)

---

## Checklist

- [x] Root cause identified
- [x] Solution implemented and tested
- [x] All migrations apply successfully
- [x] Database tests pass
- [ ] Documentation updated
- [ ] Code review guidelines updated
- [ ] Knowledge base entry created
