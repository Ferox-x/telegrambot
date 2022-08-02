from telebot.types import Message
from database import code_database
from loader import bot
from keyboards.reply.commands_buttons import commands_buttons


def bot_start(message: Message) -> None:
    """
    Хендлер, принимает команду /start.

    :param message:
    """

    message_to_user: str = 'Привет, {0.first_name}, меня зовут Travel'.format(
        message.from_user)
    bot.send_message(message.chat.id, message_to_user,
                     reply_markup=commands_buttons())

    us_id: int = message.from_user.id
    us_name: str = message.from_user.first_name

    code_database.insert_info(us_id, us_name)
