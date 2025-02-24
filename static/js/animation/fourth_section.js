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

    // Наблюдаем за текстом и блоками страниц
    const animatedElements = document.querySelectorAll('.animate-top, .animate-bottom');
    animatedElements.forEach(element => observer.observe(element));
});
