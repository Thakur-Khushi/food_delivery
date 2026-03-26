/**
 * QuickBite — Main JavaScript
 * Handles: Cart AJAX calls, Toast notifications, Mobile menu, Dynamic updates
 */

// ===== CSRF TOKEN (needed for Django AJAX POST requests) =====
// Get CSRF token from cookie set by Django
function getCsrfToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
        const [key, val] = c.trim().split('=');
        if (key === name) return decodeURIComponent(val);
    }
    return '';
}

// ===== TOAST NOTIFICATION =====
/**
 * Show a temporary toast message at bottom-right
 * @param {string} message - Message to display
 * @param {number} duration - Duration in ms (default: 2500)
 */
function showToast(message, duration = 2500) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), duration);
}

// ===== ADD TO CART (AJAX) =====
/**
 * Add a food item to cart via AJAX — no page reload!
 * Updates cart badge count and shows toast.
 * @param {number} itemId - FoodItem ID
 * @param {string} itemName - Item display name
 */
async function addToCart(itemId, itemName) {
    const btn = document.querySelector(`.btn-add-cart[data-item-id="${itemId}"]`);

    try {
        // Visual feedback on button click
        if (btn) {
            btn.classList.add('adding');
            btn.textContent = '✓ Added!';
        }

        const response = await fetch('/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                item_id: itemId,
                quantity: 1,
                action: 'add'
            })
        });

        const data = await response.json();

        if (data.success) {
            // Update the cart badge in navbar
            const badge = document.getElementById('cart-badge');
            if (badge) {
                badge.textContent = data.cart_count;
                // Animate the badge
                badge.style.transform = 'scale(1.4)';
                setTimeout(() => badge.style.transform = 'scale(1)', 300);
            }
            showToast(`🛒 ${itemName} added to cart!`);
        } else {
            showToast('❌ ' + (data.error || 'Could not add item.'));
        }
    } catch (error) {
        console.error('Cart add error:', error);
        showToast('❌ Network error. Try again.');
    } finally {
        // Restore button after delay
        if (btn) {
            setTimeout(() => {
                btn.classList.remove('adding');
                btn.innerHTML = '<span class="btn-icon">+</span> Add to Cart';
            }, 1200);
        }
    }
}

// ===== MOBILE MENU TOGGLE =====
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    if (menu) {
        menu.classList.toggle('open');
    }
}

// ===== AUTO-DISMISS ALERTS =====
// Django messages auto-dismiss after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// ===== CLOSE MOBILE MENU ON OUTSIDE CLICK =====
document.addEventListener('click', function (e) {
    const menu = document.getElementById('mobile-menu');
    const toggle = document.querySelector('.nav-toggle');
    if (menu && toggle && !menu.contains(e.target) && !toggle.contains(e.target)) {
        menu.classList.remove('open');
    }
});

// ===== CATEGORY FILTER (home page) =====
// Category pills filtering via URL (handled by Django view)
// JS just adds smooth transitions
document.querySelectorAll('.pill').forEach(pill => {
    pill.addEventListener('click', function () {
        document.querySelectorAll('.pill').forEach(p => p.classList.remove('pill-active'));
        this.classList.add('pill-active');
    });
});
