document.addEventListener("DOMContentLoaded", function () {
    const descriptionField = document.querySelector(".work-select");

    function handleServiceSelection() {
        if (descriptionField.value === "new") {
            $('#add-service-modal').modal('show'); // Открываем модальное окно
        }
    }

    descriptionField.addEventListener("change", handleServiceSelection);

    document.getElementById("save-service-btn").addEventListener("click", function () {
        const serviceName = document.getElementById("new-service-name").value.trim();

        if (serviceName === "") {
            alert("Введите название услуги!");
            return;
        }

        fetch("/add_service/", {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
            body: JSON.stringify({ description: serviceName }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const newOption = new Option(serviceName, serviceName, true, true);
                descriptionField.add(newOption);
                descriptionField.value = serviceName;  // Предвыбираем новую услугу
                $('#add-service-modal').modal('hide'); // Закрываем модальное окно
            } else {
                alert("Ошибка при добавлении услуги");
            }
        });
    });

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});
