from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

"""Создание Flask объекта, аргумент - этот файл"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.bd'  # Выбор БД в данном случае - sqlite и название
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)        # добавление запускаемого файла (этого) в бд

"""Создание БД"""


class Artikle(db.Model):   # Создание колонок в бд + параметры
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Artikle %r>" % self.id

"""
Для создания файла БД (site.bd) в интерактивном режиме:
python
from app import db
db.create_all()
"""

"""Главная страница"""


@app.route('/')             # отслеживание главное страницы
@app.route('/home')             # страница home обрабатыватся также как и главная
def index():
    return render_template("index.html")  # функция выводит html шаблон


"""Все посты из БД"""


@app.route('/posts')
def post():
    articles = Artikle.query.order_by(Artikle.date.desc()).all()  # вывод отсортирован по последней дате
    return render_template('post.html', articles=articles)  # функция выводит html шаблон


"""Страница конкретно выбраднного поста"""


@app.route('/posts/<int:id>')  # адрес страницы зависит от id поста
def post_detail(id):  # функция принимаети аргумент - id поста
    article = Artikle.query.get(id)  # переменная получает строку по id поста со всеми колонками
    return render_template('post_detail.html', article=article)  # функция выводит html шаблон,
    # с атрибутом(заданная переменная)


"""Удаление поста"""


@app.route('/posts/<int:id>/delete')
def post_delete(id):  # функция принимаети аргумент - id поста
    article = Artikle.query.get_or_404(id)  # переменная получает строку по id поста со всеми колонками
    # (для удаления)

    try:  # в случае отсутствия ошибок
        db.session.delete(article)  # удаление строки из БД
        db.session.commit()  # сохранение результатов
        return redirect('/posts')  # переход на страницу /posts
    except:  # при ошибке
        return "При удалении статьи произошла ошибка"


"""Создание поста"""


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Artikle(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template('create-article.html')  # функция выводит html шаблон


"""Изменение поста"""


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Artikle.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']



        try:

            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"

    else:

        return render_template('post_update.html',  article=article)  # функция выводит html шаблон



"""
В параметрах функции user указываем что брать из адресной строки, этаже информациия отображается на странице.
"""

if __name__ == '__main__':  # если программа запускается через этот файл, т-е. app = Flask(этот файл)
    app.run(debug=False)               # запуск Flask(вывод ошибок на сайт)

