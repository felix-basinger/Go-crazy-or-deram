document.addEventListener("DOMContentLoaded", function () {
    const options = {
        threshold: 0.3
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
            }
        });
    }, options);

    // Выбираем все элементы с анимацией
    const animatedElements = document.querySelectorAll('.animate-title, .animate-left, .animate-right');

    animatedElements.forEach(element => observer.observe(element));
});