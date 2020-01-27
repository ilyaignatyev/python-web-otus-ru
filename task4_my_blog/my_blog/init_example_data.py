"""
Создание тестовых данных
"""

import random

from .db import session
from .models import User, Tag, Post

USERS = [
    ['User1', 'User1 Full', 'user1@gmail.com'],
    ['User2', 'User2 Full', 'user2@gmail.com'],
    ['User3', 'User3 Full', 'user3@gmail.com'],
]

TAGS = ['Tag1', 'Tag2', 'Tag3']

POSTS = [
    ['Post1 title', 'Post1 text', True],
    ['Post2 title', 'Post2 text', False],
    ['Post3 title', 'Post3 text', False]
]


def create_example_data():
    """
    Заполняет таблицы тестовыми данными
    """
    users = []
    for user in USERS:
        users.append(User(name=user[0], fullname=user[1], email=user[2]))
    session.add_all(users)

    tags = []
    for tag in TAGS:
        tags.append(Tag(name=tag))
    session.add_all(tags)

    session.flush()

    posts = []
    for post in POSTS:
        posts.append(Post(title=post[0], text=post[1], published=post[2], user_id=random.choice(users).id))

    posts[0].tags = [tags[0], tags[1]]
    posts[1].tags = [tags[1]]
    posts[2].tags = [tags[1], tags[2]]

    session.add_all(posts)

    session.commit()
