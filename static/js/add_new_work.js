document.addEventListener("DOMContentLoaded", function () {
    const addWorkButton = document.getElementById("add-work");
    const emptyFormTemplate = document.getElementById("empty-form").innerHTML;
    const workFormsContainer = document.getElementById("work-forms");
    const totalFormsInput = document.getElementById("id_works-TOTAL_FORMS");

    let formCount = parseInt(totalFormsInput.value, 10);

    // Добавление новой формы
    addWorkButton.addEventListener("click", function () {
        const newFormDiv = document.createElement("div");
        newFormDiv.classList.add("work-form");
        newFormDiv.innerHTML = emptyFormTemplate;

        const descriptionField = newFormDiv.querySelector('select[name="description"]');
        const priceField = newFormDiv.querySelector('input[name="price"]');
        const warrantyField = newFormDiv.querySelector('input[name="warranty"]');

        descriptionField.name = `works-${formCount}-description`;
        priceField.name = `works-${formCount}-price`;
        warrantyField.name = `works-${formCount}-warranty`;

        workFormsContainer.appendChild(newFormDiv);
        formCount++;
        totalFormsInput.value = formCount;
    });

    // Удаление формы
    document.body.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-work")) {
            const workDiv = event.target.closest(".work-form");
            const workId = workDiv.dataset.workId;

            if (workId) {
                fetch(`/delete-work/${workId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                    },
                })
                    .then((response) => {
                        if (response.ok) {
                            workDiv.remove();
                            formCount--;
                            totalFormsInput.value = formCount;
                        }
                    })
                    .catch((error) => console.error("Ошибка при удалении:", error));
            } else {
                workDiv.remove();
                formCount--;
                totalFormsInput.value = formCount;
            }
        }
    });
});
