document.addEventListener('DOMContentLoaded', function() {
    let tg = window.Telegram.WebApp;

    function loadData() {
        fetch('/get_data')
            .then(response => response.json())
            .then(data => {
                updateSelectOptions('account', data.accounts, 'Выберите счет');
                updateSelectOptions('project', data.projects, 'Выберите проект');
                updateSelectOptions('article', data.articles, 'Выберите статью');

                updateSelectOptions('accountIncome', data.accounts, 'Выберите счет');
                updateSelectOptions('projectIncome', data.projects, 'Выберите проект');
                updateSelectOptions('articleIncome', data.articles, 'Выберите статью');
            })
            .catch(error => {
                console.error('Ошибка при загрузке данных:', error);
            });
    }

    function updateSelectOptions(selectId, options, placeholderText) {
        let select = document.getElementById(selectId);
        if (select) {
            select.innerHTML = '';

            let placeholderOption = document.createElement('option');
            placeholderOption.value = '';
            placeholderOption.textContent = placeholderText;
            placeholderOption.disabled = true;
            placeholderOption.selected = true;
            select.appendChild(placeholderOption);

            options.forEach(option => {
                let opt = document.createElement('option');
                opt.value = option;
                opt.textContent = option;
                select.appendChild(opt);
            });
        }
    }

    loadData();

    function sendData(formId, transactionType) {
        const form = document.getElementById(formId);
        if (!form) {
            console.error('Форма с ID ' + formId + ' не найдена.');
            return;
        }
        console.log('Добавление обработчика для формы:', formId);

        form.addEventListener('submit', function(e) {
            e.preventDefault();

            let data = {
                date: form.querySelector('input[name="date"]').value,
                amount: form.querySelector('input[name="amount"]').value,
                account: form.querySelector('select[name="account"]').value,
                project: form.querySelector('select[name="project"]').value,
                article: form.querySelector('select[name="article"]').value,
                comment: form.querySelector('textarea[name="comment"]').value,
                username: 'TEST',
                transactionType: transactionType
            };

            console.log('Отправка данных:', data);

            fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Change to your telegram bot token
                    'X-Telegram-Bot-Api-Secret-Token': 'YOUR_TELEGRAM_BOT_TOKEN'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                console.log('Ответ от сервера:', result);
                if (result.ok) {
                    $('#successModal').modal('show');

                    $('#successModal').on('hidden.bs.modal', function () {
                        form.reset();
                    });
                } else {
                    alert('Ошибка при сохранении данных: ' + result.error);
                }
            })
            .catch(error => {
                console.error('Ошибка при отправке данных:', error);
                alert('Произошла ошибка при отправке данных.');
            });
        });
    }

    sendData('expenseForm', 'Расход');
    sendData('incomeForm', 'Приход');
});
