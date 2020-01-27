#Тестовое приложение "Мой Блог" (sqlite + sqlalchemy)
Инициализация БД, создание тестовых данных, получение постов пользователя с двумя тегами.

## Пример использования
~~~
from my_blog.init_tables import create_tables
from my_blog.init_example_data import create_example_data
from my_blog.utils import print_posts, get_posts_session_execute, get_posts_session_query


if __name__ == '__main__':
    # Инициализация БД
    create_tables()

    # Создание тестовых данных
    create_example_data()

    # Поиск постов определенного пользователя с двумя тегами
    user_name = 'User1 Full'
    print(f'Posts of user "{user_name}" with 2 tags:')
    print('Version 1:')
    print_posts(get_posts_session_execute(user_name, 2))
    print('Version 2:')
    print_posts(get_posts_session_query(user_name, 2))
~~~
