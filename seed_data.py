"""
Seed Data Script
Run with: python manage.py shell < seed_data.py
OR: python seed_data.py (from project root)

Creates sample categories and food items for testing.
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')
django.setup()

from menu.models import Category, FoodItem
from django.contrib.auth.models import User

# Create categories
categories_data = [
    ('Pizza', '🍕'),
    ('Burger', '🍔'),
    ('Drinks', '🥤'),
    ('Biryani', '🍛'),
    ('Desserts', '🍰'),
    ('Sandwiches', '🥪'),
]

print("Creating categories...")
categories = {}
for name, icon in categories_data:
    cat, created = Category.objects.get_or_create(name=name, defaults={'icon': icon})
    categories[name] = cat
    if created:
        print(f"  Created category: {name}")

# Create food items
food_items_data = [
    # Pizza
    ('Margherita Pizza', 'Pizza', 199.00, 'Classic tomato sauce with fresh mozzarella and basil', True),
    ('Pepperoni Pizza', 'Pizza', 249.00, 'Loaded with spicy pepperoni and cheese', False),
    ('BBQ Chicken Pizza', 'Pizza', 279.00, 'Tangy BBQ sauce with grilled chicken', False),
    ('Veggie Supreme Pizza', 'Pizza', 229.00, 'Loaded with fresh vegetables and herbs', True),

    # Burger
    ('Classic Veg Burger', 'Burger', 129.00, 'Crispy veggie patty with lettuce and tomato', True),
    ('Chicken Zinger Burger', 'Burger', 169.00, 'Spicy crispy chicken with special sauce', False),
    ('Double Beef Burger', 'Burger', 219.00, 'Double beef patty with cheese and pickles', False),
    ('Mushroom Swiss Burger', 'Burger', 189.00, 'Sauteed mushrooms with Swiss cheese', True),

    # Drinks
    ('Fresh Lime Soda', 'Drinks', 59.00, 'Refreshing lime with sparkling water', True),
    ('Mango Lassi', 'Drinks', 89.00, 'Creamy mango yogurt drink', True),
    ('Cold Coffee', 'Drinks', 99.00, 'Rich cold brew with milk and ice cream', True),
    ('Fresh Orange Juice', 'Drinks', 79.00, 'Freshly squeezed oranges', True),

    # Biryani
    ('Chicken Biryani', 'Biryani', 249.00, 'Aromatic basmati rice with tender chicken', False),
    ('Veg Biryani', 'Biryani', 199.00, 'Fragrant rice with mixed vegetables', True),
    ('Mutton Biryani', 'Biryani', 299.00, 'Slow cooked mutton with spiced rice', False),

    # Desserts
    ('Chocolate Lava Cake', 'Desserts', 149.00, 'Warm chocolate cake with molten center', True),
    ('Gulab Jamun', 'Desserts', 79.00, 'Soft milk dumplings in sugar syrup', True),
    ('Ice Cream Sundae', 'Desserts', 129.00, 'Three scoops with toppings', True),

    # Sandwiches
    ('Club Sandwich', 'Sandwiches', 139.00, 'Triple decker with chicken, egg and veggies', False),
    ('Paneer Grilled Sandwich', 'Sandwiches', 119.00, 'Spiced paneer with bell peppers', True),
]

print("\nCreating food items...")
for name, cat_name, price, desc, is_veg in food_items_data:
    item, created = FoodItem.objects.get_or_create(
        name=name,
        defaults={
            'category': categories[cat_name],
            'price': price,
            'description': desc,
            'is_vegetarian': is_veg,
            'is_available': True,
        }
    )
    if created:
        print(f"  Created: {name} - ₹{price}")

# Create admin superuser if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@foodapp.com', 'admin123')
    print("\nCreated superuser: admin / admin123")

print("\n✅ Seed data complete!")
print(f"   Categories: {Category.objects.count()}")
print(f"   Food Items: {FoodItem.objects.count()}")
print(f"\n🔑 Admin login: username=admin, password=admin123")
