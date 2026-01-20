# Blocks Test Report

- Suite: blocks
- Total tests: 49
- Result: OK (all passed)
- Runtime: ~0.15s
- Django: 6.0.1
- Database: test_se2_calculator_db

## Summary
All 49 tests for the Blocks component passed successfully. The suite covers model creation, field and timestamp validations, JSON component rules, consumer/producer validations, component relationships, meta checks, and integration flows including save-time validations.

## Command
```
uv run python manage.py test blocks -v 2
```

## Snippet of Output
```
Found 49 test(s).
System check identified no issues (0 silenced).
...
Ran 49 tests in 0.151s

OK
```

## Notes
- Helper `create_component()` now uses a unique ore per component (`<component-name>-Ore`) to avoid unique name conflicts.
- Invalid-state tests construct `Block(...)` without saving, then call `validate_*` methods directly to inspect errors, while integration tests exercise `save()` error aggregation.
