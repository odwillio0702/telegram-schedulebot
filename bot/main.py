import os
import json
from datetime import datetime
from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from config import BOT_TOKEN, CHANNEL_ID, WEBAPP_URL
from bot.database import init_db
from bot.handlers import register_user, send_profile

if __name__ == "__main__":
    init_db()  # создаем таблицу если нет
    print("Bot started")
    bot.infinity_polling()
# ==============================
# Flask
# ==============================
app = Flask(__name__)

# ==============================
# Бот
# ==============================
bot = telebot.TeleBot(BOT_TOKEN)

# ==============================
# /start
# ==============================
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Открыть профиль", web_app=WebAppInfo(url=WEBAPP_URL)))
    bot.send_message(message.chat.id, "клац👇", reply_markup=markup)

# ==============================
# ДАННЫЕ С WEBAPP
# ==============================
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app(message):
    try:
        data = json.loads(message.web_app_data.data)
        print("WEBAPP DATA:", data)
        text = (
            f"👤 Открытие профиля\n\n"
            f"ID: {data.get('id')}\n"
            f"Имя: {data.get('first_name','')}\n"
            f"Username: @{data.get('username','')}\n"
            f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
        )
        bot.send_message(CHANNEL_ID, text)
    except Exception as e:
        print("Ошибка WebApp:", e)

# ==============================
# Запуск Flask + Bot
# ==============================
@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: bot.infinity_polling()).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))