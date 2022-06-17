from unittest.mock import MagicMock

import pytest

from project.dao.director import DirectorDAO
from project.dao.models.director import Director
from project.services.director_service import DirectorService
from project.setup_db import db


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)
    d1 = Director(id=1, name='Боевик')
    d2 = Director(id=2, name='Триллер')
    d3 = Director(id=3, name='Ужастик')

    director_dao.get_one = MagicMock(return_value=d1)
    director_dao.get_all = MagicMock(return_value=[d1, d2, d3])
    director_dao.get_by_page = MagicMock()
    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director['id'] is not None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) == 3

    def test_get_by_page(self):
        directors = self.director_service.get_by_page(2)
        assert len(directors) == 0
