import pytest

from project.dao.director import DirectorDAO
from project.dao.models.director import Director


class TestDirectorDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = DirectorDAO(db.session)

    @pytest.fixture
    def director_1(self, db):
        d = Director(name="Кевин Смит")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def director_2(self, db):
        d = Director(name="Говард Шульц")
        db.session.add(d)
        db.session.commit()
        return d

    def test_get_director_by_id(self, director_1):
        assert self.dao.get_one(director_1.id) == director_1

    def test_get_director_by_id_not_found(self):
        assert self.dao.get_one(1) is None

    def test_get_all_directors(self, director_1, director_2):
        assert self.dao.get_all() == [director_1, director_2]

    def test_get_by_page(self):
        page = 2
        assert len(self.dao.get_by_page(page)) == 0
