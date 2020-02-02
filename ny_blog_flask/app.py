"""
Основное приложение + роутинги главной страницы и страницы "Об авторе"
"""

from flask import Flask, request, render_template

from posts_views import posts_app
from fake_posts import test_posts

app = Flask(__name__)
app.register_blueprint(posts_app, url_prefix='/posts')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', posts=test_posts[:20])


@app.route('/about/', methods=['GET'], endpoint='about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
