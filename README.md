# Калькулятор эвакуатора — Telegram-бот

Telegram-бот на aiogram 3.x для компании, оказывающей услуги эвакуатора в Ташкенте.
У бота два режима:

- **Клиентский калькулятор** — расчёт стоимости эвакуации по маркам и весовым категориям.
- **Админ-панель** — управление прайсом, марками, категориями и просмотр заявок прямо в Telegram, без отдельного сайта.

## 1. Создание бота через @BotFather

1. Откройте в Telegram чат с [@BotFather](https://t.me/BotFather).
2. Отправьте команду `/newbot` и следуйте инструкциям (укажите имя и username бота).
3. BotFather выдаст токен вида `123456789:AAExampleToken...` — это и есть `BOT_TOKEN`.
4. Узнайте свой Telegram `user_id`, написав `/start` боту [@userinfobot](https://t.me/userinfobot).

## 2. Установка и запуск локально

```bash
git clone <URL вашего репозитория>
cd Evakuator-

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# откройте .env и заполните BOT_TOKEN, ADMIN_IDS, ADMIN_CONTACT

python seed.py                  # засеять базу начальными марками/ценами
python bot.py                   # запустить бота (long polling)
```

Если всё настроено верно, в консоли появится строка `Бот запускается...`, и бот начнёт отвечать в Telegram.

### Переменные окружения (`.env`)

| Переменная    | Описание                                                                 | Пример                    |
|---------------|---------------------------------------------------------------------------|----------------------------|
| `BOT_TOKEN`   | Токен бота от @BotFather                                                 | `123456789:AAExample...`   |
| `ADMIN_IDS`   | Telegram `user_id` администраторов через запятую                        | `111111111,222222222`      |
| `ADMIN_CONTACT` | Username (`@username`) или телефон (`+998901234567`) для кнопки связи | `@driver_username`         |
| `DB_PATH`     | (необязательно) путь к файлу SQLite                                     | `evacuator.db`              |

## 3. Тесты

```bash
pytest
```

Юнит-тесты покрывают функцию расчёта стоимости (`km * price_per_km`) и валидацию пользовательского ввода: 0 км, отрицательное число, нецелое число, очень большое расстояние.

## 4. Структура проекта

```
bot.py              — точка входа, запуск polling
config.py           — загрузка конфигурации из .env
utils.py            — расчёт цены, форматирование денег, валидация ввода
keyboards.py        — inline-клавиатуры
seed.py             — засев базы начальными данными
db/
  models.py         — модели SQLAlchemy (async) и инициализация БД
  queries.py        — функции доступа к БД
handlers/
  client.py         — клиентский калькулятор
  admin.py           — админ-панель (FSM)
tests/
  test_calculator.py — юнит-тесты
```

## 5. Развёртывание на VPS

### Вариант А: systemd (рекомендуется для постоянной работы)

1. Склонируйте проект на сервер и настройте `.env`, как описано выше (в virtualenv).
2. Создайте юнит `/etc/systemd/system/evacuator-bot.service`:

```ini
[Unit]
Description=Evacuator Calculator Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/evacuator-bot
ExecStart=/opt/evacuator-bot/venv/bin/python /opt/evacuator-bot/bot.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Запустите бота как сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable evacuator-bot
sudo systemctl start evacuator-bot
sudo systemctl status evacuator-bot
journalctl -u evacuator-bot -f   # просмотр логов
```

### Вариант Б: screen / tmux (быстрый способ без systemd)

```bash
tmux new -s evacuator-bot
cd /opt/evacuator-bot
source venv/bin/activate
python bot.py
# отсоединиться от сессии: Ctrl+B, затем D
# вернуться к сессии: tmux attach -t evacuator-bot
```

### Вариант В: Docker + docker-compose

```bash
cp .env.example .env
# заполните .env

docker compose up -d --build
docker compose logs -f          # просмотр логов
docker compose exec bot python seed.py   # засеять базу (один раз)
```

База данных SQLite и `bot.log` сохраняются в именованном Docker-томе `bot_data`, поэтому данные не теряются при пересборке контейнера.

## 6. Что нужно заполнить в `.env` перед первым запуском

1. **`BOT_TOKEN`** — токен, полученный от @BotFather.
2. **`ADMIN_IDS`** — ваш Telegram `user_id` (узнать через @userinfobot); при необходимости — несколько ID через запятую.
3. **`ADMIN_CONTACT`** — ваш username (`@ваш_username`) или номер телефона для кнопки «Связаться с водителем».

После этого администратор открывает панель управления командой `/admin` прямо в боте.
