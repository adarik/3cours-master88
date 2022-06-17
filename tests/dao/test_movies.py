import pytest

from project.dao.models.movie import Movie
from project.dao.movie import MovieDAO


class TestMovieDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = MovieDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        m = Movie(title="test1",
                  description='test1',
                  trailer='test1',
                  year=2000,
                  rating=3.8,
                  genre_id=5,
                  director_id=4)
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def movie_2(self, db):
        m = Movie(title="test2",
                  description='test2',
                  trailer='test2',
                  year=2010,
                  rating=3.8,
                  genre_id=5,
                  director_id=4)
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie_by_id(self, movie_1):
        assert self.dao.get_one(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self):
        assert self.dao.get_one(1) is None

    def test_get_all_movies(self, movie_1, movie_2):
        assert self.dao.get_all() == [movie_1, movie_2]

    def test_get_by_page(self):
        page = 2
        assert len(self.dao.get_by_page(page)) == 0

    def test_newest_movie_by_page(self, movie_1, movie_2):
        page = 1
        assert self.dao.get_newest_by_page(page) == [movie_2, movie_1]
