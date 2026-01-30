/**
 * Block Component Selector
 * 
 * Dynamic component selection for Block forms.
 * Allows adding/removing component rows with quantity inputs.
 * Validates quantities and converts to JSON for JSONField storage.
 * 
 * Pattern adapted from material-selector.js (ENH-0000006)
 * 
 * @version 1.0
 * @date 2026-01-25
 */

(function() {
    'use strict';
    
    let componentRowCount = 0;
    const componentsData = {}; // Stores {component_id: quantity}
    
    /**
     * Initialize the component selector on page load
     */
    function initComponentSelector() {
        console.log('Initializing block component selector...');
        
        // Set up add component button
        const addButton = document.getElementById('add-component-btn');
        if (addButton) {
            addButton.addEventListener('click', addComponentRow);
        }
        
        // Pre-populate existing components (for update forms)
        const existingComponents = document.getElementById('existing-components-data');
        if (existingComponents && existingComponents.value) {
            try {
                const components = JSON.parse(existingComponents.value);
                for (const [compId, quantity] of Object.entries(components)) {
                    addComponentRow(compId, quantity);
                }
            } catch (error) {
                console.error('Error parsing existing components:', error);
            }
        }
        
        // Handle form submission
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', handleFormSubmit);
        }
        
        console.log('Component selector initialized');
    }
    
    /**
     * Add a new component row to the form
     * 
     * @param {string} componentId - Pre-selected component UUID (optional)
     * @param {number} quantity - Pre-filled quantity (optional)
     */
    function addComponentRow(componentId = null, quantity = 1) {
        const container = document.getElementById('components-container');
        if (!container) {
            console.error('Components container not found');
            return;
        }
        
        componentRowCount++;
        const rowId = `component-row-${componentRowCount}`;
        
        // Create row HTML
        const row = document.createElement('div');
        row.className = 'row mb-3 component-row';
        row.id = rowId;
        row.innerHTML = `
            <div class="col-md-6">
                <label for="component-select-${componentRowCount}" class="form-label">Component</label>
                <select class="form-select component-select" 
                        id="component-select-${componentRowCount}" 
                        data-row-id="${rowId}" 
                        required>
                    <option value="">Select a component...</option>
                    ${generateComponentOptions(componentId)}
                </select>
            </div>
            <div class="col-md-4">
                <label for="quantity-${componentRowCount}" class="form-label">Quantity</label>
                <input type="number" 
                       class="form-control quantity-input" 
                       id="quantity-${componentRowCount}"
                       data-row-id="${rowId}"
                       value="${quantity}" 
                       min="1" 
                       step="1" 
                       required>
            </div>
            <div class="col-md-2 d-flex align-items-end">
                <button type="button" 
                        class="btn btn-danger remove-component-btn" 
                        data-row-id="${rowId}">
                    <i class="bi bi-trash"></i> Remove
                </button>
            </div>
        `;
        
        container.appendChild(row);
        
        // Add event listeners
        const select = row.querySelector('.component-select');
        const quantityInput = row.querySelector('.quantity-input');
        const removeBtn = row.querySelector('.remove-component-btn');
        
        select.addEventListener('change', updateComponentsData);
        quantityInput.addEventListener('input', updateComponentsData);
        removeBtn.addEventListener('click', () => removeComponentRow(rowId));
        
        // Update data
        updateComponentsData();
        
        console.log(`Added component row: ${rowId}`);
    }
    
    /**
     * Generate component option elements
     * 
     * @param {string} selectedId - Component UUID to pre-select (optional)
     * @returns {string} HTML options string
     */
    function generateComponentOptions(selectedId = null) {
        const select = document.querySelector('#component-template-data');
        if (!select) {
            console.error('Component template data not found');
            return '';
        }
        
        const options = Array.from(select.querySelectorAll('option'))
            .filter(opt => opt.value !== '')
            .map(opt => {
                const selected = opt.value === selectedId ? 'selected' : '';
                return `<option value="${opt.value}" ${selected}>${opt.text}</option>`;
            });
        
        return options.join('');
    }
    
    /**
     * Remove a component row from the form
     * 
     * @param {string} rowId - ID of the row to remove
     */
    function removeComponentRow(rowId) {
        const row = document.getElementById(rowId);
        if (row) {
            const select = row.querySelector('.component-select');
            if (select && select.value) {
                delete componentsData[select.value];
            }
            
            row.remove();
            updateComponentsData();
            console.log(`Removed component row: ${rowId}`);
        }
    }
    
    /**
     * Update the components data object from all rows
     */
    function updateComponentsData() {
        // Clear existing data
        Object.keys(componentsData).forEach(key => delete componentsData[key]);
        
        // Collect data from all rows
        const rows = document.querySelectorAll('.component-row');
        let isValid = true;
        
        rows.forEach(row => {
            const select = row.querySelector('.component-select');
            const quantityInput = row.querySelector('.quantity-input');
            
            if (select && quantityInput) {
                const componentId = select.value;
                const quantity = parseInt(quantityInput.value, 10);
                
                if (componentId && quantity > 0) {
                    componentsData[componentId] = quantity;
                } else {
                    isValid = false;
                }
            }
        });
        
        // Update hidden field
        const hiddenField = document.getElementById('id_components_json');
        if (hiddenField) {
            hiddenField.value = JSON.stringify(componentsData);
        }
        
        // Update validation state
        updateValidationState(isValid);
        
        console.log('Components data updated:', componentsData);
    }
    
    /**
     * Update form validation state
     * 
     * @param {boolean} isValid - Whether the form is valid
     */
    function updateValidationState(isValid) {
        const submitBtn = document.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = !isValid || Object.keys(componentsData).length === 0;
        }
    }
    
    /**
     * Handle form submission
     * 
     * @param {Event} event - Submit event
     */
    function handleFormSubmit(event) {
        // Final validation
        if (Object.keys(componentsData).length === 0) {
            event.preventDefault();
            alert('Please add at least one component before submitting.');
            return false;
        }
        
        // Ensure hidden field is up to date
        const hiddenField = document.getElementById('id_components_json');
        if (hiddenField) {
            hiddenField.value = JSON.stringify(componentsData);
        }
        
        console.log('Form submitted with components:', componentsData);
        return true;
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initComponentSelector);
    } else {
        initComponentSelector();
    }
})();
