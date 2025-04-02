document.addEventListener("DOMContentLoaded", function () {
    const addWorkButton = document.getElementById("add-work");
    const workFormsContainer = document.getElementById("work-forms");
    const emptyFormTemplate = document.getElementById("empty-form").innerHTML;

    let formCount = document.querySelectorAll(".work-form").length;
    const totalFormsInput = document.querySelector("#id_works-TOTAL_FORMS");

    addWorkButton.addEventListener("click", function () {
        let newFormHtml = emptyFormTemplate.replace(/__prefix__/g, formCount);
        const newForm = document.createElement("div");
        newForm.classList.add("work-form");
        newForm.innerHTML = newFormHtml;
        workFormsContainer.appendChild(newForm);

        formCount++;
        totalFormsInput.value = formCount;  // Обновляем количество форм
    });
});