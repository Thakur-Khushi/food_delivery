"""
Orders Admin - Admin can update order status
"""
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Show order items inside the order admin"""
    model = OrderItem
    extra = 0
    readonly_fields = ['food_name', 'food_price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method']
    list_editable = ['status']  # Update status directly from list view
    search_fields = ['user__username', 'phone']
    inlines = [OrderItemInline]
    readonly_fields = ['user', 'total_price', 'created_at']
