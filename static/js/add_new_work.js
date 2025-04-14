document.addEventListener('DOMContentLoaded', function () {
    console.log("Страница загружена, скрипт активирован."); // Лог запуска скрипта

    // Кнопка добавления работы и контейнеры
    const addWorkButton = document.getElementById('add-work-button');
    const workFormsContainer = document.getElementById('work-forms');
    const emptyFormTemplate = document.getElementById('empty-form');
    const totalFormsInput = document.querySelector('#id_works-TOTAL_FORMS');

    // Проверка наличия необходимых элементов
    if (!addWorkButton || !workFormsContainer || !emptyFormTemplate || !totalFormsInput) {
        console.error("Ошибка: Один из необходимых элементов не найден!");
        return;
    }

    console.log("Все необходимые элементы найдены.");

    // Добавление новой формы
    addWorkButton.addEventListener('click', function () {
        console.log("Нажата кнопка 'Добавить работу'.");

        const currentFormCount = parseInt(totalFormsInput.value, 10);
        console.log("Текущее количество форм:", currentFormCount);

        const newFormHtml = emptyFormTemplate.innerHTML.replace(/__prefix__/g, currentFormCount);

        totalFormsInput.value = currentFormCount + 1; // Увеличиваем счётчик форм
        console.log("Обновлено значение TOTAL_FORMS:", totalFormsInput.value);

        const newFormDiv = document.createElement('div');
        newFormDiv.classList.add('work-form');
        newFormDiv.innerHTML = newFormHtml;

        workFormsContainer.appendChild(newFormDiv); // Добавляем новую форму
        console.log("Новая форма добавлена в контейнер:", newFormDiv);
    });

    // Отслеживание изменения чекбоксов удаления
    document.addEventListener('change', function (e) {
        if (e.target.matches('input[type="checkbox"][name$="-DELETE"]')) {
            console.log("Чекбокс удаления изменён. Элемент:", e.target);

            const formContainer = e.target.closest('.work-form');
            console.log("Пытаемся найти контейнер формы. Результат:", formContainer);

            if (formContainer) {
                // Скрываем весь контейнер формы
                formContainer.classList.toggle('hidden', e.target.checked);
                console.log(
                    "Контейнер формы обновлён. Добавлен класс hidden:",
                    formContainer.classList.contains('hidden')
                );

                // Скрываем отдельные поля формы по ID
                const fieldSelectors = [
                    '[id^="id_works-"][id$="-description"]',
                    '[id^="id_works-"][id$="-price"]',
                    '[id^="id_works-"][id$="-warranty"]'
                ];
                fieldSelectors.forEach((selector) => {
                    const fields = document.querySelectorAll(selector);
                    fields.forEach((field) => {
                        if (field.closest('.work-form') === formContainer) {
                            field.classList.toggle('hidden', e.target.checked);
                            console.log(`Поле ${field.id} теперь скрыто:`, e.target.checked);
                        }
                    });
                });
            } else {
                console.error("Контейнер формы не найден для чекбокса:", e.target);
            }
        }
    });
});
