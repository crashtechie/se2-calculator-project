"""
Forms for BuildOrders app.

Handles JSONField blocks with custom form processing:
- Converts between form data (blocks_json hidden field) and JSON storage
- Validates block UUIDs against database
- Validates quantities (positive integers)
- Reuses BuildOrder.validate_blocks() helper from ENH-0000009

Pattern adapted from Phase 2 BlockForm (ENH-0000007).
"""

import json
import logging
import uuid

from django import forms
from django.core.exceptions import ValidationError

from blocks.models import Block

from .models import BuildOrder

logger = logging.getLogger(__name__)


class BuildOrderForm(forms.ModelForm):
    """
    Form for creating/updating BuildOrders with dynamic block selection.

    Blocks are handled as a hidden JSON field (blocks_json) and converted
    to JSONField format on save. The JavaScript block selector (ENH-0000011)
    will populate this field dynamically.
    """

    # Hidden field to carry JSON block payload from the client
    blocks_json = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        help_text="JSON representation of blocks",
    )

    class Meta:
        model = BuildOrder
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": 'Enter build order name (e.g., "Heavy Armor Ship")',
                    "maxlength": 200,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe the build order and its purpose...",
                    "rows": 3,
                    "maxlength": 1000,
                }
            ),
        }
        help_texts = {
            "name": "Unique name for the build order (max 200 characters)",
            "description": "Optional description of the build order",
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form and prepare for block handling.

        If updating an existing build order (instance provided), pre-populate
        the blocks_json field with existing block data.
        """
        super().__init__(*args, **kwargs)

        # Pre-populate blocks for update forms
        if self.instance and self.instance.pk and self.instance.blocks:
            # Convert blocks dict to JSON string for hidden field
            self.initial["blocks_json"] = json.dumps(self.instance.blocks)
            logger.debug(
                f"BuildOrderForm.__init__: Pre-populated blocks_json for order_id={self.instance.order_id}"
            )

    def clean_name(self):
        """
        Validate build order name is not empty.

        Returns:
            str: Cleaned name

        Raises:
            ValidationError: If name is empty or whitespace-only
        """
        name = self.cleaned_data.get("name", "").strip()

        if not name:
            raise ValidationError("Build order name is required.")

        logger.debug(f"BuildOrderForm.clean_name: Validated name='{name}'")
        return name

    def clean(self):
        """
        Cross-field validation and block processing.

        Converts blocks_json from client into proper JSONField format
        and validates using BuildOrder.validate_blocks() helper from ENH-0000009.

        Returns:
            dict: Cleaned form data with processed blocks

        Raises:
            ValidationError: If block validation fails
        """
        cleaned_data = super().clean()

        # Process blocks from JSON payload
        blocks_json = cleaned_data.get("blocks_json", "").strip()

        if not blocks_json or blocks_json == "{}":
            logger.warning("BuildOrderForm.clean: No blocks provided")
            raise ValidationError({"blocks_json": "At least one block is required."})

        try:
            blocks_data = json.loads(blocks_json)
        except json.JSONDecodeError as e:
            logger.warning(f"BuildOrderForm.clean: Invalid JSON format: {e}")
            raise ValidationError({"blocks_json": "Invalid JSON format for blocks."})

        # Validate blocks structure
        if not isinstance(blocks_data, dict):
            logger.warning(
                f"BuildOrderForm.clean: Blocks data is not a dict: {type(blocks_data)}"
            )
            raise ValidationError(
                {"blocks_json": "Blocks must be a dictionary of {block_id: quantity}."}
            )

        # Convert and validate each block
        validated_blocks = {}

        for block_id_str, quantity in blocks_data.items():
            # Validate UUID format
            try:
                block_uuid = uuid.UUID(block_id_str)
            except (ValueError, AttributeError):
                logger.warning(
                    f"BuildOrderForm.clean: Invalid block UUID: {block_id_str}"
                )
                raise ValidationError(
                    {"blocks_json": f"Invalid block UUID: {block_id_str}"}
                )

            # Validate quantity
            try:
                qty = int(quantity)
                if qty <= 0:
                    raise ValueError()
            except (ValueError, TypeError):
                logger.warning(
                    f"BuildOrderForm.clean: Invalid quantity for block {block_id_str}: {quantity}"
                )
                raise ValidationError(
                    {
                        "blocks_json": f"Invalid quantity for block {block_id_str}: {quantity}. Must be positive integer."
                    }
                )

            # Verify block exists in database
            if not Block.objects.filter(block_id=block_uuid).exists():
                logger.warning(
                    f"BuildOrderForm.clean: Block {block_id_str} does not exist in database"
                )
                raise ValidationError(
                    {"blocks_json": f"Block {block_id_str} does not exist in database."}
                )

            validated_blocks[str(block_uuid)] = qty

        # Store validated blocks for save
        cleaned_data["blocks"] = validated_blocks

        # Use BuildOrder validation helper (create temporary instance)
        temp_order = BuildOrder(
            name=cleaned_data.get("name", "temp"),
            blocks=validated_blocks,
        )

        validation_errors = temp_order.validate_blocks()

        if validation_errors:
            logger.warning(
                f"BuildOrderForm.clean: Block validation failed: {validation_errors}"
            )
            raise ValidationError(
                {
                    "blocks_json": f"Block validation failed: {', '.join(validation_errors)}"
                }
            )

        logger.debug(
            f"BuildOrderForm.clean: Validated {len(validated_blocks)} blocks successfully"
        )
        return cleaned_data

    def save(self, commit=True):
        """
        Save build order with validated blocks.

        Args:
            commit: Whether to save to database immediately

        Returns:
            BuildOrder: Saved build order instance
        """
        instance = super().save(commit=False)

        # Set blocks from cleaned_data
        if "blocks" in self.cleaned_data:
            instance.blocks = self.cleaned_data["blocks"]
            logger.debug(
                f"BuildOrderForm.save: Set blocks for order_id={instance.order_id if instance.pk else 'new'}"
            )

        if commit:
            instance.save()
            logger.info(
                f"BuildOrderForm.save: Saved build order order_id={instance.order_id}, name='{instance.name}'"
            )

        return instance
