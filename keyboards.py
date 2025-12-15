from telebot import types

def done_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("✅ Я сделал", callback_data="done"))
    return kb

def done_delay_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Я сделал", callback_data="done"),
        types.InlineKeyboardButton("⏰ Отложить на 10 минут", callback_data="delay10")
    )
    return kb