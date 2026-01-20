from django.contrib import admin
from django.utils.html import mark_safe
import json
from .models import Block


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Block model.
    """
    list_display = (
        'name',
        'health',
        'pcu',
        'mass',
        'components_preview',
        'consumer_info',
        'producer_info',
        'created_at'
    )
    search_fields = ('name', 'description', 'consumer_type', 'producer_type')
    list_filter = ('consumer_type', 'producer_type', 'created_at', 'updated_at')
    readonly_fields = (
        'block_id',
        'created_at',
        'updated_at',
        'components_formatted',
        'component_objects',
        'validation_status'
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'mass')
        }),
        ('Block Properties', {
            'fields': ('health', 'pcu', 'snap_size', 'input_mass', 'output_mass')
        }),
        ('Components & Production', {
            'fields': (
                'components',
                'components_formatted',
                'component_objects'
            ),
            'description': 'Define components as JSON array: [{"component_id": "uuid", "component_name": "name", "quantity": int}, ...]'
        }),
        ('Power & Resources', {
            'fields': (
                'consumer_type',
                'consumer_rate',
                'producer_type',
                'producer_rate',
                'storage_capacity'
            )
        }),
        ('Validation', {
            'fields': ('validation_status',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('block_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def components_preview(self, obj):
        """Display components count in list view."""
        if not obj.components:
            return mark_safe('<em>No components</em>')
        
        component_count = len(obj.components)
        plural = 's' if component_count != 1 else ''
        return mark_safe(
            '<span title=\"{}\">{} component{}</span>'.format(
                json.dumps(obj.components),
                component_count,
                plural
            )
        )
    components_preview.short_description = 'Components'
    
    def components_formatted(self, obj):
        """Display components as formatted JSON in detail view."""
        if not obj.components:
            return mark_safe('<em>No components</em>')
        
        formatted = json.dumps(obj.components, indent=2)
        return mark_safe(
            '<pre style="background-color: #f5f5f5; padding: 10px; '
            'border-radius: 5px; overflow-x: auto;">{}</pre>'.format(formatted)
        )
    components_formatted.short_description = 'Components (Formatted)'
    
    def component_objects(self, obj):
        """Display component names referenced in components."""
        components = obj.get_component_objects()
        if not components:
            return mark_safe('<em>No components referenced</em>')
        
        # Create lookup dict for quantities
        quantity_map = {item['component_id']: item['quantity'] for item in obj.components}
        
        component_list = '<br>'.join([
            '<strong>{}</strong>: {} units'.format(
                comp.name,
                quantity_map.get(str(comp.component_id), 0)
            )
            for comp in components
        ])
        return mark_safe(component_list)
    component_objects.short_description = 'Referenced Components'
    
    def consumer_info(self, obj):
        """Display consumer information."""
        if not obj.consumer_type:
            return mark_safe('<em>None</em>')
        return mark_safe(
            '<strong>{}</strong><br>{} /s'.format(
                obj.consumer_type,
                obj.consumer_rate
            )
        )
    consumer_info.short_description = 'Consumer'
    
    def producer_info(self, obj):
        """Display producer information."""
        if not obj.producer_type:
            return mark_safe('<em>None</em>')
        return mark_safe(
            '<strong>{}</strong><br>{} /s'.format(
                obj.producer_type,
                obj.producer_rate
            )
        )
    producer_info.short_description = 'Producer'
    
    def validation_status(self, obj):
        """Display validation status for all validations."""
        all_valid = True
        all_errors = []
        
        # Validate components
        is_valid, errors = obj.validate_components()
        if not is_valid:
            all_valid = False
            all_errors.extend(['Components: ' + e for e in errors])
        
        # Validate consumer
        is_valid, errors = obj.validate_consumer()
        if not is_valid:
            all_valid = False
            all_errors.extend(['Consumer: ' + e for e in errors])
        
        # Validate producer
        is_valid, errors = obj.validate_producer()
        if not is_valid:
            all_valid = False
            all_errors.extend(['Producer: ' + e for e in errors])
        
        if all_valid:
            return mark_safe(
                '<span style="color: green; font-weight: bold;">✓ Valid</span>'
            )
        else:
            error_text = '<br>'.join(['• ' + error for error in all_errors])
            return mark_safe(
                '<span style="color: red; font-weight: bold;">✗ Invalid</span><br>' +
                error_text
            )
    validation_status.short_description = 'Validation Status'