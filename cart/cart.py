"""
Cart Logic using Django Sessions
Cart is stored in the user's session (no database needed)
"""
from menu.models import FoodItem
from decimal import Decimal


class Cart:
    """
    Session-based shopping cart.
    Cart data is stored as: session['cart'] = { 'item_id': {'quantity': N, 'price': X}, ... }
    """

    def __init__(self, request):
        """Initialize the cart from the session"""
        self.session = request.session
        # Get existing cart from session, or create a new empty one
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, food_item, quantity=1, override_quantity=False):
        """Add a food item to the cart or update its quantity"""
        item_id = str(food_item.id)

        if item_id not in self.cart:
            # New item - add to cart
            self.cart[item_id] = {
                'quantity': 0,
                'price': str(food_item.price)
            }

        if override_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity

        # Remove item if quantity drops to 0
        if self.cart[item_id]['quantity'] <= 0:
            self.remove(food_item)
        else:
            self.save()

    def remove(self, food_item):
        """Remove a food item from the cart"""
        item_id = str(food_item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def save(self):
        """Mark session as modified so Django saves it"""
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over cart items and fetch FoodItem objects from DB.
        Yields dicts with food_item, price, quantity, subtotal.
        """
        item_ids = self.cart.keys()
        food_items = FoodItem.objects.filter(id__in=item_ids)
        cart = self.cart.copy()

        for food_item in food_items:
            cart_item = cart[str(food_item.id)]
            cart_item['food_item'] = food_item
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['subtotal'] = cart_item['price'] * cart_item['quantity']
            yield cart_item

    def __len__(self):
        """Return total number of items in cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate total price of all items in cart"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """Empty the cart (after order is placed)"""
        del self.session['cart']
        self.save()
