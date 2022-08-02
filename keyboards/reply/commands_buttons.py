from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def commands_buttons() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    lowprice_button = KeyboardButton(text='/lowprice')
    highprice_button = KeyboardButton(text='/highprice')
    bestdeal_button = KeyboardButton(text='/bestdeal')
    help_button = KeyboardButton(text='/help')
    history_button = KeyboardButton(text='/history')
    markup.add(lowprice_button, highprice_button, bestdeal_button,
               history_button, help_button)
    return markup
