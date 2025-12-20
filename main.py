import os
import json
import hmac
import hashlib
from urllib.parse import parse_qsl

import telebot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6342709681

bot = telebot.TeleBot(BOT_TOKEN)

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

WEBAPP_URL = "https://odwillio0702.github.io/personalinfo/"  # сюда твой сайт

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(
            "Открыть профиль",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    bot.send_message(message.chat.id, "👇", reply_markup=markup)

def check_init_data(init_data: str) -> bool:
    data = dict(parse_qsl(init_data, keep_blank_values=True))
    hash_received = data.pop("hash", None)

    if not hash_received:
        return False

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(data.items())
    )

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hash_calculated = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(hash_received, hash_calculated)


@bot.message_handler(content_types=["web_app_data"])
def handle_web_app(message):
    try:
        data = json.loads(message.web_app_data.data)
        init_data = message.web_app_data.init_data

        if not check_init_data(init_data):
            bot.send_message(message.chat.id, "❌ Invalid initData")
            return

        if message.from_user.id != ADMIN_ID:
            bot.send_message(message.chat.id, "⛔ Access denied")
            return

        # === ТУТ ТЫ АДМИН ===
        bot.send_message(message.chat.id, "✅ Admin action accepted")
        print("Admin data:", data)

    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Error")
        print(e)

@bot.message_handler(content_types=['web_app_data'])
def handle_webapp_data(message):
    import json
    from datetime import datetime

    try:
        data = json.loads(message.web_app_data.data)
        print("Received data:", data)  # <-- проверка в консоли

        if data.get("action") == "log_user":
            text = (
                f"👤 Пользователь открыл WebApp\n"
                f"ID: {data.get('id')}\n"
                f"Имя: {data.get('first_name')} {data.get('last_name','')}\n"
                f"Username: @{data.get('username','')}\n"
                f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            bot.send_message(CHANNEL_ID, text)
    except Exception as e:
        print("Ошибка:", e)