#!/usr/bin/env python
"""Generate and assign UUIDv7 to fixture files.

This script reads fixture files (ores, components, blocks) and generates
UUIDv7 values for each entity's pk field, replacing any existing values
and updating all references throughout the fixture files.

Usage:
    uv run python scripts/generate_fixture_uuids.py
"""
import json
import sys
from pathlib import Path
from uuid_utils import uuid7


def load_fixture(filepath):
    """Load fixture file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Fixture file not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {filepath}: {e}")
        return None


def save_fixture(filepath, data):
    """Save fixture file with pretty formatting."""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"❌ Failed to save {filepath}: {e}")
        return False


def generate_fixture_uuids():
    """Generate and assign UUIDs to all fixture files."""
    
    print("=" * 70)
    print("ENH-0000004: Fixture UUID Assignment")
    print("=" * 70)
    print()
    
    # Define fixture file paths
    ore_fixture = Path('ores/fixtures/sample_ores.json')
    component_fixture = Path('components/fixtures/sample_components.json')
    block_fixture = Path('blocks/fixtures/sample_blocks.json')
    
    # Load all fixtures
    print("📂 Loading fixture files...")
    ores_data = load_fixture(ore_fixture)
    components_data = load_fixture(component_fixture)
    blocks_data = load_fixture(block_fixture)
    
    if not all([ores_data, components_data, blocks_data]):
        print("\n❌ Failed to load all fixture files. Aborting.")
        return False
    
    print(f"  ✅ Loaded {len(ores_data)} ores")
    print(f"  ✅ Loaded {len(components_data)} components")
    print(f"  ✅ Loaded {len(blocks_data)} blocks")
    print()
    
    # Generate new UUIDs for ores and build mapping
    print("🔄 Generating UUIDs for ores...")
    ore_uuid_map = {}  # Maps old pk to new pk
    for ore in ores_data:
        old_pk = ore['pk']
        new_uuid = str(uuid7())
        ore_uuid_map[old_pk] = new_uuid
        ore['pk'] = new_uuid
        print(f"  ✅ {ore['fields']['name']:20s} → {new_uuid}")
    print()
    
    # Generate new UUIDs for components and update ore references
    print("🔄 Generating UUIDs for components and updating ore references...")
    component_uuid_map = {}  # Maps old pk to new pk
    for component in components_data:
        old_pk = component['pk']
        new_uuid = str(uuid7())
        component_uuid_map[old_pk] = new_uuid
        component['pk'] = new_uuid
        
        # Update ore references in materials field
        if 'materials' in component['fields']:
            materials = component['fields']['materials']
            updated_materials = {}
            for ore_pk, quantity in materials.items():
                # Replace old ore PKs with new ones
                new_ore_pk = ore_uuid_map.get(ore_pk, ore_pk)
                updated_materials[new_ore_pk] = quantity
            component['fields']['materials'] = updated_materials
        
        print(f"  ✅ {component['fields']['name']:30s} → {new_uuid}")
    print()
    
    # Generate new UUIDs for blocks and update component references
    print("🔄 Generating UUIDs for blocks and updating component references...")
    block_uuid_map = {}  # Maps old pk to new pk
    for block in blocks_data:
        old_pk = block['pk']
        new_uuid = str(uuid7())
        block_uuid_map[old_pk] = new_uuid
        block['pk'] = new_uuid
        
        # Update component references
        if 'components' in block['fields']:
            for component_ref in block['fields']['components']:
                old_comp_pk = component_ref['component_id']
                new_comp_pk = component_uuid_map.get(old_comp_pk, old_comp_pk)
                component_ref['component_id'] = new_comp_pk
        
        print(f"  ✅ {block['fields']['name']:30s} → {new_uuid}")
    print()
    
    # Save updated fixtures
    print("💾 Saving updated fixture files...")
    success = True
    
    if save_fixture(ore_fixture, ores_data):
        print(f"  ✅ Saved {ore_fixture}")
    else:
        success = False
    
    if save_fixture(component_fixture, components_data):
        print(f"  ✅ Saved {component_fixture}")
    else:
        success = False
    
    if save_fixture(block_fixture, blocks_data):
        print(f"  ✅ Saved {block_fixture}")
    else:
        success = False
    
    print()
    
    if not success:
        print("❌ Failed to save some fixture files.")
        return False
    
    # Generate and save UUID mapping document
    print("📝 Creating UUID mapping document...")
    mapping_content = "# ENH-0000004 UUID Mapping\n\n"
    mapping_content += "This document contains the UUIDv7 mappings for all fixture entities.\n\n"
    mapping_content += "**Generated:** 2026-01-20\n"
    mapping_content += "**Purpose:** Reference document for fixture file assignments\n\n"
    
    mapping_content += "## Ores\n\n"
    for ore in ores_data:
        mapping_content += f"- **{ore['fields']['name']}**: `{ore['pk']}`\n"
    
    mapping_content += "\n## Components\n\n"
    for component in components_data:
        mapping_content += f"- **{component['fields']['name']}**: `{component['pk']}`\n"
    
    mapping_content += "\n## Blocks\n\n"
    for block in blocks_data:
        mapping_content += f"- **{block['fields']['name']}**: `{block['pk']}`\n"
    
    mapping_file = Path('docs/enhancementRequests/phase1_models/ENH0000004/uuid-mapping.md')
    try:
        with open(mapping_file, 'w') as f:
            f.write(mapping_content)
        print(f"  ✅ Saved {mapping_file}")
    except Exception as e:
        print(f"  ❌ Failed to save mapping document: {e}")
        success = False
    
    print()
    print("=" * 70)
    print(f"Total UUIDs Generated: {len(ores_data) + len(components_data) + len(blocks_data)}")
    print("=" * 70)
    print()
    
    if success:
        print("✅ All fixtures successfully updated with new UUIDs!")
        print()
        print("Next steps:")
        print("  1. Verify fixture files: uv run python scripts/verify_fixtures.py")
        print("  2. Load fixtures: uv run python manage.py loaddata sample_ores sample_components sample_blocks")
        print()
    else:
        print("❌ Some operations failed. Please review the errors above.")
    
    return success


if __name__ == '__main__':
    success = generate_fixture_uuids()
    sys.exit(0 if success else 1)