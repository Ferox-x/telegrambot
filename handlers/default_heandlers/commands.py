from telebot.types import Message
from utils.info.user_info import UserInfo
from utils.info.getinfo import get_info


def commands(message: Message) -> None:
    """
    Функция вызывается при следующих командах:
    'lowprice', 'highprice', 'bestdeal'

    :param message:
    """
    tg_user: UserInfo = UserInfo.get_user(message.chat.id)
    command = message.text

    if message.chat.type == 'private':

        if command == '/lowprice':
            tg_user.low_price = True

        elif command == '/highprice':
            tg_user.high_price = True

        elif command == '/bestdeal':
            tg_user.beast_deal = True

        get_info(message=message)
