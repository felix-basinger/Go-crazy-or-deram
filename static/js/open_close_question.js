document.addEventListener("DOMContentLoaded", () => {
    const faqItems = document.querySelectorAll(".faq-item");

    faqItems.forEach(item => {
        const question = item.querySelector(".faq-question");
        const answer = item.querySelector(".faq-answer");
        const icon = question.querySelector("i");

        question.addEventListener("click", () => {
            // Закрыть все ответы, кроме текущего
            faqItems.forEach(i => {
                if (i !== item) {
                    i.querySelector(".faq-answer").style.display = "none";
                    i.querySelector(".faq-question").classList.remove("open");
                }
            });

            // Переключение видимости текущего ответа
            if (answer.style.display === "block") {
                answer.style.display = "none";
                question.classList.remove("open");
            } else {
                answer.style.display = "block";
                question.classList.add("open");
            }
        });
    });
});
