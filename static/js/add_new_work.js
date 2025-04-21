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

    function initializeSelect2WithEvents(selectElement) {
        console.log("Инициализация Select2 для элемента:", selectElement);
        if (selectElement) {
            $(selectElement).select2({
                width: '600px'
            }).on('select2:select', function (e) {
                const selectedValue = e.params.data.id;
                console.log(`Выбрано значение: ${selectedValue} в select с ID: ${this.id}`);
                handleSelectChange(this, selectedValue);
            });
        } else {
            console.error("Элемент <select> не найден для инициализации Select2.");
        }
    }

    console.log("Проверка наличия полей price и warranty...");
    console.log("Поле price:", document.querySelector('#id_price'));
    console.log("Поле warranty:", document.querySelector('#id_warranty'));

    const initialSelectFields = document.querySelectorAll('.work-form:not(.hidden) .form-control[id$="-description"]');
    console.log("Найдено селектов для инициализации:", initialSelectFields.length);
    initialSelectFields.forEach(initializeSelect2WithEvents);

    addWorkButton.addEventListener('click', function () {
        console.log("Нажата кнопка 'Добавить работу'.");

        const currentFormCount = parseInt(totalFormsInput.value, 10);
        console.log("Текущее количество форм:", currentFormCount);

        const newFormHtml = emptyFormTemplate.innerHTML.replace(/__prefix__/g, currentFormCount);
        totalFormsInput.value = currentFormCount + 1;
        console.log("Обновлено значение TOTAL_FORMS:", totalFormsInput.value);

        const newFormDiv = document.createElement('div');
        newFormDiv.classList.add('work-form');
        newFormDiv.innerHTML = newFormHtml;

        workFormsContainer.appendChild(newFormDiv);
        console.log("Новая форма добавлена в контейнер:", newFormDiv);

        const newSelectField = newFormDiv.querySelector('.form-control[id$="-description"]');
        initializeSelect2WithEvents(newSelectField);
    });

    document.addEventListener('change', function (e) {
        if (e.target.matches('input[type="checkbox"][name$="-DELETE"]')) {
            console.log("Чекбокс удаления изменён. Элемент:", e.target);

            const formContainer = e.target.closest('.work-form');
            console.log("Контейнер формы найден:", formContainer);

            if (formContainer) {
                const isChecked = e.target.checked;
                console.log("Состояние чекбокса:", isChecked);
                formContainer.classList.toggle('hidden', isChecked);

                const descriptionField = formContainer.querySelector('.form-control[id$="-description"]');
                if (isChecked) {
                    if ($(descriptionField).hasClass('select2-hidden-accessible')) {
                        $(descriptionField).select2('destroy');
                        console.log("Select2 уничтожен для скрытой формы description.");
                    }
                } else {
                    initializeSelect2WithEvents(descriptionField);
                    console.log("Select2 заново инициализирован для формы.");
                }
            } else {
                console.error("Контейнер формы не найден для чекбокса:", e.target);
            }
        }
    });

    function handleSelectChange(selectElement, selectedValue) {
        console.log(`Обрабатывается выбор значения: ${selectedValue} в select ID: ${selectElement.id}`);
        if (selectedValue === "new") {
            modal.style.display = "block";
            console.log("Модальное окно открыто.");
        } else {
            modal.style.display = "none";
            console.log("Модальное окно скрыто.");
        }
    }

    document.getElementById('closeModal').addEventListener('click', function() {
        console.log("Нажата кнопка закрытия модального окна.");
        document.getElementById('modal').style.display = 'none';
    });

    document.getElementById('submitModal').addEventListener('click', function () {
        console.log("Кнопка 'Сохранить' нажата.");
    
        const priceField = document.querySelector('#id_price');
        const warrantyField = document.querySelector('#id_warranty');
    
        console.log("Перед отправкой формы:");
        console.log("price:", priceField ? priceField.value : "Элемент не найден");
        console.log("warranty:", warrantyField ? warrantyField.value : "Элемент не найден");
    
        const requestData = {
            description: document.getElementById('new_work_description_name').value.trim(),
            price: priceField && priceField.value ? priceField.value : null,
            warranty: warrantyField && warrantyField.value ? warrantyField.value : null
        };
    
        console.log("Данные, отправляемые в запрос:", requestData);
    
        fetch('/api/typical_work_create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Ответ от сервера:", data);
        })
        .catch(error => {
            console.error("Ошибка при отправке данных:", error);
        });
    });

    function updateSelectFields() {
        console.log("Запуск обновления всех select-полей...");
        fetch('/api/typical_work_data/')
            .then(response => response.json())
            .then(data => {
                console.log("Полученные данные для обновления select:", data);

                document.querySelectorAll('.form-control[id$="-description"]').forEach(selectElement => {
                    const currentValue = selectElement.value;
                    console.log(`Обновляем select ID: ${selectElement.id}, текущий выбранный элемент: ${currentValue}`);

                    $(selectElement).empty();
                    data.forEach(([value, label]) => {
                        $(selectElement).append(`<option value="${value}">${label}</option>`);
                    });

                    $(selectElement).val(currentValue).trigger('change');
                });

                console.log("Все поля description успешно обновлены.");
            })
            .catch(error => {
                console.error("Ошибка при запросе данных:", error);
            });
    }
});
