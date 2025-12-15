
import time
import threading
from datetime import datetime
from keyboards import done_delay_keyboard
import threading
import time

def send(bot, uid, reminder):
    bot.send_message(
        uid,
        f"⏰ Напоминание:\n\n{reminder['text']}",
        reply_markup=done_delay_keyboard()  # используем новую клавиатуру с кнопками
    )

    def repeat():
        time.sleep(600)  # 10 минут
        if not reminder["done"] and not reminder.get("delayed", False):
            send(bot, uid, reminder)

    threading.Thread(target=repeat).start()
