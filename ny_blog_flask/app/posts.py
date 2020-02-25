"""
Функции для рботы с постами
"""

import datetime
from typing import List

from flask_login import current_user
from sqlalchemy import desc

from app import db
from app.constants import API_METHOD_RESULT
from app.images import save_image, delete_image
from app.models import Post
from app.tags import update_post_tags, get_tag_names_from_str, delete_unused_tags, \
    get_tags_by_names
from config import POSTS_PER_PAGE


def find_post(post_id: int) -> Post:
    """
    Возвращает пост по идентификатору
    :param post_id: Идентификатор поста
    :return: Пост
    """
    return db.session.query(Post).filter_by(id=post_id).first()


def get_last_posts(page: int = 1) -> List[Post]:
    """
    Возвращает список последних постов
    :param page: Номер страницы
    :return: Посты
    """
    return db.session.query(Post) \
        .filter(Post.published.is_(True)) \
        .filter(Post.published_date_time.isnot(None)) \
        .order_by(Post.published_date_time.desc()) \
        .paginate(page, POSTS_PER_PAGE, False)


def get_posts(user_id: int = None, only_published: bool = True, page: int = 1) -> List[Post]:
    """
    Возвращает все посты
    :param page: Номер страницы
    :param user_id: Идентификатор автора
    :param only_published: Только опубликованные
    :return: Посты
    """
    query = db.session.query(Post)

    if user_id is not None:
        query = query.filter(Post.user_id == user_id)

    if only_published:
        query = query.filter(Post.published.is_(True))

    # sqlite не умеет nulls first
    # query = query.order_by(nullsfirst(desc(Post.published_date_time)))

    query = query.order_by(desc(Post.published_date_time.is_(None))) \
        .order_by(desc(Post.published_date_time)) \
        .paginate(page, POSTS_PER_PAGE, False)

    return query


def change_post_published_state(post_id: int, publish: bool) -> Post or int:
    """
    Изменяет состояние опубликованности поста
    :param post_id: Идентификатор поста
    :param publish: Опубликован
    :return: Пост или код ошибки
    """
    post = find_post(post_id)

    if post is None:
        return API_METHOD_RESULT.NOT_FOUND

    if post.user_id != current_user.id:
        return API_METHOD_RESULT.NO_RIGHTS

    # Проставляем дату/время публикации только при первой публикации
    if publish and post.published_date_time is None:
        post.published_date_time = datetime.datetime.now()
    post.published = publish
    db.session.commit()
    return post


def create_post(user_id: int, title: str, text: str, image, tags: str) -> int:
    """
    Создание поста
    :param user_id: Идентификатор пользователя
    :param title: Заголовок
    :param text: Текст
    :param image: Изображение
    :param tags: Тэги
    :return: Идентификатор поста
    """
    image_name, image_uuid = save_image(image)
    tags = get_tags_by_names(get_tag_names_from_str(tags))
    post = Post(user_id=user_id, title=title, text=text, image_name=image_name, image_uuid=image_uuid, tags=tags)
    db.session.add(post)
    db.session.flush()
    post_id = post.id
    db.session.commit()
    return post_id


def update_post(post_id: int, title: str, text: str, image, tags: str):
    """
    Редактирование поста
    :param post_id: Идентификатор поста
    :param title: Заголовок
    :param text: Текст
    :param image: Изображение
    :param tags: Тэги
    :return: Идентификатор поста
    """
    post = find_post(post_id)

    if post is None:
        return API_METHOD_RESULT.NOT_FOUND

    if post.user_id != current_user.id:
        return API_METHOD_RESULT.NO_RIGHTS

    post.title = title
    post.text = text

    update_post_tags(post, get_tag_names_from_str(tags))

    if image.filename:
        delete_image(post.image_uuid)
        post.image_name, post.image_uuid = save_image(image)

    db.session.commit()
    return post_id


def delete_post(post_id: int) -> bool or int:
    """
    Удаление поста
    :param post_id: Идентификатор поста
    :return: Успешно удален или код ошибки
    """
    post = find_post(post_id)

    if post is None:
        return API_METHOD_RESULT.NOT_FOUND

    if post.user_id != current_user.id:
        return API_METHOD_RESULT.NO_RIGHTS

    tags = post.tags
    image_uuid = post.image_uuid
    db.session.delete(post)

    # Удаляем изображение
    delete_image(image_uuid)

    # Удалям тэги, которые не используются в других постах
    delete_unused_tags(tags)

    db.session.commit()
    return True
