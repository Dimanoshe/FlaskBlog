from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

"""Создание Flask объекта, аргумент - этот файл."""
app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.bd'  # Выбор БД в данном случае - sqlite и название
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'sweater/static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)        # добавление запускаемого файла (этого) в бд
manager = LoginManager(app)


from Flask_project.sweater import models, routes