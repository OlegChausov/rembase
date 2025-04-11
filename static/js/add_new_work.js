document.addEventListener('DOMContentLoaded', function() {
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

        // Используем ID с префиксом "works", который мы указали при создании formset'а
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
    });
});
