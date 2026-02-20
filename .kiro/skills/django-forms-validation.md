# Django Forms & Validation

## When to Activate This Skill

- Creating or modifying Django forms
- Implementing complex validation logic
- Working with formsets or inline formsets
- Building dynamic forms
- Handling file uploads
- Creating custom form widgets
- Implementing multi-step forms

## Form Basics

### ModelForm Pattern
```python
from django import forms
from .models import Block

class BlockForm(forms.ModelForm):
    """Form for creating/editing blocks"""
    
    class Meta:
        model = Block
        fields = ['name', 'description', 'component', 'input_mass', 'output_mass']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'component': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'input_mass': 'Input Mass (kg)',
            'output_mass': 'Output Mass (kg)',
        }
        help_texts = {
            'name': 'Enter a unique name for this block',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
```

### Regular Form
```python
class ResourceCalculatorForm(forms.Form):
    """Non-model form for calculations"""
    block = forms.ModelChoiceField(
        queryset=Block.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10000,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    include_subcomponents = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
```

## Field Validation

### Built-in Validators
```python
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class ComponentForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s\-]+$',
                message='Name can only contain letters, numbers, spaces, and hyphens'
            )
        ]
    )
    mass = forms.DecimalField(
        validators=[MinValueValidator(0.01), MaxValueValidator(1000000)]
    )
```

### Custom Field Validation
```python
class BlockForm(forms.ModelForm):
    def clean_name(self):
        """Validate single field"""
        name = self.cleaned_data['name']
        
        # Check for reserved words
        if name.lower() in ['admin', 'system', 'root']:
            raise forms.ValidationError('This name is reserved')
        
        # Check uniqueness (excluding current instance)
        qs = Block.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('A block with this name already exists')
        
        return name.strip()
    
    def clean_input_mass(self):
        """Validate and transform data"""
        mass = self.cleaned_data['input_mass']
        if mass <= 0:
            raise forms.ValidationError('Mass must be positive')
        return round(mass, 2)  # Round to 2 decimal places
```

### Cross-Field Validation
```python
class BlockForm(forms.ModelForm):
    def clean(self):
        """Validate multiple fields together"""
        cleaned_data = super().clean()
        input_mass = cleaned_data.get('input_mass')
        output_mass = cleaned_data.get('output_mass')
        
        if input_mass and output_mass:
            if input_mass < output_mass:
                raise forms.ValidationError({
                    'output_mass': 'Output mass cannot exceed input mass'
                })
            
            # Calculate efficiency
            efficiency = (output_mass / input_mass) * 100
            if efficiency < 50:
                self.add_error(
                    None,  # Non-field error
                    f'Warning: Low efficiency ({efficiency:.1f}%)'
                )
        
        return cleaned_data
```

## Dynamic Forms

### Conditional Fields
```python
class BuildOrderForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter choices based on user
        if user and not user.is_staff:
            self.fields['block'].queryset = Block.objects.filter(is_public=True)
        
        # Make field required conditionally
        if self.instance.pk and self.instance.status == 'completed':
            self.fields['completion_notes'].required = True
        
        # Add dynamic field
        if user and user.has_perm('buildorders.can_expedite'):
            self.fields['priority'] = forms.ChoiceField(
                choices=[('normal', 'Normal'), ('high', 'High'), ('urgent', 'Urgent')]
            )
```

### Dynamic Field Generation
```python
class MaterialSelectionForm(forms.Form):
    def __init__(self, *args, component=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if component:
            # Generate fields for each material
            for material in component.materials.all():
                field_name = f'material_{material.id}'
                self.fields[field_name] = forms.IntegerField(
                    label=material.name,
                    min_value=0,
                    initial=material.default_quantity,
                    widget=forms.NumberInput(attrs={'class': 'form-control'})
                )
```

## Formsets

### Basic Formset
```python
from django.forms import formset_factory

# Create formset from form
MaterialFormSet = formset_factory(
    MaterialForm,
    extra=3,  # Number of empty forms
    max_num=10,  # Maximum total forms
    validate_max=True,
    can_delete=True
)

# In view
def manage_materials(request):
    if request.method == 'POST':
        formset = MaterialFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    material = form.save()
    else:
        formset = MaterialFormSet()
    
    return render(request, 'materials.html', {'formset': formset})
```

### Model Formset
```python
from django.forms import modelformset_factory

ComponentFormSet = modelformset_factory(
    Component,
    fields=['name', 'mass', 'volume'],
    extra=1,
    can_delete=True
)

# In view
def edit_components(request, block_id):
    block = get_object_or_404(Block, pk=block_id)
    queryset = Component.objects.filter(block=block)
    
    if request.method == 'POST':
        formset = ComponentFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return redirect('block_detail', pk=block_id)
    else:
        formset = ComponentFormSet(queryset=queryset)
    
    return render(request, 'components.html', {'formset': formset, 'block': block})
```

### Inline Formset
```python
from django.forms import inlineformset_factory

# Create formset for related objects
MaterialInlineFormSet = inlineformset_factory(
    Component,  # Parent model
    Material,   # Child model
    fields=['name', 'quantity', 'unit'],
    extra=2,
    can_delete=True,
    min_num=1,  # Minimum required forms
    validate_min=True
)

# In view
def edit_component_with_materials(request, pk):
    component = get_object_or_404(Component, pk=pk)
    
    if request.method == 'POST':
        form = ComponentForm(request.POST, instance=component)
        formset = MaterialInlineFormSet(request.POST, instance=component)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('component_detail', pk=pk)
    else:
        form = ComponentForm(instance=component)
        formset = MaterialInlineFormSet(instance=component)
    
    return render(request, 'component_form.html', {
        'form': form,
        'formset': formset
    })
```

### Formset Validation
```python
from django.forms import BaseFormSet

class BaseComponentFormSet(BaseFormSet):
    def clean(self):
        """Validate across all forms in formset"""
        if any(self.errors):
            return
        
        names = []
        total_mass = 0
        
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                name = form.cleaned_data.get('name')
                mass = form.cleaned_data.get('mass', 0)
                
                # Check for duplicate names
                if name in names:
                    raise forms.ValidationError(f'Duplicate component name: {name}')
                names.append(name)
                
                total_mass += mass
        
        # Validate total
        if total_mass > 10000:
            raise forms.ValidationError('Total mass exceeds maximum (10000 kg)')

# Use custom base class
ComponentFormSet = formset_factory(
    ComponentForm,
    formset=BaseComponentFormSet,
    extra=3
)
```

## Custom Widgets

### Custom Widget Class
```python
from django.forms import Widget
from django.utils.safestring import mark_safe

class ColorPickerWidget(Widget):
    """Custom color picker widget"""
    template_name = 'widgets/color_picker.html'
    
    def __init__(self, attrs=None):
        default_attrs = {'class': 'color-picker'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget"""
        context = self.get_context(name, value, attrs)
        return mark_safe(
            f'<input type="color" name="{name}" value="{value or "#000000"}" '
            f'class="{attrs.get("class", "")}">'
        )

class BlockForm(forms.ModelForm):
    color = forms.CharField(widget=ColorPickerWidget())
```

### Widget with JavaScript
```python
class AutocompleteWidget(forms.TextInput):
    """Widget with autocomplete functionality"""
    template_name = 'widgets/autocomplete.html'
    
    class Media:
        css = {
            'all': ('css/autocomplete.css',)
        }
        js = ('js/autocomplete.js',)
    
    def __init__(self, attrs=None, data_url=None):
        self.data_url = data_url
        super().__init__(attrs)
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['data_url'] = self.data_url
        return context
```

## File Upload Forms

### Single File Upload
```python
class DocumentUploadForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        help_text='Max file size: 10MB',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])
        ]
    )
    
    def clean_file(self):
        file = self.cleaned_data['file']
        
        # Validate file size (10MB)
        if file.size > 10 * 1024 * 1024:
            raise forms.ValidationError('File size cannot exceed 10MB')
        
        # Validate content type
        if file.content_type not in ['application/pdf', 'application/msword']:
            raise forms.ValidationError('Invalid file type')
        
        return file
```

### Multiple File Upload
```python
class MultipleFileUploadForm(forms.Form):
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    )
    
    def clean_files(self):
        files = self.files.getlist('files')
        
        if len(files) > 5:
            raise forms.ValidationError('Maximum 5 files allowed')
        
        for file in files:
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError(f'{file.name} exceeds 5MB limit')
        
        return files
```

### Image Upload with Validation
```python
from PIL import Image

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = BlockImage
        fields = ['image', 'caption']
    
    def clean_image(self):
        image = self.cleaned_data['image']
        
        try:
            # Open image to validate
            img = Image.open(image)
            
            # Validate dimensions
            if img.width > 4000 or img.height > 4000:
                raise forms.ValidationError('Image dimensions too large (max 4000x4000)')
            
            # Validate format
            if img.format not in ['JPEG', 'PNG', 'GIF']:
                raise forms.ValidationError('Invalid image format')
            
        except Exception as e:
            raise forms.ValidationError(f'Invalid image file: {str(e)}')
        
        return image
```

## Advanced Validation Patterns

### Async Validation (External API)
```python
import requests

class UsernameForm(forms.Form):
    username = forms.CharField(max_length=50)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        
        # Check external service
        try:
            response = requests.get(
                f'https://api.example.com/check-username/{username}',
                timeout=5
            )
            if response.json().get('exists'):
                raise forms.ValidationError('Username already taken')
        except requests.RequestException:
            # Handle API errors gracefully
            pass
        
        return username
```

### Conditional Validation
```python
class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=[('credit', 'Credit Card'), ('paypal', 'PayPal')]
    )
    card_number = forms.CharField(required=False)
    paypal_email = forms.EmailField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('payment_method')
        
        if method == 'credit':
            if not cleaned_data.get('card_number'):
                self.add_error('card_number', 'Card number is required')
        elif method == 'paypal':
            if not cleaned_data.get('paypal_email'):
                self.add_error('paypal_email', 'PayPal email is required')
        
        return cleaned_data
```


### Custom Validators
```python
from django.core.exceptions import ValidationError

def validate_positive_mass(value):
    """Reusable validator function"""
    if value <= 0:
        raise ValidationError('Mass must be positive')

def validate_json_structure(value):
    """Validate JSON field structure"""
    import json
    try:
        data = json.loads(value) if isinstance(value, str) else value
        if not isinstance(data, dict):
            raise ValidationError('Must be a JSON object')
        # Validate required keys
        required_keys = ['name', 'quantity']
        if not all(key in data for key in required_keys):
            raise ValidationError(f'Missing required keys: {required_keys}')
    except json.JSONDecodeError:
        raise ValidationError('Invalid JSON format')

class ComponentForm(forms.ModelForm):
    mass = forms.DecimalField(validators=[validate_positive_mass])
    metadata = forms.JSONField(validators=[validate_json_structure])
```

## Form Rendering

### Manual Rendering
```html
<!-- Template with manual field rendering -->
<form method="post">
    {% csrf_token %}
    
    <div class="mb-3">
        <label for="{{ form.name.id_for_label }}" class="form-label">
            {{ form.name.label }}
        </label>
        {{ form.name }}
        {% if form.name.errors %}
            <div class="invalid-feedback d-block">
                {{ form.name.errors }}
            </div>
        {% endif %}
        {% if form.name.help_text %}
            <small class="form-text text-muted">{{ form.name.help_text }}</small>
        {% endif %}
    </div>
    
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### Custom Template Tags
```python
# templatetags/form_tags.py
from django import template

register = template.Library()

@register.inclusion_tag('forms/field.html')
def render_field(field):
    """Render form field with Bootstrap styling"""
    return {'field': field}

@register.filter
def add_class(field, css_class):
    """Add CSS class to form field"""
    return field.as_widget(attrs={'class': css_class})
```

### Crispy Forms Integration
```python
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column

class BlockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Block Information',
                'name',
                'description',
                Row(
                    Column('input_mass', css_class='col-md-6'),
                    Column('output_mass', css_class='col-md-6'),
                )
            ),
            Fieldset(
                'Component Selection',
                'component',
            ),
            Submit('submit', 'Save Block', css_class='btn btn-primary')
        )
```

## Multi-Step Forms

### Session-Based Wizard
```python
from django.contrib.formtools.wizard.views import SessionWizardView

class BuildOrderWizard(SessionWizardView):
    """Multi-step form wizard"""
    template_name = 'buildorders/wizard.html'
    
    def get_form_kwargs(self, step):
        """Pass data between steps"""
        kwargs = super().get_form_kwargs(step)
        if step == 'materials':
            # Pass block from previous step
            block_data = self.get_cleaned_data_for_step('block')
            if block_data:
                kwargs['block'] = block_data['block']
        return kwargs
    
    def done(self, form_list, **kwargs):
        """Process all forms when wizard completes"""
        # Combine data from all steps
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        
        # Create build order
        build_order = BuildOrder.objects.create(**data)
        return redirect('buildorder_detail', pk=build_order.pk)

# urls.py
from .forms import BlockSelectionForm, MaterialSelectionForm, QuantityForm

urlpatterns = [
    path('create/', BuildOrderWizard.as_view([
        ('block', BlockSelectionForm),
        ('materials', MaterialSelectionForm),
        ('quantity', QuantityForm),
    ]), name='buildorder_create'),
]
```

## AJAX Form Handling

### AJAX Form Submission
```python
from django.http import JsonResponse

def ajax_form_view(request):
    """Handle AJAX form submission"""
    if request.method == 'POST':
        form = BlockForm(request.POST)
        if form.is_valid():
            block = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Block created successfully',
                'block_id': block.id,
                'block_name': block.name
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    
    form = BlockForm()
    return render(request, 'blocks/ajax_form.html', {'form': form})
```

### JavaScript Integration
```javascript
// AJAX form submission with fetch
document.getElementById('blockForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch('/blocks/create/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('success', data.message);
            window.location.href = `/blocks/${data.block_id}/`;
        } else {
            displayErrors(data.errors);
        }
    } catch (error) {
        showMessage('error', 'An error occurred');
    }
});
```

## Form Testing

### Basic Form Tests
```python
from django.test import TestCase

class BlockFormTest(TestCase):
    def test_form_with_valid_data(self):
        """Test form accepts valid data"""
        form = BlockForm(data={
            'name': 'Test Block',
            'description': 'Test description',
            'input_mass': 100,
            'output_mass': 90,
        })
        self.assertTrue(form.is_valid())
    
    def test_form_with_invalid_mass(self):
        """Test form rejects negative mass"""
        form = BlockForm(data={
            'name': 'Test Block',
            'input_mass': -10,
            'output_mass': 90,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('input_mass', form.errors)
    
    def test_cross_field_validation(self):
        """Test output mass cannot exceed input mass"""
        form = BlockForm(data={
            'name': 'Test Block',
            'input_mass': 50,
            'output_mass': 100,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('output_mass', form.errors)
```

### Formset Tests
```python
def test_formset_validation(self):
    """Test formset validates all forms"""
    formset_data = {
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '0',
        'form-0-name': 'Component 1',
        'form-0-mass': '10',
        'form-1-name': 'Component 1',  # Duplicate
        'form-1-mass': '20',
    }
    formset = ComponentFormSet(data=formset_data)
    self.assertFalse(formset.is_valid())
```

## Best Practices

### Form Organization
- Keep forms in dedicated `forms.py` files
- Use ModelForm when working with models
- Group related forms in classes or modules
- Reuse common validation logic

### Validation
- Validate at the field level when possible
- Use `clean()` for cross-field validation
- Provide clear, user-friendly error messages
- Validate on both client and server side
- Use Django's built-in validators

### Performance
- Use `select_related()` for ModelChoiceField querysets
- Limit queryset size for large datasets
- Cache expensive form initialization
- Use AJAX for dynamic field updates

### Security
- Always use CSRF protection
- Validate file uploads thoroughly
- Sanitize user input
- Use Django's form validation (don't bypass it)
- Be careful with `required=False` fields

### User Experience
- Provide helpful error messages
- Use placeholders and help text
- Add client-side validation for immediate feedback
- Show field-level errors near the field
- Preserve form data on validation errors

## Common Pitfalls

### Not Calling super()
```python
# Bad
def clean(self):
    # Missing super() call
    if self.cleaned_data['input_mass'] < 0:
        raise forms.ValidationError('Invalid mass')

# Good
def clean(self):
    cleaned_data = super().clean()
    if cleaned_data.get('input_mass', 0) < 0:
        raise forms.ValidationError('Invalid mass')
    return cleaned_data
```

### Modifying Queryset After Form Creation
```python
# Bad: Queryset evaluated before filtering
form = BlockForm()
form.fields['component'].queryset = Component.objects.filter(is_active=True)

# Good: Filter in __init__
class BlockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['component'].queryset = Component.objects.filter(is_active=True)
```

### Not Handling Missing Keys in cleaned_data
```python
# Bad: KeyError if field has errors
def clean(self):
    mass = self.cleaned_data['mass']  # May not exist

# Good: Use .get() with default
def clean(self):
    cleaned_data = super().clean()
    mass = cleaned_data.get('mass', 0)
```

## Resources

- [Django Forms Documentation](https://docs.djangoproject.com/en/stable/topics/forms/)
- [Django Form Validation](https://docs.djangoproject.com/en/stable/ref/forms/validation/)
- [Django Formsets](https://docs.djangoproject.com/en/stable/topics/forms/formsets/)
- [Crispy Forms](https://django-crispy-forms.readthedocs.io/)
