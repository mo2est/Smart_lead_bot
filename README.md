# Smart Lead Bot — Telegram-бот для сбора заявок

> Пошаговый сбор контактов клиентов прямо в Telegram: имя, телефон, описание задачи — и мгновенное уведомление администратору.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![aiogram](https://img.shields.io/badge/aiogram-3.x-green) ![SQLite](https://img.shields.io/badge/SQLite-async-orange)

**Стек:** Python 3.11 · aiogram 3 · SQLAlchemy (async) · SQLite / aiosqlite  
**Версия:** 1.0.0

---

## Содержание

1. [Возможности](#возможности)
2. [Запуск на Windows — пошагово с нуля](#запуск-на-windows)
3. [Быстрый старт (macOS / Linux)](#быстрый-старт-macos--linux)
4. [Развёртывание на сервере (production)](#развёртывание-на-сервере)
5. [Конфигурация](#конфигурация)
6. [Структура проекта](#структура-проекта)
7. [Схема базы данных](#схема-базы-данных)
8. [Сценарии использования](#сценарии-использования)
9. [Обновление и обслуживание](#обновление-и-обслуживание)
10. [Частые проблемы](#частые-проблемы)

---

## Возможности

### Для пользователей
- [x] Команда `/start` — приветствие и кнопка «Оставить заявку»
- [x] Пошаговый сбор данных: имя → телефон → описание задачи
- [x] Отправка номера телефона кнопкой (без ручного ввода)
- [x] Валидация ввода: имя от 2 символов, проверка формата телефона, описание от 3 символов
- [x] Кнопка «Отмена» на шагах ввода имени и описания (на шаге телефона — кнопка отправки контакта)
- [x] Кнопки «Отмена» прошлых шагов автоматически деактивируются — нельзя отменить уже отправленную заявку
- [x] Подтверждение после успешной отправки заявки

### Для администраторов
- [x] Мгновенное уведомление в Telegram при каждой новой заявке
- [x] `/admin` — последние 10 заявок с датой, именем, телефоном и описанием
- [x] `/stats` — количество заявок за сегодня и за всё время
- [x] Защита от спама (throttling-мидлварь)
- [x] Поддержка нескольких администраторов одновременно

---

## Запуск на Windows

> Этот раздел написан для людей без опыта программирования. Следуйте шагам по порядку.

### Шаг 1 — Создать бота в @BotFather

1. Откройте Telegram, найдите бота **@BotFather** и нажмите `/start`
2. Отправьте команду `/newbot`
3. Придумайте **название** бота (например: `Заявки моей компании`)
4. Придумайте **username** — должен заканчиваться на `bot` (например: `my_company_leads_bot`)
5. BotFather пришлёт **токен** — длинную строку вида `123456789:AAF...`  
   ⚠️ Сохраните токен — он понадобится на Шаге 8

### Шаг 2 — Узнать свой Telegram ID

1. Найдите в Telegram бота **@userinfobot**
2. Нажмите `/start`
3. Бот пришлёт ваш **ID** — число вида `123456789`  
   ⚠️ Сохраните его — он понадобится на Шаге 8

### Шаг 3 — Установить Python

1. Перейдите на сайт [python.org/downloads](https://www.python.org/downloads/)
2. Нажмите большую кнопку **Download Python 3.x.x**
3. Запустите скачанный установщик
4. ⚠️ **ВАЖНО:** поставьте галочку **«Add Python to PATH»** в самом низу окна установщика перед тем, как нажать Install
5. Нажмите **Install Now** и дождитесь завершения
6. Проверьте установку: откройте **Пуск → cmd** и введите:
   ```
   python --version
   ```
   Должно появиться что-то вроде `Python 3.11.x`

### Шаг 4 — Скачать код

**Вариант А — через ZIP (проще):**
1. На странице репозитория GitHub нажмите зелёную кнопку **Code → Download ZIP**
2. Распакуйте архив в удобное место, например `C:\bots\smart_lead_bot`

**Вариант Б — через git:**
```
git clone https://github.com/mo2est/Smart_lead_bot.git
```

### Шаг 5 — Открыть папку в командной строке

1. Откройте папку с ботом в Проводнике
2. Щёлкните на **адресной строке** (вверху окна, где показан путь)
3. Введите `cmd` и нажмите **Enter** — откроется командная строка уже в нужной папке

### Шаг 6 — Создать виртуальное окружение

Введите в командной строке:
```
python -m venv venv
venv\Scripts\activate
```

Если PowerShell выдаёт ошибку про `execution policy`:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Затем повторите `venv\Scripts\activate`. После активации в начале строки появится `(venv)`.

### Шаг 7 — Установить зависимости

```
pip install -r requirements.txt
```

Дождитесь завершения — будут скачаны все необходимые библиотеки.

### Шаг 8 — Создать файл .env

1. Скопируйте файл `.env.example` и переименуйте копию в `.env`  
   (в проводнике: правая кнопка → Копировать, вставить, переименовать)
2. Откройте `.env` блокнотом и заполните:

```
BOT_TOKEN=вставьте_токен_из_шага_1
ADMIN_IDS=вставьте_ваш_id_из_шага_2
DATABASE_URL=sqlite+aiosqlite:///leads.db
```

Если администраторов несколько, перечислите ID через запятую: `111111111,222222222`

### Шаг 9 — Запустить бота

```
python main.py
```

В консоли появятся логи — бот запущен. Откройте Telegram, найдите вашего бота и нажмите `/start`.

Чтобы остановить бота: нажмите **Ctrl + C** в командной строке.

### Шаг 10 — Постоянная работа бота

**Вариант А — .bat-файл с автозагрузкой (для домашнего ПК):**

1. Создайте файл `start_bot.bat` в папке бота с содержимым:
   ```bat
   @echo off
   cd /d C:\bots\smart_lead_bot
   call venv\Scripts\activate
   python main.py
   ```
2. Нажмите **Win + R**, введите `shell:startup` → Enter
3. Скопируйте `start_bot.bat` в открывшуюся папку автозагрузки

**Вариант Б — VPS-сервер (рекомендуется для постоянной работы):**  
Смотрите раздел [Развёртывание на сервере](#развёртывание-на-сервере).

### Таблица ошибок Windows

| Симптом | Причина | Решение |
|---|---|---|
| `python` не является внутренней командой | Python не добавлен в PATH | Переустановите Python с галочкой «Add to PATH» |
| `No module named aiogram` | Не установлены зависимости или не активировано venv | Активируйте venv и запустите `pip install -r requirements.txt` |
| `Unauthorized` при запуске | Неверный токен в `.env` | Проверьте BOT_TOKEN — скопируйте заново из BotFather |
| `execution policy` ошибка в PowerShell | Ограничения политики | Выполните команду из Шага 6 |
| Файл `.env` не отображается в Проводнике | Windows скрывает файлы без расширения | Включите «Показывать расширения файлов» в настройках Проводника |

---

## Быстрый старт (macOS / Linux)

```bash
git clone https://github.com/mo2est/Smart_lead_bot.git && cd Smart_lead_bot
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && nano .env   # заполните BOT_TOKEN и ADMIN_IDS
python main.py
```

---

## Развёртывание на сервере

### Требования к серверу

| Параметр | Минимум | Рекомендуется |
|---|---|---|
| ОС | Ubuntu 22.04 | Ubuntu 22.04 LTS |
| CPU | 1 ядро | 1–2 ядра |
| RAM | 256 МБ | 512 МБ |
| Диск | 2 ГБ | 5 ГБ |
| Python | 3.11 | 3.11+ |

### Шаги развёртывания

**Шаг 1 — Обновить систему и установить Python:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3.11 python3.11-venv python3-pip git -y
```

**Шаг 2 — Создать отдельного пользователя:**
```bash
sudo useradd -m -s /bin/bash botuser
sudo su - botuser
```

**Шаг 3 — Скачать код:**
```bash
git clone https://github.com/mo2est/Smart_lead_bot.git
cd Smart_lead_bot
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

**Шаг 4 — Создать .env:**
```bash
cp .env.example .env
nano .env   # заполните BOT_TOKEN, ADMIN_IDS
```

**Шаг 5 — Настроить systemd-сервис:**
```bash
sudo nano /etc/systemd/system/smartleadbot.service
```

Содержимое файла:
```ini
[Unit]
Description=Smart Lead Bot
After=network.target

[Service]
User=botuser
WorkingDirectory=/home/botuser/Smart_lead_bot
EnvironmentFile=/home/botuser/Smart_lead_bot/.env
ExecStart=/home/botuser/Smart_lead_bot/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable smartleadbot
sudo systemctl start smartleadbot
```

**Шаг 6 — Проверить логи:**
```bash
sudo journalctl -u smartleadbot -f
```

---

### Альтернатива: Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

**docker-compose.yml:**
```yaml
version: "3.9"
services:
  bot:
    build: .
    restart: unless-stopped
    env_file: .env
    volumes:
      - ./leads.db:/app/leads.db
```

```bash
touch leads.db   # обязательно ДО первого запуска: иначе Docker создаст каталог leads.db вместо файла
docker compose up -d
docker compose logs -f
```

---

## Конфигурация

Все настройки задаются через файл `.env` в корне проекта.

| Переменная | Описание | По умолчанию |
|---|---|---|
| `BOT_TOKEN` | Токен бота от @BotFather | *(обязательно)* |
| `ADMIN_IDS` | Telegram ID администраторов через запятую | *(обязательно)* |
| `DATABASE_URL` | Строка подключения к базе данных | `sqlite+aiosqlite:///leads.db` |

---

## Структура проекта

```
Smart_lead_bot/
│
├── main.py                  # Точка входа: запуск бота и диспетчера
├── requirements.txt         # Зависимости проекта
├── .env.example             # Шаблон файла конфигурации
├── leads.db                 # База данных SQLite (создаётся автоматически)
│
└── app/
    ├── config.py            # Загрузка переменных окружения
    │
    ├── db/
    │   ├── models.py        # ORM-модели SQLAlchemy
    │   ├── engine.py        # Подключение к БД, создание таблиц
    │   └── requests.py      # Функции для работы с данными
    │
    ├── handlers/
    │   ├── states.py        # FSM-состояния (LeadForm)
    │   ├── client.py        # Хэндлеры для клиентов (/start, FSM-шаги)
    │   └── admin.py         # Хэндлеры для администраторов (/admin, /stats)
    │
    ├── keyboards/
    │   └── keyboards.py     # Inline и Reply клавиатуры
    │
    ├── filters/
    │   └── admin.py         # Фильтр IsAdmin для защиты команд
    │
    └── middlewares/
        └── throttling.py    # Антиспам-мидлварь (TTL-кэш)
```

---

## Схема базы данных

```
┌─────────────────────────────────────────────┐
│                    leads                    │
├──────────────┬──────────────┬───────────────┤
│ Колонка      │ Тип          │ Описание      │
├──────────────┼──────────────┼───────────────┤
│ id           │ INTEGER PK   │ Уникальный ID │
│ user_id      │ BIGINT       │ Telegram ID   │
│ username     │ VARCHAR(64)  │ @username     │
│ name         │ VARCHAR(256) │ Имя клиента   │
│ phone        │ VARCHAR(32)  │ Телефон       │
│ description  │ TEXT         │ Описание зад. │
│ created_at   │ DATETIME     │ Дата создания │
└──────────────┴──────────────┴───────────────┘
```

---

## Сценарии использования

### Пользовательский путь

```
/start
  └── [Оставить заявку]
        ├── Введите имя
        │     ├── [Отмена] → Заявка отменена
        │     └── Имя принято
        │           ├── Введите телефон (текстом или кнопкой «Отправить контакт»)
        │           │     └── Телефон принят
        │           │           ├── Опишите задачу
        │           │           │     ├── [Отмена] → Заявка отменена
        │           │           │     └── ✅ Спасибо! Мы свяжемся с вами в течение часа
        │           │           │           └── 🔔 Уведомление администраторам
```

### Административный путь

```
/admin  →  Список последних 10 заявок
             └── ID | Дата | Имя | Телефон | Описание

/stats  →  📊 Заявок сегодня: N
             📊 Заявок всего: N
```

---

## Настройка контента

### Изменение текстов бота

Все тексты, которые бот отправляет пользователям, находятся в файле `app/handlers/client.py`. Откройте файл и найдите нужный текст в кавычках — отредактируйте и перезапустите бота.

Например, приветственное сообщение:
```python
# app/handlers/client.py, функция cmd_start
"👋 Здравствуйте! Я бот для приёма заявок.\n\n..."
```

### Изменение кнопок

Кнопки редактируются в файле `app/keyboards/keyboards.py`.

### Перезапуск после изменений

```bash
# systemd
sudo systemctl restart smartleadbot

# Docker
docker compose restart

# Вручную (Windows / dev)
Ctrl+C  →  python main.py
```

---

## Обновление и обслуживание

### Обновление кода

```bash
cd Smart_lead_bot
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
sudo systemctl restart smartleadbot
```

### Бэкап базы данных

**Вручную:**
```bash
cp leads.db leads_backup_$(date +%Y%m%d).db
```

**Автоматически через cron (каждый день в 3:00):**
```bash
crontab -e
```
Добавьте строку (используется `sqlite3 .backup` — безопасно для базы, в которую в этот момент идёт запись, в отличие от `cp`):
```
0 3 * * * sqlite3 /home/botuser/Smart_lead_bot/leads.db ".backup /home/botuser/backups/leads_$(date +\%Y\%m\%d).db"
```

### Быстрые команды systemd

| Команда | Действие |
|---|---|
| `sudo systemctl start smartleadbot` | Запустить бота |
| `sudo systemctl stop smartleadbot` | Остановить бота |
| `sudo systemctl restart smartleadbot` | Перезапустить бота |
| `sudo systemctl status smartleadbot` | Статус бота |
| `sudo journalctl -u smartleadbot -f` | Просмотр логов в реальном времени |
| `sudo journalctl -u smartleadbot --since today` | Логи за сегодня |

---

## Частые проблемы

| Симптом | Причина | Решение |
|---|---|---|
| Бот не отвечает на `/start` | Бот не запущен или упал | Проверьте `systemctl status` или запустите вручную |
| `Unauthorized` в логах | Неверный `BOT_TOKEN` | Проверьте `.env`, скопируйте токен из BotFather заново |
| Не приходят уведомления админу | Неверный `ADMIN_IDS` | Проверьте `.env` — ID должен быть числом, не username |
| `ModuleNotFoundError` | Зависимости не установлены | Активируйте venv и выполните `pip install -r requirements.txt` |
| `PermissionError` на `.db` файл | Нет прав записи | Проверьте права на папку: `chmod 755 /home/botuser/Smart_lead_bot` |
| Бот принимает одно сообщение из нескольких быстрых | Throttling-мидлварь | Это нормально — защита от спама. Норма: 1 сообщение каждые 0.7 сек |
| База данных не создаётся | Путь в `DATABASE_URL` недоступен | Убедитесь, что папка существует и бот имеет права на запись |

---

## Лицензия

MIT License — используйте свободно в личных и коммерческих проектах.

---

<details>
<summary>✅ Чеклист перед сдачей клиенту</summary>

- [ ] Токен бота вставлен в `.env` и бот запускается без ошибок
- [ ] `ADMIN_IDS` заполнен и уведомления приходят администратору
- [ ] Все тексты бота проверены и соответствуют стилю клиента
- [ ] Сценарий протестирован от `/start` до получения подтверждения
- [ ] Бот настроен как systemd-сервис и стартует автоматически после перезагрузки
- [ ] Настроен cron-бэкап базы данных
- [ ] Клиент получил инструкцию по пользованию и ссылку на этот README
- [ ] Проверено, что уведомления приходят при отправке тестовой заявки

</details>
