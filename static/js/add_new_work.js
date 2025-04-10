document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript подключён!");

    const addWorkButton = document.getElementById("add-work");
    const workFormsContainer = document.getElementById("work-forms");
    const emptyFormTemplate = document.getElementById("empty-form").innerHTML;
    const totalFormsInput = document.getElementById("id_works-TOTAL_FORMS");

    if (!addWorkButton || !workFormsContainer || !emptyFormTemplate || !totalFormsInput) {
        console.error("Ошибка: Один из необходимых элементов не найден.");
        return;
    }

    addWorkButton.addEventListener("click", () => {
        console.log("Кнопка 'Добавить работу' нажата!");

        const currentIndex = totalFormsInput.value;

        // Заменяем префикс в шаблоне на текущий индекс
        const newWorkFormHTML = emptyFormTemplate.replace(/__prefix__/g, currentIndex);
        const newWorkForm = document.createElement("div");
        newWorkForm.classList.add("work-form");
        newWorkForm.innerHTML = newWorkFormHTML;

        workFormsContainer.appendChild(newWorkForm);
        console.log("Добавлена новая форма:", newWorkForm);

        // Увеличиваем значение TOTAL_FORMS
        totalFormsInput.value = parseInt(totalFormsInput.value, 10) + 1;
        console.log("Новый TOTAL_FORMS:", totalFormsInput.value);

        // Инициализируем обработчик для новой формы
        initWorkForm(newWorkForm);
    });

    // Инициализация формы: активация полей при изменении выбора
    function initWorkForm(formElement) {
        console.log("Инициализация формы:", formElement.innerHTML);

        const descriptionField = formElement.querySelector("select[name*='description']");
        const priceField = formElement.querySelector("input[name*='price']");
        const warrantyField = formElement.querySelector("input[name*='warranty']");

        if (!descriptionField) {
            console.error("Поле 'description' не найдено в форме:", formElement);
        }
        if (!priceField) {
            console.error("Поле 'price' не найдено в форме:", formElement);
        }
        if (!warrantyField) {
            console.error("Поле 'warranty' не найдено в форме:", formElement);
        }

        if (descriptionField && priceField && warrantyField) {
            descriptionField.addEventListener("change", () => {
                const selectedValue = descriptionField.value;
                const isDisabled = selectedValue === "";
                priceField.disabled = isDisabled;
                warrantyField.disabled = isDisabled;
                console.log(`Выбрано описание: ${selectedValue}. Цена disabled: ${priceField.disabled}, Гарантия disabled: ${warrantyField.disabled}`);
            });
        }
    }

    // Инициализация всех уже существующих форм на странице
    const existingForms = workFormsContainer.querySelectorAll(".work-form");
    existingForms.forEach(initWorkForm);

    // Перед отправкой формы убираем disabled для всех input
    const orderForm = document.getElementById("order-form");
    orderForm.addEventListener("submit", function () {
        const disabledInputs = orderForm.querySelectorAll("input[disabled]");
        disabledInputs.forEach(function (input) {
            input.disabled = false;
        });
        console.log("Перед отправкой формы удалены все disabled-атрибуты.");
    });
});
