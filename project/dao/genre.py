from flask import current_app

from project.dao.models.genre import Genre


class GenreDAO:
    """
    Класс описывает Data Access Object (DAO) для работы с базой данный, с таблицей фильмов.
    """

    def __init__(self, session):
        """
        Метод инициализирует поле класса session, как сессию работы с базой данных.

        :param session: Сессия базы данных
        """
        self.session = session

    def get_one(self, gig: int) -> list[Genre]:
        """
        Метод реализует получение записи об одном жанре из базы данных по id.

        :param gig: id жанра в базе данных.
        :return: Ответ базы данных на запрос о получении записи о жанре по id.
        """
        return self.session.query(Genre).get(gig)

    def get_all(self) -> list[Genre]:
        """
        Метод реализует получение записей о всех жанрах из базы данных.

        :return: Ответ базы данных на запрос получения данных о всех жанрах.
        """
        return self.session.query(Genre).all()

    def get_by_page(self, page: int) -> list[Genre]:
        """
        Метод реализует получение записи о всех жанрах из базы данных в количестве, заданном огранчением на выдачу
        страниц.

        :param page: Номер страницы.
        :return: Ответ базы данных на запрос
        """
        page_limit = current_app.config["ITEMS_PER_PAGE"]
        current_page = page_limit * (int(page) - 1)

        return self.session.query(Genre).limit(page_limit).offset(current_page).all()
