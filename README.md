# 🍜 QuickBite — Online Food Delivery Web App

A full-stack food delivery application built with **Django + SQLite + Vanilla JS**.  
Beginner-friendly, modular, fully commented, production-structured.

---

## 🗂️ Project Structure

```
food_delivery/
├── food_delivery/          ← Django project settings & main URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/                  ← Registration, Login, Logout, Dashboard
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── menu/                   ← Food items, Categories, Home + Menu pages
│   ├── models.py           (Category, FoodItem)
│   ├── views.py
│   ├── admin.py
│   └── urls.py
│
├── cart/                   ← Session-based cart logic
│   ├── cart.py             (Cart class — core logic)
│   ├── context_processors.py
│   ├── views.py            (AJAX endpoints)
│   └── urls.py
│
├── orders/                 ← Checkout, Order placement, Order tracking
│   ├── models.py           (Order, OrderItem)
│   ├── forms.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
│
├── templates/              ← All HTML templates
│   ├── base.html           (Navbar, Footer, Messages layout)
│   ├── home.html           (Hero + Food grid)
│   ├── menu.html           (Sidebar filter + Food grid)
│   ├── cart.html           (Cart items + Summary)
│   ├── checkout.html       (Delivery form + COD)
│   ├── orders.html         (All orders list)
│   ├── order_detail.html   (Status tracker + Item details)
│   └── users/
│       ├── login.html
│       ├── register.html
│       └── dashboard.html
│
├── static/
│   ├── css/style.css       ← All styling (Terracotta + Cream theme)
│   └── js/main.js          ← Cart AJAX, Toast, Mobile menu
│
├── media/                  ← Uploaded food images (auto-created)
├── db.sqlite3              ← SQLite database (auto-created)
├── seed_data.py            ← Sample data script
└── manage.py
```

---

## ⚡ Quick Setup (Step-by-Step)

### Step 1 — Clone / Extract the project
```bash
cd your/projects/folder
# If zip: unzip food_delivery.zip
cd food_delivery
```

### Step 2 — Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install django pillow
```
> `pillow` is needed for handling food item images.

### Step 4 — Apply database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5 — Load sample data (categories + food items + admin user)
```bash
python seed_data.py
```
This creates:
- 6 categories: Pizza, Burger, Drinks, Biryani, Desserts, Sandwiches
- 20 food items with prices
- Admin superuser: **username=`admin`**, **password=`admin123`**

### Step 6 — Run the server
```bash
python manage.py runserver
```

### Step 7 — Open in browser
| URL | Page |
|-----|------|
| http://127.0.0.1:8000/ | Home page |
| http://127.0.0.1:8000/menu/ | Full menu with filters |
| http://127.0.0.1:8000/register/ | Create account |
| http://127.0.0.1:8000/login/ | Login |
| http://127.0.0.1:8000/cart/ | View cart |
| http://127.0.0.1:8000/orders/checkout/ | Checkout |
| http://127.0.0.1:8000/orders/ | My orders |
| http://127.0.0.1:8000/admin/ | Django admin panel |

---

## 🔑 Admin Panel Usage


**To update order status:**
1. Go to Admin → Orders
2. Find the order
3. Change "Status" column directly in the list view → Save

---

## 🛠️ How the Cart Works

The cart uses **Django sessions** (no extra database table needed):

```
Session['cart'] = {
    "1": { "quantity": 2, "price": "199.00" },
    "3": { "quantity": 1, "price": "129.00" }
}
```

When you add an item → **AJAX POST** to `/cart/add/` → response updates badge count.  
No page reload needed! The `cart.py` `Cart` class handles all logic.

---

## 🌐 URL Summary

| URL Pattern | View | Purpose |
|------------|------|---------|
| `/` | `menu.views.home` | Home + food grid |
| `/menu/` | `menu.views.menu` | Full menu + sidebar filter |
| `/register/` | `users.views.register_view` | Registration |
| `/login/` | `users.views.login_view` | Login |
| `/logout/` | `users.views.logout_view` | Logout |
| `/dashboard/` | `users.views.dashboard` | User dashboard |
| `/cart/` | `cart.views.cart_detail` | View cart |
| `/cart/add/` | `cart.views.cart_add` | AJAX: Add to cart |
| `/cart/remove/` | `cart.views.cart_remove` | AJAX: Remove item |
| `/cart/update/` | `cart.views.cart_update` | AJAX: Update qty |
| `/orders/checkout/` | `orders.views.checkout` | Checkout form |
| `/orders/` | `orders.views.order_list` | All orders |
| `/orders/<id>/` | `orders.views.order_detail` | Order detail + tracker |

---

## 🍕 Adding Food Items with Images

**Option 1 — Django Admin (recommended):**
1. Go to http://127.0.0.1:8000/admin/menu/fooditem/add/
2. Fill name, price, category, upload image
3. Save

**Option 2 — Programmatically (in seed_data.py or shell):**
```python
from menu.models import FoodItem, Category
cat = Category.objects.get(name='Pizza')
FoodItem.objects.create(
    name='Cheese Burst',
    price=299,
    category=cat,
    description='Extra cheese everywhere',
    is_vegetarian=True
)
```

> 📌 If no image is uploaded, a colored placeholder is automatically shown.

---

## 🧩 Models Overview

### `menu.Category`
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | e.g. "Pizza" |
| icon | CharField | Emoji e.g. "🍕" |

### `menu.FoodItem`
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Item name |
| price | DecimalField | In ₹ |
| category | FK → Category | |
| image | ImageField | Optional |
| is_vegetarian | BooleanField | Shows green badge |
| is_available | BooleanField | Hides if False |

### `orders.Order`
| Field | Type | Notes |
|-------|------|-------|
| user | FK → User | |
| address | TextField | Delivery address |
| phone | CharField | |
| total_price | DecimalField | |
| status | CharField | placed/preparing/out_for_delivery/delivered |
| payment_method | CharField | cod |

### `orders.OrderItem`
| Field | Type | Notes |
|-------|------|-------|
| order | FK → Order | |
| food_item | FK → FoodItem | SET_NULL on delete |
| food_name | CharField | Snapshot at order time |
| food_price | DecimalField | Snapshot at order time |
| quantity | PositiveIntegerField | |

---

## 🚀 Extending the App

| Feature | How to add |
|---------|-----------|
| Online payment | Integrate Razorpay/Stripe in `orders/views.py` checkout |
| Food ratings | Add a `Rating` model in menu app |
| Search | Add search filter in `menu/views.py` using `Q()` objects |
| Email confirmation | Use Django's `send_mail()` after order placement |
| REST API | Install `djangorestframework`, add serializers |
| Custom user profile | Extend `AbstractUser` in `users/models.py` |

---

## ❓ Troubleshooting

**`ModuleNotFoundError: No module named 'PIL'`**
```bash
pip install pillow
```

**`OperationalError: no such table`**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Static files not loading**
- Make sure `DEBUG = True` in `settings.py`
- Run `python manage.py collectstatic` for production

**Images not showing**
- Check `MEDIA_URL` and `MEDIA_ROOT` in `settings.py`
- Ensure `urls.py` includes `static(MEDIA_URL, ...)` at the end

---

Built with ❤️ using Django 🐍 | SQLite 🗄️ | Vanilla JS ⚡
