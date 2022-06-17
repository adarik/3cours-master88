from flask import request, abort
from flask_restx import Namespace, Resource

from project.exceptions import ItemNotFound
from project.implemented import movie_service

movies_ns = Namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):
    """
    Class-Based View для отображения фильмов.
    Реализовано:
    - отображение всех фильмов GET-запросом на /movies;
    - отображение фильмов постранично;
    (GET-запросом на /movies с использованием квери-параметра page);
    - отображение фильмов постранично, отфильтрованных по году выпуска
    (GET-запросом на /movies с использованием квери-параметра page и status);
    """

    @movies_ns.response(200, "OK")
    def get(self) -> tuple:
        """
        Метод реализует отправку GET-запросов на /movies.
        Возможные варианты исполнения:
        - отображение всех фильмов GET-запросом на /movies;
        - отображение фильмов постранично;
        (GET-запросом на /movies с использованием квери-параметра page);
        - отображение фильмов постранично, отфильтрованных по году выпуска
        (GET-запросом на /movies с использованием квери-параметра page и status);

        :return: Сериализованные данные в формате JSON, в зависимости от реализации запроса и HTTP-код 200
        """
        page = request.args.get('page')
        status = request.args.get('status')

        if status == 'new' and page:
            return movie_service.get_newest(page), 200
        elif status == 'new':
            return movie_service.get_newest()
        elif page:
            return movie_service.get_by_page(page), 200
        return movie_service.get_all(), 200


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    """
    Class-Based View для отображения конкретного фильма из БД.
    Реализовано:
    - отображение данных о конкретном фильме GET-запросом на /movies/id;
    """

    @movies_ns.response(200, 'OK')
    @movies_ns.response(404, "Movie not found")
    def get(self, mid: int) -> tuple:
        """
        Метод реализует GET-запрос на /movie/id.

        :param mid: id фильма, информацию о котором нужно вытащить из БД.
        :return: Сериализованные данные в формате JSON и HTTP-код 200.
        В случае, если id нет в базе данных - exctention и HTTP-код 404.
        """
        try:
            return movie_service.get_one(mid)
        except ItemNotFound:
            abort(404, "Movie not found")
