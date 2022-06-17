from sqlalchemy import and_

from project.dao.models.movie import Movie
from project.dao.models.user_movie import UserMovie


class FavoriteMovieDAO:
    def __init__(self, session):
        """
        Метод инициализирует поле класса session, как сессию работы с базой данных.

        :param session: Сессия базы данных
        """
        self.session = session

    def get_one(self, id_: int) -> list:
        """
        Метод получает данные из таблицы по id
        """
        return self.session.query(UserMovie).filter(UserMovie.id == id_).first()

    def create(self, movie_id: int, user_id: int):
        """
        Метод реализует запись новых данных в базу данных.

        :param movie_id: id фильма.
        :param user_id: id авторизованного пользователя
        """
        new_fav = UserMovie(user_id=user_id, movie_id=movie_id)
        self.session.add(new_fav)
        self.session.commit()

    def is_movie_id_in(self, mid: int) -> list or None:
        """
        Метод реализует поиск фильма в таблице с избранными

        :param mid: id фильма
        :return: list or None
        """
        return self.session.query(UserMovie).filter(UserMovie.movie_id == mid).one_or_none()

    def delete(self, data: list) -> None:
        """
        Метод производит удаление данных из таблицы
        """
        self.session.delete(data)
        self.session.commit()

    def get_id(self, movie_id: int, user_id: int):
        """
        Метод реализует получение id записи в таблице
        """
        data = self.session.query(UserMovie).filter(
            and_(UserMovie.user_id == user_id, UserMovie.movie_id == movie_id)).first()
        return data.id

    def get_movies_for_user(self, user_id) -> list:
        """
        Метод реализует получение всех фильмов, понравившихся пользователю.

        :param user_id: id авторизованного пользователя
        """
        return self.session.query(Movie).select_from(UserMovie).filter(UserMovie.user_id == user_id,
                                                                       UserMovie.movie_id == Movie.id).all()
