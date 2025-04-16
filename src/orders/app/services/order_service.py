

import os


class OrderService:

    BASE_URL_USER_API = os.getenv('PATH_API_USER')
    PASSWORD_DEFAULT = os.getenv('PASSWORD_DEFAULT')

    @staticmethod
    def get_all():
        orders = OrderRepository.get_all()