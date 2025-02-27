 // Функция для предварительного просмотра изображения
    function previewImage(input) {
        var preview = document.getElementById('preview');
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }

            reader.readAsDataURL(input.files[0]);
        } else {
            preview.src = '#';
            preview.style.display = 'none';
        }
    }

    // Найти элемент загрузки файла и добавить обработчик события
    var fileInput = document.querySelector('input[type="file"][name="photo"]');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            previewImage(this);
        });
    }