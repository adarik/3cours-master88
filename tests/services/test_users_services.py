from unittest.mock import MagicMock

import pytest

from project.dao.user import UserDAO
from project.dao.models.user import User
from project.services.user_service import UserService
from project.setup_db import db


@pytest.fixture()
def user_dao():
    user_dao = UserDAO(db.session)
    u1 = User(id=1, email='test1', password="test1")
    u2 = User(id=2, email='test2', password="test2")
    u3 = User(id=3, email='test3', password="test3")

    user_dao.get_one = MagicMock(return_value=u1)
    user_dao.get_all = MagicMock(return_value=[u1, u2, u3])
    user_dao.get_by_email = MagicMock(return_value=u1)
    return user_dao


class TestUserService:
    @pytest.fixture(autouse=True)
    def user_service(self, user_dao):
        self.user_service = UserService(dao=user_dao)

    def test_get_one(self):
        user = self.user_service.get_one(1)
        assert user is not None
        assert user.id is not None

    def test_get_all(self):
        users = self.user_service.get_all()
        assert len(users) == 3

    def test_get_by_page(self):
        users = self.user_service.get_by_email("test1")
        assert users == self.user_service.get_one(1)
