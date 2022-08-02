from loader import bot
from handlers.default_heandlers import commands, help, history, start, clear_history
from utils.set_bot_commands import set_default_commands
from telebot.types import Message
from utils.info.user_info import UserInfo


@bot.message_handler(commands=['start', 'help', 'lowprice',
                               'highprice', 'bestdeal', 'history', 'clear'])
def get_start_message(message: Message) -> None:

    """ Функция, для получения запроса от пользователя и дальнейшей передачи информации """
    tg_user: UserInfo = UserInfo.get_user(message.chat.id)
    tg_user.clear()
    tg_user.user_id = message.chat.id
    text = message.text
    all_commands = {
        '/start': start.bot_start,
        '/help': help.bot_help,
        '/lowprice': commands.commands,
        '/highprice': commands.commands,
        '/bestdeal': commands.commands,
        '/history': history.history,
        '/clear': clear_history.clear
    }

    if text in all_commands:

        all_commands.get(message.text)(message)


if __name__ == '__main__':
    set_default_commands(bot)
    bot.infinity_polling()
