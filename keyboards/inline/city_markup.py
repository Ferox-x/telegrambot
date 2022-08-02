from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from telebot.types import Message
from typing import List, Dict
from loguru import logger
from utils.info.user_info import UserInfo


@logger.catch()
def city(message: Message, destination_ids: List) -> None:
    """
    Функция отправляет сообщение с найденными городами для уточнения информации
    :param message: входящие сообщение пользователя
    :param destination_ids: найденные города
    """
    tg_user: UserInfo = UserInfo.get_user(message.chat.id)

    bot.send_message(tg_user.user_id, 'Уточните, пожалуйста:',
                     reply_markup=city_markup(destination_ids, message))


@logger.catch()
def city_markup(cities: List[Dict], message: Message) -> InlineKeyboardMarkup:
    """
    Формирует Inline клавиатуру с городами
    :param cities: Города
    :param message: входящие сообщение пользователя
    :return: destinations
    """
    destinations = InlineKeyboardMarkup()
    tg_user: UserInfo = UserInfo.get_user(message.chat.id)
    for town in cities:
        tg_user.cities[town['destination_id']] = town['city_name']
        destinations.add(InlineKeyboardButton(text=town['city_name'],
                                              callback_data=f'{town["destination_id"]}'))

    return destinations
