from flask import request, abort
from flask_restx import Namespace, Resource

from project.exceptions import PasswordError
from project.implemented import user_service
from project.schemas.user import UserSchema
from project.tools.decode_token import get_email_from_token
from project.tools.decorators import auth_required

users_ns = Namespace('user')


@users_ns.route('/')
class UserView(Resource):
    """
    Class-Based View для отображения профиля авторизованного пользователя.
    """

    @users_ns.response(200, "OK")
    @auth_required
    def get(self):
        """
        Метод производит получение данных о профиле авторизованного пользователя. В выдаче отсутсвует хэш-пароль,
        хранящийся в базе данных. Реализуется путем отправки GET-запроса на /user.

        :return: Сериализованные данные в формате JSON и HTTP-код 200.
        """
        email = get_email_from_token()
        user = user_service.get_by_email(email)
        return UserSchema().dump(user), 200

    @users_ns.response(204, "OK")
    @auth_required
    def patch(self):
        """
        Метод производит частичное обновление данных в профиле авторизованного пользователя (имя, фамилия, любимый жанр)
        путем отправления PATCH-запроса на /user.
        """
        email = get_email_from_token()
        data = request.json

        user_service.partial_update(email, data)
        return "Update success", 204


@users_ns.route("/password")
class PasswordUpdateView(Resource):
    """
    Class-Based View для обновления авторизованным пользователем пароля.
    """

    @users_ns.response(200, "OK")
    @users_ns.response(401, "Password is incorrect")
    @auth_required
    def put(self):
        """
        Метод реализует изменение пароля авторизованного пользователя. Для обновления необходимо отправить
        новый пароль и старый пароль путем отправления PUT-запроса на /user/password.
        """
        # password_1 - старый пароль
        # password_2 - новый пароль
        email = get_email_from_token()
        req_json = request.json

        old_password = req_json.get('password_1')
        new_password = req_json.get('password_2')

        try:
            user_service.update_password(email, old_password, new_password)
            return "OK", 200
        except PasswordError:
            abort(401, "Password is incorrect")
