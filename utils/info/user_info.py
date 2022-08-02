from typing import Dict


class UserInfo:
    """
    Класс хранящий информацию вводимую пользователем.
    """
    users = dict()
    cities = dict()

    def __init__(self, user_id):

        self.user_id: int = 0

        self.city: str = ''
        self.city_not_found = False
        self.destination_id: str = 'Город не найден'

        self.date_in = None
        self.date_out = None

        self.total: int = 0

        self.pictures: bool = False
        self.total_pictures: int = 0

        self.price_min: int = 0
        self.price_high: int = 0
        self.beast_deal: bool = False

        self.low_price = False
        self.high_price = False

        self.landmark_min: int = 0
        self.landmark_max: int = 0

        self.querystring_beast_deal: Dict = {'destinationId': '', 'pageNumber': '1',
                                             'pageSize': '', 'checkIn': '',
                                             'checkOut': '', 'adults1': '1',
                                             'priceMin': '', 'priceMax': '',
                                             'locale': 'ru_RU', 'currency': 'RUB'}
        self.querystring_low: Dict = {'destinationId': '', 'pageNumber': '1',
                                      'pageSize': '', 'checkIn': '',
                                      'checkOut': '', 'adults1': '1',
                                      'sortOrder': 'PRICE',
                                      'locale': 'ru_RU', 'currency': 'RUB'}
        self.querystring_high: Dict = {'destinationId': '', 'pageNumber': '1',
                                       'pageSize': '', 'checkIn': '',
                                       'checkOut': '', 'adults1': '1',
                                       'sortOrder': 'PRICE_HIGHEST_FIRST',
                                       'locale': 'ru_RU', 'currency': 'RUB'}
        UserInfo.add_user(user_id, self)

    def clear(self):
        """
        Метод приводит класс в изначальное состояние
        """
        self.city: str = ''
        self.destination_id = ''
        self.city_not_found = False
        self.date_in = None
        self.date_out = None
        self.total: int = 0
        self.pictures: bool = False
        self.total_pictures: int = 0
        self.price_min: int = 0
        self.price_high: int = 0
        self.beast_deal = False
        self.low_price = False
        self.high_price = False
        self.landmark_min: int = 0
        self.landmark_max: int = 0
        self.querystring_beast_deal = {'destinationId': '', 'pageNumber': '1',
                                       'pageSize': '', 'checkIn': '',
                                       'checkOut': '', 'adults1': '1',
                                       'priceMin': '', 'priceMax': '',
                                       'locale': 'ru_RU', 'currency': 'RUB'}
        self.querystring_low = {'destinationId': '', 'pageNumber': '1',
                                'pageSize': '', 'checkIn': '',
                                'checkOut': '', 'adults1': '1',
                                'sortOrder': 'PRICE',
                                'locale': 'ru_RU', 'currency': 'RUB'}
        self.querystring_high = {'destinationId': '', 'pageNumber': '1',
                                 'pageSize': '', 'checkIn': '',
                                 'checkOut': '', 'adults1': '1',
                                 'sortOrder': 'PRICE_HIGHEST_FIRST',
                                 'locale': 'ru_RU', 'currency': 'RUB'}

    @staticmethod
    def get_user(user_id):
        """
        Метод достает класс пользователя из словаря по id.
        :param user_id:
        :return: user
        """
        if UserInfo.users.get(user_id) is None:
            new_user: UserInfo = UserInfo(user_id)
            return new_user
        return UserInfo.users.get(user_id)

    @classmethod
    def add_user(cls, user_id, user) -> None:
        """
        Добавляет нового пользователя в словарь пользователей
        :param user_id: Ид пользователя
        :param user: Пользователь
        """
        cls.users[user_id] = user
