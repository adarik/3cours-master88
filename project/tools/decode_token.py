import jwt
from flask import request, current_app

from project.implemented import user_service


def get_email_from_token():
    """
    Функция производит получение email для дальнейшеного поиска в базе данных авторизованного пользователя из токена,
    который передает пользователь
    """

    data = request.headers["Authorization"]
    token = data.split("Bearer ")[-1]
    user_data = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=[current_app.config["JWT_ALGORITHM"]])

    return user_data['email']


def get_id_from_token():
    """
    Функция производит получение id для дальнейшеного поиска в базе данных авторизованного пользователя из токена,
    который передает пользователь
    """
    data = request.headers["Authorization"]
    token = data.split("Bearer ")[-1]
    user_data = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=[current_app.config["JWT_ALGORITHM"]])
    user = user_service.get_by_email(user_data["email"])

    return user.id
