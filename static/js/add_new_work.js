document.addEventListener('DOMContentLoaded', function () {
    console.log("Страница загружена, скрипт активирован.");

    const addWorkButton = document.getElementById('add-work-button');
    const workFormsContainer = document.getElementById('work-forms');
    const emptyFormTemplate = document.getElementById('empty-form');
    const totalFormsInput = document.querySelector('#id_works-TOTAL_FORMS');
    const modal = document.getElementById("modal");
    const form = document.getElementById('work-form-container');

    if (!addWorkButton || !workFormsContainer || !emptyFormTemplate || !totalFormsInput || !modal || !form) {
        console.error("Ошибка: Один из необходимых элементов не найден!");
        return;
    }

    console.log("Все необходимые элементы найдены.");

    function initializeSelect2WithEvents(selectElement) {
        console.log("Вызвана initializeSelect2WithEvents для элемента:", selectElement, selectElement ? selectElement.id : 'null');
        if (selectElement) {
            if ($(selectElement).data('select2')) {
                console.log("Уничтожаем существующий Select2 для элемента:", selectElement.id);
                $(selectElement).select2('destroy');
            }
            $(selectElement).select2({
                width: '600px'
            }).on('select2:select', function (e) {
                const selectedValue = e.params.data.id;
                console.log(`Выбрано значение: ${selectedValue} в select ID: ${this.id}`);
                handleSelectChange(this, selectedValue);
            });
            console.log("Select2 успешно инициализирован для элемента:", selectElement.id);
        } else {
            console.error("Элемент <select> не найден для инициализации Select2.");
        }
    }

    console.log("Проверка наличия полей price и warranty...");
    console.log("Поле price:", document.querySelector('#id_price'));
    console.log("Поле warranty:", document.querySelector('#id_warranty'));

    const initialSelectFields = document.querySelectorAll('#work-forms .work-form:not(.hidden) .form-control[id$="-description"]');
    console.log("Найдено селектов для инициализации при загрузке:", initialSelectFields.length);
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
                if (descriptionField) {
                    if (isChecked && $(descriptionField).data('select2')) {
                        $(descriptionField).select2('destroy');
                        console.log("Select2 уничтожен для скрытой формы description.");
                    } else if (!isChecked && !$(descriptionField).data('select2')) {
                        initializeSelect2WithEvents(descriptionField);
                        console.log("Select2 инициализирован для показанной формы description.");
                    }
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
    
        const requestData = {
            description: document.getElementById('new_work_description_name').value.trim(),
            price: document.querySelector('#id_price')?.value || null,
            warranty: document.querySelector('#id_warranty')?.value || null
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
    
            if (data.success) {
                const newWorkDescription = data.typicwork.description;
    
                document.getElementById('modal').style.display = 'none';
                console.log("Модальное окно закрыто.");
    
                // Обновление и выбор новой работы
                updateSelectFieldsAndSetNewOption(newWorkDescription);
            } else {
                console.error("Ошибка от сервера:", data.error);
            }
        })
        .catch(error => {
            console.error("Ошибка при отправке данных:", error);
        });
    });

    function updateSelectFieldsAndSetNewOption(newWorkDescription) {
        console.log("Обновление всех select-полей и установка новой опции...");
    
        document.querySelectorAll('.form-control[id$="-description"]').forEach(selectElement => {
            fetch('/api/typical_work_data/')
                .then(response => response.json())
                .then(data => {
                    console.log("Полученные данные для обновления select:", data);
    
                    // Очищаем поле и добавляем новые опции
                    $(selectElement).empty();
                    data.forEach(([value, label]) => {
                        $(selectElement).append(`<option value="${value}">${label}</option>`);
                    });
    
                    if (selectElement.dataset.modalTriggered === "true") {
                        console.log(`Пытаемся выбрать новую опцию: ${newWorkDescription}`);
    
                        // Добавляем новую опцию вручную, если её нет
                        let optionExists = false;
                        $(selectElement).find('option').each(function () {
                            if ($(this).val() === newWorkDescription) {
                                optionExists = true;
                            }
                        });
    
                        if (!optionExists) {
                            const newOption = new Option(newWorkDescription, newWorkDescription, true, true);
                            $(selectElement).append(newOption);
                            console.log(`Добавлена вручную новая опция: ${newWorkDescription}`);
                        }
    
                        // Явно устанавливаем значение перед пересозданием Select2
                        $(selectElement).val(newWorkDescription);
    
                        // Полностью уничтожаем и пересоздаём Select2
                        if ($(selectElement).data('select2')) {
                            $(selectElement).select2('destroy');
                        }
    
                        // Пересоздаём Select2 с обновлёнными данными
                        $(selectElement).select2({
                            width: '600px'
                        });
    
                        console.log(`Выбрана новая работа "${newWorkDescription}" для select ID: ${selectElement.id}`);
                        delete selectElement.dataset.modalTriggered;
                    } else {
                        console.log(`Сохраняем текущее значение для select ID: ${selectElement.id}`);
                        $(selectElement).val(selectElement.value);
    
                        // Пересоздаём Select2
                        if ($(selectElement).data('select2')) {
                            $(selectElement).select2('destroy');
                        }
                        $(selectElement).select2({
                            width: '600px'
                        });
                    }
                })
                .catch(error => {
                    console.error("Ошибка при запросе данных для обновления select:", error);
                });
        });
    }
    
    
    
    

    document.querySelectorAll('.form-control[id$="-description"]').forEach(selectElement => {
        selectElement.addEventListener('select2:select', function (e) {
            const selectedValue = e.params.data.id;
    
            if (selectedValue === "new") {
                modal.style.display = "block";
                console.log("Модальное окно открыто.");
                this.dataset.modalTriggered = "true";
            } else {
                modal.style.display = "none";
                console.log("Модальное окно скрыто.");
            }
        });
    });

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        console.log("Данные перед отправкой основной формы:");
        for (const [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }
        this.submit();
    });
});
