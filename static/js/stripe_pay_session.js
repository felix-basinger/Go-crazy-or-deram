let isSubmitting = false;

function redirectToLiqPay(formId, deliveryType) {


    const form = document.getElementById(formId);
    if (!validateForm(form)) {
        return;  // Если форма не прошла валидацию, прекращаем выполнение
    }

    isSubmitting = true;

    const formData = new FormData(form);
    formData.append('delivery_type', deliveryType);
    const currentLang = document.documentElement.lang || form.querySelector('input[name="lang"]').value || 'ua';
    formData.append('lang', currentLang);

    fetch("/create-checkout-session/", {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Ошибка создания платежной сессии: " + data.error);
        } else {
            const paymentForm = document.createElement('form');
            paymentForm.method = 'POST';
            paymentForm.action = 'https://www.liqpay.ua/api/3/checkout';
            paymentForm.innerHTML = `
                <input type="hidden" name="data" value="${data.data}" />
                <input type="hidden" name="signature" value="${data.signature}" />
            `;
            document.body.appendChild(paymentForm);
            paymentForm.submit();
        }
    })
    .catch(error => {
        console.error("Ошибка:", error);
        alert("Произошла ошибка при создании платежной сессии.");
    })
    .finally(() => {
        isSubmitting = false;  // Сброс флага после завершения запроса
    });
}

// Мониторинг статуса платежа через обратный вызов
function monitorPaymentStatus(orderId, lang) {
    setTimeout(() => {
        fetch(`/check-payment-status/?order_id=${orderId}&lang=${lang}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = `/payment_success/?lang=${lang}`;
            } else if (data.redirect_url) {
                window.location.href = data.redirect_url;  // Перенаправление на страницу отмены
            } else {
                window.location.href = `/payment_cancel/?lang=${lang}`;
            }
        })
        .catch(error => {
            console.error("Ошибка проверки статуса платежа:", error);
            alert("Ошибка при проверке статуса платежа.");
        });
    }, 5000); // Задержка перед проверкой
}

// Функция для валидации формы
function validateForm(form) {
    let isValid = true;

    form.querySelectorAll(".error-message").forEach(el => el.remove());
    form.querySelectorAll(".form-control").forEach(el => el.classList.remove("is-invalid"));

    form.querySelectorAll(".form-control[required]").forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add("is-invalid");

            const error = document.createElement("div");
            error.className = "error-message text-danger mt-1";
            error.textContent = "Поле обязательно для заполнения.";
            input.parentNode.appendChild(error);
        }
    });

    return isValid;
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.btn-submit').forEach(button => {
        button.addEventListener('click', function () {
            const formId = button.closest('form').id;
            const deliveryType = formId === 'ukraineForm' ? 'ukraine' : 'world';
            redirectToLiqPay(formId, deliveryType);
        });
    });
});
