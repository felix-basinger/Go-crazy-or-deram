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

    // Наблюдаем за заголовком и отзывами
    const animatedElements = document.querySelectorAll('.animate-title-right, .animate-reviews-left');
    animatedElements.forEach(element => observer.observe(element));
});