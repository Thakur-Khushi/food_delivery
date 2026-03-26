"""
Orders Models
Stores order information with status tracking
"""
from django.db import models
from django.contrib.auth.models import User
from menu.models import FoodItem


class Order(models.Model):
    """
    Represents a placed order by a user.
    Tracks delivery info and order status.
    """
    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.TextField()
    phone = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Most recent orders first

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - {self.status}"

    def get_status_display_info(self):
        """Returns step index for progress bar (0-3)"""
        steps = ['placed', 'preparing', 'out_for_delivery', 'delivered']
        try:
            return steps.index(self.status)
        except ValueError:
            return 0


class OrderItem(models.Model):
    """
    Represents each food item in an order.
    Stores snapshot of price at time of order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True)
    food_name = models.CharField(max_length=200)  # Snapshot: item name at order time
    food_price = models.DecimalField(max_digits=8, decimal_places=2)  # Snapshot price
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.food_name}"

    def get_subtotal(self):
        return self.food_price * self.quantity
