from flask import current_app

from project.dao.models.director import Director


class DirectorDAO:
    """
    Класс описывает Data Access Object (DAO) для работы с базой данный, с таблицей фильмов.
    """

    def __init__(self, session):
        """
        Метод инициализирует поле класса session, как сессию работы с базой данных.

        :param session: Сессия базы данных
        """
        self.session = session

    def get_one(self, did: int) -> list[Director]:
        """
        Метод реализует получение записи об одном фильме из базы данных по id.

        :param did: id фильма в базе данных.
        :return: Ответ базы данных на запрос о получении записи о фильме по id.
        """
        return self.session.query(Director).get(did)

    def get_all(self) -> list[Director]:
        """
        Метод реализует получение записей о всех режиссерах из базы данных.

        :return: Ответ базы данных на запрос получения данных о всех режиссерах.
        """
        return self.session.query(Director).all()

    def get_by_page(self, page: int) -> list[Director]:
        """
        Метод реализует получение записи о всех режиссерах из базы данных в количестве, заданном огранчением на выдачу
        страниц.

        :param page: Номер страницы.
        :return: Ответ базы данных на запрос
        """
        page_limit = current_app.config["ITEMS_PER_PAGE"]
        current_page = page_limit * (int(page) - 1)

        return self.session.query(Director).limit(page_limit).offset(current_page).all()
