# Task Tracker Api "Альфа-софт"

REST API для таск трекерв, разработанный на Django. 
Управление проектами, задачами и комментариями

### Как запустить проект:

- создайте виртуальное окружение:
```
python -m venv venv
```
- установите зависимости:
```
pip install -r requirements.txt
```
- примените миграции
```
python manage.py migrate
```
- Запустите сервер:
```
python manage.py runserver
```

### документация API:

- Swagger UI: http://127.0.0.1:8000/api/docs/swagger/
- ReDoc: http://127.0.0.1:8000/api/docs/redoc/
