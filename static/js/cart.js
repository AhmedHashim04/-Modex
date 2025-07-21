document.addEventListener('DOMContentLoaded', function () {
    initializeCartForms();
    setupQuantityButtons();
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

function updateCartIndicator(count) {
    document.querySelectorAll('.cart-counter').forEach(counter => {
        counter.textContent = count;
    });
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

    if (source) {
        formData.append('source', source);
    }

    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;

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

                if (html) {
                    instance.innerHTML = html;
                }
            });

            initializeCartForms();
            setupQuantityButtons();
        }

        if (data.cart_count !== undefined) {
            updateCartIndicator(data.cart_count);
            animateCartIcon();
        }

    } catch (err) {
        console.error(err);
        showToast("A network error occurred.", 'error');  // تأكد أنك معرف showToast في سكريبت تاني أو من مكتبة
    } finally {
        if (submitBtn) submitBtn.disabled = false;
    }
}

function initializeCartForms() {
    document.querySelectorAll('.product-cart-form').forEach(form => {
        form.replaceWith(form.cloneNode(true));  // إزالة الأحداث القديمة
    });

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
