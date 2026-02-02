# buildorders/models.py
from django.db import models
from django.core.exceptions import ValidationError
from uuid_utils import uuid7
from blocks.models import Block
from components.models import Component
from ores.models import Ore
from django.core.cache import cache

def generate_uuid():
    return str(uuid7())

class BuildOrder(models.Model):
    order_id = models.UUIDField(
        primary_key=True,
        default=generate_uuid,
        editable=False,
        help_text="UUIDv7 primary key"
    )
    
    name = models.CharField(
        max_length=200,
        help_text="Name of the build order"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Optional description"
    )
    
    blocks = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON object mapping block IDs to quantities"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Build Order'
        verbose_name_plural = 'Build Orders'
        db_table = 'buildorders_buildorder'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    # Validate Blocks
    def validate_blocks(self):
        errors = []
        for block_id, quantity in self.blocks.items():
            try:
                block = Block.objects.get(block_id=block_id)
                if quantity <= 0:
                    errors.append(f"Invalid quantity for block {block.name}: {quantity}")
            except Block.DoesNotExist:
                errors.append(f"Block with ID {block_id} does not exist")
        return errors
    
    # Get Block Objects
    def get_block_objects(self):
        blocks = []
        for block_id, quantity in self.blocks.items():
            try:
                block = Block.objects.get(block_id=block_id)
                blocks.append((block, quantity))
            except Block.DoesNotExist:
                continue
        return blocks
    
    # clean function that validates before saving
    def clean(self):
        errors = self.validate_blocks()
        if errors:
            raise ValidationError("Block validation errors: " + "; ".join(errors))
        
    # Save override to call clean() and invalidate cache
    def save(self, *args, **kwargs):
        self.full_clean()  # This calls clean()
        super().save(*args, **kwargs)
        # Invalidate cache after saving
        cache_key = f'buildorder_calc_{self.order_id}'
        cache.delete(cache_key)

    # Calculates total mass as sum of block masses * quantity
    def calculate_total_mass(self):
        total_mass = 0.0
        for block_id, quantity in self.blocks.items():
            try:
                block = Block.objects.get(block_id=block_id)
                total_mass += block.mass * quantity
            except Block.DoesNotExist:
                continue
        return total_mass
    
    # Calculate the aggregate components across blocks
    def calculate_required_components(self):
        components = {}
        for block_id, quantity in self.blocks.items():
            try:
                block = Block.objects.get(block_id=block_id)
                for comp_id, comp_qty in block.components.items():
                    if comp_id in components:
                        components[comp_id] += comp_qty * quantity
                    else:
                        components[comp_id] = comp_qty * quantity
            except Block.DoesNotExist:
                continue
        return components
    
    # Traverse components to calculate aggregate of ores across blocks
    def calculate_required_ores(self):
        ores = {}
        components = self.calculate_required_components()
        for comp_id, comp_qty in components.items():
            try:
                component = Component.objects.get(component_id=comp_id)
                for ore_name, ore_qty in component.materials.items():
                    if ore_name in ores:
                        ores[ore_name] += ore_qty * comp_qty
                    else:
                        ores[ore_name] = ore_qty * comp_qty
            except Component.DoesNotExist:
                continue
        return ores

    # Group by fabricator type and calculate crafting time
    def calculate_fabricator_times(self):
        fabricators = {}
        components = self.calculate_required_components()
        for comp_id, comp_qty in components.items():
            try:
                component = Component.objects.get(component_id=comp_id)
                fab_type = component.fabricator_type
                crafting_time = component.crafting_time * comp_qty

                if fab_type in fabricators:
                    fabricators[fab_type] += crafting_time
                else:
                    fabricators[fab_type] = crafting_time
            except Component.DoesNotExist:
                continue
        return fabricators
    
    # return complete summary with caching
    def get_calculation_summary(self):
        return {
            'total_mass': self.calculate_total_mass(),
            'required_components': self.calculate_required_components(),
            'required_ores': self.calculate_required_ores(),
            'fabricator_times': self.calculate_fabricator_times(),
        }
        
    # helper for component details
    def _get_components_with_details(self):
        components = self.calculate_required_components()
        result = []
        for comp_id, qty in components.items():
            try:
                comp = Component.objects.get(component_id=comp_id)
                result.append({
                    'component': comp,
                    'quantity': qty,
                    'total_mass': comp.mass * qty
                })
            except Component.DoesNotExist:
                continue
        return result

    # helper for ore details
    def _get_ores_with_details(self):
        ores = self.calculate_required_ores()
        result = []
        for ore_id, qty in ores.items():
            try:
                ore = Ore.objects.get(ore_id=ore_id)
                result.append({
                    'ore': ore,
                    'quantity': qty,
                })
            except Ore.DoesNotExist:
                continue
        return result

    # cache calculation results within 5 minutes ttl cache key: buildorder_calc_{order_id},
    # invalidate cache on save, and optional use_cache parameter for testing
    def get_cached_calculation_summary(self, use_cache=True):
        cache_key = f'buildorder_calc_{self.order_id}'
        if use_cache:
            cached_result = cache.get(cache_key)
            if cached_result:
                return cached_result

        summary = self.get_calculation_summary()
        cache.set(cache_key, summary, 300)  # 5 minute TTL
        return summary
