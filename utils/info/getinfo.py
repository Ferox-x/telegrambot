from telebot.types import Message
from loader import bot
from keyboards.inline.yes_or_not import yes_or_not
from utils.search.search import search_hotel_info, find_destination_id
from utils.info.user_info import UserInfo
from loguru import logger
from keyboards.inline.calendar import calendar_keyboard


logger.add('debug.log', format='{time} {level} {message}',
           level='DEBUG')


@logger.catch()
def get_info(message: Message) -> None:
    """
    Функция собирает информацию от пользователя
    (Город, количество отелей, надобность картинок)

    :param message: входящие сообщение пользователя
    """

    bot.send_message(message.chat.id, 'Введите город.')
    bot.register_next_step_handler(message, get_city)


@logger.catch()
def get_city(message: Message) -> None:
    """
    Функция получает город для

    :param message: входящие сообщение пользователя
    """
    tg_user: UserInfo = UserInfo.get_user(message.chat.id)

    tg_user.city = message.text
    find_destination_id(info_destination_id=tg_user.city, message=message)

    if tg_user.city_not_found:
        bot.send_message(tg_user.user_id, 'Город не найден.')
        bot.register_next_step_handler(tg_user.user_id, get_city)


@logger.catch()
def get_date(message: Message) -> None:
    """
    Функция получает информацию о дате заезда и выезда из отеля

    :param message: входящие сообщение пользователя
    """

    calendar_keyboard(message)


@logger.catch()
def get_total(message: Message) -> None:
    """
    Функция получает количество отелей

    :param message: входящие сообщение пользователя
    """

    tg_user = UserInfo.get_user(message.chat.id)

    if message.text.isdigit() and int(message.text) > 0:

        if int(message.text) > 25:
            bot.send_message(tg_user.user_id, 'Превышено максимальное '
                                              'количество отелей, '
                                              'значение изменено на 25.')
            tg_user.total = 25

        tg_user.total = int(message.text)

        bot.send_message(tg_user.user_id, 'Картинки?',
                         reply_markup=yes_or_not())

    else:
        bot.send_message(tg_user.user_id,
                         'Введите цифрами, значение должно быть больше 0.')
        bot.register_next_step_handler(message, get_total)


@logger.catch()
def get_total_pictures(message: Message):
    """
    Функция принимает количество картинок, если их больше 10
    присваивает значение 10

    :param message: входящие сообщение пользователя
    """
    tg_user = UserInfo.get_user(message.chat.id)

    if message.text.isdigit() and int(message.text) > 0:
        if int(message.text) > 5:
            tg_user.total_pictures = 5
            bot.send_message(tg_user.user_id,
                             'Превышено максимальное количество фотографий,'
                             ' значение изменено на 5.')
        tg_user.total_pictures = int(message.text)
        bestdeal_check(message)

    else:
        bot.send_message(tg_user.user_id,
                         'Введите цифрами, значение должно быть больше 0.')
        bot.register_next_step_handler(message, get_total_pictures)


@logger.catch()
def bestdeal_check(message) -> None:
    """
    Функция получает информацию о надобности картинок отелей

    :param message: входящие сообщение пользователя
    """
    tg_user: UserInfo = UserInfo.get_user(message.chat.id)

    if tg_user.beast_deal:
        bot.send_message(tg_user.user_id,
                         'Введите минимальную цену (руб).')
        bot.register_next_step_handler(message, get_price_min)
    else:
        search_hotel_info(message=message)


@logger.catch()
def get_price_min(message: Message) -> None:
    """
    Функция получает информацию о минимальной стоимости за одну ночь

    :param message: входящие сообщение пользователя
    """

    tg_user = UserInfo.get_user(message.chat.id)

    if message.text.isdigit() and int(message.text) > 0:

        tg_user.price_min = int(message.text)
        bot.send_message(tg_user.user_id,
                         'Введите максимальную цену (руб).')
        bot.register_next_step_handler(message, get_price_max)

    else:
        bot.send_message(tg_user.user_id,
                         'Введите цифрами, значение должно быть больше 0.')
        bot.register_next_step_handler(message, get_price_min)


@logger.catch()
def get_price_max(message: Message) -> None:
    """
    Функция получает информацию о максимальной стоимости за ночь

    :param message: входящие сообщение пользователя
    """
    tg_user = UserInfo.get_user(message.chat.id)

    if message.text.isdigit() and int(message.text) > 0:

        tg_user.price_high = int(message.text)
        bot.send_message(tg_user.user_id,
                         'Введите минимальное расстояние от центра (км).')
        bot.register_next_step_handler(message, get_distance_centre_min)

    else:
        bot.send_message(tg_user.user_id,
                         'Введите цифрами, значение должно быть больше 0.')
        bot.register_next_step_handler(message, get_price_max)


@logger.catch()
def get_distance_centre_min(message: Message) -> None:
    """
    Функция принимает значение о минимальной дистанции до центра

    :param message: входящие сообщение пользователя
    """
    tg_user = UserInfo.get_user(message.chat.id)

    if message.text.isdigit() and int(message.text) > 0:

        tg_user.landmark_min = int(message.text)
        bot.send_message(tg_user.user_id,
                         'Введите максимальное расстояние от центра (км).')
        bot.register_next_step_handler(message, get_distance_centre_max)

    else:
        bot.send_message(tg_user.user_id,
                         'Введите цифрами, значение должно быть больше 0')
        bot.register_next_step_handler(message, get_distance_centre_min)


@logger.catch()
def get_distance_centre_max(message: Message) -> None:
    """
    Функция принимает значение о максимальной дистанции до центра

    :param message: входящие сообщение пользователя
    """
    tg_user = UserInfo.get_user(message.chat.id)

    if message.text.isdigit() and int(message.text) > 0:

        tg_user.landmark_max = int(message.text)
        search_hotel_info(message=message)

    else:
        bot.send_message(tg_user.user_id,
                         'Введите цифрами, значение должно быть больше 0')
        bot.register_next_step_handler(message, get_distance_centre_min)
