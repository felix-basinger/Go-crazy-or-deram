document.addEventListener("DOMContentLoaded", () => {
    const pages = document.querySelectorAll(".book-page");
    let currentPage = 0;

    const btnNext = document.querySelector(".btn-next");
    const btnPrev = document.querySelector(".btn-prev");

    // Инициализация начальных стилей страниц
    function initializePages() {
        pages.forEach((page, index) => {
            page.style.zIndex = pages.length - index; // Правильное наложение страниц
            page.style.transform = "rotateY(0deg)"; // Все страницы начинаются с начального положения
        });
        updateButtonsState(); // Проверка состояния кнопок при загрузке
    }

    // Функция для перелистывания вперед с задержкой изменения z-index
    function nextPage() {
        if (currentPage < pages.length - 1) {
            pages[currentPage].style.transform = `rotateY(-180deg)`; // Поворачиваем текущую страницу

            // Задержка перед изменением z-index, чтобы страница успела полностью повернуться
            setTimeout(() => {
                pages[currentPage].style.zIndex = currentPage;
                currentPage++;
                updateButtonsState(); // Обновляем состояние кнопок
            }, 100);
        }
    }

    // Функция для перелистывания назад с мгновенным изменением z-index
    function prevPage() {
        if (currentPage > 0) {
            currentPage--;
            pages[currentPage].style.zIndex = pages.length - currentPage; // Восстанавливаем z-index
            pages[currentPage].style.transform = `rotateY(0deg)`; // Возвращаем страницу в исходное положение
            updateButtonsState(); // Обновляем состояние кнопок
        }
    }

    // Функция для управления состоянием кнопок
    function updateButtonsState() {
        btnPrev.disabled = currentPage === 0; // Блокируем кнопку "Назад" на первой странице
        btnNext.disabled = currentPage === pages.length - 1; // Блокируем кнопку "Вперед" на последней странице
    }

    // Инициализация страниц при загрузке
    initializePages();

    // Обработчики событий на кнопки
    btnNext.addEventListener("click", nextPage);
    btnPrev.addEventListener("click", prevPage);
});
