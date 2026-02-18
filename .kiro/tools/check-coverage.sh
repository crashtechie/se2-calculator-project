#!/bin/bash
# Check test coverage and enforce minimum threshold.
#
# Usage:
#     bash .kiro/tools/check-coverage.sh
#     bash .kiro/tools/check-coverage.sh 85  # Custom threshold

THRESHOLD=${1:-80}

echo "=================================="
echo "Running tests with coverage..."
echo "Minimum threshold: ${THRESHOLD}%"
echo "=================================="

# Change to app directory where pytest is configured
cd app

# Run pytest with coverage
uv run pytest --cov --cov-report=term --cov-report=html --cov-fail-under=${THRESHOLD}

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Coverage check passed! (>=${THRESHOLD}%)"
    echo "📊 HTML report: htmlcov/index.html"
    exit 0
else
    echo ""
    echo "❌ Coverage check failed! (<${THRESHOLD}%)"
    echo "📊 Review HTML report: htmlcov/index.html"
    echo ""
    echo "Tips to improve coverage:"
    echo "  - Add tests for uncovered lines"
    echo "  - Test edge cases and error conditions"
    echo "  - Test all CRUD operations"
    echo "  - Test validation logic"
    exit 1
fi
