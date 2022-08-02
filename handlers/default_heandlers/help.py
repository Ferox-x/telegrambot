from telebot.types import Message
from typing import List
from config_data.config import DEFAULT_COMMANDS
from loader import bot


def bot_help(message: Message) -> None:
    """
    Хендлер, принимает команду /help.

    :param message: входящие сообщение пользователя
    """
    text: List[str] = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))
