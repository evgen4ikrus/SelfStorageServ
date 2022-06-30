# Хранение вещей

## Запуск:

### 1. Копируем содержимое проекта себе в рабочую директорию
```
git clone <метод копирования>
```

### 2. Разворачиваем внутри скопированного проекта виртуальное окружение:
```
python -m venv <название виртуального окружения>
```

### 3. Устанавливаем библиотеки:
```
pip install -r requirements.txt
```

### 4. Для хранения переменных окружения создаем файл .env:
```
touch .env
```
Генерируем секретный ключ DJANGO в интерактивном режиме python:
    1. `python`
    2. `import django`
    3. `from django.core.management.utils import get_random_secret_key`
    4. `print(get_random_secret_key())`
    5. Копируем строку в `.env` файл: `DJANGO_KEY='ваш ключ'`    
    6. Для тестирования бота добавляем токен в `.env` файл: `BOT_TOKEN='токен вашего бота'

### 5. Переходим в директорию проекта и выполняем миграции в ДБ: 
```
cd storage_bot/

python manage.py makemigrations db; python manage.py migrate
```
#### Важно: Выполнять этот шаг нужно при изменении models.py

### 6. Запускаем модуль:
```
python manage.py bot
```
