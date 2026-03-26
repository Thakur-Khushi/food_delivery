"""
Orders Views - Checkout and Order Listing
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.cart import Cart


@login_required
def checkout(request):
    """Checkout page - collect address and place order"""
    cart = Cart(request)

    # Redirect to cart if cart is empty
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Add items before checking out.")
        return redirect('cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create the Order object
            order = Order.objects.create(
                user=request.user,
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
                total_price=cart.get_total_price(),
                payment_method=form.cleaned_data['payment_method'],
                status='placed'
            )

            # Create OrderItem for each cart item
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    food_item=item['food_item'],
                    food_name=item['food_item'].name,
                    food_price=item['price'],
                    quantity=item['quantity']
                )

            # Clear the cart after order placed
            cart.clear()

            messages.success(request, f"Order #{order.id} placed successfully! We'll deliver soon 🚀")
            return redirect('order_detail', order_id=order.id)
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'cart': cart,
        'cart_items': list(cart),
        'total': cart.get_total_price(),
    }
    return render(request, 'checkout.html', context)


@login_required
def order_list(request):
    """Show all orders for the logged-in user"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Show details of a specific order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    status_steps = ['placed', 'preparing', 'out_for_delivery', 'delivered']
    current_step = order.get_status_display_info()

    context = {
        'order': order,
        'items': items,
        'status_steps': status_steps,
        'current_step': current_step,
    }
    return render(request, 'order_detail.html', context)
