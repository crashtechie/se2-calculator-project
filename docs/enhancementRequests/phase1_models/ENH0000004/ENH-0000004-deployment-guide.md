# ENH-0000004 Deployment Guide: Create Sample Data Fixtures

**Document Version:** 1.0  
**Created Date:** 2026-01-20  
**Enhancement ID:** ENH-0000004  
**Status:** Completed  

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Pre-Deployment Checklist](#pre-deployment-checklist)
4. [Deployment Steps](#deployment-steps)
5. [Verification Procedures](#verification-procedures)
6. [Rollback Procedures](#rollback-procedures)
7. [Troubleshooting](#troubleshooting)
8. [Post-Deployment Tasks](#post-deployment-tasks)

---

## Overview

### Purpose
This guide provides step-by-step instructions for implementing ENH-0000004: Create Sample Data Fixtures. This enhancement adds JSON fixtures with sample ore, component, and block data for testing and development purposes.

### Scope
- Create fixture directories in ores/, components/, and blocks/ apps
- Generate UUIDv7 strings for all fixture entities
- Create sample_ores.json with 5+ ores
- Create sample_components.json with 10+ components
- Create sample_blocks.json with 15+ blocks
- Implement comprehensive test suite (35+ tests across 8+ test classes)
- Create verification script for fixture integrity
- Update project documentation

### Dependencies
- **ENH-0000001:** Create Ores App and Model (REQUIRED)
- **ENH-0000002:** Create Components App and Model (REQUIRED)
- **ENH-0000003:** Create Blocks App and Model (REQUIRED)

### Deployment Environment
- Development environment (local)
- Python 3.11+ with uv package manager
- Django project with ores, components, and blocks apps

### Estimated Time
- **Fixture Creation:** 2 hours
- **Test Implementation:** 1.5 hours
- **Documentation:** 30 minutes
- **Total:** 4 hours

---

## Prerequisites

### Required Software
- [x] Python 3.11+
- [x] uv package manager installed
- [x] Django project configured
- [x] uuid-utils library installed (`uv pip install uuid-utils`)

### Required Dependencies
Verify all dependencies are implemented:

```bash
# Check that models exist
uv run python manage.py shell -c "from ores.models import Ore; from components.models import Component; from blocks.models import Block; print('✅ All models available')"

# Check migrations are applied
uv run python manage.py showmigrations ores components blocks
```

Expected output: All migrations should show `[X]` checkmarks.

### Environment Setup
```bash
# Ensure you're in the project root
cd /home/dsmi001/app/se2-calculator-project

# Verify virtual environment
uv run python --version  # Should show Python 3.11+

# Verify Django is working
uv run python manage.py check
```

### Branch Setup
```bash
# Create feature branch (if not already created)
git checkout develop
git pull origin develop
git checkout -b feat/enh0000004-create-sample-fixtures
```

---

## Pre-Deployment Checklist

### Code Review
- [x] Enhancement request document reviewed and approved
- [x] Implementation plan understood
- [x] UUID generation strategy confirmed (UUIDv7 format)
- [x] Fixture data sourced from Space Engineers 2 references

### Testing Environment
- [x] Development database is accessible
- [x] Database has existing test data (can be flushed if needed)
- [x] All previous migrations applied successfully

### Backup
- [x] Development database backed up (optional for dev environment)
- [x] Git working directory is clean or changes are stashed

```bash
# Backup database (PostgreSQL example)
pg_dump -U se2_user se2_calculator_db > backups/pre_enh0000004_backup_$(date +%Y%m%d_%H%M%S).sql

# Or for SQLite
cp db.sqlite3 backups/db_pre_enh0000004_$(date +%Y%m%d_%H%M%S).sqlite3
```

---

## Deployment Steps

### Step 1: Create Fixture Directories

Create the fixtures/ directory in each app:

```bash
# Create fixture directories
mkdir -p ores/fixtures
mkdir -p components/fixtures
mkdir -p blocks/fixtures

# Verify directories created
ls -la ores/fixtures components/fixtures blocks/fixtures
```

**Expected Result:** Three empty fixture directories exist.

---

### Step 2: Create UUID Generation Script

Create the UUID generation script to produce all needed UUIDs:

**File:** `scripts/generate_fixture_uuids.py`

```bash
# Create the script
cat > scripts/generate_fixture_uuids.py << 'EOF'
#!/usr/bin/env python
"""Generate UUIDv7 strings for all fixture entities.

This script generates pre-computed UUIDv7 strings for ores, components,
and blocks to be used in fixture files. UUIDs are displayed with their
corresponding entity names for easy reference.

Usage:
    uv run python scripts/generate_fixture_uuids.py
    uv run python scripts/generate_fixture_uuids.py > docs/enhancementRequests/phase1_models/ENH0000004/uuid-mapping.txt
"""
from uuid_utils import uuid7

print("=" * 70)
print("ENH-0000004: Fixture UUID Generation")
print("=" * 70)
print()

# Generate UUIDs for ores (minimum 5, we'll generate 8)
print("=== ORES (8 total) ===")
ores = [
    "Iron Ore",
    "Silicon Ore", 
    "Nickel Ore",
    "Cobalt Ore",
    "Silver Ore",
    "Gold Ore",
    "Platinum Ore",
    "Uranium Ore"
]
ore_uuids = {}
for ore_name in ores:
    uuid = str(uuid7())
    ore_uuids[ore_name] = uuid
    print(f"{ore_name:20s} : {uuid}")

print()

# Generate UUIDs for components (minimum 10, we'll generate 12)
print("=== COMPONENTS (12 total) ===")
components = [
    "Steel Plate",
    "Construction Component",
    "Motor",
    "Computer",
    "Large Steel Tube",
    "Metal Grid",
    "Interior Plate",
    "Small Steel Tube",
    "Display",
    "Bulletproof Glass",
    "Girder",
    "Power Cell"
]
component_uuids = {}
for comp_name in components:
    uuid = str(uuid7())
    component_uuids[comp_name] = uuid
    print(f"{comp_name:30s} : {uuid}")

print()

# Generate UUIDs for blocks (minimum 15, we'll generate 18)
print("=== BLOCKS (18 total) ===")
blocks = [
    "Light Armor Block",
    "Heavy Armor Block",
    "Small Reactor",
    "Large Reactor",
    "Battery",
    "Assembler",
    "Refinery",
    "O2/H2 Generator",
    "Cockpit",
    "Gyroscope",
    "Small Thruster",
    "Large Thruster",
    "Small Container",
    "Large Container",
    "Connector",
    "Merge Block",
    "Landing Gear",
    "Spotlight"
]
block_uuids = {}
for block_name in blocks:
    uuid = str(uuid7())
    block_uuids[block_name] = uuid
    print(f"{block_name:30s} : {uuid}")

print()
print("=" * 70)
print(f"Total UUIDs Generated: {len(ore_uuids) + len(component_uuids) + len(block_uuids)}")
print("=" * 70)
print()
print("⚠️  IMPORTANT: Copy these UUIDs to your fixture files!")
print("⚠️  Each UUID must be used exactly once across all fixtures.")
print()
EOF

# Make script executable
chmod +x scripts/generate_fixture_uuids.py
```

**Run the script and save output:**

```bash
# Generate UUIDs and save to mapping file
uv run python scripts/generate_fixture_uuids.py | tee docs/enhancementRequests/phase1_models/ENH0000004/uuid-mapping.txt

# Create markdown version for documentation
cat > docs/enhancementRequests/phase1_models/ENH0000004/uuid-mapping.md << 'EOF'
# ENH-0000004 UUID Mapping

This document contains the UUIDv7 mappings for all fixture entities.

**Generated:** 2026-01-20  
**Purpose:** Reference document for fixture file creation

## Usage

When creating fixture files, copy the appropriate UUID from this document
for each entity. Ensure each UUID is used only once.

EOF

# Append the generated UUIDs
uv run python scripts/generate_fixture_uuids.py >> docs/enhancementRequests/phase1_models/ENH0000004/uuid-mapping.md
```

**Expected Result:** 
- `uuid-mapping.txt` contains all generated UUIDs
- `uuid-mapping.md` formatted as documentation
- 38 total UUIDs generated (8 ores + 12 components + 18 blocks)

---

### Step 3: Create Ore Fixtures

Create the ore fixtures file with at least 5 ores:

**File:** `ores/fixtures/sample_ores.json`

⚠️ **Important:** Use the UUIDs from your `uuid-mapping.txt` file, not these examples!

```bash
cat > ores/fixtures/sample_ores.json << 'EOF'
[
  {
    "model": "ores.ore",
    "pk": "REPLACE_WITH_IRON_UUID",
    "fields": {
      "name": "Iron Ore",
      "description": "Common metallic ore used in basic construction",
      "mass": 0.37
    }
  },
  {
    "model": "ores.ore",
    "pk": "REPLACE_WITH_SILICON_UUID",
    "fields": {
      "name": "Silicon Ore",
      "description": "Essential ore for computer and display components",
      "mass": 0.42
    }
  },
  {
    "model": "ores.ore",
    "pk": "REPLACE_WITH_NICKEL_UUID",
    "fields": {
      "name": "Nickel Ore",
      "description": "Metallic ore used in armor and electronics",
      "mass": 0.37
    }
  },
  {
    "model": "ores.ore",
    "pk": "REPLACE_WITH_COBALT_UUID",
    "fields": {
      "name": "Cobalt Ore",
      "description": "Rare metallic ore used in advanced components",
      "mass": 0.37
    }
  },
  {
    "model": "ores.ore",
    "pk": "REPLACE_WITH_SILVER_UUID",
    "fields": {
      "name": "Silver Ore",
      "description": "Conductive ore used in electrical components",
      "mass": 0.37
    }
  },
  {
    "model": "ores.ore",
    "pk": "REPLACE_WITH_GOLD_UUID",
    "fields": {
      "name": "Gold Ore",
      "description": "Highly conductive rare ore for advanced electronics",
      "mass": 0.37
    }
  },
  {
    "model": "ores.ore",
    "pk": "REPLACE_WITH_PLATINUM_UUID",
    "fields": {
      "name": "Platinum Ore",
      "description": "Extremely rare ore for specialized components",
      "mass": 0.37
    }
  },
  {
    "model": "ores.ore",
    "pk": "REPLACE_WITH_URANIUM_UUID",
    "fields": {
      "name": "Uranium Ore",
      "description": "Radioactive ore used as reactor fuel",
      "mass": 0.37
    }
  }
]
EOF
```

**Manual Step:** Open `ores/fixtures/sample_ores.json` and replace all `REPLACE_WITH_*_UUID` placeholders with actual UUIDs from `uuid-mapping.txt`.

**Validation:**
```bash
# Validate JSON syntax
uv run python -m json.tool ores/fixtures/sample_ores.json > /dev/null && echo "✅ Valid JSON" || echo "❌ Invalid JSON"

# Count ores
uv run python -c "import json; data=json.load(open('ores/fixtures/sample_ores.json')); print(f'Ore count: {len(data)}')"
```

---

### Step 4: Create Component Fixtures

Create the component fixtures file with at least 10 components:

**File:** `components/fixtures/sample_components.json`

⚠️ **Important:** 
- Use UUIDs from `uuid-mapping.txt` for component PKs
- Reference ore UUIDs in the `materials` field from Step 3

```bash
cat > components/fixtures/sample_components.json << 'EOF'
[
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_STEEL_PLATE_UUID",
    "fields": {
      "name": "Steel Plate",
      "description": "Basic building material made from iron ore",
      "materials": {
        "REPLACE_WITH_IRON_ORE_UUID": 21.0
      },
      "crafting_time": 2.5,
      "mass": 20.0,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_CONSTRUCTION_COMPONENT_UUID",
    "fields": {
      "name": "Construction Component",
      "description": "Used in constructing blocks and structures",
      "materials": {
        "REPLACE_WITH_IRON_ORE_UUID": 8.0
      },
      "crafting_time": 1.5,
      "mass": 8.0,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_MOTOR_UUID",
    "fields": {
      "name": "Motor",
      "description": "Mechanical component for moving parts",
      "materials": {
        "REPLACE_WITH_IRON_ORE_UUID": 12.0,
        "REPLACE_WITH_NICKEL_ORE_UUID": 5.0
      },
      "crafting_time": 4.0,
      "mass": 24.0,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_COMPUTER_UUID",
    "fields": {
      "name": "Computer",
      "description": "Advanced component for control systems",
      "materials": {
        "REPLACE_WITH_IRON_ORE_UUID": 0.5,
        "REPLACE_WITH_SILICON_ORE_UUID": 0.2
      },
      "crafting_time": 5.0,
      "mass": 0.5,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_LARGE_STEEL_TUBE_UUID",
    "fields": {
      "name": "Large Steel Tube",
      "description": "Structural component for large builds",
      "materials": {
        "REPLACE_WITH_IRON_ORE_UUID": 30.0
      },
      "crafting_time": 3.0,
      "mass": 25.0,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_METAL_GRID_UUID",
    "fields": {
      "name": "Metal Grid",
      "description": "Lightweight structural reinforcement",
      "materials": {
        "REPLACE_WITH_IRON_ORE_UUID": 12.0,
        "REPLACE_WITH_NICKEL_ORE_UUID": 5.0,
        "REPLACE_WITH_COBALT_ORE_UUID": 3.0
      },
      "crafting_time": 2.5,
      "mass": 6.0,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_INTERIOR_PLATE_UUID",
    "fields": {
      "name": "Interior Plate",
      "description": "Component for interior structures",
      "materials": {
        "REPLACE_WITH_IRON_ORE_UUID": 3.0
      },
      "crafting_time": 1.0,
      "mass": 3.0,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_SMALL_STEEL_TUBE_UUID",
    "fields": {
      "name": "Small Steel Tube",
      "description": "Small structural tubes for compact builds",
      "materials": {
        "REPLACE_WITH_IRON_ORE_UUID": 5.0
      },
      "crafting_time": 1.5,
      "mass": 4.0,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_DISPLAY_UUID",
    "fields": {
      "name": "Display",
      "description": "Screen component for information display",
      "materials": {
        "REPLACE_WITH_IRON_ORE_UUID": 1.0,
        "REPLACE_WITH_SILICON_ORE_UUID": 5.0
      },
      "crafting_time": 3.0,
      "mass": 1.0,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_BULLETPROOF_GLASS_UUID",
    "fields": {
      "name": "Bulletproof Glass",
      "description": "Reinforced transparent material",
      "materials": {
        "REPLACE_WITH_SILICON_ORE_UUID": 15.0
      },
      "crafting_time": 4.0,
      "mass": 15.0,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_GIRDER_UUID",
    "fields": {
      "name": "Girder",
      "description": "Heavy structural support beam",
      "materials": {
        "REPLACE_WITH_IRON_ORE_UUID": 6.0
      },
      "crafting_time": 2.0,
      "mass": 6.0,
      "fabricator_type": "assembler"
    }
  },
  {
    "model": "components.component",
    "pk": "REPLACE_WITH_POWER_CELL_UUID",
    "fields": {
      "name": "Power Cell",
      "description": "Energy storage component",
      "materials": {
        "REPLACE_WITH_IRON_ORE_UUID": 10.0,
        "REPLACE_WITH_NICKEL_ORE_UUID": 2.0,
        "REPLACE_WITH_SILICON_ORE_UUID": 1.0
      },
      "crafting_time": 3.5,
      "mass": 25.0,
      "fabricator_type": "assembler"
    }
  }
]
EOF
```

**Manual Step:** Replace all UUID placeholders with actual values from `uuid-mapping.txt`.

**Validation:**
```bash
# Validate JSON syntax
uv run python -m json.tool components/fixtures/sample_components.json > /dev/null && echo "✅ Valid JSON" || echo "❌ Invalid JSON"

# Count components
uv run python -c "import json; data=json.load(open('components/fixtures/sample_components.json')); print(f'Component count: {len(data)}')"
```

---

### Step 5: Create Block Fixtures

Create the block fixtures file with at least 15 blocks:

**File:** `blocks/fixtures/sample_blocks.json`

⚠️ **Important:** Reference component UUIDs from Step 4 in the `components` array.

```bash
# Create a starter file (you'll need to add more blocks to reach 15+)
cat > blocks/fixtures/sample_blocks.json << 'EOF'
[
  {
    "model": "blocks.block",
    "pk": "REPLACE_WITH_LIGHT_ARMOR_UUID",
    "fields": {
      "name": "Light Armor Block",
      "description": "Basic armor protection for ships and stations",
      "components": [
        {
          "component_id": "REPLACE_WITH_STEEL_PLATE_UUID",
          "component_name": "Steel Plate",
          "quantity": 25
        }
      ],
      "mass": 500.0,
      "max_health": 15000,
      "pcu_cost": 1,
      "power_consumer": "",
      "power_consumer_rate": 0.0,
      "power_producer": "",
      "power_producer_rate": 0.0,
      "max_storage": "",
      "max_storage_amount": 0.0
    }
  },
  {
    "model": "blocks.block",
    "pk": "REPLACE_WITH_HEAVY_ARMOR_UUID",
    "fields": {
      "name": "Heavy Armor Block",
      "description": "Reinforced armor with maximum protection",
      "components": [
        {
          "component_id": "REPLACE_WITH_STEEL_PLATE_UUID",
          "component_name": "Steel Plate",
          "quantity": 150
        },
        {
          "component_id": "REPLACE_WITH_METAL_GRID_UUID",
          "component_name": "Metal Grid",
          "quantity": 50
        }
      ],
      "mass": 3000.0,
      "max_health": 50000,
      "pcu_cost": 1,
      "power_consumer": "",
      "power_consumer_rate": 0.0,
      "power_producer": "",
      "power_producer_rate": 0.0,
      "max_storage": "",
      "max_storage_amount": 0.0
    }
  },
  {
    "model": "blocks.block",
    "pk": "REPLACE_WITH_SMALL_REACTOR_UUID",
    "fields": {
      "name": "Small Reactor",
      "description": "Compact nuclear reactor for power generation",
      "components": [
        {
          "component_id": "REPLACE_WITH_STEEL_PLATE_UUID",
          "component_name": "Steel Plate",
          "quantity": 50
        },
        {
          "component_id": "REPLACE_WITH_CONSTRUCTION_COMPONENT_UUID",
          "component_name": "Construction Component",
          "quantity": 20
        },
        {
          "component_id": "REPLACE_WITH_MOTOR_UUID",
          "component_name": "Motor",
          "quantity": 4
        },
        {
          "component_id": "REPLACE_WITH_COMPUTER_UUID",
          "component_name": "Computer",
          "quantity": 10
        }
      ],
      "mass": 2500.0,
      "max_health": 25000,
      "pcu_cost": 75,
      "power_consumer": "",
      "power_consumer_rate": 0.0,
      "power_producer": "MW",
      "power_producer_rate": 15.0,
      "max_storage": "",
      "max_storage_amount": 0.0
    }
  }
]
EOF
```

**Manual Steps:**
1. Replace all UUID placeholders
2. Add 12+ more blocks to reach the minimum of 15 blocks
3. Use realistic Space Engineers 2 data for masses, health, PCU, etc.
4. Ensure component references are valid

**Validation:**
```bash
# Validate JSON syntax
uv run python -m json.tool blocks/fixtures/sample_blocks.json > /dev/null && echo "✅ Valid JSON" || echo "❌ Invalid JSON"

# Count blocks
uv run python -c "import json; data=json.load(open('blocks/fixtures/sample_blocks.json')); print(f'Block count: {len(data)}')"
```

---

### Step 6: Create Fixture Verification Script

Create a Python script to verify fixture integrity:

**File:** `scripts/verify_fixtures.py`

```bash
cat > scripts/verify_fixtures.py << 'EOF'
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
EOF

# Make script executable
chmod +x scripts/verify_fixtures.py
```

**Run verification:**
```bash
uv run python scripts/verify_fixtures.py
```

**Expected Output:** All validation checks should pass with ✅ marks.

---

### Step 7: Create Comprehensive Test Suite

Add fixture tests to each app's test file. You can either:
- Add test classes to existing `tests.py` files, OR
- Create dedicated `tests_fixtures.py` files

**Example test structure** (add to `ores/tests.py`):

```python
# Add these test classes to ores/tests.py
class OreFixtureFileValidationTests(TestCase):
    """Test fixture file is valid and loadable."""
    
    def test_fixture_file_exists(self):
        """Test ore fixture file exists."""
        fixture_path = Path('ores/fixtures/sample_ores.json')
        self.assertTrue(fixture_path.exists())
    
    def test_fixture_is_valid_json(self):
        """Test ore fixture contains valid JSON."""
        with open('ores/fixtures/sample_ores.json') as f:
            data = json.load(f)  # Should not raise
            self.assertIsInstance(data, list)
    
    # Add more tests...

class OreFixtureUUIDTests(TestCase):
    """Test UUID format and uniqueness in fixtures."""
    
    def test_all_uuids_valid_format(self):
        """Test all ore UUIDs are valid UUIDv7 format."""
        # Implementation here...
    
    # Add more tests...
```

**Run tests after implementation:**
```bash
# Run ore fixture tests
uv run python manage.py test ores.tests

# Run component fixture tests
uv run python manage.py test components.tests

# Run block fixture tests
uv run python manage.py test blocks.tests

# Run all tests
uv run python manage.py test
```

**Expected Results:**
- Minimum 35+ tests total
- 100% pass rate
- Execution time < 0.5 seconds
- 8+ test classes across all apps

---

### Step 8: Load Fixtures and Verify

Test loading the fixtures into the database:

```bash
# OPTION 1: Fresh database (recommended for testing)
uv run python manage.py flush --no-input
uv run python manage.py loaddata sample_ores sample_components sample_blocks

# OPTION 2: Add to existing database (may cause conflicts)
uv run python manage.py loaddata sample_ores sample_components sample_blocks
```

⚠️ **Critical:** Fixtures must be loaded in this order:
1. `sample_ores` (no dependencies)
2. `sample_components` (depends on ores)
3. `sample_blocks` (depends on components)

**Verify data loaded:**
```bash
uv run python manage.py shell << 'EOF'
from ores.models import Ore
from components.models import Component
from blocks.models import Block

ore_count = Ore.objects.count()
component_count = Component.objects.count()
block_count = Block.objects.count()

print(f"\n{'='*50}")
print(f"Fixture Loading Results:")
print(f"{'='*50}")
print(f"Ores:       {ore_count:3d} (expected: 8+)")
print(f"Components: {component_count:3d} (expected: 12+)")
print(f"Blocks:     {block_count:3d} (expected: 15+)")
print(f"{'='*50}\n")

# Verify a relationship
iron = Ore.objects.filter(name="Iron Ore").first()
if iron:
    print(f"✅ Found Iron Ore: {iron}")
    
steel = Component.objects.filter(name="Steel Plate").first()
if steel:
    print(f"✅ Found Steel Plate: {steel}")
    print(f"   Materials: {steel.materials}")

light_armor = Block.objects.filter(name="Light Armor Block").first()
if light_armor:
    print(f"✅ Found Light Armor Block: {light_armor}")
    print(f"   Components: {light_armor.components}")

print("\n✅ Fixture data successfully loaded and verified!")
EOF
```

---

### Step 9: Update Documentation

Update project documentation to reflect the new fixtures:

#### 9.1 Update README.md

Add a section on using fixtures:

```bash
# Add to README.md (find appropriate section or create "Loading Sample Data")
cat >> README.md << 'EOF'

## Loading Sample Data

The project includes sample fixtures for ores, components, and blocks.

### Loading Fixtures

```bash
# Load all sample data (requires empty database or will add to existing data)
uv run python manage.py loaddata sample_ores sample_components sample_blocks

# Or load individually
uv run python manage.py loaddata sample_ores
uv run python manage.py loaddata sample_components
uv run python manage.py loaddata sample_blocks
```

### Resetting Database with Sample Data

```bash
# WARNING: This will delete all existing data!
uv run python manage.py flush --no-input
uv run python manage.py loaddata sample_ores sample_components sample_blocks
```

### Fixture Contents

- **Ores:** 8 sample ores (Iron, Silicon, Nickel, Cobalt, Silver, Gold, Platinum, Uranium)
- **Components:** 12 sample components (Steel Plate, Construction Component, Motor, Computer, etc.)
- **Blocks:** 15+ sample blocks (Light Armor, Heavy Armor, Reactors, etc.)

All fixture data is based on Space Engineers 2 game data.

EOF
```

#### 9.2 Update CHANGELOG.md

```bash
# Add entry to CHANGELOG.md
cat >> CHANGELOG.md << 'EOF'

## [Unreleased]

### Added
- [ENH-0000004] Created sample data fixtures for ores, components, and blocks
- [ENH-0000004] Added `sample_ores.json` with 8 sample ores
- [ENH-0000004] Added `sample_components.json` with 12 sample components  
- [ENH-0000004] Added `sample_blocks.json` with 15+ sample blocks
- [ENH-0000004] Created UUID generation script (`scripts/generate_fixture_uuids.py`)
- [ENH-0000004] Created fixture verification script (`scripts/verify_fixtures.py`)
- [ENH-0000004] Added comprehensive fixture test suite (35+ tests across 8 test classes)

EOF
```

#### 9.3 Update Phase 1 Documentation

```bash
# Update docs/projectPlan/phase1_models.md
# Add ENH-0000004 completion status (manual edit required)
```

---

## Verification Procedures

### Post-Deployment Verification Checklist

- [ ] **Fixture Files Created**
  - [ ] `ores/fixtures/sample_ores.json` exists with 5+ ores
  - [ ] `components/fixtures/sample_components.json` exists with 10+ components
  - [ ] `blocks/fixtures/sample_blocks.json` exists with 15+ blocks

- [ ] **UUID Validation**
  - [ ] All UUIDs are valid UUIDv7 format
  - [ ] All UUIDs are unique across all fixtures
  - [ ] No placeholder UUIDs remain

- [ ] **Fixture Verification Script**
  - [ ] `scripts/verify_fixtures.py` exists and is executable
  - [ ] Verification script passes all checks
  ```bash
  uv run python scripts/verify_fixtures.py
  ```

- [ ] **Fixture Loading**
  - [ ] Fixtures load without errors
  ```bash
  uv run python manage.py flush --no-input
  uv run python manage.py loaddata sample_ores sample_components sample_blocks
  ```
  - [ ] Correct counts in database
  - [ ] Relationships intact (components reference ores, blocks reference components)

- [ ] **Test Suite**
  - [ ] Minimum 35+ tests implemented
  - [ ] All tests passing (100% pass rate)
  - [ ] Test execution time < 0.5 seconds
  - [ ] 8+ test classes created
  ```bash
  uv run python manage.py test
  ```

- [ ] **Admin Interface**
  - [ ] Fixtures display correctly in admin list views
  - [ ] Fixture data can be viewed in admin detail views
  - [ ] JSONField data displays properly

- [ ] **Documentation**
  - [ ] README.md updated with fixture loading instructions
  - [ ] CHANGELOG.md updated with ENH-0000004 entry
  - [ ] UUID mapping document created
  - [ ] Deployment guide completed (this document)

---

## Rollback Procedures

### If Deployment Fails

#### 1. Remove Fixture Data (if loaded)

```bash
# Option A: Delete specific fixtures
uv run python manage.py shell << 'EOF'
from ores.models import Ore
from components.models import Component
from blocks.models import Block

# Get fixture UUIDs from uuid-mapping.txt and delete
# (Implement specific deletion logic)
EOF

# Option B: Flush entire database (nuclear option)
uv run python manage.py flush --no-input
uv run python manage.py migrate
```

#### 2. Remove Fixture Files

```bash
# Remove fixture files
rm -f ores/fixtures/sample_ores.json
rm -f components/fixtures/sample_components.json
rm -f blocks/fixtures/sample_blocks.json

# Remove fixture directories if empty
rmdir ores/fixtures 2>/dev/null || true
rmdir components/fixtures 2>/dev/null || true
rmdir blocks/fixtures 2>/dev/null || true
```

#### 3. Remove Scripts

```bash
rm -f scripts/generate_fixture_uuids.py
rm -f scripts/verify_fixtures.py
```

#### 4. Revert Documentation Changes

```bash
# Revert README.md
git checkout README.md

# Revert CHANGELOG.md
git checkout CHANGELOG.md
```

#### 5. Remove Tests

```bash
# If you created dedicated test files
rm -f ores/tests_fixtures.py
rm -f components/tests_fixtures.py
rm -f blocks/tests_fixtures.py

# If you added to existing files, manual revert required
git diff ores/tests.py
git diff components/tests.py  
git diff blocks/tests.py
```

#### 6. Git Rollback

```bash
# Discard all changes
git checkout .
git clean -fd

# Or reset to previous commit
git reset --hard HEAD~1
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: JSON Syntax Errors

**Symptom:** `json.decoder.JSONDecodeError` when loading fixtures

**Solution:**
```bash
# Validate JSON syntax
uv run python -m json.tool ores/fixtures/sample_ores.json
uv run python -m json.tool components/fixtures/sample_components.json
uv run python -m json.tool blocks/fixtures/sample_blocks.json

# Common issues:
# - Missing commas between objects
# - Trailing commas after last object
# - Unquoted strings
# - Single quotes instead of double quotes
```

#### Issue 2: Integrity Errors on Load

**Symptom:** `IntegrityError: FOREIGN KEY constraint failed`

**Solution:**
```bash
# Ensure fixtures are loaded in correct order
uv run python manage.py loaddata sample_ores    # Load first
uv run python manage.py loaddata sample_components  # Load second
uv run python manage.py loaddata sample_blocks  # Load third

# Verify referenced UUIDs exist
uv run python scripts/verify_fixtures.py
```

#### Issue 3: Duplicate Primary Key

**Symptom:** `IntegrityError: duplicate key value violates unique constraint`

**Solution:**
```bash
# Check for existing data with same PKs
uv run python manage.py shell << 'EOF'
from ores.models import Ore
# Check if any fixture UUIDs already exist
existing = Ore.objects.filter(pk__in=["uuid1", "uuid2", ...])
print(f"Existing ores: {existing.count()}")
EOF

# Solution: Flush database or use different UUIDs
uv run python manage.py flush --no-input
uv run python manage.py loaddata sample_ores sample_components sample_blocks
```

#### Issue 4: Invalid UUID Format

**Symptom:** `ValidationError: "invalid UUID format"`

**Solution:**
```bash
# Run verification script
uv run python scripts/verify_fixtures.py

# Check for:
# - Placeholder UUIDs (REPLACE_WITH_*_UUID)
# - Invalid characters
# - Wrong UUID version (must be UUIDv7, version field = 7)
```

#### Issue 5: Missing Materials/Components References

**Symptom:** Components or blocks have empty/invalid material/component references

**Solution:**
```bash
# Verify all references match uuid-mapping.txt
# Check components reference ore UUIDs
# Check blocks reference component UUIDs

# Use verification script
uv run python scripts/verify_fixtures.py
```

#### Issue 6: Test Failures

**Symptom:** Tests fail after fixture creation

**Solution:**
```bash
# Run tests with verbose output
uv run python manage.py test --verbosity=2

# Check specific test
uv run python manage.py test ores.tests.OreFixtureFileValidationTests

# Common issues:
# - File paths incorrect
# - Expected counts don't match actual
# - UUID format regex incorrect
```

---

## Post-Deployment Tasks

### Immediate Tasks (Day 1)

- [ ] **Create Post-Deployment Review Document**
  - File: `ENH-0000004-post-deployment-review.md`
  - Document: Deployment results, issues encountered, metrics

- [ ] **Create Testing Validation Document**
  - File: `ENH-0000004-testing-validation.md`
  - Document: Test results, coverage, execution times

- [ ] **Verify Admin Interface**
  - Start development server
  - Load admin interface
  - Verify all fixture data displays correctly

- [ ] **Team Communication**
  - Notify team that fixtures are available
  - Share fixture loading instructions
  - Document any gotchas or issues

### Follow-up Tasks (Week 1)

- [ ] **Monitor Usage**
  - Track how often fixtures are used
  - Gather feedback from team members
  - Document any issues or enhancement requests

- [ ] **Update Knowledge Base**
  - Add fixture creation process to team wiki
  - Document UUID generation procedure
  - Create troubleshooting guide

- [ ] **Consider Enhancements**
  - Additional fixtures for edge cases?
  - Fixture versioning (v1.0, v1.1)?
  - Automated fixture updates?

---

## Success Criteria

This deployment is considered successful when:

✅ All fixture files created with correct counts (5+ ores, 10+ components, 15+ blocks)  
✅ All UUIDs are valid UUIDv7 format and unique  
✅ Verification script passes all checks  
✅ Fixtures load without errors  
✅ Test suite implemented (35+ tests, 100% pass rate, < 0.5s execution)  
✅ Documentation updated (README, CHANGELOG, Phase 1 docs)  
✅ Admin interface displays fixture data correctly  
✅ Post-deployment review completed  

---

## References

- **Enhancement Request:** `ENH0000004-create-sample-fixtures.md`
- **Related Enhancements:**
  - ENH-0000001: Create Ores App and Model
  - ENH-0000002: Create Components App and Model
  - ENH-0000003: Create Blocks App and Model
- **Django Documentation:** https://docs.djangoproject.com/en/stable/howto/initial-data/
- **UUIDv7 Specification:** https://datatracker.ietf.org/doc/html/draft-peabody-dispatch-new-uuid-format

---

## Sign-off

**Deployed By:** _________________  
**Date:** _________________  
**Verified By:** _________________  
**Date:** _________________  

---

**Document End**
