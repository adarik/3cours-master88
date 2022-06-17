from flask import request, abort
from flask_restx import Namespace, Resource

from project.exceptions import ItemNotFound
from project.implemented import director_service

directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    """
    Class-Based View для отображения режиссеров из БД.
    Реализовано:
    - отображение всех режиссеров GET-запросом на /directors.
    - отображение режиссеров постранично;
    (GET-запросом на /directors с использованием квери-параметра page);
    """

    @directors_ns.response(200, "OK")
    def get(self) -> tuple:
        """
        Метод реализует отправку GET-запроса на /directors.
        Или отображение режиссеров постранично;
        (GET-запросом на /directors с использованием квери-параметра page);

        :return: Сериализованные данные в формате JSON и HTTP-код 200.
        """
        page = request.args.get('page')
        if page:
            return director_service.get_by_page(page), 200
        return director_service.get_all(), 200


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    """
    Class-Based View для отображения конкретного режиссера из БД.
    Реализовано:
    - отображение данных о конкретном режиссере GET-запросом на /directors/id;
    """

    @directors_ns.response(200, "OK")
    @directors_ns.response(404, "Director not found")
    def get(self, did):
        """
        Метод реализует отправку GET-запроса на /directors/id.

        :param did: id режиссера, информацию о котором нужно вытащить из БД.
        :return: Сериализованные данные в формате JSON и HTTP-код 200.
        В случае, если id нет в базе данных - exception и HTTP-код 404.
        """
        try:
            return director_service.get_one(did)
        except ItemNotFound:
            abort(404, "Director not found")
