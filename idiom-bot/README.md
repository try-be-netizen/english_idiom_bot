# 🇬🇧 Бот «Английская идиома дня»

Telegram-бот, который каждый день в **09:00 МСК** публикует одну английскую идиому в канал. Всего 200 идиом — на 200 дней (~6.5 месяцев). После исчерпания списка бот шлёт уведомление и останавливается.

## Архитектура

- `idioms.json` — корпус из 200 идиом (`id`, `idiom`, `translation_ru`, `meaning_en`, `example_en`, `cambridge_url`).
- `history.json` — список ID уже опубликованных идиом + время последнего запуска.
- `bot.py` — берёт следующую неопубликованную идиому по порядку `id` и постит её.
- `.github/workflows/daily.yml` — крон GitHub Actions раз в сутки + коммит обновлённого `history.json`.

## Формат поста

```
🇬🇧 Идиома дня: A piece of cake

🇷🇺 Перевод: проще простого, плёвое дело

💡 Meaning: something very easy to do

📝 Example:
The exam was a piece of cake — I finished in twenty minutes.

[📖 Cambridge Dictionary]
[🤍 Поблагодарить]
```

Кнопка «Поблагодарить» ведёт на `https://pay.cloudtips.ru/p/9bbd58f8`.

## Настройка

### 1. Создай бота и канал

1. У `@BotFather` создай бота → получи `BOT_TOKEN`.
2. Создай канал, **добавь бота администратором** с правом публиковать сообщения.
3. Узнай `CHANNEL_ID`: либо `@username_канала` (если канал публичный), либо числовой ID `-100xxxxxxxxxx` (для приватного — например, через `@getidsbot`).
4. (Опц.) Узнай свой `ADMIN_CHAT_ID` — туда придёт уведомление, когда 200 идиом закончатся. Если не задать — уведомление уйдёт в сам канал.

### 2. Добавь секреты в GitHub

`Settings → Secrets and variables → Actions → New repository secret`:

| Имя | Значение |
|---|---|
| `BOT_TOKEN` | токен от BotFather |
| `CHANNEL_ID` | `@my_channel` или `-1001234567890` |
| `ADMIN_CHAT_ID` | твой `chat_id` (опционально) |

### 3. Залей в репозиторий и проверь

```bash
git add .
git commit -m "init: idiom of the day bot"
git push
```

В разделе **Actions** запусти workflow `Daily Idiom` вручную (`Run workflow`) для проверки. Если всё ок — пост появится в канале, а в репо будет коммит `chore: update history YYYY-MM-DD`.

## Расписание

GitHub Actions использует UTC. Крон `0 6 * * *` = **09:00 МСК**.

⚠️ GitHub может задерживать запуск шедулера на 5–15 минут под нагрузкой — это нормальное поведение, не баг.

## Что делать, когда 200 идиом закончатся

Бот сам пришлёт уведомление и проставит `"exhausted": true` в `history.json`. Дальше:

- **Добавить новые идиомы** — расширь `idioms.json` (новые `id` подряд) и продолжишь, ничего сбрасывать не надо.
- **Перезапустить с начала** — очисти `history.json` до состояния `{"published_ids": [], "last_run": null, "exhausted": false}` и закоммить.

## Локальный запуск (для отладки)

```bash
pip install -r requirements.txt
export BOT_TOKEN="..."
export CHANNEL_ID="@my_channel"
python bot.py
```

## Регенерация idioms.json

Файл собран из `_generate_idioms.py` — там же лежит источник правды (200 кортежей). Если правишь корпус, запусти:

```bash
python _generate_idioms.py
```
