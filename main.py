import os
import telebot
import threading
import time
from datetime import datetime
from storage import load, save
from keyboards import done_delay_keyboard

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("Bot token is not defined")

bot = telebot.TeleBot(BOT_TOKEN)
data = load()
temp = {}

# ===== Создание напоминания =====
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "📝 О чём мне напоминать?")
    temp[m.chat.id] = {}
    bot.register_next_step_handler(m, get_text)

def get_text(m):
    temp[m.chat.id]["text"] = m.text
    bot.send_message(m.chat.id, "⏰ Время? (HH:MM, 24h)")
    bot.register_next_step_handler(m, get_time)

def get_time(m):
    temp[m.chat.id]["time"] = m.text
    bot.send_message(
        m.chat.id,
        "📅 Дни? (Mon,Tue,Wed,Thu,Fri,Sat,Sun, через запятую)\n"
        "Пример: Mon,Wed,Fri"
    )
    bot.register_next_step_handler(m, get_days)

def get_days(m):
    uid = str(m.chat.id)
    reminder = {
        "text": temp[m.chat.id]["text"],
        "time": temp[m.chat.id]["time"],
        "days": [d.strip() for d in m.text.split(",")],
        "done": False,
        "delayed": False
    }
    data.setdefault(uid, []).append(reminder)
    save(data)
    bot.send_message(m.chat.id, "✅ Напоминание сохранено с кнопками")

# ===== Callback кнопок =====
@bot.callback_query_handler(func=lambda c: c.data in ["done", "delay10"])
def callback(c):
    uid = str(c.message.chat.id)
    for r in data.get(uid, []):
        if c.data == "done":
            r["done"] = True
            bot.edit_message_text(
                "🎉 Отлично! До следующего раза",
                c.message.chat.id,
                c.message.message_id
            )
        elif c.data == "delay10":
            r["delayed"] = True
            bot.edit_message_text(
                "⏰ Напоминание отложено на 10 минут",
                c.message.chat.id,
                c.message.message_id
            )
            def delayed_send():
                time.sleep(600)
                r["delayed"] = False
                if not r["done"]:
                    send(bot, c.message.chat.id, r)
            threading.Thread(target=delayed_send).start()
    save(data)

# ===== Функция отправки напоминания =====
def send(bot, uid, reminder):
    bot.send_message(
        uid,
        f"⏰ Напоминание:\n\n{reminder['text']}",
        reply_markup=done_delay_keyboard()
    )

    def repeat():
        time.sleep(600)
        if not reminder["done"] and not reminder.get("delayed", False):
            send(bot, uid, reminder)

    threading.Thread(target=repeat).start()

# ===== Шедулер =====
def start_scheduler():
    def loop():
        while True:
            now = datetime.now()
            weekday_full = now.strftime("%A")
            weekday_map = {
                "Monday": "Mon", "Tuesday": "Tue", "Wednesday": "Wed",
                "Thursday": "Thu", "Friday": "Fri", "Saturday": "Sat", "Sunday": "Sun"
            }
            today = weekday_map[weekday_full]

            for uid, reminders in data.items():
                for r in reminders:
                    try:
                        h, m = map(int, r["time"].split(":"))
                        reminder_time = now.replace(hour=h, minute=m, second=0, microsecond=0)
                    except:
                        continue

                    if now >= reminder_time and today in r["days"] and not r["done"] and not r.get("delayed", False):
                        send(bot, int(uid), r)

            time.sleep(10)

    threading.Thread(target=loop, daemon=True).start()

start_scheduler()
print("Бот запущен с кнопками и поддержкой дней недели")
bot.infinity_polling()