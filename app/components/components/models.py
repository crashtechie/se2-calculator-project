from django.db import models
from uuid_utils import uuid7
from ores.models import Ore

# Create your models here.
def generate_uuid():
    return str(uuid7())

class Component(models.Model):
    component_id = models.UUIDField(
        primary_key=True,
        default=generate_uuid,
        editable=False,
        help_text="Unique identifier for the component",
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique Name of the component",
    )

    description = models.TextField(
        blank=True,
        help_text="Description of the component",
    )

    materials = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON field to store material properties associated with the component",
    )

    fabricator_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="Type of fabricator used for the component",
    )

    crafting_time = models.FloatField(
            default=0.0,
            help_text="Time required to craft in seconds"
    )
            
    mass = models.FloatField(
            default=0.0,
            help_text="Total mass of the component in kilograms"
    )
        
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the component was created"
    )
        
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the component was last updated"
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Component'
        verbose_name_plural = 'Components'
        db_table = 'components_component'

    def __str__(self):
        return self.name

    def validate_materials(self):
        """
        Validate that all ore_ids in materials JSON reference valid Ores.
        
        Returns:
            tuple: (is_valid: bool, errors: list of error messages)
        """
        if not self.materials:
            return True, []
        
        errors = []
        
        for ore_id_str, quantity in self.materials.items():
            try:
                # Validate quantity is numeric
                if not isinstance(quantity, (int, float)) or quantity <= 0:
                    errors.append(
                        f"Invalid quantity for ore {ore_id_str}: "
                        f"must be positive number, got {quantity}"
                    )
                    continue
                
                # Validate ore_id references existing Ore
                try:
                    ore = Ore.objects.get(ore_id=ore_id_str)
                except Ore.DoesNotExist:
                    errors.append(
                        f"Ore with ID {ore_id_str} does not exist"
                    )
            except Exception as e:
                errors.append(f"Error validating material {ore_id_str}: {str(e)}")
        
        return len(errors) == 0, errors

    def get_material_ores(self):
        """
        Get all Ore objects referenced in materials JSON.
        
        Returns:
            QuerySet: Ore objects used in this component
        """
        if not self.materials:
            return Ore.objects.none()
        
        ore_ids = list(self.materials.keys())
        return Ore.objects.filter(ore_id__in=ore_ids)

    def clean(self):
        """Validate model before saving."""
        from django.core.exceptions import ValidationError
        
        is_valid, errors = self.validate_materials()
        if not is_valid:
            raise ValidationError(
                f"Materials validation failed: {', '.join(errors)}"
            )

    def save(self, *args, **kwargs):
        """Override save to validate materials before saving."""
        self.clean()
        super().save(*args, **kwargs)