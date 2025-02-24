document.addEventListener("DOMContentLoaded", () => {
    const orderButtons = document.querySelectorAll(".btn-order");
    const modalOverlay = document.getElementById("orderModal");
    const modalTitle = document.getElementById("modalTitle");
    const btnClose = document.querySelector(".btn-close");

    // Показать модальное окно
    orderButtons.forEach(button => {
        button.addEventListener("click", () => {
            const bookTitle = button.getAttribute("data-book");

            modalOverlay.style.display = "flex"; // Показать оверлей
        });
    });

    // Закрытие модального окна
    btnClose.addEventListener("click", () => {
        modalOverlay.style.display = "none"; // Скрыть оверлей
    });

    // Закрытие при клике на оверлей
    modalOverlay.addEventListener("click", (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.style.display = "none";
        }
    });
});
