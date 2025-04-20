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
// Обработчик закрытия модального окна
    document.getElementById('closeModal').addEventListener('click', function() {
        document.getElementById('modal').style.display = 'none';
    });

    document.getElementById('submitModal').addEventListener('click', function () {
        console.log("Кнопка 'Сохранить' нажата.");
    
        const descriptionInput = document.getElementById('new_work_description_name');
        if (!descriptionInput) {
            console.error("Поле ввода описания (new_work_description_name) не найдено.");
            return;
        }
    
        const description = descriptionInput.value.trim();
        if (!description) {
            alert("Пожалуйста, введите описание работы.");
            console.warn("Поле описания пустое.");
            return;
        }
    
        // Отправка данных на сервер через fetch
        console.log("Начинается отправка данных на сервер...");
        fetch('/api/typical_work_create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ description: description })
        })
        .then(response => {
            console.log("Ответ от сервера получен. Статус ответа:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Данные от сервера:", data);
    
            if (data.success) {
                alert("Услуга успешно добавлена!");
                console.log("Объект TypicalWork создан с ID:", data.typicwork.id);
    
                // Очистка поля ввода
                descriptionInput.value = "";
    
                // Закрытие модального окна
                document.getElementById('modal').style.display = 'none';
                console.log("Модальное окно скрыто.");
            } else {
                alert("Ошибка: " + data.error);
                console.warn("Ошибка от API:", data.error);
            }
        })
        .catch(error => {
            console.error("Произошла ошибка при запросе:", error);
            alert("Ошибка связи с сервером.");
        });
    });


    

});

    
