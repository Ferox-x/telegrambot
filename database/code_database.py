from peewee import IntegrityError
from peewee import SqliteDatabase, Model, IntegerField, CharField, DateField
from playhouse.sqlite_ext import JSONField
from json import loads
from datetime import datetime
from typing import Dict
from loader import bot
from telebot.types import Message
from loguru import logger
from utils.info.user_info import UserInfo


logger.add('debug.log', format='{time} {level} {message}',
           level='DEBUG')

data: SqliteDatabase = SqliteDatabase('database/database.db')


class BaseModel(Model):
    class Meta:
        database: SqliteDatabase = data


class User(BaseModel):
    """Класс с информацией о полях таблицы"""
    telegram_id: IntegerField = IntegerField(column_name='telegram_id',
                                             unique=True, null=True)
    user_name: CharField = CharField(column_name='user_name', null=True)
    hotels_in_city: JSONField = JSONField(column_name='hotels_in_city', null=True)
    parent_id: IntegerField = IntegerField(column_name='parent_id', null=True)
    date: DateField = DateField(column_name='date', null=True)


@logger.catch()
def insert_info(telegram_id: int, name: str) -> None:
    """
    Функция добавляет информацию в базу данных.

    :param telegram_id: ид пользователя
    :param name: имя пользователя
    """
    data.connect()
    User.create_table()
    with data:
        try:
            user: User = User(telegram_id=telegram_id, user_name=name)
            user.save()
        except IntegrityError as error:
            logger.exception(error)


@logger.catch()
def insert_user_history(telegram_id: int, hotels_in_city: str) -> None:
    """
    Функция добавляет историю в базу данных.

    :param telegram_id: ид пользователя
    :param hotels_in_city: информация об отелях в формате JSON
    :return:
    """
    data.connect()
    User.create_table()
    with data:
        user: User = User(hotels_in_city=hotels_in_city, parent_id=telegram_id,
                          date=datetime.now())
        user.save()


@logger.catch()
def show_history(telegram_id: int, message: Message) -> None:
    """
    Функция отправляет историю поисков пользователю.

    :param telegram_id: ид пользователя
    :param message: входящие сообщение пользователя
    """
    data.connect()
    tg_user: UserInfo = UserInfo.get_user(message.chat.id)

    with data:
        query = (User.select(User.hotels_in_city, User.date)
                 .where(User.parent_id == telegram_id))

        history_message: str = ''
        empty_history = True
        for note in query:
            empty_history = False
            try:

                hotels_info: Dict = loads(note.hotels_in_city)
                history_message += '=' * 48 + '\n'

                command: str = hotels_info.get('0').get('command')
                city: str = hotels_info.get('0').get('destination_id')

                history_message += ('<i>{city}</i>, '
                                    '<i>{command}</i>, '
                                    '<i>{date}</i> \n\n').format(city=city,
                                                                 command=command,
                                                                 date=note.date)
            except AttributeError as error:
                logger.exception(error)
            else:
                for key_hotel, hotel in hotels_info.items():

                    hotel_info: str = hotel.get('hotel_info')
                    history_message += '{hotel_info}\n\n'.format(
                        hotel_info=hotel_info)

                    if len(history_message) > 2000:
                        bot.send_message(tg_user.user_id, history_message,
                                         parse_mode='html')
                        history_message = ''
        if empty_history:
            bot.send_message(tg_user.user_id, 'История пуста.')


@logger.catch()
def clear_history(telegram_id: int) -> None:
    """
    Функция удаляет историю поиска пользователя

    :param telegram_id: ид пользователя
    """
    data.connect()

    with data:
        query = User.select(User.parent_id).where(User.parent_id == telegram_id)
        User.delete().where(User.parent_id.in_(query)).execute()
