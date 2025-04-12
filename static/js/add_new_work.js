document.addEventListener('DOMContentLoaded', function () {
    const addWorkButton = document.getElementById('add-work-button');
    const workFormsContainer = document.getElementById('work-forms');
    const emptyFormTemplate = document.getElementById('empty-form');
    const totalFormsInput = document.querySelector('#id_works-TOTAL_FORMS'); // Убедитесь, что ID корректный

    if (!addWorkButton || !workFormsContainer || !emptyFormTemplate || !totalFormsInput) {
        console.error("Один из необходимых элементов не найден!");
        return;
    }

    addWorkButton.addEventListener('click', function () {
        const currentFormCount = parseInt(totalFormsInput.value, 10);
        const newFormHtml = emptyFormTemplate.innerHTML.replace(/__prefix__/g, currentFormCount);

        totalFormsInput.value = currentFormCount + 1; // Увеличиваем счётчик форм

        const newFormDiv = document.createElement('div');
        newFormDiv.classList.add('work-form');
        newFormDiv.innerHTML = newFormHtml;

        workFormsContainer.appendChild(newFormDiv); // Добавляем новую форму
        console.log("Форма успешно добавлена!", newFormDiv);
    });
});
