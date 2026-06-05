document.addEventListener('click', function (e) {
    const plus = e.target.closest('.cart-qty-plus');
    const minus = e.target.closest('.cart-qty-minus');
    const removeBtn = e.target.closest('.cart-remove-btn');

    if (plus) {
        const item = plus.closest('.cart-item');
        const input = item.querySelector('.cart-qty-input');
        const form = item.querySelector('.cart-qty-form');

        let qty = parseInt(input.value || '1', 10) + 1;
        const maxQty = parseInt(input.max || '999999', 10);
        if (qty > maxQty) qty = maxQty;

        input.value = qty;
        recalcItem(item, qty);
        updateCartTotal();
        if (form) form.submit();
        return;
    }

    if (minus) {
        const item = minus.closest('.cart-item');
        const input = item.querySelector('.cart-qty-input');
        const form = item.querySelector('.cart-qty-form');

        let qty = parseInt(input.value || '1', 10);
        if (qty > 1) {
            qty -= 1;
            input.value = qty;
            recalcItem(item, qty);
            updateCartTotal();
            if (form) form.submit();
        }
        return;
    }

    if (removeBtn) {
        e.preventDefault();
        const form = removeBtn.closest('.cart-remove-form');
        if (form && confirm('Вы уверены, что хотите удалить этот товар из корзины?')) {
            form.submit();
        }
    }
});

function recalcItem(item, qty) {
    const oldPrice = parseFloat(item.dataset.oldPrice);
    const discountedPrice = parseFloat(item.dataset.discountedPrice);
    const minQty = parseInt(item.dataset.minQty || '1', 10);
    const hasDiscount = item.dataset.hasDiscount === '1';
    const totalBox = item.querySelector('.cart-item-total');

    if (hasDiscount && qty >= minQty) {
        const oldTotal = (oldPrice * qty).toFixed(2) + ' ₽';
        const newTotal = (discountedPrice * qty).toFixed(2) + ' ₽';
        totalBox.innerHTML = `<span class="old-price">${oldTotal}</span><span class="new-price">${newTotal}</span>`;
        item.dataset.price = discountedPrice;
    } else {
        totalBox.innerHTML = `<span>${(oldPrice * qty).toFixed(2)} ₽</span>`;
        item.dataset.price = oldPrice;
    }
}

function updateCartTotal() {
    let total = 0;

    document.querySelectorAll('.cart-item').forEach(item => {
        const qty = parseInt(item.querySelector('.cart-qty-input').value || '1', 10);
        const hasDiscount = item.dataset.hasDiscount === '1';
        const minQty = parseInt(item.dataset.minQty || '1', 10);
        const oldPrice = parseFloat(item.dataset.oldPrice);
        const discountedPrice = parseFloat(item.dataset.discountedPrice);

        if (hasDiscount && qty >= minQty) {
            total += discountedPrice * qty;
        } else {
            total += oldPrice * qty;
        }
    });

    const totalBox = document.querySelector('.summary-total strong');
    const totalRow = document.querySelector('.summary-row strong');
    if (totalBox) totalBox.textContent = total.toFixed(2) + ' ₽';
    if (totalRow) totalRow.textContent = total.toFixed(2) + ' ₽';
}

document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('guest-checkout-btn');
    const modal = document.getElementById('auth-modal');

    if (btn && modal) {
        btn.addEventListener('click', function () {
            modal.classList.add('is-open');
        });

        modal.addEventListener('click', function (e) {
            if (e.target.matches('[data-close-auth-modal]')) {
                modal.classList.remove('is-open');
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', updateCartTotal);