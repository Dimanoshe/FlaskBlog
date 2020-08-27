from flask import Flask, render_template, url_for


app = Flask(__name__)       # сощдание Flask объекта, аргумент - этот файл


@app.route('/')             # отслеживание главное страницы
@app.route('/home')             # страница home обрабатыватся также как и главная
def index():
    return render_template("index.html")  # функция выводит html шаблон


@app.route('/about')             # отслеживание главное страницы
def about():
    return render_template('about.html')  # функция выводит html шаблон


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return 'User page ' + ' Name: ' + name + ' id: ' + str(id)

"""
В параметрах функции user указываем что брать из адресной строки, этаже информациия отображается на странице.
"""

if __name__ == '__main__':  # если программа запускается через этот файл, т-е. app = Flask(этот файл)
    app.run(debug=True)               # запуск Flask(вывод ошибок на сайт)

