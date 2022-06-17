from project.dao.favorite_movie import FavoriteMovieDAO
from project.exceptions import ItemNotFound
from project.schemas.movie import MovieSchema


class FavoriteMovieService:
    def __init__(self, dao: FavoriteMovieDAO):
        """
        Метод инициализирует DAO

        :param dao: DAO объект
        """
        self.dao = dao

    def get_one(self, id_: int) -> list:
        """
        Метод получает данные из таблицы по id
        """
        return self.dao.get_one(id_)

    def create(self, user_id: int, movie_id: int) -> None:
        """
        Метод реализует запись новых данных в базу данных.

        :param movie_id: id фильма.
        :param user_id: id авторизованного пользователя
        """
        return self.dao.create(movie_id=movie_id, user_id=user_id)

    def is_movie_id_in(self, movie_id: int) -> bool:
        """
        Метод реализует поиск фильма в таблице с избранными

        :param movie_id: id фильма
        :return: True или ошибка
        """
        if not self.dao.is_movie_id_in(movie_id):
            raise ItemNotFound
        return True

    def delete(self, id_: int) -> None:
        """
        Метод реализует удаление записи в базе данных.

        :param id_: id записи в базе данных.
        """
        data = self.get_one(id_)
        self.dao.delete(data)

    def get_id(self, movie_id: int, user_id: int):
        """
        Метод реализует получение id записи в таблицы базы данных.

        :param movie_id: id фильма
        :param user_id: id авторизованного пользователя
        """

        data_id = self.dao.get_id(movie_id, user_id)
        if not data_id:
            raise ItemNotFound
        return data_id

    def get_movies_for_user(self, user_id: int) -> list:
        """
        Метод реализует получение всех фильмов, понравившихся пользователю.

        :param user_id: id авторизованного пользователя
        """

        movies = self.dao.get_movies_for_user(user_id)
        if not movies:
            raise ItemNotFound
        return MovieSchema(many=True).dump(movies)
