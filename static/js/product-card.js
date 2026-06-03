document.addEventListener('click', function (e) {
    const plus = e.target.closest('.qty-plus');
    const minus = e.target.closest('.qty-minus');

    if (plus) {
        const box = plus.closest('.qty');
        const input = box.querySelector('.qty-input');
        input.value = parseInt(input.value || '1', 10) + 1;
        return;
    }

    if (minus) {
        const box = minus.closest('.qty');
        const input = box.querySelector('.qty-input');
        const current = parseInt(input.value || '1', 10);
        input.value = current > 1 ? current - 1 : 1;
    }
});