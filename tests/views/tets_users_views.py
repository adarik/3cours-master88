import pytest

from project.dao.models.user import User


class TestUsersView:
    url = "/users/"

    @pytest.fixture
    def user(self, db):
        g = User(email="neonyan15@gmail.com",
                 name="Slava",
                 password='Deagleneo123',
                 surname="Leontev",
                 favorite_genre="Horror",)
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_users(self, client, user):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json == [
            {"id": user.id,
             "email": user.email,
             "name": user.name,
             "surname": user.surname,
             "favorite_genre": user.favorite_genre,
             },
        ]


class TestUserView:
    url = "/users/{user_id}"

    @pytest.fixture
    def user(self, db):
        g = User(email="neonyan15@gmail.com",
                 password='Deagleneo123',
                 name="Slava",
                 surname="Leontev",
                 favorite_genre="Horror",
                 )
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_user(self, client, user):
        response = client.get(self.url.format(email=user.email))
        assert response.status_code == 200
        assert response.json == {"id": user.id,
                                 "email": user.email,
                                 "name": user.name,
                                 "surname": user.surname,
                                 "favorite_genre": user.favorite_genre,
                                 }

    def test_genre_not_found(self, client):
        response = client.get(self.url.format(user_id=1))
        assert response.status_code == 404
