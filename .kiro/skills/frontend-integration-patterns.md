# Frontend Integration Patterns

## When to Activate This Skill

- Building interactive Django templates
- Implementing AJAX functionality
- Integrating JavaScript with Django views
- Creating dynamic forms and UI updates
- Implementing progressive enhancement
- Working with HTMX or Alpine.js
- Building single-page-like experiences in Django

## Django Template JavaScript Integration

### Inline JavaScript with Template Variables
```html
<!-- Pass Django data to JavaScript -->
<script>
    const blockData = {
        id: {{ block.id }},
        name: "{{ block.name|escapejs }}",
        mass: {{ block.input_mass }},
        components: {{ block.components|safe }}
    };
    
    // Use the data
    console.log(`Block: ${blockData.name}`);
</script>
```

### JSON Script Tag Pattern
```html
<!-- Better: Use JSON script tag -->
{{ block_data|json_script:"block-data" }}

<script>
    const blockData = JSON.parse(
        document.getElementById('block-data').textContent
    );
</script>
```

### Data Attributes
```html
<!-- Pass data via data attributes -->
<div id="block-calculator"
     data-block-id="{{ block.id }}"
     data-block-name="{{ block.name }}"
     data-input-mass="{{ block.input_mass }}">
</div>

<script>
    const calculator = document.getElementById('block-calculator');
    const blockId = calculator.dataset.blockId;
    const blockName = calculator.dataset.blockName;
</script>
```

## AJAX Patterns

### Fetch API with Django
```javascript
// GET request
async function fetchBlockDetails(blockId) {
    try {
        const response = await fetch(`/api/blocks/${blockId}/`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        displayBlockDetails(data);
    } catch (error) {
        console.error('Error fetching block:', error);
        showError('Failed to load block details');
    }
}

// POST request with CSRF token
async function createBlock(formData) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    try {
        const response = await fetch('/api/blocks/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to create block');
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error creating block:', error);
        throw error;
    }
}
```

### Form Submission with AJAX
```javascript
document.getElementById('blockForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitButton = form.querySelector('[type="submit"]');
    
    // Disable submit button
    submitButton.disabled = true;
    submitButton.textContent = 'Saving...';
    
    try {
        const response = await fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccess(data.message);
            // Optionally redirect or update UI
            window.location.href = data.redirect_url;
        } else {
            displayFormErrors(data.errors);
        }
    } catch (error) {
        showError('An error occurred. Please try again.');
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Save';
    }
});

function displayFormErrors(errors) {
    // Clear previous errors
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    
    // Display new errors
    for (const [field, messages] of Object.entries(errors)) {
        const fieldElement = document.querySelector(`[name="${field}"]`);
        if (fieldElement) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-danger';
            errorDiv.textContent = messages.join(', ');
            fieldElement.parentNode.appendChild(errorDiv);
        }
    }
}
```

### Django View for AJAX
```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def create_block_ajax(request):
    """Handle AJAX block creation"""
    form = BlockForm(request.POST)
    
    if form.is_valid():
        block = form.save()
        return JsonResponse({
            'success': True,
            'message': 'Block created successfully',
            'block': {
                'id': block.id,
                'name': block.name,
                'url': block.get_absolute_url()
            },
            'redirect_url': reverse('block_detail', args=[block.id])
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)
```

## HTMX Integration

### Basic HTMX Patterns
```html
<!-- Load content on click -->
<button hx-get="/blocks/{{ block.id }}/details/"
        hx-target="#block-details"
        hx-swap="innerHTML">
    Load Details
</button>

<div id="block-details"></div>

<!-- Form submission with HTMX -->
<form hx-post="/blocks/create/"
      hx-target="#block-list"
      hx-swap="beforeend">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create Block</button>
</form>

<!-- Auto-refresh content -->
<div hx-get="/blocks/stats/"
     hx-trigger="every 5s"
     hx-swap="innerHTML">
    Loading stats...
</div>
```

### Django Views for HTMX
```python
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

def block_list(request):
    """Return full page or partial based on HTMX"""
    blocks = Block.objects.all()
    
    if request.headers.get('HX-Request'):
        # Return partial template for HTMX
        return render(request, 'blocks/_block_list_partial.html', {
            'blocks': blocks
        })
    else:
        # Return full page
        return render(request, 'blocks/block_list.html', {
            'blocks': blocks
        })

@require_http_methods(["DELETE"])
def delete_block_htmx(request, pk):
    """Delete block and return updated list"""
    block = get_object_or_404(Block, pk=pk)
    block.delete()
    
    # Return empty response with HX-Trigger header
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'blockDeleted'
    return response
```

### HTMX with Django Messages
```python
from django.contrib import messages

def create_block_htmx(request):
    """Create block with HTMX and show message"""
    if request.method == 'POST':
        form = BlockForm(request.POST)
        if form.is_valid():
            block = form.save()
            messages.success(request, f'Block "{block.name}" created successfully')
            
            # Return updated list with messages
            return render(request, 'blocks/_block_list_partial.html', {
                'blocks': Block.objects.all()
            })
    else:
        form = BlockForm()
    
    return render(request, 'blocks/_block_form_partial.html', {'form': form})
```

## Alpine.js Integration

### Basic Alpine.js with Django
```html
<!-- Counter example -->
<div x-data="{ count: 0 }">
    <button @click="count++">Increment</button>
    <span x-text="count"></span>
</div>

<!-- Toggle visibility -->
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle Details</button>
    <div x-show="open" x-transition>
        <p>{{ block.description }}</p>
    </div>
</div>

<!-- Form validation -->
<form x-data="{ 
    quantity: 1,
    get isValid() { return this.quantity > 0 && this.quantity <= 1000; }
}">
    <input type="number" 
           x-model="quantity"
           min="1" 
           max="1000">
    <button type="submit" 
            :disabled="!isValid">
        Calculate
    </button>
    <span x-show="!isValid" class="text-danger">
        Quantity must be between 1 and 1000
    </span>
</form>
```

### Alpine.js with AJAX
```html
<div x-data="blockCalculator()">
    <select x-model="selectedBlockId" @change="loadBlock()">
        <option value="">Select a block</option>
        {% for block in blocks %}
        <option value="{{ block.id }}">{{ block.name }}</option>
        {% endfor %}
    </select>
    
    <input type="number" 
           x-model="quantity" 
           @input="calculate()"
           placeholder="Quantity">
    
    <div x-show="loading">Loading...</div>
    
    <div x-show="result && !loading">
        <h3>Required Resources:</h3>
        <template x-for="(qty, resource) in result" :key="resource">
            <div>
                <span x-text="resource"></span>: 
                <span x-text="qty"></span>
            </div>
        </template>
    </div>
</div>

<script>
function blockCalculator() {
    return {
        selectedBlockId: '',
        quantity: 1,
        result: null,
        loading: false,
        
        async loadBlock() {
            if (!this.selectedBlockId) return;
            await this.calculate();
        },
        
        async calculate() {
            if (!this.selectedBlockId || this.quantity <= 0) return;
            
            this.loading = true;
            
            try {
                const response = await fetch(
                    `/api/blocks/${this.selectedBlockId}/calculate/`,
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCsrfToken()
                        },
                        body: JSON.stringify({ quantity: this.quantity })
                    }
                );
                
                const data = await response.json();
                this.result = data.resources;
            } catch (error) {
                console.error('Calculation failed:', error);
            } finally {
                this.loading = false;
            }
        }
    };
}

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
</script>
```

## Dynamic Form Updates

### Dependent Dropdowns
```html
<form id="blockForm">
    {% csrf_token %}
    
    <select name="category" id="categorySelect">
        <option value="">Select Category</option>
        {% for category in categories %}
        <option value="{{ category.id }}">{{ category.name }}</option>
        {% endfor %}
    </select>
    
    <select name="component" id="componentSelect" disabled>
        <option value="">Select Component</option>
    </select>
</form>

<script>
document.getElementById('categorySelect').addEventListener('change', async (e) => {
    const categoryId = e.target.value;
    const componentSelect = document.getElementById('componentSelect');
    
    if (!categoryId) {
        componentSelect.disabled = true;
        componentSelect.innerHTML = '<option value="">Select Component</option>';
        return;
    }
    
    try {
        const response = await fetch(`/api/components/?category=${categoryId}`);
        const components = await response.json();
        
        componentSelect.innerHTML = '<option value="">Select Component</option>' +
            components.map(c => 
                `<option value="${c.id}">${c.name}</option>`
            ).join('');
        
        componentSelect.disabled = false;
    } catch (error) {
        console.error('Failed to load components:', error);
    }
});
</script>
```

### Django View for Dynamic Options
```python
from django.http import JsonResponse

def get_components_by_category(request):
    """Return components filtered by category"""
    category_id = request.GET.get('category')
    
    if not category_id:
        return JsonResponse({'error': 'Category required'}, status=400)
    
    components = Component.objects.filter(
        category_id=category_id
    ).values('id', 'name', 'mass')
    
    return JsonResponse(list(components), safe=False)
```

### Live Search
```html
<input type="text" 
       id="blockSearch" 
       placeholder="Search blocks..."
       autocomplete="off">

<div id="searchResults"></div>

<script>
let searchTimeout;

document.getElementById('blockSearch').addEventListener('input', (e) => {
    const query = e.target.value;
    
    // Debounce search
    clearTimeout(searchTimeout);
    
    if (query.length < 2) {
        document.getElementById('searchResults').innerHTML = '';
        return;
    }
    
    searchTimeout = setTimeout(async () => {
        try {
            const response = await fetch(`/api/blocks/search/?q=${encodeURIComponent(query)}`);
            const results = await response.json();
            
            displaySearchResults(results);
        } catch (error) {
            console.error('Search failed:', error);
        }
    }, 300);
});

function displaySearchResults(results) {
    const container = document.getElementById('searchResults');
    
    if (results.length === 0) {
        container.innerHTML = '<p>No results found</p>';
        return;
    }
    
    container.innerHTML = results.map(block => `
        <div class="search-result">
            <a href="/blocks/${block.id}/">${block.name}</a>
            <span class="text-muted">${block.component_name}</span>
        </div>
    `).join('');
}
</script>
```


## Progressive Enhancement

### Basic Progressive Enhancement
```html
<!-- Works without JavaScript -->
<form method="post" action="/blocks/create/" id="blockForm">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create Block</button>
</form>

<script>
// Enhance with AJAX if JavaScript available
document.getElementById('blockForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Enhanced experience
            showSuccessMessage();
            updateUIWithoutReload();
        } else {
            // Fall back to normal form submission
            form.submit();
        }
    } catch (error) {
        // Fall back to normal form submission
        form.submit();
    }
});
</script>
```

### Feature Detection
```javascript
// Check for fetch support
if ('fetch' in window) {
    // Use fetch API
    enhanceWithAjax();
} else {
    // Fall back to traditional forms
    console.log('Fetch not supported, using traditional forms');
}

// Check for localStorage
if ('localStorage' in window) {
    // Save form data locally
    saveFormDataLocally();
}
```

## Real-time Updates

### WebSocket Integration
```python
# consumers.py (Django Channels)
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BlockUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'blocks_updates'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def block_update(self, event):
        """Send block update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'block_update',
            'block': event['block']
        }))
```

```javascript
// WebSocket client
const socket = new WebSocket('ws://localhost:8000/ws/blocks/');

socket.onopen = () => {
    console.log('WebSocket connected');
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'block_update') {
        updateBlockInUI(data.block);
    }
};

socket.onerror = (error) => {
    console.error('WebSocket error:', error);
};

socket.onclose = () => {
    console.log('WebSocket disconnected');
    // Attempt to reconnect
    setTimeout(connectWebSocket, 5000);
};
```

### Server-Sent Events (SSE)
```python
# views.py
from django.http import StreamingHttpResponse
import json
import time

def block_updates_stream(request):
    """Stream block updates using SSE"""
    def event_stream():
        while True:
            # Get latest updates
            updates = get_recent_block_updates()
            
            if updates:
                data = json.dumps(updates)
                yield f"data: {data}\n\n"
            
            time.sleep(5)  # Check every 5 seconds
    
    response = StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    return response
```

```javascript
// SSE client
const eventSource = new EventSource('/blocks/updates/stream/');

eventSource.onmessage = (event) => {
    const updates = JSON.parse(event.data);
    updates.forEach(update => {
        updateBlockInUI(update);
    });
};

eventSource.onerror = (error) => {
    console.error('SSE error:', error);
    eventSource.close();
};
```

## File Upload with Progress

### AJAX File Upload
```html
<form id="uploadForm" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="file" name="file" id="fileInput" required>
    <button type="submit">Upload</button>
    
    <div id="progressContainer" style="display: none;">
        <progress id="uploadProgress" value="0" max="100"></progress>
        <span id="progressText">0%</span>
    </div>
</form>

<script>
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('uploadProgress');
    const progressText = document.getElementById('progressText');
    
    progressContainer.style.display = 'block';
    
    try {
        const xhr = new XMLHttpRequest();
        
        // Track upload progress
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressBar.value = percentComplete;
                progressText.textContent = `${Math.round(percentComplete)}%`;
            }
        });
        
        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                showSuccess('File uploaded successfully');
            } else {
                showError('Upload failed');
            }
            progressContainer.style.display = 'none';
        });
        
        xhr.open('POST', form.action);
        xhr.setRequestHeader('X-CSRFToken', formData.get('csrfmiddlewaretoken'));
        xhr.send(formData);
        
    } catch (error) {
        console.error('Upload error:', error);
        showError('Upload failed');
        progressContainer.style.display = 'none';
    }
});
</script>
```

### Django View for File Upload
```python
from django.core.files.storage import default_storage
from django.http import JsonResponse

def upload_file(request):
    """Handle file upload with validation"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    uploaded_file = request.FILES.get('file')
    
    if not uploaded_file:
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    # Validate file size (10MB max)
    if uploaded_file.size > 10 * 1024 * 1024:
        return JsonResponse({'error': 'File too large'}, status=400)
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
    if uploaded_file.content_type not in allowed_types:
        return JsonResponse({'error': 'Invalid file type'}, status=400)
    
    # Save file
    filename = default_storage.save(
        f'uploads/{uploaded_file.name}',
        uploaded_file
    )
    
    return JsonResponse({
        'success': True,
        'filename': filename,
        'url': default_storage.url(filename)
    })
```

## Infinite Scroll

### Infinite Scroll Implementation
```html
<div id="blockList">
    {% for block in blocks %}
        {% include 'blocks/_block_item.html' %}
    {% endfor %}
</div>

<div id="loadingIndicator" style="display: none;">
    Loading more blocks...
</div>

<script>
let page = 1;
let loading = false;
let hasMore = true;

window.addEventListener('scroll', () => {
    if (loading || !hasMore) return;
    
    const scrollPosition = window.innerHeight + window.scrollY;
    const threshold = document.body.offsetHeight - 500;
    
    if (scrollPosition >= threshold) {
        loadMoreBlocks();
    }
});

async function loadMoreBlocks() {
    loading = true;
    document.getElementById('loadingIndicator').style.display = 'block';
    
    try {
        page++;
        const response = await fetch(`/api/blocks/?page=${page}`);
        const data = await response.json();
        
        if (data.results.length === 0) {
            hasMore = false;
            document.getElementById('loadingIndicator').textContent = 'No more blocks';
            return;
        }
        
        const blockList = document.getElementById('blockList');
        data.results.forEach(block => {
            const blockHtml = createBlockElement(block);
            blockList.insertAdjacentHTML('beforeend', blockHtml);
        });
        
    } catch (error) {
        console.error('Failed to load more blocks:', error);
    } finally {
        loading = false;
        document.getElementById('loadingIndicator').style.display = 'none';
    }
}

function createBlockElement(block) {
    return `
        <div class="block-item">
            <h3>${block.name}</h3>
            <p>${block.description}</p>
        </div>
    `;
}
</script>
```

## Modal Dialogs

### Dynamic Modal with AJAX
```html
<!-- Modal container -->
<div class="modal fade" id="blockModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="modalTitle">Loading...</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" id="modalBody">
                <div class="spinner-border" role="status"></div>
            </div>
        </div>
    </div>
</div>

<script>
async function openBlockModal(blockId) {
    const modal = new bootstrap.Modal(document.getElementById('blockModal'));
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    modal.show();
    
    try {
        const response = await fetch(`/blocks/${blockId}/modal/`);
        const html = await response.text();
        
        modalBody.innerHTML = html;
        modalTitle.textContent = 'Block Details';
        
        // Initialize form if present
        const form = modalBody.querySelector('form');
        if (form) {
            initializeModalForm(form, modal);
        }
        
    } catch (error) {
        modalBody.innerHTML = '<p class="text-danger">Failed to load content</p>';
    }
}

function initializeModalForm(form, modal) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                modal.hide();
                location.reload(); // Or update UI dynamically
            } else {
                const html = await response.text();
                document.getElementById('modalBody').innerHTML = html;
            }
        } catch (error) {
            console.error('Form submission failed:', error);
        }
    });
}
</script>
```

### Django View for Modal
```python
def block_modal(request, pk):
    """Return modal content"""
    block = get_object_or_404(Block, pk=pk)
    
    if request.method == 'POST':
        form = BlockForm(request.POST, instance=block)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = BlockForm(instance=block)
    
    return render(request, 'blocks/_modal_form.html', {
        'form': form,
        'block': block
    })
```

## Best Practices

### JavaScript Organization
- Keep JavaScript in separate files when possible
- Use modules for better organization
- Minimize inline JavaScript in templates
- Use event delegation for dynamic content
- Cache DOM queries

### AJAX Best Practices
- Always handle errors gracefully
- Provide loading indicators
- Implement request timeouts
- Use CSRF tokens for POST requests
- Validate responses before using data

### Performance
- Debounce frequent events (scroll, input)
- Use event delegation instead of multiple listeners
- Lazy load images and content
- Minimize DOM manipulations
- Cache AJAX responses when appropriate

### Accessibility
- Ensure keyboard navigation works
- Provide ARIA labels for dynamic content
- Announce dynamic updates to screen readers
- Don't break browser back button
- Maintain focus management

### Security
- Always validate on server side
- Sanitize user input
- Use CSRF protection
- Don't expose sensitive data in JavaScript
- Validate file uploads thoroughly

## Common Pitfalls

### Not Handling CSRF Tokens
```javascript
// Bad: Missing CSRF token
fetch('/api/blocks/', {
    method: 'POST',
    body: JSON.stringify(data)
});

// Good: Include CSRF token
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
fetch('/api/blocks/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrfToken
    },
    body: JSON.stringify(data)
});
```

### Memory Leaks with Event Listeners
```javascript
// Bad: Adding listeners without cleanup
function addBlock(block) {
    const element = createBlockElement(block);
    element.addEventListener('click', handleClick);
    container.appendChild(element);
}

// Good: Clean up when removing
function removeBlock(element) {
    element.removeEventListener('click', handleClick);
    element.remove();
}

// Better: Use event delegation
container.addEventListener('click', (e) => {
    if (e.target.matches('.block-item')) {
        handleClick(e);
    }
});
```

### Not Handling Errors
```javascript
// Bad: No error handling
fetch('/api/blocks/').then(r => r.json()).then(data => {
    displayBlocks(data);
});

// Good: Proper error handling
fetch('/api/blocks/')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        displayBlocks(data);
    })
    .catch(error => {
        console.error('Failed to load blocks:', error);
        showError('Failed to load blocks. Please try again.');
    });
```

## Testing Frontend Integration

### Testing AJAX Endpoints
```python
from django.test import TestCase, Client
import json

class AjaxViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_ajax_create_block(self):
        """Test AJAX block creation"""
        data = {
            'name': 'Test Block',
            'input_mass': 100,
            'output_mass': 90
        }
        
        response = self.client.post(
            '/api/blocks/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertIn('block', response_data)
```

### Testing with Selenium
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FrontendIntegrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def test_ajax_form_submission(self):
        """Test AJAX form submission"""
        self.driver.get(self.live_server_url + '/blocks/create/')
        
        # Fill form
        name_input = self.driver.find_element(By.NAME, 'name')
        name_input.send_keys('Test Block')
        
        # Submit form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
        submit_button.click()
        
        # Wait for success message
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        
        # Verify block was created
        self.assertTrue(Block.objects.filter(name='Test Block').exists())
```

## Resources

- [Django AJAX Documentation](https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-editing/)
- [HTMX Documentation](https://htmx.org/docs/)
- [Alpine.js Documentation](https://alpinejs.dev/)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Django Channels](https://channels.readthedocs.io/)
