#!/bin/bash
# Sync .env.example with .env file structure (without values).
#
# Usage:
#     bash .kiro/tools/sync-env.sh

ENV_FILE=".env"
EXAMPLE_FILE=".env.example"

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ .env file not found"
    exit 1
fi

echo "=================================="
echo "Syncing .env.example with .env"
echo "=================================="

# Extract keys from .env (ignore comments and empty lines)
grep -v '^#' "$ENV_FILE" | grep -v '^$' | cut -d '=' -f 1 | sort > /tmp/env_keys.txt

# Extract keys from .env.example
if [ -f "$EXAMPLE_FILE" ]; then
    grep -v '^#' "$EXAMPLE_FILE" | grep -v '^$' | cut -d '=' -f 1 | sort > /tmp/example_keys.txt
    
    # Find keys in .env but not in .env.example
    MISSING_IN_EXAMPLE=$(comm -23 /tmp/env_keys.txt /tmp/example_keys.txt)
    
    # Find keys in .env.example but not in .env
    MISSING_IN_ENV=$(comm -13 /tmp/env_keys.txt /tmp/example_keys.txt)
    
    if [ -n "$MISSING_IN_EXAMPLE" ]; then
        echo ""
        echo "⚠️  Keys in .env but missing in .env.example:"
        echo "$MISSING_IN_EXAMPLE"
        echo ""
        echo "Add these to .env.example with placeholder values"
    fi
    
    if [ -n "$MISSING_IN_ENV" ]; then
        echo ""
        echo "⚠️  Keys in .env.example but missing in .env:"
        echo "$MISSING_IN_ENV"
        echo ""
        echo "Add these to .env with actual values"
    fi
    
    if [ -z "$MISSING_IN_EXAMPLE" ] && [ -z "$MISSING_IN_ENV" ]; then
        echo ""
        echo "✅ .env and .env.example are in sync!"
    fi
else
    echo "⚠️  .env.example not found, creating from .env..."
    
    # Create .env.example with placeholder values
    while IFS='=' read -r key value; do
        if [[ $key =~ ^[A-Z_]+ ]]; then
            echo "${key}=" >> "$EXAMPLE_FILE"
        fi
    done < "$ENV_FILE"
    
    echo "✅ Created .env.example"
    echo "⚠️  Review and add placeholder values/comments"
fi

# Cleanup
rm -f /tmp/env_keys.txt /tmp/example_keys.txt

echo "=================================="
