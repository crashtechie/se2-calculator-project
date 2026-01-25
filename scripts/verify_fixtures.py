#!/usr/bin/env python
"""Verify fixture integrity and relationships.

This script performs comprehensive validation of fixture files:
- JSON syntax validation
- UUID format verification (UUIDv7)
- Uniqueness checks
- Relationship integrity (foreign key references)
- Minimum count requirements

Usage:
    uv run python scripts/verify_fixtures.py
"""
import json
import re
from pathlib import Path

# UUIDv7 regex pattern
UUID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
    re.IGNORECASE
)

def verify_fixtures():
    """Verify all fixture files for integrity and relationships."""
    print("🔍 Verifying fixture files...\n")
    
    # Load fixture files
    print("Loading fixture files...")
    try:
        ores = json.load(open('ores/fixtures/sample_ores.json'))
        print(f"  ✅ Loaded ores fixture")
    except Exception as e:
        print(f"  ❌ Failed to load ores fixture: {e}")
        return False
    
    try:
        components = json.load(open('components/fixtures/sample_components.json'))
        print(f"  ✅ Loaded components fixture")
    except Exception as e:
        print(f"  ❌ Failed to load components fixture: {e}")
        return False
    
    try:
        blocks = json.load(open('blocks/fixtures/sample_blocks.json'))
        print(f"  ✅ Loaded blocks fixture")
    except Exception as e:
        print(f"  ❌ Failed to load blocks fixture: {e}")
        return False
    
    print(f"\n📊 Counts: {len(ores)} ores, {len(components)} components, {len(blocks)} blocks\n")
    
    # Collect all UUIDs
    ore_uuids = {ore['pk'] for ore in ores}
    component_uuids = {comp['pk'] for comp in components}
    block_uuids = {block['pk'] for block in blocks}
    
    # Verify counts
    errors = []
    
    if len(ores) < 5:
        errors.append(f"❌ Need at least 5 ores, got {len(ores)}")
    else:
        print(f"✅ Ore count meets minimum (5+): {len(ores)}")
    
    if len(components) < 10:
        errors.append(f"❌ Need at least 10 components, got {len(components)}")
    else:
        print(f"✅ Component count meets minimum (10+): {len(components)}")
    
    if len(blocks) < 15:
        errors.append(f"❌ Need at least 15 blocks, got {len(blocks)}")
    else:
        print(f"✅ Block count meets minimum (15+): {len(blocks)}")
    
    # Verify UUID uniqueness
    all_uuids = ore_uuids | component_uuids | block_uuids
    if len(all_uuids) != len(ores) + len(components) + len(blocks):
        errors.append("❌ Duplicate UUIDs found across fixtures!")
    else:
        print(f"✅ All UUIDs are unique ({len(all_uuids)} total)")
    
    # Verify UUIDv7 format
    invalid_uuids = []
    for uuid in all_uuids:
        if not UUID_PATTERN.match(uuid):
            invalid_uuids.append(uuid)
    
    if invalid_uuids:
        errors.append(f"❌ Invalid UUIDv7 format found: {', '.join(invalid_uuids[:3])}")
    else:
        print("✅ All UUIDs are valid UUIDv7 format")
    
    # Verify component material references
    invalid_material_refs = []
    for comp in components:
        comp_name = comp['fields']['name']
        materials = comp['fields'].get('materials', {})
        for ore_id in materials.keys():
            if ore_id not in ore_uuids:
                invalid_material_refs.append(f"{comp_name} → {ore_id}")
    
    if invalid_material_refs:
        errors.append(f"❌ Invalid ore references in components: {', '.join(invalid_material_refs[:3])}")
    else:
        print("✅ All component material references are valid")
    
    # Verify block component references
    invalid_component_refs = []
    for block in blocks:
        block_name = block['fields']['name']
        components_list = block['fields'].get('components', [])
        for comp_ref in components_list:
            comp_id = comp_ref.get('component_id')
            if comp_id not in component_uuids:
                invalid_component_refs.append(f"{block_name} → {comp_id}")
            
            # Verify required fields
            if 'component_name' not in comp_ref:
                invalid_component_refs.append(f"{block_name}: missing component_name")
            if 'quantity' not in comp_ref:
                invalid_component_refs.append(f"{block_name}: missing quantity")
    
    if invalid_component_refs:
        errors.append(f"❌ Invalid component references in blocks: {', '.join(invalid_component_refs[:3])}")
    else:
        print("✅ All block component references are valid")
    
    # Check for placeholder UUIDs
    placeholder_pattern = re.compile(r'REPLACE_WITH_.*_UUID', re.IGNORECASE)
    placeholders_found = []
    
    for ore in ores:
        if placeholder_pattern.search(ore['pk']):
            placeholders_found.append(f"ore: {ore['fields']['name']}")
    
    for comp in components:
        if placeholder_pattern.search(comp['pk']):
            placeholders_found.append(f"component: {comp['fields']['name']}")
        for ore_id in comp['fields'].get('materials', {}).keys():
            if placeholder_pattern.search(ore_id):
                placeholders_found.append(f"component material: {comp['fields']['name']}")
    
    for block in blocks:
        if placeholder_pattern.search(block['pk']):
            placeholders_found.append(f"block: {block['fields']['name']}")
        for comp_ref in block['fields'].get('components', []):
            if placeholder_pattern.search(comp_ref.get('component_id', '')):
                placeholders_found.append(f"block component: {block['fields']['name']}")
    
    if placeholders_found:
        errors.append(f"❌ Placeholder UUIDs still present: {', '.join(placeholders_found[:3])}")
    else:
        print("✅ No placeholder UUIDs found")
    
    # Print summary
    print("\n" + "=" * 70)
    if errors:
        print("❌ VALIDATION FAILED")
        print("=" * 70)
        for error in errors:
            print(error)
        return False
    else:
        print("🎉 ALL FIXTURES VERIFIED SUCCESSFULLY!")
        print("=" * 70)
        return True

if __name__ == '__main__':
    import sys
    success = verify_fixtures()
    sys.exit(0 if success else 1)
