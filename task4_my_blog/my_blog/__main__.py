"""
Инициализация БД, создание тестовых данных, получение постов пользователя с двумя тегами.
"""

from .init_tables import create_tables
from .init_example_data import create_example_data
from .utils import print_posts, get_posts_session_execute, get_posts_session_query


if __name__ == '__main__':
    create_tables()
    create_example_data()
    user_name = 'User1 Full'
    print(f'Posts of user "{user_name}" with 2 tags:')
    print('Version 1:')
    print_posts(get_posts_session_execute(user_name, 2))
    print('Version 2:')
    print_posts(get_posts_session_query(user_name, 2))
