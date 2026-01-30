"""
Template filters for Blocks app.

Provides custom template filters for displaying block data,
particularly for converting component UUIDs to human-readable names
and calculating resource chains.

Pattern adapted from ENH-0000006 component_filters.py
"""
from django import template
from components.models import Component
from django.core.cache import cache
from django.core.exceptions import ValidationError
import logging

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def get_component_name(component_id):
    """
    Convert component UUID to component name for display in templates.
    
    Usage:
        {{ component_id|get_component_name }}
    
    Args:
        component_id: UUID string or UUID object
    
    Returns:
        Component name if found, otherwise "Unknown Component (uuid)"
    
    Caches component lookups to improve performance.
    """
    if not component_id:
        return "Unknown Component"
    
    # Convert to string if UUID object
    component_id_str = str(component_id)
    
    # Check cache first (5 minute TTL)
    cache_key = f'component_name_{component_id_str}'
    cached_name = cache.get(cache_key)
    
    if cached_name:
        return cached_name
    
    # Query database
    try:
        component = Component.objects.get(component_id=component_id_str)
        component_name = component.name
        
        # Cache for 5 minutes
        cache.set(cache_key, component_name, 300)
        
        logger.debug(f"Resolved component {component_id_str} to '{component_name}'")
        return component_name
        
    except Component.DoesNotExist:
        logger.warning(f"Component {component_id_str} not found in database")
        return f"Unknown Component"
    except (ValidationError, ValueError, TypeError) as e:
        logger.error(f"Error resolving component {component_id_str}: {e}")
        return f"Unknown Component"


@register.filter
def get_component_mass(component_id):
    """
    Get component mass for calculations.
    
    Usage:
        {{ component_id|get_component_mass }}
    
    Args:
        component_id: UUID string or UUID object
    
    Returns:
        float: Component mass in kg, or 0 if not found
    """
    if not component_id:
        return 0
    
    component_id_str = str(component_id)
    cache_key = f'component_mass_{component_id_str}'
    cached_mass = cache.get(cache_key)
    
    if cached_mass is not None:
        return cached_mass
    
    try:
        component = Component.objects.get(component_id=component_id_str)
        mass = float(component.mass)
        cache.set(cache_key, mass, 300)
        return mass
    except (Component.DoesNotExist, ValidationError, ValueError, TypeError):
        return 0


@register.filter
def multiply(value, arg):
    """
    Multiply two numbers in template.
    
    Usage:
        {{ quantity|multiply:mass }}
    
    Args:
        value: First number
        arg: Second number
    
    Returns:
        Product of the two numbers
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
