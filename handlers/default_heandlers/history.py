from telebot.types import Message
from database.code_database import show_history
from loader import bot


def history(message: Message) -> None:
    """
    Хендлер, принимает команду /history.

    :param message:
    """
    show_history(message.chat.id, message)

