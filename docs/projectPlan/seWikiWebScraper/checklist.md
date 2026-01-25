# SE2 Wiki Web Scraper - Development Checklist

## Phase 1: Docker Environment Setup (0.5 days)

- [ ] Create project directory structure
- [ ] Write Dockerfile
- [ ] Write docker-compose.yml
- [ ] Create requirements.txt
- [ ] Create .dockerignore
- [ ] Test container build
- [ ] Verify volume mounts
- [ ] Test Python environment

## Phase 2: Core Scraper Implementation (1.5 days)

### HTTP Client
- [ ] Implement get_page() with retry logic
- [ ] Implement get_category_links()
- [ ] Add rate limiting
- [ ] Add timeout handling
- [ ] Test with real wiki URLs

### Ore Parser
- [ ] Implement parse_ore_page()
- [ ] Extract name from druid-title
- [ ] Extract mass from druid-data-mass
- [ ] Handle missing data
- [ ] Test with sample HTML

### Component Parser
- [ ] Implement parse_component_page()
- [ ] Extract name, mass, crafting time
- [ ] Extract fabricator type with mapping
- [ ] Extract materials from Inputs section
- [ ] Handle components without materials
- [ ] Test with sample HTML

### Block Parser
- [ ] Implement parse_block_page()
- [ ] Extract name and mass
- [ ] Extract components from grid items
- [ ] Handle blocks without components
- [ ] Test with sample HTML

### JSON Writer
- [ ] Implement UUIDv7 generation
- [ ] Implement write_fixture()
- [ ] Format output for Django
- [ ] Test JSON validity

### Main Orchestrator
- [ ] Implement main() workflow
- [ ] Scrape all ore pages
- [ ] Scrape all component pages
- [ ] Scrape all block pages
- [ ] Write all JSON files
- [ ] Add progress logging

### Configuration
- [ ] Define all URLs
- [ ] Set request parameters
- [ ] Configure logging

## Phase 3: Data Validation and Testing (0.5 days)

- [ ] Create validation functions
- [ ] Validate ore data
- [ ] Validate component data
- [ ] Validate block data
- [ ] Test JSON schema compliance
- [ ] Test Django fixture loading
- [ ] Generate completeness report
- [ ] Handle edge cases
- [ ] Fix data quality issues

## Phase 4: Documentation and Deployment (0.5 days)

- [ ] Write README.md
- [ ] Document usage instructions
- [ ] Create deployment guide
- [ ] Add troubleshooting section
- [ ] Document maintenance procedures
- [ ] Final testing
- [ ] Deploy to production

## Post-Deployment

- [ ] Run full scrape
- [ ] Validate all output files
- [ ] Load fixtures into Django
- [ ] Verify data in database
- [ ] Document any issues found
