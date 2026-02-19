---
inclusion: auto
fileMatchPattern: '**/*.js'
description: Frontend JavaScript patterns for Django projects including vanilla JS, AJAX, form handling, and Bootstrap 5 integration
---

# Frontend JavaScript Patterns

## Project Context

Space Engineers 2 Calculator uses:
- **Vanilla JavaScript** (no framework)
- **Bootstrap 5.3.2** for UI components
- **Django CSRF** protection for AJAX
- **Progressive enhancement** approach
- **Minimal JavaScript** (server-side rendering preferred)

## JavaScript Organization

### File Structure

```
static/
├── js/
│   ├── main.js              # Global utilities
│   ├── blocks.js            # Block-specific functionality
│   ├── components.js        # Component-specific functionality
│   └── build-orders.js      # Build order calculator
```

### Loading JavaScript

```django
{# In base.html #}
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script src="{% static 'js/main.js' %}"></script>

{# In specific templates #}
{% block extra_js %}
<script src="{% static 'js/blocks.js' %}"></script>
<script>
    // Page-specific initialization
    document.addEventListener('DOMContentLoaded', function() {
        initializeBlockSearch();
    });
</script>
{% endblock %}
```

## CSRF Token Handling

### Get CSRF Token

```javascript
// main.js - Global CSRF utility
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
```

### AJAX with CSRF

```javascript
// Fetch API with CSRF
fetch('/api/blocks/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
        name: 'New Block',
        mass: 10.0
    })
})
.then(response => response.json())
.then(data => {
    console.log('Success:', data);
})
.catch(error => {
    console.error('Error:', error);
});

// XMLHttpRequest with CSRF
const xhr = new XMLHttpRequest();
xhr.open('POST', '/api/blocks/');
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.setRequestHeader('X-CSRFToken', csrftoken);
xhr.onload = function() {
    if (xhr.status === 200) {
        const data = JSON.parse(xhr.responseText);
        console.log('Success:', data);
    }
};
xhr.send(JSON.stringify({ name: 'New Block' }));
```

## AJAX Patterns

### GET Request

```javascript
// Fetch data from API
async function fetchBlocks(searchQuery = '') {
    try {
        const url = `/api/blocks/?q=${encodeURIComponent(searchQuery)}`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data.results;
    } catch (error) {
        console.error('Error fetching blocks:', error);
        showError('Failed to load blocks');
        return [];
    }
}

// Usage
fetchBlocks('reactor').then(blocks => {
    displayBlocks(blocks);
});
```

### POST Request

```javascript
// Create new block
async function createBlock(blockData) {
    try {
        const response = await fetch('/api/blocks/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(blockData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to create block');
        }
        
        const data = await response.json();
        showSuccess('Block created successfully!');
        return data;
    } catch (error) {
        console.error('Error creating block:', error);
        showError(error.message);
        throw error;
    }
}

// Usage
const blockData = {
    name: 'Light Armor Block',
    mass: 10.0,
    pcu: 100
};

createBlock(blockData).then(block => {
    console.log('Created block:', block);
    window.location.href = `/blocks/${block.id}/`;
});
```

### PUT/PATCH Request

```javascript
// Update existing block
async function updateBlock(blockId, updates) {
    try {
        const response = await fetch(`/api/blocks/${blockId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(updates)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update block');
        }
        
        const data = await response.json();
        showSuccess('Block updated successfully!');
        return data;
    } catch (error) {
        console.error('Error updating block:', error);
        showError('Failed to update block');
        throw error;
    }
}
```

### DELETE Request

```javascript
// Delete block
async function deleteBlock(blockId) {
    if (!confirm('Are you sure you want to delete this block?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/blocks/${blockId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken,
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete block');
        }
        
        showSuccess('Block deleted successfully!');
        window.location.href = '/blocks/';
    } catch (error) {
        console.error('Error deleting block:', error);
        showError('Failed to delete block');
    }
}
```

## Form Handling

### Form Submission with AJAX

```javascript
// Handle form submission
document.getElementById('block-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch(this.action, {
            method: this.method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errors = await response.json();
            displayFormErrors(errors);
            return;
        }
        
        const result = await response.json();
        showSuccess('Form submitted successfully!');
        window.location.href = result.redirect_url;
    } catch (error) {
        console.error('Error submitting form:', error);
        showError('Failed to submit form');
    }
});

// Display form errors
function displayFormErrors(errors) {
    // Clear previous errors
    document.querySelectorAll('.invalid-feedback').forEach(el => {
        el.textContent = '';
    });
    document.querySelectorAll('.is-invalid').forEach(el => {
        el.classList.remove('is-invalid');
    });
    
    // Display new errors
    for (const [field, messages] of Object.entries(errors)) {
        const input = document.querySelector(`[name="${field}"]`);
        if (input) {
            input.classList.add('is-invalid');
            const feedback = input.nextElementSibling;
            if (feedback && feedback.classList.contains('invalid-feedback')) {
                feedback.textContent = messages[0];
            }
        }
    }
}
```

### Form Validation

```javascript
// Client-side validation
function validateBlockForm(formData) {
    const errors = {};
    
    if (!formData.name || formData.name.trim() === '') {
        errors.name = 'Name is required';
    }
    
    if (!formData.mass || parseFloat(formData.mass) <= 0) {
        errors.mass = 'Mass must be greater than 0';
    }
    
    if (!formData.pcu || parseInt(formData.pcu) < 0) {
        errors.pcu = 'PCU cannot be negative';
    }
    
    return errors;
}

// Use validation
document.getElementById('block-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
    const errors = validateBlockForm(data);
    
    if (Object.keys(errors).length > 0) {
        displayFormErrors(errors);
        return;
    }
    
    // Submit form
    submitForm(data);
});
```

## Search and Autocomplete

### Live Search

```javascript
// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Live search implementation
const searchInput = document.getElementById('search');
const searchResults = document.getElementById('search-results');

const performSearch = debounce(async function(query) {
    if (query.length < 2) {
        searchResults.innerHTML = '';
        return;
    }
    
    try {
        const blocks = await fetchBlocks(query);
        displaySearchResults(blocks);
    } catch (error) {
        console.error('Search error:', error);
    }
}, 300);

searchInput.addEventListener('input', function(e) {
    performSearch(e.target.value);
});

function displaySearchResults(blocks) {
    if (blocks.length === 0) {
        searchResults.innerHTML = '<p class="text-muted">No results found</p>';
        return;
    }
    
    const html = blocks.map(block => `
        <a href="/blocks/${block.id}/" class="list-group-item list-group-item-action">
            <div class="d-flex w-100 justify-content-between">
                <h6 class="mb-1">${escapeHtml(block.name)}</h6>
                <small>${block.mass} kg</small>
            </div>
        </a>
    `).join('');
    
    searchResults.innerHTML = html;
}
```

### Autocomplete

```javascript
// Simple autocomplete
class Autocomplete {
    constructor(input, options) {
        this.input = input;
        this.options = options;
        this.currentFocus = -1;
        
        this.input.addEventListener('input', this.onInput.bind(this));
        this.input.addEventListener('keydown', this.onKeyDown.bind(this));
    }
    
    onInput(e) {
        const value = e.target.value;
        this.closeAllLists();
        
        if (!value) return;
        
        const matches = this.options.filter(option => 
            option.toLowerCase().includes(value.toLowerCase())
        );
        
        this.showSuggestions(matches);
    }
    
    showSuggestions(matches) {
        const list = document.createElement('div');
        list.className = 'autocomplete-items list-group';
        
        matches.forEach((match, index) => {
            const item = document.createElement('a');
            item.className = 'list-group-item list-group-item-action';
            item.textContent = match;
            item.addEventListener('click', () => {
                this.input.value = match;
                this.closeAllLists();
            });
            list.appendChild(item);
        });
        
        this.input.parentNode.appendChild(list);
    }
    
    closeAllLists() {
        const items = document.querySelectorAll('.autocomplete-items');
        items.forEach(item => item.remove());
    }
    
    onKeyDown(e) {
        const items = document.querySelectorAll('.autocomplete-items a');
        
        if (e.keyCode === 40) { // Down arrow
            this.currentFocus++;
            this.addActive(items);
        } else if (e.keyCode === 38) { // Up arrow
            this.currentFocus--;
            this.addActive(items);
        } else if (e.keyCode === 13) { // Enter
            e.preventDefault();
            if (this.currentFocus > -1 && items[this.currentFocus]) {
                items[this.currentFocus].click();
            }
        }
    }
    
    addActive(items) {
        if (!items) return;
        this.removeActive(items);
        
        if (this.currentFocus >= items.length) this.currentFocus = 0;
        if (this.currentFocus < 0) this.currentFocus = items.length - 1;
        
        items[this.currentFocus].classList.add('active');
    }
    
    removeActive(items) {
        items.forEach(item => item.classList.remove('active'));
    }
}

// Usage
const blockNames = ['Light Armor', 'Heavy Armor', 'Reactor', 'Thruster'];
new Autocomplete(document.getElementById('block-search'), blockNames);
```

## Bootstrap 5 JavaScript

### Modals

```javascript
// Show modal
const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
modal.show();

// Hide modal
modal.hide();

// Modal events
const modalElement = document.getElementById('deleteModal');
modalElement.addEventListener('show.bs.modal', function(e) {
    console.log('Modal is about to be shown');
});

modalElement.addEventListener('shown.bs.modal', function(e) {
    console.log('Modal is now visible');
});

// Confirm delete with modal
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const blockId = this.dataset.blockId;
        const blockName = this.dataset.blockName;
        
        document.getElementById('delete-block-name').textContent = blockName;
        document.getElementById('confirm-delete-btn').onclick = function() {
            deleteBlock(blockId);
        };
        
        const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
        modal.show();
    });
});
```

### Toasts

```javascript
// Show toast notification
function showToast(message, type = 'info') {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">${escapeHtml(message)}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                        data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const container = document.getElementById('toast-container');
    container.insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = container.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Usage
showToast('Block created successfully!', 'success');
showToast('Failed to delete block', 'danger');
```

### Tooltips and Popovers

```javascript
// Initialize tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(el => new bootstrap.Tooltip(el));

// Initialize popovers
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
const popoverList = [...popoverTriggerList].map(el => new bootstrap.Popover(el));
```

## Utility Functions

### DOM Manipulation

```javascript
// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show/hide elements
function show(element) {
    element.classList.remove('d-none');
}

function hide(element) {
    element.classList.add('d-none');
}

// Toggle element
function toggle(element) {
    element.classList.toggle('d-none');
}
```

### Notifications

```javascript
// Show success message
function showSuccess(message) {
    showToast(message, 'success');
}

// Show error message
function showError(message) {
    showToast(message, 'danger');
}

// Show info message
function showInfo(message) {
    showToast(message, 'info');
}
```

### Loading States

```javascript
// Show loading spinner
function showLoading(button) {
    button.disabled = true;
    button.dataset.originalText = button.innerHTML;
    button.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status"></span>
        Loading...
    `;
}

// Hide loading spinner
function hideLoading(button) {
    button.disabled = false;
    button.innerHTML = button.dataset.originalText;
}

// Usage
const submitBtn = document.getElementById('submit-btn');
showLoading(submitBtn);

// After operation completes
hideLoading(submitBtn);
```

## Event Handling

### Event Delegation

```javascript
// Handle clicks on dynamically added elements
document.getElementById('block-list').addEventListener('click', function(e) {
    // Delete button
    if (e.target.matches('.delete-btn')) {
        const blockId = e.target.dataset.blockId;
        deleteBlock(blockId);
    }
    
    // Edit button
    if (e.target.matches('.edit-btn')) {
        const blockId = e.target.dataset.blockId;
        window.location.href = `/blocks/${blockId}/edit/`;
    }
});
```

### Custom Events

```javascript
// Dispatch custom event
function notifyBlockCreated(block) {
    const event = new CustomEvent('blockCreated', {
        detail: { block: block }
    });
    document.dispatchEvent(event);
}

// Listen for custom event
document.addEventListener('blockCreated', function(e) {
    console.log('Block created:', e.detail.block);
    updateBlockList();
});
```

## JavaScript Checklist

### Security
- [ ] Use CSRF token for AJAX requests
- [ ] Escape user input before displaying
- [ ] Validate data on client and server
- [ ] Use HTTPS for API calls
- [ ] Don't expose sensitive data in JavaScript

### Performance
- [ ] Debounce search inputs
- [ ] Use event delegation
- [ ] Minimize DOM manipulation
- [ ] Cache DOM queries
- [ ] Load scripts at end of body

### Best Practices
- [ ] Use async/await for promises
- [ ] Handle errors gracefully
- [ ] Provide user feedback
- [ ] Show loading states
- [ ] Use semantic variable names

### Accessibility
- [ ] Manage focus for modals
- [ ] Announce dynamic content changes
- [ ] Support keyboard navigation
- [ ] Provide ARIA labels
- [ ] Test with screen readers
