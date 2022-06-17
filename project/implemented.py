from project.dao.favorite_movie import FavoriteMovieDAO
from project.dao.genre import GenreDAO
from project.dao.director import DirectorDAO
from project.dao.movie import MovieDAO
from project.dao.user import UserDAO
from project.services.auth_service import AuthService
from project.services.director_service import DirectorService
from project.services.favorite_movie_service import FavoriteMovieService
from project.services.genres_service import GenreService
from project.services.movie_service import MovieService
from project.services.user_service import UserService
from project.setup_db import db

favorite_movie_dao = FavoriteMovieDAO(db.session)
movie_dao = MovieDAO(db.session)
director_dao = DirectorDAO(db.session)
genre_dao = GenreDAO(db.session)
user_dao = UserDAO(db.session)

movie_service = MovieService(movie_dao)
director_service = DirectorService(director_dao)
genre_service = GenreService(genre_dao)
user_service = UserService(user_dao)
auth_service = AuthService(user_service)
favorite_movie_service = FavoriteMovieService(favorite_movie_dao)
