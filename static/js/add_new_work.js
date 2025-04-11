document.addEventListener('DOMContentLoaded', function() {
    // Функция для установки значений и disabled для полей price и warranty
    function toggleWorkFields(selectElem) {
        var formContainer = selectElem.closest('.work-form');
        if (!formContainer) return;

        // Ищем поля по окончанию имени (они будут иметь префикс вида works-0-price, works-0-warranty и т.д.)
        var priceInput = formContainer.querySelector('input[name$="-price"]');
        var warrantyInput = formContainer.querySelector('input[name$="-warranty"]');

        if (selectElem.value === '') {
            // Если выбрана опция по умолчанию ("Выбор услуги"), устанавливаем дефолтные значения и отключаем поля
            if (priceInput) {
                priceInput.value = "0.00";
                priceInput.disabled = true;
            }
            if (warrantyInput) {
                warrantyInput.value = "";
                warrantyInput.disabled = true;
            }
        } else {
            // Если выбрана другая услуга — активируем поля для ввода
            if (priceInput) priceInput.disabled = false;
            if (warrantyInput) warrantyInput.disabled = false;
        }
    }

    // Функция для привязки обработчика изменения к элементу select
    function attachWorkSelectListener(selectElem) {
        selectElem.addEventListener('change', function() {
            toggleWorkFields(selectElem);
        });
        // Вызываем сразу для установки корректного состояния при загрузке
        toggleWorkFields(selectElem);
    }

    // Привязываем обработчики для уже существующих форм (при редактировании заказа)
    var workSelects = document.querySelectorAll('.work-select');
    workSelects.forEach(function(selectElem) {
        attachWorkSelectListener(selectElem);
    });

    // Функционал кнопки "Добавить работу"
    var addWorkBtn = document.getElementById('add-work-btn');
    if (!addWorkBtn) {
        console.error("Кнопка 'Добавить работу' не найдена");
        return;
    }

    addWorkBtn.addEventListener('click', function() {
        var workFormset = document.getElementById('work-formset');
        if (!workFormset) {
            console.error("Контейнер для форм работ не найден");
            return;
        }

        // Используем префикс, заданный при создании formset'а (например, "works")
        var totalFormsInput = document.getElementById('id_works-TOTAL_FORMS');
        if (!totalFormsInput) {
            console.error("Поле TOTAL_FORMS не найдено. Проверьте префикс формсета");
            return;
        }
        var currentFormCount = parseInt(totalFormsInput.value, 10);
        console.log("Текущее количество форм:", currentFormCount);

        var emptyFormDiv = document.getElementById('empty-form');
        if (!emptyFormDiv) {
            console.error("Шаблон пустой формы не найден");
            return;
        }
        var newFormHtml = emptyFormDiv.innerHTML.replace(/__prefix__/g, currentFormCount);
        console.log("Новый HTML формы:", newFormHtml);

        var newDiv = document.createElement('div');
        newDiv.classList.add('work-form');
        newDiv.innerHTML = newFormHtml;
        workFormset.appendChild(newDiv);

        totalFormsInput.value = currentFormCount + 1;
        console.log("Обновлено значение TOTAL_FORMS:", totalFormsInput.value);

        // Привязываем обработчик изменения к вновь созданному полю description
        var newSelect = newDiv.querySelector('.work-select');
        if (newSelect) {
            attachWorkSelectListener(newSelect);
        }
    });
});
