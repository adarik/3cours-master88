import pytest

from project.dao.models.movie import Movie


class TestMoviesView:
    url = "/movies/"

    @pytest.fixture
    def movie(self, db):
        m = Movie(title="test1",
                  description='test1',
                  trailer='test1',
                  year=2000,
                  rating='3.8',
                  genre_id='5',
                  director_id='4')
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movies(self, client, movie):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json == [
            {"id": movie.id,
             "title": movie.title,
             "description": movie.description,
             "trailer": movie.trailer,
             "year": movie.year,
             "rating": movie.rating,
             "genre_id": str(movie.genre_id),
             "director_id": str(movie.director_id),
             },
        ]


class TestMovieView:
    url = "/movies/{movie_id}"

    @pytest.fixture
    def movie(self, db):
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

    def test_get_movie(self, client, movie):
        response = client.get(self.url.format(movie_id=movie.id))
        assert response.status_code == 200
        assert response.json == {"id": movie.id,
                                 "title": movie.title,
                                 "description": movie.description,
                                 "trailer": movie.trailer,
                                 "year": movie.year,
                                 "rating": movie.rating,
                                 "genre_id": str(movie.genre_id),
                                 "director_id": str(movie.director_id),
                                 }

    def test_movie_not_found(self, client):
        response = client.get(self.url.format(movie_id=1))
        assert response.status_code == 404
