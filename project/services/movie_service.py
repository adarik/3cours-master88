from project.dao.movie import MovieDAO
from project.exceptions import ItemNotFound
from project.schemas.movie import MovieSchema


class MovieService:
    """
    Класс описывает сервисы для работы в приложении Flask с таблицей фильмов.
    """
    def __init__(self, dao: MovieDAO):
        """
        Метод инициализирует DAO

        :param dao: DAO объект
        """
        self.dao = dao

    def get_one(self, mid: int) -> ItemNotFound or list:
        """
        Метод реализует получение записи об одном фильме из базы данных по id.

        :param mid: id фильма в базе данных.
        :return: Cериализованные данные о фильме по id.
        При отсутствии id в базе данных возвращает exception.
        """
        movie = self.dao.get_one(mid)
        if not movie:
            raise ItemNotFound
        return MovieSchema().dump(movie)

    def get_all(self) -> list:
        """
        Метод реализует получение записей о всех фильмах из базы данных.

        :return: Cериализованные данные о всех фильмах
        """
        movies = self.dao.get_all()
        return MovieSchema(many=True).dump(movies)

    def get_by_page(self, page: int) -> list:
        """
        Метод реализует получение записей из базы данных постранично.
        Ограничение на количество записей устанавливается в конфигурации приложения.

        :param page: Номер страницы.
        :return: Cериализованные данные о всех фильмах постранично.
        """
        movies_by_page = self.dao.get_by_page(page)
        return MovieSchema(many=True).dump(movies_by_page)

    def get_newest_by_page(self, page: int) -> list:
        """
        Метод реализует получение записей из базы данных постранично, отсортированным по году выпуска.
        Ограничение на количество записей устанавливается в конфигурации приложения.

        :param page: Номер страницы.
        :return: Cериализованные данные о всех фильмах постранично, в отсортированном по году выпуска виде.
        """

        newest_movies_by_page = self.dao.get_newest_by_page(page)
        return MovieSchema(many=True).dump(newest_movies_by_page)

    def get_newest(self) -> list:
        """
        Метод реализует получение записей из базы данных, отсортированным по году выпуска.
        Ограничение на количество записей устанавливается в конфигурации приложения.

        :return: Cериализованные данные о всех фильмах, в отсортированном по году выпуска виде.
        """
        newest_movies = self.dao.get_newest()
        return MovieSchema(many=True).dump(newest_movies)
