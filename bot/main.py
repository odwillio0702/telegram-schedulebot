import os
import json
from datetime import datetime
from threading import Thread
from dotenv import load_dotenv
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# ==============================
# Загрузка переменных из .env
# ==============================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # ID канала для логов
WEBAPP_URL = os.getenv("WEBAPP_URL")      # ссылка на WebApp

# ==============================
# Создаем бота
# ==============================
bot = telebot.TeleBot(BOT_TOKEN)

# ==============================
# /start
# ==============================
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(
            "Открыть профиль",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    bot.send_message(
        message.chat.id,
        "Клац 👇",
        reply_markup=markup
    )

# ==============================
# Обработка данных с WebApp
# ==============================
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app(message):
    try:
        data = json.loads(message.web_app_data.data)
        print("WEBAPP DATA:", data)

        text = (
            f"👤 Открытие профиля\n"
            f"ID: {data.get('id')}\n"
            f"Имя: {data.get('first_name','')}\n"
            f"Username: @{data.get('username','')}\n"
            f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
        )

        bot.send_message(CHANNEL_ID, text)

    except Exception as e:
        print("Ошибка WebApp:", e)

from PIL import Image
import io

# ==============================
# Фото → ASCII
# ==============================
ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image: Image.Image, width=80):
    image = image.convert("L")  # в ч/б
    w, h = image.size
    aspect_ratio = h / w
    new_height = int(aspect_ratio * width * 0.55)
    image = image.resize((width, new_height))

    pixels = image.getdata()
    chars = "".join(ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixels)

    ascii_image = "\n".join(
        chars[i:i+width] for i in range(0, len(chars), width)
    )
    return ascii_image


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)

        image = Image.open(io.BytesIO(downloaded))
        ascii_art = image_to_ascii(image)

        # Telegram ограничение по длине сообщений
        if len(ascii_art) > 4000:
            ascii_art = ascii_art[:4000]

        bot.send_message(
            message.chat.id,
            f"<pre>{ascii_art}</pre>",
            parse_mode="HTML"
        )

    except Exception as e:
        bot.send_message(message.chat.id, "❌ Не смог обработать изображение")
        print("IMAGE ERROR:", e)
# ==============================
# Запуск бота
# ==============================
if __name__ == "__main__":
    print("Bot started")
    bot.infinity_polling()