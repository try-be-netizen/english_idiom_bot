"""
Бот «Английская идиома дня».

Каждый запуск:
1. Читает idioms.json (массив из 200 идиом).
2. Читает history.json (список ID уже опубликованных).
3. Берёт следующую неопубликованную идиому по порядку id.
4. Публикует пост в Telegram-канал с inline-кнопкой благодарности.
5. Если все 200 опубликованы — отправляет уведомление админу и завершается без ошибки.
6. Дописывает ID в history.json для последующего коммита workflow'ом.

ENV:
    BOT_TOKEN       — токен бота
    CHANNEL_ID      — id канала (например, @my_channel или -1001234567890)
    ADMIN_CHAT_ID   — куда слать уведомление об окончании списка (опционально)
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests

ROOT = Path(__file__).parent
IDIOMS_PATH = ROOT / "idioms.json"
HISTORY_PATH = ROOT / "history.json"

TIP_URL = "https://pay.cloudtips.ru/p/9bbd58f8"
TIP_BUTTON_TEXT = "🤍 Поблагодарить"
DICT_BUTTON_TEXT = "📖 Cambridge Dictionary"

TG_API = "https://api.telegram.org/bot{token}/{method}"


def env(name: str, required: bool = True) -> str:
    value = os.environ.get(name, "").strip()
    if required and not value:
        print(f"ERROR: переменная окружения {name} не задана", file=sys.stderr)
        sys.exit(1)
    return value


def load_idioms() -> list[dict]:
    with IDIOMS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_history() -> dict:
    """history.json: {"published_ids": [1, 2, 3, ...], "last_run": "..."}"""
    if not HISTORY_PATH.exists():
        return {"published_ids": [], "last_run": None}
    with HISTORY_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history: dict) -> None:
    with HISTORY_PATH.open("w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def html_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def format_post(idiom: dict) -> str:
    """Собирает HTML-сообщение для Telegram."""
    title = html_escape(idiom["idiom"])
    translation = html_escape(idiom["translation_ru"])
    meaning = html_escape(idiom["meaning_en"])
    example = html_escape(idiom["example_en"])

    return (
        f"🇬🇧 <b>Идиома дня:</b> <b>{title}</b>\n\n"
        f"🇷🇺 <b>Перевод:</b> {translation}\n\n"
        f"💡 <b>Meaning:</b> <i>{meaning}</i>\n\n"
        f"📝 <b>Example:</b>\n<i>{example}</i>"
    )


def build_keyboard(cambridge_url: str) -> dict:
    return {
        "inline_keyboard": [
            [{"text": DICT_BUTTON_TEXT, "url": cambridge_url}],
            [{"text": TIP_BUTTON_TEXT, "url": TIP_URL}],
        ]
    }


def send_message(token: str, chat_id: str, text: str, reply_markup: dict | None = None) -> dict:
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if reply_markup is not None:
        payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)

    url = TG_API.format(token=token, method="sendMessage")
    r = requests.post(url, data=payload, timeout=30)
    if r.status_code != 200:
        print(f"ERROR: Telegram API вернул {r.status_code}: {r.text}", file=sys.stderr)
        r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        print(f"ERROR: Telegram ответил не ок: {data}", file=sys.stderr)
        sys.exit(1)
    return data


def pick_next(idioms: list[dict], history: dict) -> dict | None:
    published = set(history.get("published_ids", []))
    for idiom in idioms:
        if idiom["id"] not in published:
            return idiom
    return None


def msk_now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=3))).isoformat(timespec="seconds")


def main() -> None:
    token = env("BOT_TOKEN")
    channel_id = env("CHANNEL_ID")
    admin_chat_id = env("ADMIN_CHAT_ID", required=False)

    idioms = load_idioms()
    history = load_history()

    next_idiom = pick_next(idioms, history)

    if next_idiom is None:
        # Все 200 опубликованы — уведомляем админа и выходим
        msg = (
            "ℹ️ <b>Бот «Идиома дня»</b>\n\n"
            f"Все {len(idioms)} идиом из списка опубликованы.\n"
            "Расписание остановлено до пополнения idioms.json."
        )
        target = admin_chat_id or channel_id
        send_message(token, target, msg)
        print("Список исчерпан, отправлено уведомление.")
        history["last_run"] = msk_now_iso()
        history["exhausted"] = True
        save_history(history)
        return

    text = format_post(next_idiom)
    keyboard = build_keyboard(next_idiom["cambridge_url"])
    send_message(token, channel_id, text, keyboard)

    history.setdefault("published_ids", []).append(next_idiom["id"])
    history["last_run"] = msk_now_iso()
    history["exhausted"] = False
    save_history(history)

    print(
        f"Опубликовано #{next_idiom['id']}: {next_idiom['idiom']} "
        f"(всего: {len(history['published_ids'])}/{len(idioms)})"
    )


if __name__ == "__main__":
    main()
