import pytest

from project.dao.models.user import User
from project.dao.user import UserDAO


class TestUserDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = UserDAO(db.session)

    @pytest.fixture
    def user_1(self, db):
        u = User(email="test1",
                 password='test1',
                 name='test1',
                 surname='test1',
                 favorite_genre='test1',)
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture
    def user_2(self, db):
        u = User(email="test2",
                 password='test2',
                 name='test2',
                 surname='test2',
                 favorite_genre='test2',)
        db.session.add(u)
        db.session.commit()
        return u

    def test_get_user_by_id(self, user_1):
        assert self.dao.get_one(user_1.id) == user_1

    def test_get_user_by_id_not_found(self):
        assert self.dao.get_one(1) is None

    def test_get_all_users(self, user_1, user_2):
        assert self.dao.get_all() == [user_1, user_2]

    def test_get_by_email(self, user_2):
        email = "test2"
        assert self.dao.get_by_email(email) == user_2

    def test_user_create(self):  # TODO Сделать создание пользователя, потом вызвать гет ал, и посчитать длину списка == 3
        pass

    def test_user_delete(self, user_1):
        self.dao.delete(user_1)
        assert self.dao.get_one(1) is None

    def test_user_update(self, user_1):
        user_1.email = 'updated'
        self.dao.update(user_1)
        assert self.dao.get_one(1) == user_1
