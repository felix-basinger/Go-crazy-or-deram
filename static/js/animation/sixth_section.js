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

    // Наблюдаем за фото и текстом
    const animatedElements = document.querySelectorAll('.animate-photo-left, .animate-text-right');
    animatedElements.forEach(element => observer.observe(element));
});