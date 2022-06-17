import base64
import hashlib
import hmac

from flask import current_app


def compare_password(password_hash, other_password: str) -> bool:
    """
    Функция производит сравнивание двух паролей, переводит пароль, введенный пользователем в хэш
    и сравнивает с имеющимся.

    :param password_hash: Хеш-пароль.
    :param other_password: Пароль в открытом виде.
    :return: True или False
    """
    return hmac.compare_digest(
        base64.b64decode(password_hash),
        hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            current_app.config['PWD_HASH_SALT'],
            current_app.config["PWD_HASH_ITERATIONS"],
        ))


def make_user_password_hash(password: str):
    """
    Метод производит генерацию хеша из передаваемого пароля. Кодируется методом SHA256,
    с использованием SALT и количеством иттераций, задаваемых в конфигурации приложения.

    :param password: Пароль в виде строки.
    :return: Сгенерированный хэш-пароль
    """
    return base64.b64encode(hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        current_app.config['PWD_HASH_SALT'],
        current_app.config["PWD_HASH_ITERATIONS"],
    ))


