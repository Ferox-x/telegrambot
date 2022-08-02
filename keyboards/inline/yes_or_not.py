from telebot import types
from telebot.types import InlineKeyboardMarkup


def yes_or_not() -> InlineKeyboardMarkup:
    """
    Inline клавиатура да, нет.
    :return: markup
    """
    markup = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton(text='Да', callback_data='да')
    no_button = types.InlineKeyboardButton(text='Нет', callback_data='нет')
    markup.add(yes_button, no_button)
    return markup
