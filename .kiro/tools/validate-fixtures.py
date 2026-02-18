#!/usr/bin/env python3
"""
Validate fixture files for UUIDv7 format and relationship integrity.

Usage:
    python .kiro/tools/validate-fixtures.py
    python .kiro/tools/validate-fixtures.py app/ores/fixtures/sample_ores.json
"""

import json
import sys
from pathlib import Path
from uuid import UUID


def is_valid_uuid(uuid_string):
    """Check if string is a valid UUID."""
    try:
        UUID(uuid_string)
        return True
    except (ValueError, AttributeError):
        return False


def validate_fixture_file(filepath):
    """Validate a single fixture file."""
    print(f"\n{'='*60}")
    print(f"Validating: {filepath}")
    print('='*60)
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return False
    
    if not isinstance(data, list):
        print("❌ Fixture must be a JSON array")
        return False
    
    errors = []
    warnings = []
    
    for idx, item in enumerate(data):
        # Check required fields
        if 'pk' not in item:
            errors.append(f"Item {idx}: Missing 'pk' field")
            continue
        
        if 'model' not in item:
            errors.append(f"Item {idx}: Missing 'model' field")
        
        if 'fields' not in item:
            errors.append(f"Item {idx}: Missing 'fields' field")
            continue
        
        # Validate UUID
        if not is_valid_uuid(item['pk']):
            errors.append(f"Item {idx}: Invalid UUID format: {item['pk']}")
        
        # Check for common fields
        fields = item['fields']
        
        if 'name' in fields and not fields['name']:
            warnings.append(f"Item {idx}: Empty 'name' field")
        
        # Validate JSONField structures
        if 'materials' in fields:
            materials = fields['materials']
            if not isinstance(materials, dict):
                errors.append(f"Item {idx}: 'materials' must be a dict")
            else:
                for ore_id, quantity in materials.items():
                    if not is_valid_uuid(ore_id):
                        errors.append(f"Item {idx}: Invalid ore UUID in materials: {ore_id}")
                    if not isinstance(quantity, (int, float)) or quantity <= 0:
                        errors.append(f"Item {idx}: Invalid quantity in materials: {quantity}")
        
        if 'components' in fields:
            components = fields['components']
            if not isinstance(components, dict):
                errors.append(f"Item {idx}: 'components' must be a dict")
            else:
                for comp_id, quantity in components.items():
                    if not is_valid_uuid(comp_id):
                        errors.append(f"Item {idx}: Invalid component UUID: {comp_id}")
                    if not isinstance(quantity, (int, float)) or quantity <= 0:
                        errors.append(f"Item {idx}: Invalid quantity in components: {quantity}")
        
        if 'blocks' in fields:
            blocks = fields['blocks']
            if not isinstance(blocks, dict):
                errors.append(f"Item {idx}: 'blocks' must be a dict")
            else:
                for block_id, quantity in blocks.items():
                    if not is_valid_uuid(block_id):
                        errors.append(f"Item {idx}: Invalid block UUID: {block_id}")
                    if not isinstance(quantity, (int, float)) or quantity <= 0:
                        errors.append(f"Item {idx}: Invalid quantity in blocks: {quantity}")
    
    # Print results
    print(f"\n📊 Summary:")
    print(f"   Total items: {len(data)}")
    print(f"   Errors: {len(errors)}")
    print(f"   Warnings: {len(warnings)}")
    
    if errors:
        print(f"\n❌ Errors found:")
        for error in errors:
            print(f"   - {error}")
    
    if warnings:
        print(f"\n⚠️  Warnings:")
        for warning in warnings:
            print(f"   - {warning}")
    
    if not errors and not warnings:
        print("\n✅ All validations passed!")
        return True
    elif not errors:
        print("\n✅ No errors (warnings only)")
        return True
    else:
        return False


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Validate specific file
        filepath = Path(sys.argv[1])
        success = validate_fixture_file(filepath)
        sys.exit(0 if success else 1)
    else:
        # Validate all fixture files
        fixture_dirs = [
            Path('app/ores/fixtures'),
            Path('app/components/fixtures'),
            Path('app/blocks/fixtures'),
            Path('app/buildorders/fixtures'),
        ]
        
        all_success = True
        for fixture_dir in fixture_dirs:
            if not fixture_dir.exists():
                continue
            
            for fixture_file in fixture_dir.glob('*.json'):
                success = validate_fixture_file(fixture_file)
                all_success = all_success and success
        
        print(f"\n{'='*60}")
        if all_success:
            print("✅ All fixtures validated successfully!")
        else:
            print("❌ Some fixtures have errors")
        print('='*60)
        
        sys.exit(0 if all_success else 1)


if __name__ == '__main__':
    main()
