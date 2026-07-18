🍕 Food Delivery Web App

A full-stack food delivery application built with Django + SQLite + Vanilla JS. Modular, well-structured, and built following Django best practices with separate apps for auth, menu, cart, and orders.

🔗 Live Demo: [Add your PythonAnywhere link here]
🔗 GitHub: [Add repo link here]


📸 Screenshots


Add 3-4 screenshots or a short GIF here (home page, menu with filters, cart, order tracking). This is the first thing a recruiter looks at — don't skip it.




✨ Features


Browse menu with category filters (Pizza, Burger, Drinks, Biryani, Desserts, Sandwiches)
User registration, login, logout, and dashboard
Session-based shopping cart with AJAX — add/remove/update items with no page reload
Checkout flow with delivery details and Cash on Delivery
Order tracking with live status updates (placed → preparing → out for delivery → delivered)
Django admin panel for managing food items, categories, and order statuses



🗂️ Project Structure

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
│   ├── cart.py              (Cart class — core logic)
│   ├── context_processors.py
│   ├── views.py             (AJAX endpoints)
│   └── urls.py
│
├── orders/                 ← Checkout, Order placement, Order tracking
│   ├── models.py           (Order, OrderItem)
│   ├── forms.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
│
├── templates/               ← All HTML templates
│   ├── base.html            (Navbar, Footer, Messages layout)
│   ├── home.html            (Hero + Food grid)
│   ├── menu.html            (Sidebar filter + Food grid)
│   ├── cart.html            (Cart items + Summary)
│   ├── checkout.html        (Delivery form + COD)
│   ├── orders.html          (All orders list)
│   ├── order_detail.html    (Status tracker + Item details)
│   └── users/
│       ├── login.html
│       ├── register.html
│       └── dashboard.html
│
├── static/
│   ├── css/style.css        ← All styling (Terracotta + Cream theme)
│   └── js/main.js           ← Cart AJAX, Toast, Mobile menu
│
├── media/                   ← Uploaded food images (auto-created)
├── db.sqlite3                ← SQLite database (auto-created)
├── seed_data.py               ← Sample data script
└── manage.py


⚡ Setup & Installation

Step 1 — Clone the project

bashgit clone <your-repo-url>
cd food_delivery

Step 2 — Create and activate a virtual environment

bash# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

Step 3 — Install dependencies

bashpip install django pillow


pillow is required for handling food item images.



Step 4 — Apply database migrations

bashpython manage.py makemigrations
python manage.py migrate

Step 5 — Load sample data

bashpython seed_data.py

This creates:


6 categories: Pizza, Burger, Drinks, Biryani, Desserts, Sandwiches
20 sample food items with prices
An admin superuser (credentials printed in your terminal / set via env variable — see note below)



⚠️ Don't hardcode admin credentials in seed_data.py for anything beyond local testing. Read them from environment variables or prompt for input, e.g.:

pythonimport os
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme")



Step 6 — Run the server

bashpython manage.py runserver

Step 7 — Open in browser

URLPage/Home page/menu/Full menu with filters/register/Create account/login/Login/cart/View cart/orders/checkout/Checkout/orders/My orders/admin/Django admin panel


🛠️ How the Cart Works

The cart uses Django sessions — no extra database table needed:

pythonsession['cart'] = {
    "1": { "quantity": 2, "price": "199.00" },
    "3": { "quantity": 1, "price": "129.00" }
}

Adding an item triggers an AJAX POST to /cart/add/, which updates the cart badge count without a page reload. All logic lives in the Cart class in cart/cart.py.


🌐 URL Summary

URL PatternViewPurpose/menu.views.homeHome + food grid/menu/menu.views.menuFull menu + sidebar filter/register/users.views.register_viewRegistration/login/users.views.login_viewLogin/logout/users.views.logout_viewLogout/dashboard/users.views.dashboardUser dashboard/cart/cart.views.cart_detailView cart/cart/add/cart.views.cart_addAJAX: Add to cart/cart/remove/cart.views.cart_removeAJAX: Remove item/cart/update/cart.views.cart_updateAJAX: Update quantity/orders/checkout/orders.views.checkoutCheckout form/orders/orders.views.order_listAll orders/orders/<id>/orders.views.order_detailOrder detail + tracker


🧩 Models Overview

menu.Category

FieldTypeNotesnameCharFielde.g. "Pizza"iconCharFieldEmoji e.g. "🍕"

menu.FoodItem

FieldTypeNotesnameCharFieldItem namepriceDecimalFieldIn ₹categoryFK → CategoryimageImageFieldOptionalis_vegetarianBooleanFieldShows green badgeis_availableBooleanFieldHides if False

orders.Order

FieldTypeNotesuserFK → UseraddressTextFieldDelivery addressphoneCharFieldtotal_priceDecimalFieldstatusCharFieldplaced / preparing / out_for_delivery / deliveredpayment_methodCharFieldcod

orders.OrderItem

FieldTypeNotesorderFK → Orderfood_itemFK → FoodItemSET_NULL on deletefood_nameCharFieldSnapshot at order timefood_priceDecimalFieldSnapshot at order timequantityPositiveIntegerField


✅ Testing


Currently no automated tests. Planned additions:


Unit tests for Cart class (add/remove/update quantity logic)
View tests for order placement and status transitions
Auth flow tests (register/login/logout)


Run with: python manage.py test




🚀 Deployment

Deployed live on PythonAnywhere. To deploy your own copy:


Push code to GitHub
Create a PythonAnywhere web app pointed at your repo
Set DEBUG = False and configure ALLOWED_HOSTS in settings.py
Run python manage.py collectstatic
Set environment variables for SECRET_KEY and admin credentials (don't commit these)



🔭 Planned Improvements

FeatureNotesREST APIAdd Django REST Framework — serializers + ListAPIView for menu browsingOnline paymentIntegrate Razorpay/Stripe in orders/views.py checkoutFood ratingsNew Rating model in menu appSearchFilter menu using Q() objects in menu/views.pyEmail confirmationUse Django's send_mail() after order placementAutomated testsCover cart logic, order flow, and authCustom user profileExtend AbstractUser in users/models.py


❓ Troubleshooting

ModuleNotFoundError: No module named 'PIL'

bashpip install pillow

OperationalError: no such table

bashpython manage.py makemigrations
python manage.py migrate

Static files not loading


Ensure DEBUG = True locally, or run python manage.py collectstatic for production


Images not showing


Check MEDIA_URL and MEDIA_ROOT in settings.py
Ensure urls.py includes static(MEDIA_URL, ...) at the end
