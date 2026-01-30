"""
Forms for Blocks app.

Handles JSONField components with custom form processing:
- Converts between form data (component_id[], quantity[]) and JSON storage
- Validates component UUIDs against database
- Validates quantities (positive integers)
- Reuses Phase 1 Block.validate_components() helper

Pattern adapted from ENH-0000006 ComponentForm.
"""
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Block
from components.models import Component
import uuid
import json


class BlockForm(forms.ModelForm):
    """
    Form for creating/updating Blocks with dynamic component selection.
    
    Components are handled as separate form fields (component_id[], quantity[])
    and converted to JSONField format on save.
    """

    # Hidden field to carry JSON component payload from the client
    components_json = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Block
        fields = [
            'name', 'description', 'mass', 'health', 'pcu', 
            'snap_size', 'input_mass', 'output_mass',
            'consumer_type', 'consumer_rate', 
            'producer_type', 'producer_rate', 'storage_capacity'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter block name (e.g., "Light Armor Block")',
                'maxlength': 100,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the block and its uses...',
                'rows': 4,
                'maxlength': 500,
            }),
            'mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mass in kg (e.g., 250.5)',
                'step': '0.01',
                'min': '0.01',
            }),
            'health': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter health points (e.g., 100)',
                'step': '0.01',
                'min': '0.01',
            }),
            'pcu': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter PCU (e.g., 160)',
                'min': '1',
            }),
            'snap_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter snap size (e.g., 0.5)',
                'step': '0.01',
                'min': '0.01',
            }),
            'input_mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter input mass capacity in kg (optional - for production blocks)',
                'min': '0',
            }),
            'output_mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter output mass capacity in kg (optional - for production blocks)',
                'min': '0',
            }),
            'consumer_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Power, Hydrogen, Oxygen (optional)',
                'maxlength': 50,
            }),
            'consumer_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter consumption rate per second (e.g., 10.5)',
                'step': '0.01',
                'min': '0',
            }),
            'producer_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Power, Hydrogen, Oxygen (optional)',
                'maxlength': 50,
            }),
            'producer_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter production rate per second (e.g., 10.5)',
                'step': '0.01',
                'min': '0',
            }),
            'storage_capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter storage capacity in liters/units (e.g., 5000)',
                'step': '0.01',
                'min': '0',
            }),
        }
        help_texts = {
            'name': 'Unique name for the block (max 100 characters)',
            'description': 'Detailed description of the block',
            'mass': 'Total mass of the block in kilograms',
            'health': 'Block health/integrity points',
            'pcu': 'Performance Cost Units for this block',
            'snap_size': 'Grid snap size for placement',
            'input_mass': 'Input mass capacity in kg (optional - only for production blocks)',
            'output_mass': 'Output mass capacity in kg (optional - only for production blocks)',
            'consumer_type': 'Type of resource consumed (optional)',
            'consumer_rate': 'Consumption rate per second',
            'producer_type': 'Type of resource produced (optional)',
            'producer_rate': 'Production rate per second',
            'storage_capacity': 'Storage capacity in liters or units',
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form and prepare for component handling.
        
        If updating an existing block (instance provided), pre-populate
        the components_json field with existing component data.
        """
        super().__init__(*args, **kwargs)
        
        # Make input_mass and output_mass not required
        # These fields are only used by production blocks, not all blocks
        self.fields['input_mass'].required = False
        self.fields['output_mass'].required = False
        
        # Pre-populate components for update forms
        if self.instance and self.instance.pk and self.instance.components:
            # Convert components dict to JSON string for hidden field
            self.initial['components_json'] = json.dumps(self.instance.components)

    def clean_name(self):
        """
        Validate block name is unique.
        
        Raises:
            ValidationError: If name already exists (excluding current instance)
        """
        name = self.cleaned_data.get('name', '').strip()
        
        if not name:
            raise ValidationError('Block name is required.')
        
        # Check for duplicate names (case-insensitive)
        existing = Block.objects.filter(name__iexact=name)
        
        # Exclude current instance if updating
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise ValidationError(f'Block with name "{name}" already exists.')
        
        return name

    def clean_mass(self):
        """Validate mass is positive."""
        mass = self.cleaned_data.get('mass')
        
        if mass is not None and mass <= 0:
            raise ValidationError('Mass must be greater than 0.')
        
        return mass

    def clean_pcu(self):
        """Validate PCU is positive."""
        pcu = self.cleaned_data.get('pcu')
        
        if pcu is not None and pcu < 1:
            raise ValidationError('PCU must be at least 1.')
        
        return pcu

    def clean(self):
        """
        Cross-field validation and component processing.
        
        Converts components_json from client into proper JSONField format
        and validates using Block.validate_components() helper from Phase 1.
        
        Returns:
            dict: Cleaned form data with processed components
        
        Raises:
            ValidationError: If component validation fails
        """
        cleaned_data = super().clean()
        
        # Process components from JSON payload
        components_json = cleaned_data.get('components_json', '').strip()
        
        if not components_json or components_json == '{}':
            raise ValidationError({
                'components_json': 'At least one component is required.'
            })
        
        try:
            components_data = json.loads(components_json)
        except json.JSONDecodeError:
            raise ValidationError({
                'components_json': 'Invalid JSON format for components.'
            })
        
        # Validate components structure and UUIDs
        if not isinstance(components_data, dict):
            raise ValidationError({
                'components_json': 'Components must be a dictionary of {component_id: quantity}.'
            })
        
        # Convert and validate each component
        validated_components = {}
        
        for comp_id_str, quantity in components_data.items():
            # Validate UUID format
            try:
                comp_uuid = uuid.UUID(comp_id_str)
            except (ValueError, AttributeError):
                raise ValidationError({
                    'components_json': f'Invalid component UUID: {comp_id_str}'
                })
            
            # Validate quantity
            try:
                qty = int(quantity)
                if qty <= 0:
                    raise ValueError()
            except (ValueError, TypeError):
                raise ValidationError({
                    'components_json': f'Invalid quantity for component {comp_id_str}: {quantity}. Must be positive integer.'
                })
            
            # Verify component exists in database
            if not Component.objects.filter(component_id=comp_uuid).exists():
                raise ValidationError({
                    'components_json': f'Component {comp_id_str} does not exist in database.'
                })
            
            validated_components[str(comp_uuid)] = qty
        
        # Store validated components for save
        cleaned_data['components'] = validated_components
        
        # Use Phase 1 validation helper (create temporary instance)
        temp_block = Block(
            name=cleaned_data.get('name', 'temp'),
            mass=cleaned_data.get('mass', 1.0),
            components=validated_components
        )
        
        is_valid, validation_errors = temp_block.validate_components()
        
        if not is_valid:
            raise ValidationError({
                'components_json': f'Component validation failed: {", ".join(validation_errors)}'
            })
        
        return cleaned_data

    def save(self, commit=True):
        """
        Save block with validated components.
        
        Args:
            commit: Whether to save to database immediately
        
        Returns:
            Block: Saved block instance
        """
        instance = super().save(commit=False)
        
        # Set components from cleaned_data
        if 'components' in self.cleaned_data:
            instance.components = self.cleaned_data['components']
        
        if commit:
            instance.save()
        
        return instance
