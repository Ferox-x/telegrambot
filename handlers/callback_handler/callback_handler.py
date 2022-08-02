from loader import bot
from telebot.types import CallbackQuery
from utils.info.getinfo import get_total_pictures, bestdeal_check, get_date
from utils.info.user_info import UserInfo


@bot.callback_query_handler(func=lambda call: True)
def answer(call: CallbackQuery) -> None:
    """
    Хендлер, принимающий сообщение от InlineButtons

    :param call: сообщение от InlineButtons
    """
    tg_user: UserInfo = UserInfo.get_user(call.message.chat.id)

    if call.data == 'да':
        tg_user.pictures = True
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='<i>Показать картинки</i>: '
                                   '<b>Да</b>',
                              parse_mode='html')
        bot.send_message(tg_user.user_id, 'Сколько картинок?')
        bot.register_next_step_handler(call.message, get_total_pictures)

    elif call.data == 'нет':
        bot.edit_message_text(chat_id=tg_user.user_id,
                              message_id=call.message.message_id,
                              text='<i>Показать картинки</i>: '
                                   '<b>нет</b>',
                              parse_mode='html')
        bestdeal_check(call.message)

    elif call.data.isdigit():
        destination_id: str = call.data
        name = UserInfo.cities.get(destination_id)
        bot.edit_message_text(chat_id=tg_user.user_id,
                              message_id=call.message.message_id,
                              text='<i>Вы выбрали</i>: '
                                   '<b>{name}</b>'.format(name=name),
                              parse_mode='html')

        tg_user.destination_id = destination_id
        bot.send_message(tg_user.user_id,
                         'Выберите дату заезда.')
        get_date(call.message)
