"""
Контроллер
"""

from flask import request, render_template, redirect, url_for, send_from_directory
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound, Forbidden

from app import app
from app.constants import API_METHOD_RESULT
from .forms.post import PostForm
from .posts import get_last_posts, get_posts, create_post, find_post, update_post, \
    change_post_published_state, delete_post
from .users import get_users, register_user, authenticate_user, find_user


@app.route('/uploads/<path:filename>', methods=['GET'], endpoint='uploads')
def uploaded_file(filename):
    """
    Возвращает загруженный файл
    :param filename: Имя файла
    """
    return send_from_directory(app.config['UPLOADS_PATH'], filename)


@app.route('/', methods=['GET'], endpoint='index')
@app.route('/<int:page>/', methods=['GET'], endpoint='index')
def index(page: int = 1):
    """
    Главная страница
    :param page: Номер страницы навигации
    """
    posts = get_last_posts(page)
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    return render_template('index.html', posts=posts, prev_url=prev_url, next_url=next_url, current_user=current_user)


@app.route('/about/', methods=['GET'], endpoint='about')
def about():
    """
    Страница "О проекте"
    """
    return render_template('about.html', current_user=current_user)


@app.route('/users/', methods=['GET'], endpoint='users')
@app.route('/users/<int:page>/', methods=['GET'], endpoint='users')
def authors(page: int = 1):
    """
    Страница "Авторы"
    """
    users = get_users(page)
    prev_url = url_for('users', page=users.prev_num) if users.has_prev else None
    next_url = url_for('users', page=users.next_num) if users.has_next else None
    return render_template('users.html', users=get_users(), prev_url=prev_url, next_url=next_url,
                           current_user=current_user)


@app.route('/register/', methods=['GET'], endpoint='register')
def register():
    """
    Страница регистрации пользователя
    """
    return render_template('register.html', current_user=current_user)


@app.route('/register/', methods=['POST'])
def register_post():
    """
    Сохранение нового пользователя
    """
    form = request.form
    error_msg = register_user(form.get('name'), form.get('email'), form.get('password'))
    if error_msg:
        return render_template('register.html', error_msg=error_msg, current_user=current_user)
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET'], endpoint='login')
def login():
    """
    Страница аутентификации
    """
    return render_template('login.html', current_user=current_user)


@app.route('/login/', methods=['POST'])
def login_post():
    """
    Аутентификация пользователя
    """
    form = request.form
    user = authenticate_user(form.get('email'), form.get('password'))
    if user:
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', error_msg='Неверный email или пароль')


@app.route('/logout/', methods=['GET'], endpoint='logout')
@login_required
def logout():
    """
    Завершение сеанса текущего пользователя
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/posts/', methods=['GET'], endpoint='posts')
@app.route('/posts/<int:page>/', methods=['GET'], endpoint='posts')
@app.route('/posts/<int:page>/user/<int:user_id>/', methods=['GET'], endpoint='posts')
@app.route('/posts/user/<int:user_id>/', methods=['GET'], endpoint='posts')
def post_list(user_id: int = None, page: int = 1):
    """
    Страница "Все посты"/"Мои посты"/Посты конкретного пользователя
    :param user_id: Пользователь
    :param page: Номер страницы навигации
    """
    only_published = not current_user.is_authenticated or current_user.id != user_id
    posts = get_posts(user_id=user_id, page=page, only_published=only_published)
    prev_url = url_for('posts', user_id=user_id, page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('posts', user_id=user_id, page=posts.next_num) if posts.has_next else None
    return render_template('posts.html', posts=posts, prev_url=prev_url, next_url=next_url, current_user=current_user)


@app.route('/post/add/', methods=['GET', 'POST'], endpoint='add_post')
@login_required
def add_post():
    """
    Страница "Добавить пост" и добаеление нового поста
    """
    form = PostForm()
    if form.validate_on_submit():
        data = form.data
        post_id = create_post(current_user.id, data.get('title'), data.get('text'), form.image.data, data.get('tags'))
        return redirect(url_for('post', post_id=post_id))
    return render_template('post_edit.html', post=None, form=form, current_user=current_user)


@app.route('/post/edit/<int:post_id>/', methods=['GET', 'POST'], endpoint='edit_post')
@login_required
def edit_post(post_id: int):
    """
    Редактирование поста
    :param post_id: Идентификатор поста
    """
    found_post = find_post(post_id)

    if found_post is None:
        raise NotFound('Пост не найден.')

    if not found_post.published and found_post.user_id != current_user.id:
        raise Forbidden('У вас недостаточно прав для выполнения данного действия.')

    form = PostForm(title=found_post.title,
                    text=found_post.text,
                    tags=', '.join([tag.name for tag in found_post.tags]),
                    image=FileStorage(filename=found_post.image_name, name=found_post.image_name))

    if form.validate_on_submit():
        data = form.data
        post_id = update_post(post_id, data.get('title'), data.get('text'), form.image.data, data.get('tags'))
        return redirect(url_for('post', post_id=post_id))

    return render_template('post_edit.html', post=found_post, form=form, current_user=current_user)


@app.route('/post/<int:post_id>/', methods=['GET'], endpoint='post')
def post(post_id: int):
    """
    Страница поста
    :param post_id: Пост
    """
    found_post = find_post(post_id)

    if found_post is None:
        raise NotFound('Пост не найден.')

    if not found_post.published and found_post.user_id != current_user.id:
        raise Forbidden('У вас недостаточно прав для выполнения данного действия.')

    return render_template('post.html', post=found_post, current_user=current_user,
                           can_edit=current_user.is_authenticated and current_user.id == found_post.user_id)


@app.route('/post/publish/<int:post_id>/', methods=['POST'], endpoint='publish_post')
@login_required
def publish(post_id: int):
    """
    Публикация поста
    :param post_id: Пост
    """
    result = change_post_published_state(post_id, True)

    if result == API_METHOD_RESULT.NOT_FOUND:
        raise NotFound('Пост не найден.')

    if result == API_METHOD_RESULT.NO_RIGHTS:
        raise Forbidden('У вас недостаточно прав для выполнения данного действия.')

    return render_template('post.html', post=result, current_user=current_user, can_edit=True)


@app.route('/post/unpublish/<int:post_id>/', methods=['POST'], endpoint='unpublish_post')
@login_required
def unpublish(post_id: int):
    """
    Снятие поста с публикации
    :param post_id: Пост
    """
    result = change_post_published_state(post_id, False)

    if result == API_METHOD_RESULT.NOT_FOUND:
        raise NotFound('Пост не найден.')

    if result == API_METHOD_RESULT.NO_RIGHTS:
        raise Forbidden('У вас недостаточно прав для выполнения данного действия.')

    return render_template('post.html', post=result, current_user=current_user, can_edit=True)


@app.route('/post/delete/<int:post_id>/', methods=['POST'], endpoint='delete_post')
def delete(post_id: int):
    """
    Удаление поста
    :param post_id: Пост
    """
    result = delete_post(post_id)

    if result == API_METHOD_RESULT.NOT_FOUND:
        raise NotFound('Пост не найден.')

    if result == API_METHOD_RESULT.NO_RIGHTS:
        raise Forbidden('У вас недостаточно прав для выполнения данного действия.')

    return redirect(url_for('index'))
