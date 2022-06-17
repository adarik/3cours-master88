import datetime
import calendar
import jwt
from flask import current_app

from project.exceptions import ItemNotFound, PasswordError
from project.services.user_service import UserService
from project.tools.hash_tools import compare_password


class AuthService:
    def __init__(self, user_service: UserService):
        """
        Инициализация сервисов для работы.

        :param user_service: сервисы, организующие работу с таблицей пользователей
        """
        self.user_service = user_service

    def register_new_user(self, data: dict):
        """
        Метод производит регистрацию нового пользователя

        :param data:
        :return: Пользователя в базе данных
        """
        return self.user_service.create(data)

    def generate_token(self, email: str, password: str, is_refresh=False):
        """
        Метод производит генерацию токенов на основе учетных данных пользователя или refresh токена

        :param email: Email пользователя
        :param password: Пароль
        :param is_refresh: Параметр, который указывает необходимо ли использовать refresh токен
        :return: Exception или словарь, состоящий из access и refresh токенов
        """
        user = self.user_service.get_by_email(email)

        if user is None:
            raise ItemNotFound

        if not is_refresh:
            if not compare_password(user.password, password):
                raise PasswordError

        data = {
            'email': user.email,
        }

        exp_access_token = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=current_app.config["TOKEN_EXPIRE_MINUTES"])
        data['exp'] = calendar.timegm(exp_access_token.timetuple())
        access_token = jwt.encode(data, current_app.config["JWT_SECRET"],
                                  algorithm=current_app.config["JWT_ALGORITHM"])

        exp_refresh_token = datetime.datetime.utcnow() + datetime.timedelta(
            days=current_app.config["TOKEN_EXPIRE_DAYS"])
        data['exp'] = calendar.timegm(exp_refresh_token.timetuple())
        refresh_token = jwt.encode(data, current_app.config["JWT_SECRET"],
                                   algorithm=current_app.config["JWT_ALGORITHM"])

        tokens = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return tokens

    def approve_refresh_token(self, refresh_token: str):
        """
        Метод генерирует запрос на формирование пары access и refresh токенов

        :param refresh_token: refresh токен, который будет использоваться для генерации новых токенов
        :return: Exception или словарь, состоящий из access и refresh токенов
        """
        data = jwt.decode(refresh_token, current_app.config["JWT_SECRET"],
                          algorithms=[current_app.config["JWT_ALGORITHM"]])
        email = data.get('email')

        user = self.user_service.get_by_email(email)

        if user is None:
            raise ItemNotFound

        return self.generate_token(email, user.password, is_refresh=True)
