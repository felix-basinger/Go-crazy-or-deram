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

    // Наблюдаем за заголовком и карточками
    const animatedElements = document.querySelectorAll('.animate-title-top, .animate-card-bottom');
    animatedElements.forEach(element => observer.observe(element));
});