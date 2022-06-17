from project.dao.user import UserDAO
from project.exceptions import PasswordError, UserAlreadyHave
from project.tools.hash_tools import make_user_password_hash, compare_password


class UserService:
    """
    Класс описывает сервисы для работы в приложении Flask с таблицей фильмов.
    """

    def __init__(self, dao: UserDAO):
        """
        Метод инициализирует DAO

        :param dao: DAO объект
        """
        self.dao = dao

    def get_all(self) -> list:
        """
        Метод реализует получение записей о всех пользователях из базы данных.

        :return: Ответ базы данных на запрос получения данных о всех пользователях.
        """
        return self.dao.get_all()

    def get_one(self, uid: int) -> None or list:
        """
        Метод реализует получение записи об одном пользователе из базы данных по id.

        :param uid: id пользователя в базе данных.
        :return: Ответ базы данных на запрос о получении записи о пользователе по id.
        При отсутствии id в базе данных возвращает None.
        """
        user = self.dao.get_one(uid)
        if not user:
            return None
        return user

    def get_by_email(self, email: str):
        """
        Метод реализует получение записи об одном пользователе из базы данных по email.

        :param email: Имя пользователя.
        :return: Ответ базы данных на запрос о получении записи о пользователе по email
        """
        return self.dao.get_by_email(email)

    def create(self, data: dict) -> list:
        """
        Метод реализует запись новых данных в базу данных.

        :param data: Данные, которые необходимо записать в базу данных.
        """
        password = data['password']
        hash_password = make_user_password_hash(password)
        data['password'] = hash_password

        user = self.get_by_email(data['email'])

        if user:
            raise UserAlreadyHave

        return self.dao.create(data)

    def partial_update(self, email: str, data: dict) -> None:
        """
        Метод производит частичное обновление полей таблицы пользователей в базе данных

        :param email: Параметр для поиска необходимого для обновления пользователя
        :param data: Данные для обновления пользователя (имя, фамилия, любимые жанры)
        """
        user = self.get_by_email(email)

        if "name" in data:
            user.name = data.get("name")
        if "surname" in data:
            user.surname = data.get("surname")
        if "favorite_genre" in data:
            user.favorite_genre = data.get("favorite_genre")

        self.dao.update(user)

    def update_password(self, email: str, old_password: str, new_password: str) -> None:
        """
        Метод производит обновление пароля. Для обновления необходим старый пароль.

        :param email: Email для поиска пользователя в базе данных
        :param old_password: Старый пароль пользователя
        :param new_password: Новый пароль
        """
        user = self.get_by_email(email)

        if not compare_password(password_hash=user.password, other_password=old_password):
            raise PasswordError
        user.password = make_user_password_hash(new_password)

        self.dao.update(user)
