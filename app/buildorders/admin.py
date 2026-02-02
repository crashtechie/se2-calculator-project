from django.contrib import admin
from django.utils.html import mark_safe
import json
from .models import BuildOrder


@admin.register(BuildOrder)
class BuildOrderAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for BuildOrder model.
    """
    list_display = (
        'name',
        'blocks_count',
        'total_mass_display',
        'created_at',
        'updated_at'
    )
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = (
        'order_id',
        'created_at',
        'updated_at',
        'blocks_formatted',
        'calculation_summary_display',
        'validation_status'
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Blocks', {
            'fields': (
                'blocks',
                'blocks_formatted',
            ),
            'description': 'Define blocks as JSON object: {"block_id": quantity, ...}'
        }),
        ('Calculations', {
            'fields': ('calculation_summary_display',),
            'classes': ('collapse',)
        }),
        ('Validation', {
            'fields': ('validation_status',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('order_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def blocks_count(self, obj):
        """Display number of blocks in list view."""
        if not obj.blocks:
            return 0
        return len(obj.blocks)
    blocks_count.short_description = 'Blocks'
    
    def total_mass_display(self, obj):
        """Display total mass in list view."""
        try:
            total_mass = obj.calculate_total_mass()
            return f"{total_mass:,.2f} kg"
        except Exception as e:
            return mark_safe(f'<span style="color: red;">Error: {e}</span>')
    total_mass_display.short_description = 'Total Mass'
    
    def blocks_formatted(self, obj):
        """Display blocks as formatted JSON in detail view."""
        if not obj.blocks:
            return mark_safe('<em>No blocks</em>')
        
        formatted = json.dumps(obj.blocks, indent=2)
        return mark_safe(
            '<pre style="background-color: #f5f5f5; padding: 10px; '
            'border-radius: 5px; overflow-x: auto;">{}</pre>'.format(formatted)
        )
    blocks_formatted.short_description = 'Blocks (Formatted)'
    
    def calculation_summary_display(self, obj):
        """Display complete calculation summary."""
        try:
            summary = obj.get_calculation_summary()
            
            # Format total mass
            html = '<div style="font-family: monospace;">'
            html += '<h3>Total Mass</h3>'
            html += f'<p><strong>{summary["total_mass"]:,.2f} kg</strong></p>'
            
            # Format required components
            html += '<h3>Required Components</h3>'
            if summary['required_components']:
                html += '<table style="border-collapse: collapse; width: 100%;">'
                html += '<tr style="background-color: #f0f0f0;"><th style="padding: 5px; text-align: left;">Component ID</th><th style="padding: 5px; text-align: right;">Quantity</th></tr>'
                for comp_id, qty in sorted(summary['required_components'].items()):
                    html += f'<tr><td style="padding: 5px; border-top: 1px solid #ddd;">{comp_id}</td><td style="padding: 5px; border-top: 1px solid #ddd; text-align: right;">{qty}</td></tr>'
                html += '</table>'
            else:
                html += '<p><em>No components required</em></p>'
            
            # Format required ores
            html += '<h3>Required Ores</h3>'
            if summary['required_ores']:
                html += '<table style="border-collapse: collapse; width: 100%;">'
                html += '<tr style="background-color: #f0f0f0;"><th style="padding: 5px; text-align: left;">Ore Name</th><th style="padding: 5px; text-align: right;">Quantity</th></tr>'
                for ore_name, qty in sorted(summary['required_ores'].items()):
                    html += f'<tr><td style="padding: 5px; border-top: 1px solid #ddd;">{ore_name}</td><td style="padding: 5px; border-top: 1px solid #ddd; text-align: right;">{qty:,.2f}</td></tr>'
                html += '</table>'
            else:
                html += '<p><em>No ores required</em></p>'
            
            # Format fabricator times
            html += '<h3>Fabricator Times</h3>'
            if summary['fabricator_times']:
                html += '<table style="border-collapse: collapse; width: 100%;">'
                html += '<tr style="background-color: #f0f0f0;"><th style="padding: 5px; text-align: left;">Fabricator Type</th><th style="padding: 5px; text-align: right;">Time (seconds)</th></tr>'
                for fab_type, time in sorted(summary['fabricator_times'].items()):
                    html += f'<tr><td style="padding: 5px; border-top: 1px solid #ddd;">{fab_type}</td><td style="padding: 5px; border-top: 1px solid #ddd; text-align: right;">{time:,.2f}s</td></tr>'
                html += '</table>'
            else:
                html += '<p><em>No fabrication time</em></p>'
            
            html += '</div>'
            return mark_safe(html)
        except Exception as e:
            return mark_safe(f'<span style="color: red;">Error calculating summary: {e}</span>')
    calculation_summary_display.short_description = 'Calculation Summary'
    
    def validation_status(self, obj):
        """Display validation status."""
        errors = obj.validate_blocks()
        
        if not errors:
            return mark_safe(
                '<span style="color: green; font-weight: bold;">✓ Valid</span>'
            )
        else:
            error_text = '<br>'.join(['• ' + error for error in errors])
            return mark_safe(
                '<span style="color: red; font-weight: bold;">✗ Invalid</span><br>' +
                error_text
            )
    validation_status.short_description = 'Validation Status'
