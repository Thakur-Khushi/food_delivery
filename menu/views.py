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

    # 🔒 SECURITY: Validate category parameter
    selected_category = request.GET.get('category', None)
    if selected_category:
        try:
            category_id = int(selected_category)
            food_items = food_items.filter(category__id=category_id)
        except (ValueError, TypeError):
            pass  # Ignore invalid category

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

    # 🔒 SECURITY: Validate category parameter
    selected_category = request.GET.get('category', None)
    if selected_category:
        try:
            category_id = int(selected_category)
            food_items = food_items.filter(category__id=category_id)
        except (ValueError, TypeError):
            pass  # Ignore invalid category

    context = {
        'food_items': food_items,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'menu.html', context)
