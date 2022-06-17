from project.dao.models.base import BaseMixin
from project.setup_db import db


class UserMovie(BaseMixin, db.Model):
    __tablename__ = 'users_movies'

    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    movie_id = db.Column(db.String, db.ForeignKey("movies.id"))
    user = db.relationship("User")
    movie = db.relationship("Movie")
