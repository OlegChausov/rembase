// static/my_app/js/undercut.js
document.addEventListener("DOMContentLoaded", function() {
    console.log('JavaScript file loaded'); // Проверка загрузки файла
    const toggleButton = document.getElementById('toggle-button');
    const hiddenBlock = document.getElementById('hidden-block');

    if (!toggleButton) {
        console.error('Toggle button not found');
        return;
    }

    if (!hiddenBlock) {
        console.error('Hidden block not found');
        return;
    }

    toggleButton.addEventListener('click', function() {
        console.log('Button clicked');
        if (hiddenBlock.classList.contains('hidden')) {
            hiddenBlock.classList.remove('hidden');
            toggleButton.textContent = 'Скрыть дополнительные поля';
        } else {
            hiddenBlock.classList.add('hidden');
            toggleButton.textContent = 'Показать дополнительные поля';
        }
    });
});
