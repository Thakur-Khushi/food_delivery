"""
Menu Views
Handles the home page and menu page with category filtering
"""
from django.shortcuts import render
from .models import FoodItem, Category


def home(request):
    """Home page - shows featured/all food items"""
    categories = Category.objects.all()
    food_items = FoodItem.objects.filter(is_available=True).select_related('category')

    # Get selected category from URL query param
    selected_category = request.GET.get('category', None)
    if selected_category:
        food_items = food_items.filter(category__id=selected_category)

    context = {
        'food_items': food_items,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'home.html', context)


def menu(request):
    """Menu page - same as home but with different template focus"""
    categories = Category.objects.all()
    food_items = FoodItem.objects.filter(is_available=True).select_related('category')

    selected_category = request.GET.get('category', None)
    if selected_category:
        food_items = food_items.filter(category__id=selected_category)

    context = {
        'food_items': food_items,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'menu.html', context)
