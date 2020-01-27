from sqlalchemy import text, func

from .db import session
from .models import User, Post, post_tag


def print_posts(posts):
    """
    Выводит осты на экран
    :param posts: Посты
    """
    for post in posts:
        print(post)


def get_posts_session_execute(user_name: str, tag_count: int) -> list:
    """
    Возвращает все посты конкретного пользователя с 2-мя любыми тегами, вариант 1
    :param user_name: Полное имя пользователя
    :param tag_count: Количество тегов у поста
    :return: Посты
    """
    return session.execute(text("""
        SELECT
            post.id,
            post.title,
            post.text
        FROM
            post_tag
        JOIN post ON
            post.id = post_tag.post_id
        JOIN user on
            user.id = post.user_id
        WHERE
            user.fullname == :user_name
        GROUP BY
            post.id,
            post.title
        HAVING
            COUNT(post_tag.tag_id) = :tag_count
        """), {'user_name': user_name,
               'tag_count': tag_count}).fetchall()


def get_posts_session_query(user_name: str, tag_count: int) -> list:
    """
    Возвращает все посты конкретного пользователя с 2-мя любыми тегами, вариант 2
    :param user_name: Полное имя пользователя
    :param tag_count: Количество тегов у поста
    :return: Посты
    """
    return session.query(post_tag) \
        .join(Post, Post.id == post_tag.c.post_id) \
        .with_entities(Post.id, Post.title, Post.text) \
        .join(User, User.id == Post.user_id) \
        .filter(User.fullname == user_name) \
        .group_by(Post.id) \
        .group_by(Post.title) \
        .having(func.count(post_tag.c.tag_id) == tag_count)\
        .all()

