# Issue 0000001 – Performance tests lack django_db mark

## Summary
Performance tests in `scripts/tests/performance/test_blocks_queries.py` access the database without pytest-django marks, causing runtime failures when running the full suite against PostgreSQL via `uv run --env-file .env python -m pytest`.

## Impact
- Test suite fails (4 tests) due to blocked DB access.
- Blocks “All tests passing” item in pre-deployment checklist for ENH-0000008.

## Reproduction
1. Ensure PostgreSQL is reachable per `.env`.
2. Run: `DJANGO_SETTINGS_MODULE=se2CalcProject.settings uv run --env-file .env python -m pytest`
3. Observe failures in `scripts/tests/performance/test_blocks_queries.py` complaining about missing `django_db` mark.

## Recommendation
Add `@pytest.mark.django_db(transaction=True)` to the performance tests (or exclude them from default runs). Re-run pytest to confirm all tests pass.

## Status
Open
