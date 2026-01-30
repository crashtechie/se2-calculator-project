import json

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Component

# Register your models here.
@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'fabricator_type',
        'crafting_time',
        'mass',
        'materials_preview',
        'created_at',
    )
    search_fields = ('name', 'description', 'fabricator_type')
    list_filter = ('fabricator_type', 'created_at', 'updated_at')
    readonly_fields = (
        'component_id',
        'created_at',
        'updated_at',
        'materials_formatted',
        'material_ores',
        'validation_status',
    )
    
    fieldsets = (
       ('Basic Information', {
            'fields': ('name', 'description', 'fabricator_type')
        }),
        ('Materials & Production', {
            'fields': (
                'materials',
                'materials_formatted',
                'material_ores',
                'crafting_time',
                'mass'
            ),
            'description': 'Define materials as JSON: {"ore_id": quantity, ...}'
        }),
        ('Validation', {
            'fields': ('validation_status',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('component_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }), 
    )
    
    def materials_preview(self, obj):
        """Display materials as formatted JSON in list view."""
        if not obj.materials:
            return mark_safe('<em>No materials</em>')
        
        material_count = len(obj.materials)
        plural = 's' if material_count != 1 else ''
        return mark_safe(
            '<span title="{}">{} material{}</span>'.format(
                json.dumps(obj.materials),
                material_count,
                plural
            )
        )
    materials_preview.short_description = 'Materials'
    
    def materials_formatted(self, obj):
        """Display materials as formatted JSON in detail view."""
        if not obj.materials:
            return mark_safe('<em>No materials</em>')
        
        formatted = json.dumps(obj.materials, indent=2)
        return mark_safe(
            '<pre style="background-color: #f5f5f5; padding: 10px; '
            'border-radius: 5px; overflow-x: auto;">{}</pre>'.format(formatted)
        )
    materials_formatted.short_description = 'Materials (Formatted)'
    
    def material_ores(self, obj):
        """Display ore names referenced in materials."""
        if not obj.materials:
            return mark_safe('<em>No ores referenced</em>')
        
        ores = obj.get_material_ores()
        if not ores:
            return mark_safe('<em>No ores referenced</em>')
        
        ore_items = [
            '<strong>{}</strong>: {} units'.format(ore.name, obj.materials[str(ore.ore_id)])
            for ore in ores
        ]
        ore_list = '<br>'.join(ore_items)
        return mark_safe(ore_list)
    material_ores.short_description = 'Referenced Ores'
    
    def validation_status(self, obj):
        """Display validation status for materials."""
        is_valid, errors = obj.validate_materials()
        
        if is_valid:
            return mark_safe(
                '<span style="color: green; font-weight: bold;">✓ Valid</span>'
            )
        else:
            error_list = '<br>'.join(['• {}'.format(error) for error in errors])
            return mark_safe(
                '<span style="color: red; font-weight: bold;">✗ Invalid</span><br>{}'.format(error_list)
            )
    validation_status.short_description = 'Material Validation'