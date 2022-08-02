import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN')
RAPID_API_KEY: str = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS: tuple = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('lowprice', 'Поиск дешевых отелей'),
    ('highprice', 'Поиск дорогих отелей'),
    ('bestdeal', 'Лучшее предложение'),
    ('history', 'История запросов'),
    ('clear', 'Удалить историю')
)
