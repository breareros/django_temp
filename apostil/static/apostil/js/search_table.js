// Получаем элемент input
var input = document.getElementById('search');

// Устанавливаем обработчик события на фокус элемента
input.addEventListener('focus', function() {
    // Получаем тег meta
    var meta = document.querySelector('meta[http-equiv="refresh"]');

    // Остановить обновление страницы, если тег meta найден
    if (meta) {
        var timeoutId = setTimeout(function() {
            window.location.reload();
        }, 5000);

        input.dataset.timeoutId = timeoutId;
        clearTimeout(timeoutId);
    }
});

// Устанавливаем обработчик события на потерю фокуса элемента
input.addEventListener('blur', function() {
    // Получаем тег meta
    var meta = document.querySelector('meta[http-equiv="refresh"]');

    // Возобновляем обновление страницы, если тег meta найден
    if (meta) {
        var timeoutId = input.dataset.timeoutId;
        setTimeout(function() {
            window.location.reload();
        }, timeoutId);
    }
});

function searchTable() {
    // Получаем строку поиска и таблицу
    let input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("ChanksTable");
    tr = table.getElementsByTagName("tr");

    // Проходим по всем строкам таблицы и скрываем те, которые не соответствуют поиску
    for (i = 0; i < tr.length; i++) {
        // Проверяем по каждой ячейке в строке
        for (j = 0; j < tr[i].cells.length; j++) {
            td = tr[i].cells[j];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    break; // Если есть хотя бы одно совпадение, то показываем строку
                } else {
                    tr[i].style.display = "none"; // Иначе скрываем
                }
            }
        }
    }
}

function searchTodayTable() {
    // Получаем строку поиска и таблицу
    let input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("TodayChanksTable");
    tr = table.getElementsByTagName("tr");

    // Проходим по всем строкам таблицы и скрываем те, которые не соответствуют поиску
    for (i = 0; i < tr.length; i++) {
        // Проверяем по каждой ячейке в строке
        for (j = 0; j < tr[i].cells.length; j++) {
            td = tr[i].cells[j];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    break; // Если есть хотя бы одно совпадение, то показываем строку
                } else {
                    tr[i].style.display = "none"; // Иначе скрываем
                }
            }
        }
    }
}

// Добавляем обработчик события на изменение значения input
input.addEventListener('input', searchTable);
input.addEventListener('input', searchTodayTable);
