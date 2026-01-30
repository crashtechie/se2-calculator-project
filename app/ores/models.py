from django.db import models
from uuid_utils import uuid7

# Create your models here.
def generate_uuid():
    return str(uuid7())

class Ore(models.Model):
    ore_id = models.UUIDField(
        primary_key=True,
        default=generate_uuid,
        editable=False,
        unique=True,
        help_text="A unique identifier for each ore instance."
    )
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique name of the ore."
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the ore."
    )
    
    mass = models.FloatField(
        help_text="Mass of the ore in kilograms."
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the ore was created."
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the ore was last updated."
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = "Ore"
        verbose_name_plural = "Ores"
        db_table = "ores_ore"
        
    def __str__(self):
        return self.name