# Technical Specifications

## Data Extraction Specifications

### Ore Data Structure

**Source:** Category:Natural_Resources

**HTML Selectors:**
- Name: `div.druid-title`
- Mass: `div.druid-data-mass`

**Output Schema:**
```json
{
  "model": "ores.ore",
  "pk": "uuid-v7",
  "fields": {
    "name": "string",
    "mass": "float",
    "description": "string (empty)"
  }
}
```

### Component Data Structure

**Sources:**
- Category:Simple_Components
- Category:Complex_Components
- Category:High-tech_Components
- Category:Refinery_Products

**HTML Selectors:**
- Name: `div.druid-title`
- Mass: `div.druid-data-mass`
- Crafting Time: `div.druid-data-BaseTime`
- Fabricator: `div.druid-data-Location`
- Materials: `div[data-druid-section-row="Inputs"]`

**Fabricator Mapping:**
```python
{
    "Smelter 2.5 m": "Smelter",
    "Assembler 5 m": "Assembler",
    "Fabricator 10 m": "Advanced Assembler",
    "Refinery 7.5 m": "Refinery"
}
```

**Output Schema:**
```json
{
  "model": "components.component",
  "pk": "uuid-v7",
  "fields": {
    "name": "string",
    "mass": "float",
    "crafting_time": "float",
    "fabricator_type": "string",
    "materials": "object",
    "description": "string (empty)"
  }
}
```

### Block Data Structure

**Source:** Category:Blocks

**HTML Selectors:**
- Name: `div.druid-title`
- Mass: `div.druid-data-mass` (remove 'kg')
- Components: `div.druid-grid-item`

**Output Schema:**
```json
{
  "model": "blocks.block",
  "pk": "uuid-v7",
  "fields": {
    "name": "string",
    "mass": "float",
    "components": "object",
    "description": "string (empty)"
  }
}
```

## HTTP Client Specifications

**Rate Limiting:** 1 second between requests
**Timeout:** 10 seconds
**Retries:** 3 attempts with exponential backoff
**User-Agent:** Custom identifier

## Error Handling

**Network Errors:**
- Retry with backoff
- Log failure after max retries
- Continue with next item

**Parse Errors:**
- Log error with URL
- Skip item
- Continue processing

**Missing Data:**
- Use default values
- Log warning
- Include in output with null/empty values

## Logging Format

```
YYYY-MM-DD HH:MM:SS - MODULE - LEVEL - MESSAGE
```

**Log Levels:**
- INFO: Progress updates
- WARNING: Missing data
- ERROR: Parse failures
- CRITICAL: Fatal errors
