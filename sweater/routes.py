import glob
import os

from flask import render_template, request, redirect, flash, url_for, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from Flask_project.sweater import db, app, ALLOWED_EXTENSIONS
from Flask_project.sweater.models import Artikle, User, Comment



@app.route('/')             # отслеживание главное страницы
@app.route('/None')             # страница home обрабатыватся также как и главная
def index():
    """Главная страница"""
    user_load = current_user
    users = User.query.all()
    return render_template("index.html", users=users, user_load=user_load)  # функция выводит html шаблон


@app.route('/posts')
def post():
    """Все посты из БД"""
    articles = Artikle.query.order_by(Artikle.date.desc()).all()  # вывод отсортирован по последней дате
    return render_template('post.html', articles=articles)  # функция выводит html шаблон


@app.route('/posts/<int:id>')  # адрес страницы зависит от id поста
def post_detail(id):  # функция принимаети аргумент - id поста
    """Страница конкретно выбраднного поста"""
    article = Artikle.query.get(id)
    comment = Comment.query.order_by(Comment.date.desc()).all()# переменная получает строку по id поста со всеми колонками

    return render_template('post_detail.html', article=article, comment=comment)  # функция выводит html шаблон,
    # с атрибутом(заданная переменная)


@app.route('/posts/<int:id>/delete', methods=['GET'])
@login_required
def post_delete(id):
    """Удаление поста"""
    article = Artikle.query.get(id)
    user_load = current_user.login
    if user_load == article.author:

        article = Artikle.query.get_or_404(id)  # переменная получает строку по id поста со всеми колонками
        # (для удаления)
        try:  # в случае отсутствия ошибок
            db.session.delete(article)  # удаление строки из БД
            db.session.commit()  # сохранение результатов
            return redirect('/posts')  # переход на страницу /posts
        except:  # при ошибке
            return "При удалении статьи произошла ошибка"
    else:
        return "Вы не являетесь автором, пост не может быть удален."


@app.route('/create-article', methods=['POST', 'GET'])
@login_required
def create_article():
    """Создание поста"""
    author = current_user.login
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Artikle(title=title, intro=intro, text=text, author=author)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create-article.html')  # функция выводит html шаблон

@app.route('/posts/<int:id>/create-comment', methods=['POST', 'GET'])
@login_required
def create_comment(id):
    """Создание коментария"""

    if request.method == 'POST':
        text = request.form['text']
        author = current_user.login
        art_id = id
        comment = Comment(text=text, author=author, art_id=art_id)
        #try:
        db.session.add(comment)
        db.session.commit()
        return redirect('/posts')
        #except:
            #return "При добавлении коментария произошла ошибка"
    else:
        return render_template('create-comment.html', id=id)  # функция выводит html шаблон







@app.route('/create-article/uploads', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #os.chdir('C:\\Users\\Дмитрий\\PycharmProjects\\Flask_pro\\Flask_project\\sweater\\static\\images')
    #image = [i for i in os.listdir() if i.endswith('.jpg')][0]

    return render_template('uploads.html')








@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
@login_required
def post_update(id):
    """Изменение поста"""
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


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page)
        else:
            flash('Error (login or password is not correct).')

    else:
        flash('Error (login or password).')
    return render_template('login.html')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста, заполните все поля.')
        elif password != password2:
            flash('пароли не совпадают')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response


def allowed_file(filename):
    print(filename)
    return '.' in filename and \
           filename.rsplit('.')[1] in ALLOWED_EXTENSIONS




