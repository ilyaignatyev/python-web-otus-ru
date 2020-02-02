"""
Генератор тестовых постов
"""

import random

from faker import Faker

IMG_SRC = [
    'img/bali1.jpg',
    'img/bali2.jpg',
    'img/bali3.jpg'
]


def get_posts() -> list:
    """
    Возвращает тестовые посты
    :return: Посты
    """
    fake = Faker('ru_RU')
    post_count = 100
    post_ids = list(range(post_count))
    posts = []
    for idx in range(post_count):
        text = ' '.join([fake.text() for idx in range(random.randint(3, 10))])
        post_idx = random.randint(0, len(post_ids) - 1)
        post_id = post_ids[post_idx]
        post_ids.pop(post_idx)
        posts.append({
            'id': post_id,
            'title': fake.sentence(),
            'short_text': text[:200] + '...',
            'text': text,
            'date_time': fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None),
            'img_src': random.choice(IMG_SRC),
            'tags': fake.words()
        })
    return sorted(posts, key=lambda post: post['date_time'], reverse=True)


test_posts = get_posts()
