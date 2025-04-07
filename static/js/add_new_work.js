document.addEventListener("DOMContentLoaded", function () {
    const addWorkButton = document.getElementById("add-work");
    const workFormsContainer = document.getElementById("work-forms");
    const emptyFormTemplate = document.getElementById("empty-form").innerHTML;
    const totalFormsInput = document.querySelector("#id_works-TOTAL_FORMS");

    let formCount = document.querySelectorAll(".work-form").length;

    function toggleFields(form) {
        const descriptionField = form.querySelector("select[name^='works'][name$='description']");
        const priceField = form.querySelector("input[name^='works'][name$='price']");
        const warrantyField = form.querySelector("input[name^='works'][name$='warranty']");

        if (!descriptionField || !priceField || !warrantyField) {
            console.error("Ошибка: поля не найдены в форме", form);
            return;
        }

        function updateFieldState() {
            const isDisabled = !descriptionField.value || descriptionField.value === "Выбор услуги";
            priceField.disabled = isDisabled;
            warrantyField.disabled = isDisabled;
        }

        updateFieldState(); // Применяем блокировку при загрузке страницы
        descriptionField.addEventListener("change", updateFieldState);
        $(descriptionField).on("select2:select", updateFieldState);
    }

    setTimeout(() => {
        document.querySelectorAll(".work-form").forEach(toggleFields);
        $(".work-select").select2({
            placeholder: "Введите название работы...",
            allowClear: true
        }).on("change", function () {
            if ($(this).val() === "new") {
                $('#add-service-modal').modal('show');
            }
        });
    }, 50);

    addWorkButton.addEventListener("click", function () {
        let newFormHtml = emptyFormTemplate.replace(/__prefix__/g, formCount);
        const newForm = document.createElement("div");
        newForm.classList.add("work-form");
        newForm.innerHTML = newFormHtml;
        workFormsContainer.appendChild(newForm);

        formCount++;
        totalFormsInput.value = formCount;

        setTimeout(() => {
            toggleFields(newForm);
            $(newForm).find('.work-select').select2({
                placeholder: "Введите название работы...",
                allowClear: true
            }).on("change", function () {
                if ($(this).val() === "new") {
                    $('#add-service-modal').modal('show');
                }
            });
        }, 50);
    });
});
