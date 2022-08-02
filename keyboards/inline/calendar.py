from telegram_bot_calendar import DetailedTelegramCalendar
from telebot.types import Message, CallbackQuery
from loader import bot
from datetime import date
from utils.info.user_info import UserInfo
from utils.info import getinfo

LSTEP = {'y': 'год', 'm': 'месяц', 'd': 'день'}


def calendar_keyboard(message: Message) -> None:
    """
    Клавиатура календарь 1
    :param message: входящие сообщение пользователя
    """
    tg_user: UserInfo = UserInfo.get_user(message.chat.id)
    calendar, step = DetailedTelegramCalendar(locale='ru',
                                              calendar_id=1,
                                              min_date=date.today()).build()
    bot.send_message(tg_user.user_id,
                     f'Выбери <b>{LSTEP[step]}</b>',
                     reply_markup=calendar,
                     parse_mode='html')


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def cal(call: CallbackQuery) -> None:
    """
    Хендлер для первого календаря
    :param call: Сообщение от Inline клавиатуры
    """
    tg_user: UserInfo = UserInfo.get_user(call.message.chat.id)
    result, key, step = DetailedTelegramCalendar(calendar_id=1,
                                                 locale='ru',
                                                 min_date=date.today()).process(call.data)
    if not result and key:
        bot.edit_message_text(f'Выбери <b>{LSTEP[step]}</b>',
                              tg_user.user_id,
                              call.message.message_id,
                              reply_markup=key,
                              parse_mode='html')
    elif result:
        bot.edit_message_text(f'<i>Дата заезда</i> <b>{result}</b>',
                              call.message.chat.id,
                              call.message.message_id,
                              parse_mode='html')

        tg_user.date_in = result
        bot.send_message(tg_user.user_id, 'Введите дату выезда.')
        calendar_keyboard2(call.message)


def calendar_keyboard2(message: Message) -> None:
    """
    Клавиатура календарь 2
    :param message: входящие сообщение пользователя
    """
    tg_user = UserInfo.get_user(message.chat.id)
    date_in = tg_user.date_in
    calendar, step = DetailedTelegramCalendar(locale='ru',
                                              calendar_id=2,
                                              min_date=date_in).build()
    bot.send_message(tg_user.user_id,
                     f'Выбери <b>{LSTEP[step]}</b>',
                     reply_markup=calendar,
                     parse_mode='html')


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def cal(call: CallbackQuery) -> None:
    """
    Хендлер для второго календаря
    :param call: Сообщение от Inline клавиатуры
    """
    tg_user: UserInfo = UserInfo.get_user(call.message.chat.id)
    date_in = tg_user.date_in
    result, key, step = DetailedTelegramCalendar(calendar_id=2,
                                                 locale='ru',
                                                 min_date=date_in).process(call.data)
    if not result and key:
        bot.edit_message_text(f'Выбери <b>{LSTEP[step]}</b>',
                              tg_user.user_id,
                              call.message.message_id,
                              reply_markup=key,
                              parse_mode='html')
    elif result:
        bot.edit_message_text(f'<i>Дата выезда</i> <b>{result}</b>',
                              tg_user.user_id,
                              call.message.message_id,
                              parse_mode='html')

        tg_user.date_out = result
        bot.send_message(tg_user.user_id, 'Введите количество отелей.')
        bot.register_next_step_handler(call.message, getinfo.get_total)
