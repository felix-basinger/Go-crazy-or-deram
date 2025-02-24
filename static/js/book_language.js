function setBookLanguage(button) {
    // Получаем выбранный язык книги
    const bookLanguage = button.getAttribute('data-book-language');

    // Устанавливаем язык книги в обе формы
    document.getElementById('book_language_ukraine').value = bookLanguage;
    document.getElementById('book_language_world').value = bookLanguage;

}