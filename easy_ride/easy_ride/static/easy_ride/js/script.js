document.addEventListener('DOMContentLoaded', function() {
    const nextBtn = document.getElementById('next-review-btn');
    const currentReview = document.getElementById('current-review');
    const reviewItems = document.querySelectorAll('.review-item');

    let currentIndex = 0;

    // Функция обновления отзыва
    function updateReview(index) {
        const review = reviewItems[index];
        currentReview.querySelector('strong').textContent = review.dataset.name;
        currentReview.querySelector('p').childNodes[3].textContent = review.dataset.message;
        currentReview.querySelector('img').src = review.dataset.avatar;

        // Анимация
        currentReview.style.animation = 'none';
        void currentReview.offsetWidth; // Trigger reflow
        currentReview.style.animation = 'fadeIn 0.5s ease';
    }

    // Обработчик кнопки
    nextBtn.addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % reviewItems.length;
        updateReview(currentIndex);
    });

    // Инициализация анимации при загрузке
    currentReview.style.animation = 'fadeIn 0.5s ease';
});
