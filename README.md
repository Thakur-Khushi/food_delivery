# 🍕 Food Delivery Web App

A full-stack food delivery app built with **Django, SQLite and vanilla JavaScript**. Users can browse a filtered menu, manage a cart without page reloads, check out with Cash on Delivery and track their order through each stage.

**🔗 Live demo:** [khushi010305.pythonanywhere.com](https://khushi010305.pythonanywhere.com/)


## ✨ Features

- Menu browsing with category filters (Pizza, Burger, Drinks, Biryani, Desserts, Sandwiches)
- Registration, login, logout and a personal dashboard
- Session-based cart with AJAX: add, remove and update items with no page reload
- Checkout with delivery details and Cash on Delivery
- Order tracking through each status: placed → preparing → out for delivery → delivered
- Django admin for managing food items, categories and order statuses
- Custom terracotta-and-cream visual theme, responsive down to mobile

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, python-decouple |
| Database | SQLite |
| Frontend | Django templates, vanilla JavaScript (AJAX), custom CSS |
| Media | Pillow (food images) |
| Hosting | PythonAnywhere |

## 🧠 How the cart works

The cart lives in the Django session, so it needs no extra database table:

```python
session['cart'] = {
    "1": {"quantity": 2, "price": "199.00"},
    "3": {"quantity": 1, "price": "129.00"},
}
```

Adding an item sends an AJAX `POST` to `/cart/add/`, which updates the cart badge without reloading the page. All cart logic is in the `Cart` class in `cart/cart.py`.

Orders store a **snapshot** of each item's name and price (`OrderItem.food_name`, `OrderItem.food_price`), so past orders stay accurate even if the menu changes later.

## 🗂️ Project Structure

```text
food_delivery/
├── food_delivery/   # Project settings and root URLs
├── users/           # Registration, login, logout, dashboard
├── menu/            # Category and FoodItem models, home and menu pages
├── cart/            # Session cart (cart.py) and AJAX endpoints
├── orders/          # Checkout, Order/OrderItem models, order tracking
├── templates/       # All HTML templates
├── static/          # style.css and main.js (cart AJAX, toasts, mobile menu)
├── media/           # Food images
├── seed_data.py     # Sample categories, 20 food items and an admin user
└── manage.py
```

## ⚡ Run it locally

```bash
git clone https://github.com/Thakur-Khushi/food_delivery.git
cd food_delivery

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then set SECRET_KEY and DEBUG=True
python manage.py migrate
python seed_data.py             # set ADMIN_PASSWORD first, or a random one is printed
python manage.py runserver
```

Then open http://127.0.0.1:8000.

| URL | Page |
|---|---|
| `/` | Home |
| `/menu/` | Full menu with filters |
| `/register/`, `/login/` | Auth |
| `/cart/` | Cart |
| `/orders/checkout/` | Checkout |
| `/orders/` | My orders and tracking |
| `/admin/` | Django admin |

## 🔭 What's next

- Automated tests for the cart, order flow and auth
- Online payments (Razorpay)
- Menu search and food ratings
- Order confirmation emails
