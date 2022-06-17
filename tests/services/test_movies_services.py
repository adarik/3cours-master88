from unittest.mock import MagicMock

import pytest

from project.dao.movie import MovieDAO
from project.dao.models.movie import Movie
from project.services.movie_service import MovieService
from project.setup_db import db


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)
    m1 = Movie(id=1,
               title="test1",
               description='test1',
               trailer='test1',
               year=2011,
               rating=3.8,
               genre_id=5,
               director_id=4)
    m2 = Movie(id=2,
               title="test2",
               description='test2',
               trailer='test2',
               year=2003,
               rating=3.8,
               genre_id=5,
               director_id=4)
    m3 = Movie(id=3,
               title="test3",
               description='test3',
               trailer='test3',
               year=2009,
               rating=3.8,
               genre_id=5,
               director_id=4)

    movie_dao.get_one = MagicMock(return_value=m1)
    movie_dao.get_all = MagicMock(return_value=[m1, m2, m3])
    movie_dao.get_by_page = MagicMock()
    movie_dao.get_newest_by_page = MagicMock()
    movie_dao.get_newest = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie['id'] is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) == 3

    def test_get_by_page(self):
        movies = self.movie_service.get_by_page(2)
        assert len(movies) == 0
    #
    # def test_newest(self):
    #     movies = self.movie_service.get_newest()
    #     assert movies == self.movie_service.get_one(1)
