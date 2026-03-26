"""
Menu App Models
FoodItem stores all food data with category support
"""
from django.db import models

class Category(models.Model):
    """Food categories like Pizza, Burger, Drinks, etc."""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='🍽️')  # Emoji icon for category

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    """
    Represents a food item available on the menu.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_vegetarian = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_image_url(self):
        """Return image URL or a placeholder if no image uploaded"""
        if self.image:
            return self.image.url
        return f"https://placehold.co/400x300/FF6B35/FFFFFF?text={self.name.replace(' ', '+')}"
