"""
Template filters for Components app.

Provides custom template filters for displaying component data,
particularly for converting ore UUIDs to human-readable names.
"""
from django import template
from ores.models import Ore
from django.core.cache import cache
import logging

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def get_ore_name(ore_id):
    """
    Convert ore UUID to ore name for display in templates.
    
    Usage:
        {{ ore_id|get_ore_name }}
    
    Args:
        ore_id: UUID string or UUID object
    
    Returns:
        Ore name if found, otherwise "Unknown Ore (uuid)"
    
    Caches ore lookups to improve performance.
    """
    if not ore_id:
        return "Unknown Ore"
    
    # Convert to string if UUID object
    ore_id_str = str(ore_id)
    
    # Check cache first (5 minute TTL)
    cache_key = f'ore_name_{ore_id_str}'
    cached_name = cache.get(cache_key)
    
    if cached_name:
        return cached_name
    
    # Query database
    try:
        ore = Ore.objects.get(ore_id=ore_id_str)
        ore_name = ore.name
        
        # Cache for 5 minutes
        cache.set(cache_key, ore_name, 300)
        
        return ore_name
    except Ore.DoesNotExist:
        logger.warning(f'Ore not found for UUID: {ore_id_str}')
        return f"Unknown Ore ({ore_id_str[:8]}...)"
    except Exception as e:
        logger.error(f'Error looking up ore {ore_id_str}: {e}')
        return "Unknown Ore (error)"


@register.filter
def format_mass(mass):
    """
    Format mass value for display.
    
    Usage:
        {{ component.mass|format_mass }}
    
    Args:
        mass: Float or Decimal mass value
    
    Returns:
        Formatted string with 2 decimal places and " kg" suffix
    """
    if mass is None:
        return "0.00 kg"
    
    try:
        return f"{float(mass):.2f} kg"
    except (ValueError, TypeError):
        return f"{mass} kg"


@register.filter
def format_time(seconds):
    """
    Format time in seconds to human-readable format.
    
    Usage:
        {{ component.build_time|format_time }}
    
    Args:
        seconds: Time in seconds (float or int)
    
    Returns:
        Formatted string (e.g., "2m 30s" or "45s")
    """
    if seconds is None:
        return "0s"
    
    try:
        seconds = float(seconds)
        
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            return f"{minutes}m {remaining_seconds}s"
        else:
            hours = int(seconds // 3600)
            remaining_minutes = int((seconds % 3600) // 60)
            return f"{hours}h {remaining_minutes}m"
    except (ValueError, TypeError):
        return f"{seconds}s"
