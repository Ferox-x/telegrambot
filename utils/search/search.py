from loader import bot
from loguru import logger
from json import loads, dumps
from typing import Dict, List
from re import search, Match, sub
from utils.info.user_info import UserInfo
from config_data.config import RAPID_API_KEY
from keyboards.inline.city_markup import city
from requests import request, Response, codes
from telebot.types import Message, InputMediaPhoto
from database.code_database import insert_user_history
from keyboards.reply.commands_buttons import commands_buttons


logger.add('debug.log', format='{time} {level} {message}',
           level='DEBUG')


@logger.catch()
def hotel_info_print(hotel_info: dict, message: Message) -> str:
    """
    Отправляет информацию об отеле пользователю

    :param hotel_info: Содержит информацию об отеле:
    :param message: входящие сообщение пользователя
    """
    tg_user: UserInfo = UserInfo.get_user(message.chat.id)
    name: str = hotel_info.get('name', 'Имя отеля не найдено')
    hotel_url = 'www.hotels.com/ho{id}'.format(id=hotel_info.get('id'))
    try:
        address: str = hotel_info.get('address').get('streetAddress', 'Андрес не найден')
        postal_code: str = hotel_info.get('address').get('postalCode', 'Индекс не найден')
    except AttributeError:
        address = 'Андрес не найден'
        postal_code = 'Индекс не найден'

    arrival_time = tg_user.date_out - tg_user.date_in
    days = arrival_time.days

    try:
        price: str = hotel_info.get('ratePlan').get('price').get('current')
    except AttributeError:
        price = 'Цена не найдена'
        total_price = 'Цена не найдена'
    else:
        total_price = int(price[:-3].replace(',', '')) * int(days)
    try:
        centre_distance: str = hotel_info.get('landmarks')[0].get('distance')
    except AttributeError:
        centre_distance = 'Расстояние до центра не найдено'

    message_hotel_info: str = ('<b>Отель</b>: {name}\n'
                               '<b>Адрес</b>: {address}\n'
                               '<b>Цена</b>: {price}\n'
                               '<b>Цена за {arrival_time} дней</b>: {total_price} RUB\n'
                               '<b>Почтовый индекс</b>: {postal_code}\n'
                               '<b>Расстояние до центра</b>: {distance}\n'
                               '<b>Ссылка</b>: {url}'.format(
                                name=name, address=address,
                                postal_code=postal_code, price=price,
                                distance=centre_distance, url=hotel_url,
                                total_price=total_price,
                                arrival_time=days))

    bot.send_message(tg_user.user_id, message_hotel_info, parse_mode='html')

    return message_hotel_info


@logger.catch()
def find_destination_id(info_destination_id: str, message: Message):
    """
    Функция находит destination_id и добавляет его в атрибут класса UserInfo
    :param info_destination_id: Название города:
    :param message: входящие сообщение пользователя
    """
    tg_user: UserInfo = UserInfo.get_user(message.chat.id)
    bot.send_message(message.from_user.id, 'Подождите уточняем '
                                           'информацию по городу')

    url_city: str = 'https://hotels4.p.rapidapi.com/locations/v2/search'

    querystring_city: Dict = {'query': info_destination_id, 'locale': 'ru_RU'}

    headers_city: Dict = {'X-RapidAPI-Host': 'hotels4.p.rapidapi.com',
                          'X-RapidAPI-Key': RAPID_API_KEY}
    try:
        response_city: Response = request('GET', url_city,
                                          headers=headers_city,
                                          params=querystring_city,
                                          timeout=10)
    except TimeoutError as time_error:
        bot.send_message(message.chat.id, 'Превышено время ожидание '
                                          'запроса от сервера')
        logger.exception(time_error)
    else:
        pattern: str = r'(?<="CITY_GROUP",).+?[\]]'
        find: Match[str] = search(pattern, response_city.text)
        destination_ids = list()

        if response_city.status_code == codes.ok:
            if find.group() != '"entities":[]':
                data_city = loads(f"{{{find[0]}}}")

                for index in data_city['entities']:
                    destination_id: str = index['destinationId']
                    caption: str = index['caption']
                    city_clear: str = sub(pattern=r'<[^>]+>',
                                          repl='', string=caption, count=0)
                    destination_ids.append({'destination_id': destination_id,
                                            'city_name': city_clear})

                city(message, destination_ids)
            else:
                tg_user.city_not_found = True


@logger.catch()
def find_hotels(querystring_hotel: Dict, message: Message) -> List:
    """
    Функция ищет отели
    :param querystring_hotel: Параметры для поиска отелей
    :param message: входящие сообщение пользователя
    """
    tg_user: UserInfo = UserInfo.get_user(message.chat.id)

    url_hotel: str = "https://hotels4.p.rapidapi.com/properties/list"

    headers_hotel: Dict = {'X-RapidAPI-Host': 'hotels4.p.rapidapi.com',
                           'X-RapidAPI-Key': RAPID_API_KEY}

    try:
        response_hotel: Response = request("GET", url_hotel, headers=headers_hotel,
                                           params=querystring_hotel, timeout=10)
    except TimeoutError as time_error:
        bot.send_message(tg_user.user_id, 'Превышено время ожидание '
                                          'запроса от сервера')
        logger.exception(time_error)
    else:
        pattern: str = r'(?<="results").+?[\]]'
        find: Match[str] = search(pattern, response_hotel.text)
        if response_hotel.status_code == codes.ok:
            if find is not None:
                data_hotel: Dict = loads(response_hotel.text)
                try:
                    hotels: List = data_hotel['data']['body']['searchResults']['results']
                except IndexError as index_error:
                    logger.exception(index_error)
                else:
                    if tg_user.beast_deal:
                        hotels_sorted = list(filter(lambda hotel: filter_hotel_distance(hotel, tg_user),
                                                    hotels))
                        return hotels_sorted
                    return hotels
            else:
                bot.send_message(tg_user.user_id, 'Отели не найдены!')


def filter_hotel_distance(hotel: dict, tg_user: UserInfo) -> bool:
    """
    Функция используется для фильтра отелей по дистанции от центра

    :param tg_user: Класс UserInfo
    :param hotel: информация об отеле:
    :return: bool
    """

    distance = hotel.get('landmarks')[0].get('distance')
    distance_int = float(distance[:-3].replace(',', '.'))
    if tg_user.landmark_min < distance_int < tg_user.landmark_max:
        return True
    else:
        return False


@logger.catch()
def find_photo_url(message: Message, hotel_id: str) -> list:
    """
    Функция ищет фотографии отелей
    :param message: входящие сообщение пользователя
    :param hotel_id: ид отеля
    """

    tg_user: UserInfo = UserInfo.get_user(message.chat.id)
    url = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'

    querystring: Dict = {'id': hotel_id}

    headers: Dict = {
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com',
        'X-RapidAPI-Key': RAPID_API_KEY
    }

    try:
        response = request("GET", url, headers=headers, params=querystring,
                           timeout=10)
    except TimeoutError as time_error:
        bot.send_message(tg_user.user_id, 'Превышено время ожидание '
                                          'запроса от сервера')
        logger.exception(time_error)
    else:
        data_photo: Dict = loads(response.text)
        if response.status_code == codes.ok:
            photos_urls = list()
            photos = tg_user.total_pictures

            for photo in range(photos):
                try:
                    suffix = data_photo['hotelImages'][photo]['sizes'][0]['suffix']
                    base_url: str = data_photo['hotelImages'][photo]['baseUrl']
                    photo_url: str = base_url.format(size=suffix)

                except IndexError as index_error:
                    logger.exception(index_error)
                else:
                    photos_urls.append(InputMediaPhoto(photo_url))
            return photos_urls


@logger.catch()
def search_hotel_info(message: Message):
    """
    Является основной функцией для поиска информации об отелях.
    Вызывает другие функции. По завершению работы добавляет
    информацию в базу данных. И приводит класс пользователя
    в изначальное состояние.

    :param message: входящие сообщение пользователя
    """

    tg_user: UserInfo = UserInfo.get_user(message.chat.id)

    querystring_hotel = dict()
    command: str = ''

    if tg_user.low_price:
        querystring_hotel = tg_user.querystring_low
        command = 'lowprice'

    elif tg_user.high_price:

        querystring_hotel = tg_user.querystring_high
        command = 'highprice'

    elif tg_user.beast_deal:

        querystring_hotel = tg_user.querystring_beast_deal
        querystring_hotel['priceMin'] = tg_user.price_min
        querystring_hotel['priceMax'] = tg_user.price_high
        command = 'beastdeal'

    querystring_hotel['destinationId'] = tg_user.destination_id
    querystring_hotel['pageSize'] = tg_user.total
    querystring_hotel['checkIn'] = tg_user.date_in
    querystring_hotel['checkOut'] = tg_user.date_out

    destination_id = tg_user.destination_id

    bot.send_message(tg_user.user_id, 'Ищем отели...')
    hotels = find_hotels(querystring_hotel, message)

    history_hotels = dict()
    photos = list()

    if tg_user.pictures:
        bot.send_message(tg_user.user_id, 'Ищем картинки...')
        for number, hotel in enumerate(hotels):
            hotel_id = hotel['id']
            photos.append(find_photo_url(message, hotel_id))

    if hotels:

        for number, hotel in enumerate(hotels):

            history_hotel = hotel_info_print(hotel_info=hotel,
                                             message=message)

            history_hotels[number] = {'command': command,
                                      'destination_id': destination_id,
                                      'hotel_info': history_hotel}

            if tg_user.pictures:
                bot.send_media_group(tg_user.user_id, photos[number])

            hotels_in_city = dumps(history_hotels)
            insert_user_history(tg_user.user_id, hotels_in_city)

    bot.send_message(message.chat.id, 'Поиск окончен.',
                     reply_markup=commands_buttons())
    tg_user.clear()
    querystring_hotel.clear()


if __name__ == '__main__':
    pass
