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

function searchAll() {
    let filter, all_tables, table, tr, td, txtValue;
    // input = document.getElementById("search");
    filter = input.value.toUpperCase();
    all_tables = document.getElementsByClassName('table')
    console.log(all_tables.length)
    for (let a = 0; a < all_tables.length; a++) {
        // console.log(it[i])
        console.log("iter", a)
        table = all_tables[a]
        console.log(table)
        tr = table.getElementsByTagName("tr");
        // tr = table.getElementsByClassName("tohide");
        console.log(tr)
           for (i = 0; i < tr.length; i++) {
        // Проверяем по каждой ячейке в строке
            for (j = 0; j < tr[i].cells.length; j++) {
                td = tr[i].cells[j];
                if (td) {
                    txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                        table.caption.style.display = "";
                        break; // Если есть хотя бы одно совпадение, то показываем строку
                    } else {
                        tr[i].style.display = "none"; // Иначе скрываем
                        table.caption.style.display = "none"
                    }
                };
            };
        };
    };
}

// Добавляем обработчик события на изменение значения input
input.addEventListener('input', searchAll);
