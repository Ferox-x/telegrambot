from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot) -> None:
    """
    Функция формирует меню команд бота.
    :param bot: Бот
    """
    bot.set_my_commands(
        [BotCommand(*command) for command in DEFAULT_COMMANDS]
    )
