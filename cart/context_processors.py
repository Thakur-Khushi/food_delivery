"""
Cart Context Processor
Makes cart count available in ALL templates automatically
"""
from .cart import Cart


def cart_count(request):
    """Inject cart item count into every template context"""
    cart = Cart(request)
    return {'cart_count': len(cart)}
