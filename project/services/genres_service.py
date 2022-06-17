from project.dao.genre import GenreDAO
from project.exceptions import ItemNotFound
from project.schemas.genre import GenreSchema


class GenreService:
    """
    Класс описывает сервисы для работы в приложении Flask с таблицей жанров.
    """
    def __init__(self, dao: GenreDAO):
        """
        Метод инициализирует DAO
        :param dao: DAO объект
        """
        self.dao = dao

    def get_one(self, gid: int) -> ItemNotFound or list:
        """
        Метод реализует получение записи об одном жанре из базы данных по id.

        :param gid: id жанра в базе данных.
        :return: Сериализованные данные о жанре по id.
        При отсутствии id в базе данных возвращает exception.
        """
        genre = self.dao.get_one(gid)
        if not genre:
            raise ItemNotFound
        return GenreSchema().dump(genre)

    def get_all(self) -> list:
        """
        Метод реализует получение записей о всех фильмах из базы данных.

        :return: Сериализованные данные о всех жанрах
        """
        genres = self.dao.get_all()
        return GenreSchema(many=True).dump(genres)

    def get_by_page(self, page: int) -> list:
        """
        Метод реализует получение записей из базы данных постранично.
        Ограничение на количество записей устанавливается в конфигурации приложения.

        :param page: Номер страницы.
        :return: Cериализованные данные о всех фильмах постранично.
        """
        genres_by_page = self.dao.get_by_page(page)
        return GenreSchema(many=True).dump(genres_by_page)
