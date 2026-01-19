# Phase 2: Views & Templates

**Duration:** 3-4 days  
**Priority:** High  
**Dependencies:** Phase 1 complete

## Objectives
- Implement CRUD views for all three apps
- Create templates with filtering and sorting
- Set up URL routing
- Add basic styling

## Tasks

### 2.1 URL Configuration
**Files:** `se2CalcProject/urls.py`, `ores/urls.py`, `components/urls.py`, `blocks/urls.py`

- [ ] Create url patterns for ores app
- [ ] Create url patterns for components app
- [ ] Create url patterns for blocks app
- [ ] Include app URLs in main urls.py
- [ ] Create home page URL

### 2.2 Ores Views
**File:** `ores/views.py`

Views to implement:
- OreListView (with filtering by name, sorting by mass)
- OreDetailView
- OreCreateView
- OreUpdateView
- OreDeleteView

- [ ] Implement OreListView with QuerySet filtering
- [ ] Implement OreDetailView
- [ ] Implement OreCreateView with form validation
- [ ] Implement OreUpdateView
- [ ] Implement OreDeleteView with confirmation
- [ ] Add success messages for create/update/delete

### 2.3 Components Views
**File:** `components/views.py`

Views to implement:
- ComponentListView (with filtering by name, sorting by mass)
- ComponentDetailView
- ComponentCreateView (with JSONField handling)
- ComponentUpdateView
- ComponentDeleteView

- [ ] Implement ComponentListView with QuerySet filtering
- [ ] Implement ComponentDetailView (display materials from JSONField)
- [ ] Implement ComponentCreateView with material selection
- [ ] Implement ComponentUpdateView
- [ ] Implement ComponentDeleteView
- [ ] Add JavaScript for dynamic material selection

### 2.4 Blocks Views
**File:** `blocks/views.py`

Views to implement:
- BlockListView (with filtering by name, sorting by mass)
- BlockDetailView
- BlockCreateView (with JSONField handling)
- BlockUpdateView
- BlockDeleteView

- [ ] Implement BlockListView with QuerySet filtering
- [ ] Implement BlockDetailView (display components from JSONField)
- [ ] Implement BlockCreateView with component selection
- [ ] Implement BlockUpdateView
- [ ] Implement BlockDeleteView
- [ ] Add JavaScript for dynamic component selection

### 2.5 Forms
**Files:** `ores/forms.py`, `components/forms.py`, `blocks/forms.py`

- [ ] Create OreForm with validation
- [ ] Create ComponentForm with JSONField widget
- [ ] Create BlockForm with JSONField widget
- [ ] Add custom validation for JSONField structure
- [ ] Add help text for all fields

### 2.6 Templates - Base
**Files:** `templates/base.html`, `templates/home.html`

- [ ] Create base template with navigation
- [ ] Create home page with links to all apps
- [ ] Add CSS framework (Bootstrap or Tailwind)
- [ ] Create navigation menu
- [ ] Add footer with project info

### 2.7 Templates - Ores
**Files:** `ores/templates/ores/`

- [ ] ore_list.html (with filter form and sort links)
- [ ] ore_detail.html
- [ ] ore_form.html (for create/update)
- [ ] ore_confirm_delete.html

### 2.8 Templates - Components
**Files:** `components/templates/components/`

- [ ] component_list.html (with filter form and sort links)
- [ ] component_detail.html (display materials)
- [ ] component_form.html (with material selector)
- [ ] component_confirm_delete.html

### 2.9 Templates - Blocks
**Files:** `blocks/templates/blocks/`

- [ ] block_list.html (with filter form and sort links)
- [ ] block_detail.html (display components and stats)
- [ ] block_form.html (with component selector)
- [ ] block_confirm_delete.html

### 2.10 Static Files
**Files:** `static/css/`, `static/js/`

- [ ] Create main.css for custom styles
- [ ] Create material-selector.js for dynamic forms
- [ ] Create component-selector.js for dynamic forms
- [ ] Add form validation JavaScript

## Deliverables
- All CRUD views functional for three apps
- Templates with filtering and sorting capabilities
- Forms with proper validation
- Basic styling applied
- URL routing configured

## Testing Checklist
- [ ] Can create new ores/components/blocks via web interface
- [ ] Can view list of all items with filtering
- [ ] Can sort lists by mass
- [ ] Can view details of individual items
- [ ] Can update existing items
- [ ] Can delete items with confirmation
- [ ] JSONField data displays correctly in detail views
- [ ] Form validation works (required fields, data types)
- [ ] Success/error messages display properly

## URL Structure
```
/                           - Home page
/ores/                      - Ore list
/ores/<uuid>/               - Ore detail
/ores/create/               - Create ore
/ores/<uuid>/update/        - Update ore
/ores/<uuid>/delete/        - Delete ore
/components/                - Component list
/components/<uuid>/         - Component detail
/components/create/         - Create component
/components/<uuid>/update/  - Update component
/components/<uuid>/delete/  - Delete component
/blocks/                    - Block list
/blocks/<uuid>/             - Block detail
/blocks/create/             - Create block
/blocks/<uuid>/update/      - Update block
/blocks/<uuid>/delete/      - Delete block
```

## Notes
- Use Django's generic class-based views where possible
- Implement pagination for list views (25 items per page)
- Add breadcrumb navigation
- Ensure mobile responsiveness
