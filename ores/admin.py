from django.contrib import admin
from .models import Ore

# Register your models here.
@admin.register(Ore)
class OreAdmin(admin.ModelAdmin):
    list_display = ('name', 'mass', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('ore_id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'mass')
        }),
        ('System Information', {
            'fields': ('ore_id', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )