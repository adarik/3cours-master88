from unittest.mock import MagicMock

import pytest

from project.dao.genre import GenreDAO
from project.dao.models.genre import Genre
from project.services.genres_service import GenreService
from project.setup_db import db


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)
    g1 = Genre(id=1, name='Боевик')
    g2 = Genre(id=2, name='Триллер')
    g3 = Genre(id=3, name='Ужастик')

    genre_dao.get_one = MagicMock(return_value=g1)
    genre_dao.get_all = MagicMock(return_value=[g1, g2, g3])
    genre_dao.get_by_page = MagicMock()
    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre['id'] is not None

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) == 3

    def test_get_by_page(self):
        genres = self.genre_service.get_by_page(2)
        assert len(genres) == 0
