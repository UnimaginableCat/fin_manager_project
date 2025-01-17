## Запуск приложения
### Локальный запуск
Для локального запуска необходимо установить python 3.12 и poetry(https://python-poetry.org/docs/#installation).
1. После клонирования репозитория необходимо выполнить команду ```poetry install``` для установки всех зависимостей.
2. Нужно открыть файл ```.env``` и поменять настройки бд(хост, порт, креды)
3. Необходимо создать базу данных с названием FinManagementDb
4. Теперь нужно создать статические файлы ```poetry run python manage.py collectstatic```
5. После выполнения этой команды приложение можно запустить с помощью команды ```poetry run start_script```
6. Приложение доступно по адресу ```http://127.0.0.1:8000/```, но лучше сразу переходить на сваггер ```http://127.0.0.1:8000/swagger/```
### Запуск через докер
Для запуска через докер у вас должен быть установлен докер)
1. Выполните команду ```docker-compose build```
2. Выполните команду ```docker-compose up```
3. Приложение доступно по адресу ```http://127.0.0.1:8000/```, но лучше сразу переходить на сваггер ```http://127.0.0.1:8000/swagger/```
