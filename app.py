from Flask_project.sweater import app
if __name__ == '__main__':  # если программа запускается через этот файл, т-е. app = Flask(этот файл)
    app.run(debug=True)               # запуск Flask(вывод ошибок на сайт)

