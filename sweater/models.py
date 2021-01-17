from flask_login import UserMixin

from Flask_project.sweater import db, manager
from datetime import datetime


class Artikle(db.Model):
    """
    Создание БД

    Для создания файла БД (site.bd) в интерактивном режиме:
    python
    from Flask_project.sweater.models import db
    db.create_all()
    """
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return "<Artikle %r>" % self.id


class Comment (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    art_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Comment %r>" % self.id


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

