document.addEventListener('DOMContentLoaded', function () {
    initializeCartForms();
    setupQuantityButtons();
    fetchCartCountSafe();
});

document.addEventListener('cartUpdated', function (e) {
    updateCartCounter(e.detail.count);
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function animateCartIcon() {
    const icon = document.querySelector('#cart-link i.fa-shopping-cart');
    if (icon) {
        icon.classList.add('animate-bounce');
        setTimeout(() => icon.classList.remove('animate-bounce'), 800);
    }
}

async function handleCartFormSubmit(form, actionType) {
    const csrfToken = getCookie('csrftoken');
    const formData = new FormData(form);
    const source = form.dataset.source;

    if (source) formData.append('source', source);

    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.add('disabled');
    }

    try {
        const res = await fetch(form.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData,
        });

        const data = await res.json();

        if (data.success && data.product_slug && data.updated_htmls) {
            const instances = document.querySelectorAll(`[data-product-slug="${data.product_slug}"]`);
            instances.forEach(instance => {
                const source = instance.dataset.source;
                const html = data.updated_htmls[source];
                if (html) instance.innerHTML = html;
            });

            initializeCartForms();
            setupQuantityButtons();
        }

        if (data.cart_count !== undefined) {
            updateCartCounter(data.cart_count);
            animateCartIcon();
        }

    } catch (err) {
        if (err.name !== 'AbortError') {
            console.error("🛑 Network error in cart submission:", err);
        }
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('disabled');
        }
    }
}

function initializeCartForms() {
    document.querySelectorAll('.product-cart-form').forEach(form => {
        if (!form.dataset.initialized) {
            form.dataset.initialized = 'true';
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                const type = this.id.startsWith('add') ? 'add' : 'remove';
                handleCartFormSubmit(this, type);
            });
        }
    });
}

function setupQuantityButtons() {
    document.querySelectorAll('.quantity-btn.minus').forEach(btn => {
        btn.addEventListener('click', function () {
            const input = this.parentElement.querySelector('.quantity-input');
            const min = parseInt(input.min);
            if (parseInt(input.value) > min) input.value = parseInt(input.value) - 1;
        });
    });

    document.querySelectorAll('.quantity-btn.plus').forEach(btn => {
        btn.addEventListener('click', function () {
            const input = this.parentElement.querySelector('.quantity-input');
            const max = parseInt(input.max);
            if (parseInt(input.value) < max) input.value = parseInt(input.value) + 1;
        });
    });
}

window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.modex-navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

document.querySelectorAll('.modex-subnav-link').forEach(link => {
    link.addEventListener('click', function () {
        document.querySelectorAll('.modex-subnav-link').forEach(el => {
            el.classList.remove('active-category');
        });
        this.classList.add('active-category');
    });
});

async function fetchCartCount() {
    try {
        const response = await fetch('/cart/count/', {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        if (!response.ok) throw new Error(`Status ${response.status}`);
        const data = await response.json();
        updateCartCounter(data.count || 0);
    } catch (error) {
        console.warn("⚠️ Failed to load cart count:", error.message);
    }
}

function fetchCartCountSafe(attempts = 5) {
    const cartCounter = document.querySelector('.cart-counter');
    if (!cartCounter) {
        if (attempts > 0) {
            return setTimeout(() => fetchCartCountSafe(attempts - 1), 500);
        } else {
            console.warn("⚠️ Cart counter element not found after multiple attempts.");
            return;
        }
    }
    fetchCartCount();
}

function updateCartCounter(count, animate = true) {
    document.querySelectorAll('.cart-counter').forEach(counter => {
        if (parseInt(counter.textContent) !== count) {
            if (animate) {
                counter.classList.add('counter-update');
                setTimeout(() => {
                    counter.classList.remove('counter-update');
                }, 500);
            }
            counter.textContent = count;
        }
    });
}
