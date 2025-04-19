document.addEventListener('DOMContentLoaded', function () {
    console.log("Страница загружена, скрипт активирован.");

    const addWorkButton = document.getElementById('add-work-button');
    const workFormsContainer = document.getElementById('work-forms');
    const emptyFormTemplate = document.getElementById('empty-form');
    const totalFormsInput = document.querySelector('#id_works-TOTAL_FORMS');
    const modal = document.getElementById("modal");

    if (!addWorkButton || !workFormsContainer || !emptyFormTemplate || !totalFormsInput || !modal) {
        console.error("Ошибка: Один из необходимых элементов не найден!");
        return;
    }

    console.log("Все необходимые элементы найдены.");

    // Функция для инициализации Select2 на заданном элементе <select>
    function initializeSelect2WithEvents(selectElement) {
        if (selectElement) {
            $(selectElement).select2({
                width: '600px' // Устанавливаем ширину
            }).on('select2:select', function (e) {
                const selectedValue = e.params.data.id; // Получаем значение
                console.log(`Выбрано значение: ${selectedValue} в select с ID: ${this.id}`);
                handleSelectChange(this, selectedValue);
            });
            console.log("Select2 инициализирован для элемента:", selectElement);
        } else {
            console.error("Элемент <select> не найден для инициализации Select2.");
        }
    }

    // Инициализация Select2 при загрузке страницы для существующих форм
    const initialSelectFields = document.querySelectorAll('.work-form:not(.hidden) .form-control[id$="-description"]');
    initialSelectFields.forEach(initializeSelect2WithEvents);
    console.log("Select2 инициализирован для существующих полей description при загрузке.");

    // Добавление новой формы
    addWorkButton.addEventListener('click', function () {
        console.log("Нажата кнопка 'Добавить работу'.");

        const currentFormCount = parseInt(totalFormsInput.value, 10);
        console.log("Текущее количество форм:", currentFormCount);

        // Заменяем префикс на текущий индекс формы
        const newFormHtml = emptyFormTemplate.innerHTML.replace(/__prefix__/g, currentFormCount);

        totalFormsInput.value = currentFormCount + 1;
        console.log("Обновлено значение TOTAL_FORMS:", totalFormsInput.value);

        const newFormDiv = document.createElement('div');
        newFormDiv.classList.add('work-form');
        newFormDiv.innerHTML = newFormHtml;

        workFormsContainer.appendChild(newFormDiv);
        console.log("Новая форма добавлена в контейнер:", newFormDiv);

        // Инициализация Select2 для нового элемента description
        const newSelectField = newFormDiv.querySelector('.form-control[id$="-description"]');
        initializeSelect2WithEvents(newSelectField);
    });

    // Отслеживание изменения чекбоксов удаления
    document.addEventListener('change', function (e) {
        if (e.target.matches('input[type="checkbox"][name$="-DELETE"]')) {
            console.log("Чекбокс удаления изменён. Элемент:", e.target);

            const formContainer = e.target.closest('.work-form');
            console.log("Контейнер формы:", formContainer);

            if (formContainer) {
                const isChecked = e.target.checked;
                formContainer.classList.toggle('hidden', isChecked);
                console.log("Контейнер формы скрыт:", isChecked);

                // Получаем <select> элемент description в текущей форме
                const descriptionField = formContainer.querySelector('.form-control[id$="-description"]');

                if (isChecked) {
                    // Если чекбокс установлен, уничтожаем Select2, чтобы избежать проблем
                    if ($(descriptionField).hasClass('select2-hidden-accessible')) {
                        $(descriptionField).select2('destroy');
                        console.log("Select2 уничтожен для скрытой формы description.");
                    }
                } else {
                    // Если чекбокс снят, инициализируем Select2 заново
                    initializeSelect2WithEvents(descriptionField);
                    console.log("Select2 инициализирован заново для отображенной формы description.");
                }
            } else {
                console.error("Контейнер формы не найден для чекбокса:", e.target);
            }
        }
    });

    // Обработка изменения значения (при выборе "new")
    function handleSelectChange(selectElement, selectedValue) {
        if (selectedValue === "new") {
            modal.style.display = "block"; // Показываем модальное окно
            console.log("Модальное окно открыто.");
        } else {
            modal.style.display = "none"; // Скрываем модальное окно
            console.log("Модальное окно скрыто.");
        }
    }
});
