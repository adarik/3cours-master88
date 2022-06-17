from project.dao.models.movie import Movie
from flask import current_app


class MovieDAO:
    """
    Класс описывает Data Access Object (DAO) для работы с базой данный, с таблицей фильмов.
    """

    def __init__(self, session):
        """
        Метод инициализирует поле класса session, как сессию работы с базой данных.
        :param session: Сессия базы данных
        """
        self.session = session

    def get_one(self, mid: int) -> list[Movie]:
        """
        Метод реализует получение записи об одном фильме из базы данных по id.

        :param mid: id фильма в базе данных.
        :return: Ответ базы данных на запрос о получении записи о фильме по id.
        """
        return self.session.query(Movie).filter(Movie.id == mid).one_or_none()

    def get_all(self) -> list[Movie]:
        """
        Метод реализует получение записей о всех фильмах из базы данных.

        :return: Ответ базы данных на запрос получения данных о всех фильмах.
        """
        return self.session.query(Movie).all()

    def get_by_page(self, page: int) -> list[Movie]:
        """
        Метод реализует получение записи о всех фильмах из базы данных в количестве, заданном огранчением на выдачу
        страниц.

        :param page: Номер страницы.
        :return: Ответ базы данных на запрос
        """
        page_limit = current_app.config["ITEMS_PER_PAGE"]
        current_page = page_limit * (int(page) - 1)

        return self.session.query(Movie).limit(page_limit).offset(current_page).all()

    def get_newest_by_page(self, page: int) -> list[Movie]:
        """
        Метод реализует получение записи о всех фильмах из базы данных в количестве, заданном огранчением на выдачу
        страниц и отсортированном по году выпуска

        :param page: Номер страницы.
        :return: Ответ базы данных на запрос
        """
        page_limit = current_app.config["ITEMS_PER_PAGE"]
        current_page = page_limit * (int(page) - 1)

        return self.session.query(Movie).order_by(Movie.year.desc()).limit(page_limit).offset(current_page).all()

    def get_newest(self) -> list[Movie]:
        return self.session.query(Movie).order_by(Movie.year.desc()).all()
