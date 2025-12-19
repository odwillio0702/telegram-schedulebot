import telebot
from telebot import types
import json
import threading
import time

BOT_TOKEN = "8485092572:AAHIdjrrXBOaIPD6-wN17cXtxleHYOWxJiw"
bot = telebot.TeleBot(BOT_TOKEN)

# Простая память напоминаний (можно заменить на файл/базу)
reminders = []

def save_reminder(chat_id, text, remind_time, days):
    reminders.append({
        "chat_id": chat_id,
        "text": text,
        "time": remind_time,
        "days": days.split(","),
        "sent_today": False
    })

# ================= Web App данные =================
@bot.message_handler(content_types=['web_app_data'])
def web_app(message):
    data = json.loads(message.web_app_data.data)
    
    text = data["text"]
    remind_time = data["time"]
    days = data["days"]
    
    save_reminder(
        chat_id=message.chat.id,
        text=text,
        remind_time=remind_time,
        days=days
    )
    
    bot.send_message(message.chat.id, "✅ Напоминание создано")

# ================= Команды =================
@bot.message_handler(commands=['start'])
def start(message):
    msg = "Привет! Я бот-напоминалка.\nКоманды:\n"
    msg += "/schedule - создать напоминание через Mini App\n"
    msg += "/list - показать все напоминания\n"
    msg += "/done [номер] - отметить напоминание выполненным"
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['list'])
def show_list(message):
    if not reminders:
        bot.send_message(message.chat.id, "Список пуст.")
        return
    msg = ""
    for i, r in enumerate(reminders):
        msg += f"{i+1}. {r['text']} ({','.join(r['days'])} {r['time']})\n"
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['done'])
def done(message):
    try:
        num = int(message.text.split()[1]) - 1
        reminders.pop(num)
        bot.send_message(message.chat.id, "✅ Напоминание выполнено и удалено")
    except:
        bot.send_message(message.chat.id, "Ошибка, используй /done [номер]")

# ================= Отправка напоминаний =================
def reminder_thread():
    while True:
        now = time.strftime("%H:%M")
        weekday = time.strftime("%a").lower()[:3]
        for r in reminders:
            if weekday in r["days"] and r["time"] == now and not r["sent_today"]:
                bot.send_message(r["chat_id"], f"⏰ Напоминание: {r['text']}")
                r["sent_today"] = True
            # Сбрасываем отметку на следующий день
            if weekday not in r["days"]:
                r["sent_today"] = False
        time.sleep(30)

threading.Thread(target=reminder_thread, daemon=True).start()

# ================= Старт бота =================
bot.infinity_polling()