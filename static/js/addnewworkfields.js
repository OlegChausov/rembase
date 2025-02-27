    document.getElementById('toggle-button').addEventListener('click', function () {
        var hiddenBlock = document.getElementById('block-2');
        hiddenBlock.classList.toggle('hidden');

        // Проверка состояния блока и изменение текста кнопки
        if (hiddenBlock.classList.contains('hidden')) {
            this.textContent = 'Добавить еще работы';
        } else {
            this.textContent = 'Скрыть поля работы';
        }
    });