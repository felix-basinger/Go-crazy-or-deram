document.addEventListener("DOMContentLoaded", () => {
        let lastScrollTop = 0;
        const navbar = document.querySelector(".navbar");
        const navbarToggler = document.querySelector(".navbar-toggler");
        const navbarCollapse = document.querySelector("#navbarNav");
        const navLinks = document.querySelectorAll(".nav-link");
        let scrollEnabled = true;  // Флаг для включения/выключения скролла

        // Проверка состояния меню
        const isNavbarOpen = () => navbarCollapse.classList.contains('show');

        // Обработчик прокрутки
        const handleScroll = () => {
            if (!scrollEnabled) return;  // Отключаем скролл, если меню открыто

            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            if (scrollTop > lastScrollTop) {
                navbar.style.top = "-75px";  // Скрываем навбар при скролле вниз
            } else {
                navbar.style.top = "0";  // Показываем навбар при скролле вверх
            }
            lastScrollTop = scrollTop;
        };

        window.addEventListener("scroll", handleScroll);

        // Управление скроллом при открытии/закрытии меню
        navbarToggler.addEventListener("click", () => {
            if (isNavbarOpen()) {
                scrollEnabled = false;  // Отключаем скролл при открытии меню
            } else {
                setTimeout(() => {
                    scrollEnabled = true;  // Включаем скролл после закрытия меню
                }, 300);  // Небольшая задержка для завершения анимации закрытия
            }
        });

        // Закрытие меню при клике на ссылку с якорем
        navLinks.forEach((link) => {
            link.addEventListener("click", () => {
                if (isNavbarOpen()) {
                    bootstrap.Collapse.getInstance(navbarCollapse)?.hide();  // Закрываем меню
                    scrollEnabled = true;  // Включаем скролл после закрытия меню
                }
            });
        });

        // Закрытие меню при клике вне меню
        document.addEventListener("click", (e) => {
            if (!navbarToggler.contains(e.target) && !navbarCollapse.contains(e.target)) {
                bootstrap.Collapse.getInstance(navbarCollapse)?.hide();
                scrollEnabled = true;  // Включаем скролл после закрытия меню
            }
        });
    });