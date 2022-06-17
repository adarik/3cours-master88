import jwt
from flask import request, abort, current_app


def auth_required(func):
    """
    Функция-декоратор для проверки на то, что пользователь авторизован.

    :param func: Декорируемая функция
    """

    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401, "Need to authorization")

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, current_app.config["JWT_SECRET"],
                       algorithms=[current_app.config["JWT_ALGORITHM"]])
        except Exception as e:  # Надо переписать на что-то другое
            abort(401, 'JWT Decode Exception')
        return func(*args, **kwargs)

    return wrapper
