"""
Cart Views - Add, Remove, Update, View Cart
Uses AJAX for smooth UX without page reload
"""
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from menu.models import FoodItem
from .cart import Cart


def cart_detail(request):
    """Display the cart page"""
    cart = Cart(request)
    cart_items = list(cart)  # Convert generator to list for template
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total': cart.get_total_price()
    })


@require_POST
def cart_add(request):
    """
    AJAX endpoint: Add item to cart or update quantity.
    Expects JSON body: { "item_id": N, "quantity": N, "action": "add"|"set" }
    """
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        action = data.get('action', 'add')  # 'add' increases, 'set' overrides

        food_item = get_object_or_404(FoodItem, id=item_id, is_available=True)
        cart = Cart(request)

        if action == 'set':
            cart.add(food_item, quantity=quantity, override_quantity=True)
        else:
            cart.add(food_item, quantity=quantity)

        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price()),
            'message': f'{food_item.name} added to cart!'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def cart_remove(request):
    """
    AJAX endpoint: Remove item from cart entirely.
    Expects JSON body: { "item_id": N }
    """
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')

        food_item = get_object_or_404(FoodItem, id=item_id)
        cart = Cart(request)
        cart.remove(food_item)

        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price()),
            'message': 'Item removed from cart.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def cart_update(request):
    """
    AJAX endpoint: Update quantity of item in cart.
    Expects JSON body: { "item_id": N, "quantity": N }
    """
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))

        food_item = get_object_or_404(FoodItem, id=item_id)
        cart = Cart(request)

        if quantity <= 0:
            cart.remove(food_item)
        else:
            cart.add(food_item, quantity=quantity, override_quantity=True)

        # Build updated cart items for response
        cart_items = []
        for item in cart:
            cart_items.append({
                'id': item['food_item'].id,
                'name': item['food_item'].name,
                'price': str(item['price']),
                'quantity': item['quantity'],
                'subtotal': str(item['subtotal'])
            })

        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price()),
            'cart_items': cart_items
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
