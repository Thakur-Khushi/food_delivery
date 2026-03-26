"""
Menu Admin Configuration
Allows admin to manage food items and categories
"""
from django.contrib import admin
from .models import Category, FoodItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_vegetarian']
    list_filter = ['category', 'is_available', 'is_vegetarian']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_available']  # Edit price/availability inline
