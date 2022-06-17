from flask import abort
from flask_restx import Namespace, Resource

from project.exceptions import ItemNotFound
from project.implemented import favorite_movie_service, movie_service
from project.tools.decode_token import get_id_from_token
from project.tools.decorators import auth_required

favorites_ns = Namespace('favorites')


@favorites_ns.doc(securiry='Bearer')
@favorites_ns.route('/movies/')
class FavMovieView(Resource):

    @favorites_ns.response(200, 'OK')
    @favorites_ns.response(404, "User don't stared any movies")
    @auth_required
    def get(self):
        """
        Метод реализует получение избранных фильмов данного пользователя
        """

        user_id = get_id_from_token()

        try:
            return favorite_movie_service.get_movies_for_user(user_id), 200
        except ItemNotFound:
            abort(404, "User don't stared any movies")


@favorites_ns.route('/movies/<int:movie_id>')
class FavoriteMovieView(Resource):
    """
    Class-Based View для добавления или удаления определенного фильма в избранное, авторизованному пользователю.
    """

    @favorites_ns.response(201, "Created")
    @favorites_ns.response(404, "Movie not found")
    @auth_required
    def post(self, movie_id: int):
        """
        Метод реализует добавление фильма в избранное авторизованному пользователю.
        """
        try:
            movie_service.get_one(movie_id)
        except ItemNotFound:
            abort(404, "Movie not found")
        user_id = get_id_from_token()

        favorite_movie_service.create(movie_id=movie_id, user_id=user_id)
        return 'Created', 201

    @favorites_ns.response(204, "Deleted")
    @favorites_ns.response(404, "Movie is not stared")
    @auth_required
    def delete(self, movie_id: int):
        """
        Метод реализует удаление фильма из избранного авторизованного пользователя.
        """
        try:
            favorite_movie_service.is_movie_id_in(movie_id)
        except ItemNotFound:
            abort(404, "Movie is not stared")
        user_id = get_id_from_token()

        data_id = favorite_movie_service.get_id(movie_id=movie_id, user_id=user_id)
        favorite_movie_service.delete(data_id)
        return "Deleted", 204
