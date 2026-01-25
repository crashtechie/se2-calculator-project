"""
Forms for Components app.

Handles JSONField materials with custom form processing:
- Converts between form data (ore_id[], quantity[]) and JSON storage
- Validates ore UUIDs against database
- Validates quantities (positive numbers)
- Reuses Phase 1 Component.validate_materials() helper
"""
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Component
from ores.models import Ore
import uuid


class ComponentForm(forms.ModelForm):
    """
    Form for creating/updating Components with dynamic material selection.
    
    Materials are handled as separate form fields (ore_id[], quantity[])
    and converted to JSONField format on save.
    """
    
    class Meta:
        model = Component
        fields = ['name', 'description', 'mass', 'crafting_time']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter component name (e.g., "Steel Beam")',
                'maxlength': 100,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the component and its uses...',
                'rows': 4,
                'maxlength': 500,
            }),
            'mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mass in kg (e.g., 25.5)',
                'step': '0.01',
                'min': '0.01',
            }),
            'crafting_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter crafting time in seconds (e.g., 120)',
                'step': '0.1',
                'min': '0',
            }),
        }
        help_texts = {
            'name': 'Unique name for the component (max 100 characters)',
            'description': 'Detailed description of the component (max 500 characters)',
            'mass': 'Component mass in kilograms (must be positive)',
            'crafting_time': 'Time to craft in seconds (0 or positive)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add required field indicators
        for field_name in ['name', 'mass', 'crafting_time']:
            self.fields[field_name].required = True
        
        # Make description optional
        self.fields['description'].required = False
        
        # If updating existing component, prepare materials for form
        if self.instance.pk and self.instance.materials:
            # Materials will be handled by JavaScript using hidden input
            # But we store them in form for validation
            self.initial_materials = self.instance.materials
        else:
            self.initial_materials = {}
    
    def clean_name(self):
        """Validate component name is unique."""
        name = self.cleaned_data.get('name', '').strip()
        
        if not name:
            raise ValidationError("Component name cannot be empty.")
        
        # Check for duplicate names (excluding current instance if updating)
        query = Component.objects.filter(name__iexact=name)
        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        
        if query.exists():
            raise ValidationError(f"A component with name '{name}' already exists.")
        
        return name
    
    def clean_mass(self):
        """Validate mass is positive."""
        mass = self.cleaned_data.get('mass')
        
        if mass is None:
            raise ValidationError("Mass is required.")
        
        if mass <= 0:
            raise ValidationError("Mass must be greater than 0.")
        
        return mass
    
    def clean_crafting_time(self):
        """Validate crafting_time is non-negative."""
        crafting_time = self.cleaned_data.get('crafting_time')
        
        if crafting_time is None:
            raise ValidationError("Crafting time is required.")
        
        if crafting_time < 0:
            raise ValidationError("Crafting time cannot be negative.")
        
        return crafting_time
    
    def clean_materials(self):
        """
        Validate materials JSONField structure and content.
        
        This method is called by JavaScript-submitted data or direct JSON input.
        Expected format: {"ore_uuid": quantity, "ore_uuid": quantity, ...}
        """
        # Get materials from POST data (set by JavaScript)
        materials_json = self.data.get('materials_json', '{}')
        
        if not materials_json or materials_json == '{}':
            raise ValidationError("At least one material is required.")
        
        # Parse JSON
        try:
            import json
            materials = json.loads(materials_json)
        except (json.JSONDecodeError, TypeError) as e:
            raise ValidationError(f"Invalid materials format: {e}")
        
        if not isinstance(materials, dict):
            raise ValidationError("Materials must be a dictionary of ore_id: quantity pairs.")
        
        if not materials:
            raise ValidationError("At least one material is required.")
        
        # Validate each material entry
        validated_materials = {}
        ore_cache = {}  # Cache ore lookups
        
        for ore_id_str, quantity in materials.items():
            # Validate UUID format
            try:
                ore_id = uuid.UUID(ore_id_str)
            except (ValueError, AttributeError) as e:
                raise ValidationError(f"Invalid ore UUID: {ore_id_str}")
            
            # Validate ore exists in database
            if ore_id_str not in ore_cache:
                try:
                    ore = Ore.objects.get(ore_id=ore_id)
                    ore_cache[ore_id_str] = ore
                except Ore.DoesNotExist:
                    raise ValidationError(f"Ore with UUID {ore_id_str} does not exist.")
            
            # Validate quantity
            try:
                quantity_float = float(quantity)
            except (ValueError, TypeError):
                raise ValidationError(f"Invalid quantity for ore {ore_id_str}: {quantity}")
            
            if quantity_float <= 0:
                raise ValidationError(f"Quantity for ore {ore_id_str} must be positive (got {quantity_float}).")
            
            # Store validated material
            validated_materials[str(ore_id)] = quantity_float
        
        # Use Phase 1 validation helper
        # Create temporary component instance for validation
        temp_component = Component(
            name=self.cleaned_data.get('name', 'temp'),
            mass=self.cleaned_data.get('mass', 1.0),
            crafting_time=self.cleaned_data.get('crafting_time', 0),
            materials=validated_materials
        )
        
        is_valid, validation_errors = temp_component.validate_materials()
        if not is_valid:
            raise ValidationError(validation_errors)
        
        return validated_materials
    
    def clean(self):
        """Cross-field validation."""
        cleaned_data = super().clean()
        
        # Ensure materials are validated
        materials_json = self.data.get('materials_json', '{}')
        
        try:
            import json
            materials = json.loads(materials_json)
            cleaned_data['materials'] = materials
            
            # Run material validation
            self.clean_materials()
        except ValidationError as e:
            self.add_error('materials', e)
        
        return cleaned_data
    
    def save(self, commit=True):
        """Save component with materials from form data."""
        component = super().save(commit=False)
        
        # Get materials from cleaned data
        materials_json = self.data.get('materials_json', '{}')
        
        try:
            import json
            component.materials = json.loads(materials_json)
        except (json.JSONDecodeError, TypeError):
            component.materials = {}
        
        if commit:
            component.save()
        
        return component
