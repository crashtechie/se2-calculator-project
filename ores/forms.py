"""
Forms for the Ores app.
Provides form handling and validation for Ore model CRUD operations.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Ore


class OreForm(forms.ModelForm):
    """
    Form for creating and updating Ore instances.
    
    Provides enhanced form rendering with Bootstrap classes and
    custom validation for ore data.
    """
    
    class Meta:
        model = Ore
        fields = ['name', 'description', 'mass']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ore name (e.g., Iron Ore)',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter detailed description of the ore',
                'rows': 4,
            }),
            'mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mass in kilograms',
                'step': '0.01',
                'min': '0.01',
                'required': True,
            }),
        }
        labels = {
            'name': 'Ore Name',
            'description': 'Description',
            'mass': 'Mass (kg)',
        }
        help_texts = {
            'name': 'Unique identifier for the ore (e.g., "Iron Ore", "Gold Ore")',
            'description': 'Detailed description including ore properties and uses',
            'mass': 'Mass per unit in kilograms. Must be greater than 0.',
        }
    
    def clean_name(self):
        """
        Validate that the ore name is not empty and properly formatted.
        """
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError('Ore name is required.')
        
        # Strip whitespace
        name = name.strip()
        
        if len(name) < 2:
            raise ValidationError('Ore name must be at least 2 characters long.')
        
        # Check for duplicate names (case-insensitive) excluding current instance
        queryset = Ore.objects.filter(name__iexact=name)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise ValidationError(f'An ore with the name "{name}" already exists.')
        
        return name
    
    def clean_mass(self):
        """
        Validate that mass is positive and within reasonable bounds.
        """
        mass = self.cleaned_data.get('mass')
        
        if mass is None:
            raise ValidationError('Mass is required.')
        
        if mass <= 0:
            raise ValidationError('Mass must be greater than 0.')
        
        if mass > 1000000:
            raise ValidationError('Mass seems unreasonably high. Please verify.')
        
        return mass
    
    def clean_description(self):
        """
        Clean and validate description field.
        """
        description = self.cleaned_data.get('description', '')
        
        # Strip whitespace
        description = description.strip()
        
        return description