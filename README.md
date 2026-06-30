# Smart Lead Bot

Telegram-бот на aiogram 3 для сбора заявок от клиентов.

## Стек

- Python 3.11+
- aiogram 3
- SQLAlchemy (async) + SQLite (aiosqlite)

## Сценарий

1. `/start` — приветствие и кнопка «Оставить заявку»
2. Бот пошагово (FSM) спрашивает: имя → телефон → описание задачи
3. После заполнения клиенту приходит подтверждение, заявка сохраняется в БД
4. Администраторам отправляется уведомление с полными данными заявки

На каждом шаге доступна кнопка «Отмена». Включён throttling-мидлварь для защиты от спама.

## Админ-команды

- `/admin` — последние 10 заявок
- `/stats` — количество заявок за сегодня и всего

## Запуск

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # заполнить BOT_TOKEN и ADMIN_IDS
python main.py
```

## Переменные окружения

- `BOT_TOKEN` — токен бота от @BotFather
- `ADMIN_IDS` — список Telegram ID администраторов через запятую
- `DATABASE_URL` — строка подключения к БД (по умолчанию SQLite)
