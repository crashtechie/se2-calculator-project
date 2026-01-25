/**
 * Material Selector for Components
 * 
 * Provides dynamic UI for selecting materials (ores) and quantities.
 * Converts form data to JSON format for Django JSONField storage.
 * 
 * ENH-0000006: Components Views & Templates
 */

class MaterialSelector {
    constructor(containerId, ores, existingMaterials = {}) {
        this.container = document.getElementById(containerId);
        this.ores = ores; // Array of {id: uuid, name: string}
        this.existingMaterials = existingMaterials;
        this.rowCount = 0;
        
        if (!this.container) {
            console.error(`Material selector container '${containerId}' not found`);
            return;
        }
        
        this.init();
    }
    
    init() {
        // Create table structure
        this.createTable();
        
        // Load existing materials if any
        if (Object.keys(this.existingMaterials).length > 0) {
            this.loadExistingMaterials();
        } else {
            // Add one empty row by default
            this.addRow();
        }
        
        // Setup form submission handler
        this.setupFormSubmission();
    }
    
    createTable() {
        this.container.innerHTML = `
            <div class="card mb-3">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Materials Required</h5>
                    <button type="button" class="btn btn-sm btn-success" id="add-material-btn">
                        <i class="bi bi-plus-circle"></i> Add Material
                    </button>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th style="width: 50%;">Ore</th>
                                    <th style="width: 30%;">Quantity (kg)</th>
                                    <th style="width: 20%;">Action</th>
                                </tr>
                            </thead>
                            <tbody id="materials-table-body">
                                <!-- Rows added dynamically -->
                            </tbody>
                        </table>
                    </div>
                    <div class="text-muted small mt-2">
                        <i class="bi bi-info-circle"></i>
                        At least one material is required. Quantities must be positive numbers.
                    </div>
                </div>
            </div>
        `;
        
        // Attach add button handler
        document.getElementById('add-material-btn').addEventListener('click', () => {
            this.addRow();
        });
    }
    
    addRow(oreId = '', quantity = '') {
        const tbody = document.getElementById('materials-table-body');
        const rowId = `material-row-${this.rowCount++}`;
        
        const row = document.createElement('tr');
        row.id = rowId;
        row.innerHTML = `
            <td>
                <select class="form-select material-ore-select" data-row-id="${rowId}" required>
                    <option value="">-- Select Ore --</option>
                    ${this.ores.map(ore => 
                        `<option value="${ore.id}" ${ore.id === oreId ? 'selected' : ''}>
                            ${ore.name}
                        </option>`
                    ).join('')}
                </select>
            </td>
            <td>
                <input type="number" 
                       class="form-control material-quantity-input" 
                       data-row-id="${rowId}"
                       placeholder="0.00" 
                       step="0.01" 
                       min="0.01"
                       value="${quantity}"
                       required>
            </td>
            <td>
                <button type="button" 
                        class="btn btn-sm btn-danger" 
                        onclick="materialSelector.removeRow('${rowId}')">
                    <i class="bi bi-trash"></i> Remove
                </button>
            </td>
        `;
        
        tbody.appendChild(row);
        
        // Add validation listeners
        this.attachValidation(rowId);
    }
    
    removeRow(rowId) {
        const row = document.getElementById(rowId);
        if (!row) return;
        
        // Check if this is the last row
        const tbody = document.getElementById('materials-table-body');
        if (tbody.children.length <= 1) {
            alert('At least one material is required.');
            return;
        }
        
        row.remove();
        this.validateForm();
    }
    
    attachValidation(rowId) {
        const row = document.getElementById(rowId);
        if (!row) return;
        
        const select = row.querySelector('.material-ore-select');
        const input = row.querySelector('.material-quantity-input');
        
        // Validate on change
        select.addEventListener('change', () => this.validateForm());
        input.addEventListener('input', () => this.validateForm());
        input.addEventListener('blur', () => this.validateQuantity(input));
    }
    
    validateQuantity(input) {
        const value = parseFloat(input.value);
        
        if (isNaN(value) || value <= 0) {
            input.classList.add('is-invalid');
            input.setCustomValidity('Quantity must be a positive number');
        } else {
            input.classList.remove('is-invalid');
            input.setCustomValidity('');
        }
    }
    
    validateForm() {
        const tbody = document.getElementById('materials-table-body');
        const rows = tbody.querySelectorAll('tr');
        
        let isValid = true;
        const seenOres = new Set();
        
        rows.forEach(row => {
            const select = row.querySelector('.material-ore-select');
            const input = row.querySelector('.material-quantity-input');
            
            // Check if ore is selected
            if (!select.value) {
                select.classList.add('is-invalid');
                isValid = false;
            } else {
                select.classList.remove('is-invalid');
                
                // Check for duplicate ores
                if (seenOres.has(select.value)) {
                    select.classList.add('is-invalid');
                    isValid = false;
                } else {
                    seenOres.add(select.value);
                }
            }
            
            // Check quantity
            const quantity = parseFloat(input.value);
            if (isNaN(quantity) || quantity <= 0) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    }
    
    loadExistingMaterials() {
        // Load existing materials into form
        for (const [oreId, quantity] of Object.entries(this.existingMaterials)) {
            this.addRow(oreId, quantity);
        }
    }
    
    getMaterialsJSON() {
        const tbody = document.getElementById('materials-table-body');
        const rows = tbody.querySelectorAll('tr');
        const materials = {};
        
        rows.forEach(row => {
            const select = row.querySelector('.material-ore-select');
            const input = row.querySelector('.material-quantity-input');
            
            if (select.value && input.value) {
                const oreId = select.value;
                const quantity = parseFloat(input.value);
                
                if (!isNaN(quantity) && quantity > 0) {
                    materials[oreId] = quantity;
                }
            }
        });
        
        return materials;
    }
    
    setupFormSubmission() {
        // Find the form that contains this selector
        const form = this.container.closest('form');
        if (!form) {
            console.error('Material selector must be inside a form');
            return;
        }
        
        // Add hidden input for materials JSON
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'materials_json';
        hiddenInput.id = 'materials_json';
        form.appendChild(hiddenInput);
        
        // Intercept form submission
        form.addEventListener('submit', (e) => {
            // Validate materials
            if (!this.validateForm()) {
                e.preventDefault();
                alert('Please correct the material errors before submitting.');
                return false;
            }
            
            // Convert materials to JSON
            const materials = this.getMaterialsJSON();
            
            // Check for at least one material
            if (Object.keys(materials).length === 0) {
                e.preventDefault();
                alert('At least one material is required.');
                return false;
            }
            
            // Set hidden input value
            hiddenInput.value = JSON.stringify(materials);
            
            console.log('Submitting materials:', materials);
            return true;
        });
    }
}

// Make MaterialSelector available globally
window.MaterialSelector = MaterialSelector;

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Material selector JavaScript loaded');
});
