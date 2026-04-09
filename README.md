# AskPupkin - сайт вопросов и ответов

## Django

### Запуск

1. Создайте виртуальное окружение:
   - `python -m venv venv`

2. Активируйте окружение:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Установите зависимости:
   - `pip install -r requirements.txt`

4. Запустите сервер:
   - `python manage.py runserver`

5. Откройте в браузере: http://127.0.0.1:8000

### Запуск через Docker

`docker compose up --build`

Откройте: http://localhost:8000

### Страницы (маршруты)

- `/` — главная (список новых вопросов)
- `/hot/` — лучшие вопросы
- `/tag/<tag_name>/` — вопросы по тегу
- `/question/<question_id>/` — страница вопроса
- `/ask/` — создание вопроса
- `/login/` — вход
- `/signup/` — регистрация
- `/profile/` — профиль

## Статическая вёрстка

### Как открыть

1. Скачать репозиторий
2. Открыть папку `public`
3. Дважды кликнуть по `index.html`

### Страницы

- `index.html` — главная
- `question.html` — страница вопроса
- `ask.html` — создать вопрос
- `login.html` — вход
- `signup.html` — регистрация
- `profile.html` — профиль
- `base.html` — базовый макет

Все страницы лежат в папке `public/`.

### Технологии

HTML, Bootstrap (локально), CSS.

## Автор

Семёнов Фёдор