from telebot.types import Message
from loader import bot
from database.code_database import clear_history


def clear(message: Message) -> None:
    """
    Хендлер, принимающий сообщение от InlineButtons

    :param message: входящие сообщение пользователя
    """
    bot.send_message(message.chat.id, 'История удалена', parse_mode='html')
    clear_history(message.chat.id)
