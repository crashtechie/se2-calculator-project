"""
Views for BuildOrders app.

Implements CRUD operations for BuildOrders following Phase 2 patterns:
- ListView with search, sorting, and pagination
- DetailView with cached calculation summaries
- CreateView and UpdateView with form handling
- DeleteView with confirmation

All views use comprehensive logging and Django messages framework.
"""

import logging

from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blocks.models import Block
from .forms import BuildOrderForm
from .models import BuildOrder

logger = logging.getLogger(__name__)


class BuildOrderListView(ListView):
    """
    Display paginated list of build orders with search and sorting.

    Query Parameters:
    - q: Search query (searches name)
    - sort: Sort field (name, created_at, updated_at)
    - order: Sort order (asc, desc)
    - page: Page number for pagination
    """

    model = BuildOrder
    template_name = "buildorders/buildorder_list.html"
    context_object_name = "buildorder_list"
    paginate_by = 25

    def get_queryset(self):
        """Get filtered and sorted queryset."""
        queryset = BuildOrder.objects.all()

        # Search functionality (case-insensitive name matching)
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))

        # Sorting
        sort_by = self.request.GET.get("sort", "created_at")
        order = self.request.GET.get("order", "desc")

        # Validate sort field
        valid_sort_fields = ["name", "created_at", "updated_at"]
        if sort_by not in valid_sort_fields:
            sort_by = "created_at"

        # Apply sorting
        if order == "desc":
            queryset = queryset.order_by(f"-{sort_by}")
        else:
            queryset = queryset.order_by(sort_by)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                f"BuildOrderListView query: user={self.request.user}, search='{search_query}', "
                f"sort={sort_by}, order={order}, count={queryset.count()}"
            )
        return queryset

    def get_context_data(self, **kwargs):
        """Add search and sorting context."""
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["current_sort"] = self.request.GET.get("sort", "created_at")
        context["current_order"] = self.request.GET.get("order", "desc")

        # Build query string for pagination
        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop("page")
        context["query_string"] = query_params.urlencode()

        # Precompute total masses for the current page to avoid N+1 queries in template
        orders = context["buildorder_list"]
        all_block_ids = set()
        for order in orders:
            all_block_ids.update(order.blocks.keys())
        blocks_by_id = {
            str(b.block_id): b
            for b in Block.objects.filter(block_id__in=all_block_ids)
        }
        for order in orders:
            order.total_mass_cached = sum(
                blocks_by_id[bid].mass * qty
                for bid, qty in order.blocks.items()
                if bid in blocks_by_id
            )

        logger.debug(
            f"BuildOrderListView: user={self.request.user}, page={context.get('page_obj').number if context.get('is_paginated') else 1}"
        )
        return context


class BuildOrderDetailView(DetailView):
    """
    Display detailed build order with calculation summaries.

    Uses cached calculations from BuildOrder.get_cached_calculation_summary()
    and helper methods for component/ore details.
    """

    model = BuildOrder
    template_name = "buildorders/buildorder_detail.html"
    context_object_name = "buildorder"
    slug_field = "order_id"
    slug_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        """Add calculation summary and resource details to context."""
        context = super().get_context_data(**kwargs)

        # Get cached calculation summary
        calculation_summary = self.object.get_cached_calculation_summary()
        context["calculation_summary"] = calculation_summary

        # Get component and ore details using helper methods
        context["components_with_details"] = self.object._get_components_with_details()
        context["ores_with_details"] = self.object._get_ores_with_details()

        logger.info(
            f"BuildOrderDetailView: user={self.request.user}, order_id={self.object.order_id}, "
            f"name='{self.object.name}'"
        )
        return context


class BuildOrderCreateView(CreateView):
    """
    Create new build order with form validation.

    Displays success message and redirects to detail view on success.
    """

    model = BuildOrder
    form_class = BuildOrderForm
    template_name = "buildorders/buildorder_form.html"

    def get_context_data(self, **kwargs):
        """Add form title and button text to context."""
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Create Build Order"
        context["button_text"] = "Create"
        return context

    def form_valid(self, form):
        """Handle successful form submission."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Build order '{self.object.name}' created successfully!",
        )
        logger.info(
            f"BuildOrderCreateView: user={self.request.user}, created order_id={self.object.order_id}, "
            f"name='{self.object.name}'"
        )
        return response

    def form_invalid(self, form):
        """Handle validation errors."""
        logger.warning(
            f"BuildOrderCreateView: user={self.request.user}, validation failed, "
            f"errors={form.errors}"
        )
        return super().form_invalid(form)

    def get_success_url(self):
        """Redirect to detail view."""
        return reverse_lazy("buildorders:detail", kwargs={"pk": self.object.order_id})


class BuildOrderUpdateView(UpdateView):
    """
    Update existing build order with pre-populated form.

    Displays success message and redirects to detail view on success.
    """

    model = BuildOrder
    form_class = BuildOrderForm
    template_name = "buildorders/buildorder_form.html"
    slug_field = "order_id"
    slug_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        """Add form title and button text to context."""
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Update Build Order"
        context["button_text"] = "Update"
        return context

    def form_valid(self, form):
        """Handle successful form submission."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Build order '{self.object.name}' updated successfully!",
        )
        logger.info(
            f"BuildOrderUpdateView: user={self.request.user}, updated order_id={self.object.order_id}, "
            f"name='{self.object.name}'"
        )
        return response

    def form_invalid(self, form):
        """Handle validation errors."""
        logger.warning(
            f"BuildOrderUpdateView: user={self.request.user}, order_id={self.object.order_id}, "
            f"validation failed, errors={form.errors}"
        )
        return super().form_invalid(form)

    def get_success_url(self):
        """Redirect to detail view."""
        return reverse_lazy("buildorders:detail", kwargs={"pk": self.object.order_id})


class BuildOrderDeleteView(DeleteView):
    """
    Delete build order with confirmation.

    Displays success message and redirects to list view on success.
    """

    model = BuildOrder
    template_name = "buildorders/buildorder_confirm_delete.html"
    context_object_name = "buildorder"
    success_url = reverse_lazy("buildorders:list")
    slug_field = "order_id"
    slug_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        """Add build order details for confirmation."""
        context = super().get_context_data(**kwargs)
        context["blocks_count"] = len(self.object.blocks)
        return context

    def form_valid(self, form):
        """Handle confirmed deletion."""
        order_name = self.object.name
        order_id = self.object.order_id
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Build order '{order_name}' deleted successfully!",
        )
        logger.info(
            f"BuildOrderDeleteView: user={self.request.user}, deleted order_id={order_id}, "
            f"name='{order_name}'"
        )
        return response
