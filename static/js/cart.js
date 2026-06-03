document.addEventListener('click', function (e) {
    const plus = e.target.closest('.cart-qty-plus');
    const minus = e.target.closest('.cart-qty-minus');

    if (plus) {
        const item = plus.closest('.cart-item');
        const input = item.querySelector('.cart-qty-input');
        const price = parseFloat(item.dataset.price);
        const totalBox = item.querySelector('.cart-item-total');

        input.value = parseInt(input.value || '1', 10) + 1;
        totalBox.textContent = (price * parseInt(input.value, 10)).toFixed(2) + ' ₽';
        updateCartTotal();
        return;
    }

    if (minus) {
        const item = minus.closest('.cart-item');
        const input = item.querySelector('.cart-qty-input');
        const price = parseFloat(item.dataset.price);
        const totalBox = item.querySelector('.cart-item-total');

        let current = parseInt(input.value || '1', 10);
        if (current > 1) {
            current -= 1;
            input.value = current;
            totalBox.textContent = (price * current).toFixed(2) + ' ₽';
            updateCartTotal();
        }
    }
});

function updateCartTotal() {
    let total = 0;
    document.querySelectorAll('.cart-item').forEach(item => {
        const price = parseFloat(item.dataset.price);
        const qty = parseInt(item.querySelector('.cart-qty-input').value || '1', 10);
        total += price * qty;
    });

    const totalBox = document.querySelector('.summary-total strong');
    const totalRow = document.querySelector('.summary-row strong');
    if (totalBox) totalBox.textContent = total.toFixed(2) + ' ₽';
    if (totalRow) totalRow.textContent = total.toFixed(2) + ' ₽';
}