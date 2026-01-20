from django.db import models
from uuid_utils import uuid7
from components.models import Component


def generate_uuid():
    """Generate UUIDv7 string for primary key."""
    return str(uuid7())


class Block(models.Model):
    """
    Represents a buildable block in Space Engineers 2.
    
    Blocks are the final buildable items made from components.
    """
    block_id = models.UUIDField(
        primary_key=True,
        default=generate_uuid,
        editable=False,
        help_text="UUIDv7 primary key"
    )
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique name of the block (e.g., 'Large Reactor', 'Small Thruster')"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the block and its uses"
    )
    
    mass = models.FloatField(
        help_text="Total mass of the block in kilograms"
    )
    
    components = models.JSONField(
        default=list,
        blank=True,
        help_text="JSON array of component requirements with IDs, names, and quantities"
    )
    
    health = models.FloatField(
        help_text="Block health/integrity points"
    )
    
    pcu = models.IntegerField(
        help_text="Performance Cost Units (PCU) for this block"
    )
    
    snap_size = models.FloatField(
        help_text="Grid snap size for placement"
    )
    
    input_mass = models.IntegerField(
        help_text="Input mass capacity in kg"
    )
    
    output_mass = models.IntegerField(
        help_text="Output mass capacity in kg"
    )
    
    consumer_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Type of resource consumed (e.g., 'Power', 'Hydrogen', 'Oxygen')"
    )
    
    consumer_rate = models.FloatField(
        default=0.0,
        help_text="Consumption rate per second"
    )
    
    producer_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Type of resource produced (e.g., 'Power', 'Hydrogen', 'Oxygen')"
    )
    
    producer_rate = models.FloatField(
        default=0.0,
        help_text="Production rate per second"
    )
    
    storage_capacity = models.FloatField(
        default=0.0,
        help_text="Storage capacity in liters or units"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the block was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the block was last updated"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Block'
        verbose_name_plural = 'Blocks'
        db_table = 'blocks_block'
    
    def __str__(self):
        return self.name
    
    def validate_components(self):
        """
        Validate that all component_ids in components JSON reference valid Components.
        
        Returns:
            tuple: (is_valid: bool, errors: list of error messages)
        """
        if not self.components:
            return True, []
        
        errors = []
        
        for item in self.components:
            try:
                # Validate structure
                if not isinstance(item, dict):
                    errors.append(f"Component item must be dict, got {type(item)}")
                    continue
                
                required_keys = ['component_id', 'component_name', 'quantity']
                missing_keys = [k for k in required_keys if k not in item]
                if missing_keys:
                    errors.append(f"Component missing keys: {missing_keys}")
                    continue
                
                # Validate quantity
                quantity = item.get('quantity')
                if not isinstance(quantity, int) or quantity <= 0:
                    errors.append(
                        f"Invalid quantity for component {item.get('component_name')}: "
                        f"must be positive integer, got {quantity}"
                    )
                    continue
                
                # Validate component_id references existing Component
                component_id = item.get('component_id')
                try:
                    Component.objects.get(component_id=component_id)
                except Component.DoesNotExist:
                    errors.append(
                        f"Component with ID {component_id} does not exist"
                    )
            except Exception as e:
                errors.append(f"Error validating component: {str(e)}")
        
        return len(errors) == 0, errors
    
    def validate_consumer(self):
        """
        Validate consumer_type and consumer_rate relationship.
        
        Returns:
            tuple: (is_valid: bool, errors: list of error messages)
        """
        errors = []
        
        if self.consumer_type and self.consumer_rate <= 0:
            errors.append(
                f"Consumer type '{self.consumer_type}' requires consumer_rate > 0, "
                f"got {self.consumer_rate}"
            )
        
        if self.consumer_rate < 0:
            errors.append(f"Consumer rate cannot be negative, got {self.consumer_rate}")
        
        return len(errors) == 0, errors
    
    def validate_producer(self):
        """
        Validate producer_type and producer_rate relationship.
        
        Returns:
            tuple: (is_valid: bool, errors: list of error messages)
        """
        errors = []
        
        if self.producer_type and self.producer_rate <= 0:
            errors.append(
                f"Producer type '{self.producer_type}' requires producer_rate > 0, "
                f"got {self.producer_rate}"
            )
        
        if self.producer_rate < 0:
            errors.append(f"Producer rate cannot be negative, got {self.producer_rate}")
        
        return len(errors) == 0, errors
    
    def get_component_objects(self):
        """
        Get all Component objects referenced in components JSON.
        
        Returns:
            QuerySet: Component objects used in this block
        """
        if not self.components:
            return Component.objects.none()
        
        component_ids = [item['component_id'] for item in self.components]
        return Component.objects.filter(component_id__in=component_ids)
    
    def clean(self):
        """Validate model before saving."""
        from django.core.exceptions import ValidationError
        
        all_errors = []
        
        # Validate components
        is_valid, errors = self.validate_components()
        if not is_valid:
            all_errors.extend(errors)
        
        # Validate consumer
        is_valid, errors = self.validate_consumer()
        if not is_valid:
            all_errors.extend(errors)
        
        # Validate producer
        is_valid, errors = self.validate_producer()
        if not is_valid:
            all_errors.extend(errors)
        
        if all_errors:
            raise ValidationError(f"Validation failed: {', '.join(all_errors)}")
    
    def save(self, *args, **kwargs):
        """Override save to validate before saving."""
        self.clean()
        super().save(*args, **kwargs)