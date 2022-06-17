from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.implemented import genre_service

genres_ns = Namespace("genres")


@genres_ns.route("/")
class GenresView(Resource):
    """
    Метод реализует отправку GET-запросов на /genres.
    Возможные варианты исполнения:
    - отображение всех жанров GET-запросом на /genres;
    - отображение жанров постранично;
    (GET-запросом на /genres с использованием квери-параметра page);

    :return: Сериализованные данные в формате JSON, в зависимости от реализации запроса и HTTP-код 200
    """

    @genres_ns.response(200, "OK")
    def get(self):
        """
        Метод реализует отправку GET-запроса на /genres.
        Или отображение жанров постранично;
        (GET-запросом на /genres с использованием квери-параметра page);

        :return: Сериализованные данные в формате JSON и HTTP-код 200.
        """
        page = request.args.get('page')
        if page:
            return genre_service.get_by_page(page), 200
        return genre_service.get_all(), 200


@genres_ns.route("/<int:gid>")
class GenreView(Resource):
    """
        Class-Based View для отображения конкретного жанра из БД.
        Реализовано:
        - отображение данных о конкретном фильме GET-запросом на /genres/id;
        """

    @genres_ns.response(200, "OK")
    @genres_ns.response(404, "Genre not found")
    def get(self, gid: int):
        """
        Метод реализует отправку GET-запроса на /genres/id.

        :param gid: id жанра, информацию о котором нужно вытащить из БД.
        :return: Сериализованные данные в формате JSON и HTTP-код 200.
        В случае, если id нет в базе данных - exception и HTTP-код 404.
        """
        try:
            return genre_service.get_one(gid), 200
        except ItemNotFound:
            abort(404, "Genre not found")
