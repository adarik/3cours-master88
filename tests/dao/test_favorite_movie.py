import pytest

from project.dao.favorite_movie import FavoriteMovieDAO
from project.dao.models.user_movie import UserMovie


class TestMovieDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = FavoriteMovieDAO(db.session)

    @pytest.fixture
    def user_movie_1(self, db):
        um = UserMovie(user_id=1,
                       movie_id=4)
        db.session.add(um)
        db.session.commit()
        return um

    @pytest.fixture
    def user_movie_2(self, db):
        um = UserMovie(user_id=5,
                       movie_id=8)
        db.session.add(um)
        db.session.commit()
        return um

    def test_get_one(self, user_movie_1):
        assert self.dao.get_one(user_movie_1.id) == user_movie_1

    def test_get_movie_by_id_not_found(self):
        assert self.dao.get_one(1) is None

    def test_create(self, user_movie_2):
        self.dao.create(int(user_movie_2.movie_id), int(user_movie_2.user_id))
        assert self.dao.get_one(2) is not None

    def test_delete(self, user_movie_1):
        self.dao.delete(user_movie_1)
        assert self.dao.get_one(1) is None
