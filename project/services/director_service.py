from project.dao.director import DirectorDAO
from project.exceptions import ItemNotFound
from project.schemas.director import DirectorSchema


class DirectorService:
    """
    Класс описывает сервисы для работы в приложении Flask с таблицей режиссеров.
    """
    def __init__(self, dao: DirectorDAO):
        """
        Метод инициализирует DAO
        :param dao: DAO объект
        """
        self.dao = dao

    def get_one(self, did: int) -> ItemNotFound or list:
        """
        Метод реализует получение записи об одном режиссере из базы данных по id.

        :param did: id режиссера в базе данных.
        :return: Сериализованные данные о режиссере по id.
        При отсутствии id в базе данных возвращает exception.
        """
        director = self.dao.get_one(did)
        if not director:
            raise ItemNotFound
        return DirectorSchema().dump(director)

    def get_all(self) -> list:
        """
        Метод реализует получение записей о всех режиссерах из базы данных.

        :return: Сериализованные данные о всех режиссерах.
        """
        directors = self.dao.get_all()
        return DirectorSchema(many=True).dump(directors)

    def get_by_page(self, page: int) -> list:
        """
        Метод реализует получение записей из базы данных постранично.
        Ограничение на количество записей устанавливается в конфигурации приложения.

        :param page: Номер страницы.
        :return: Cериализованные данные о всех фильмах постранично.
        """
        directors_by_page = self.dao.get_by_page(page)
        return DirectorSchema(many=True).dump(directors_by_page)
