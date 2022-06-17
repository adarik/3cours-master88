from project.config import DevelopmentConfig, ProductionConfig
from project.dao.models.director import Director
from project.dao.models.genre import Genre
from project.dao.models.movie import Movie
from project.dao.models.user import User
from project.dao.models.user_movie import UserMovie
from project.server import create_app, db

app = create_app(ProductionConfig)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "Movie": Movie,
        "User": User,
        "UserMovie": UserMovie,
    }
