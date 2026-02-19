#!/bin/bash
cd "$(dirname "$0")"
uv run pytest app/buildorders/test_views.py app/buildorders/tests.py --cov=app/buildorders --cov-report=term-missing -v
