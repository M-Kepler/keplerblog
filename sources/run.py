# -*-coding:utf-8-*-

from app import create_app
from app.hook import init_hook

app = create_app()

init_hook(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(host='127.0.0.1', port=5000)
