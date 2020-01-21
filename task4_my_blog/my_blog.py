"""
Блог.
Выбрать все посты конкретного пользователя с 2-мя любыми тегами.
"""

from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, String, Text, Boolean, text
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

post_tag = Table('post_tag', Base.metadata,
                 Column('post_id', Integer, ForeignKey('post.id'), primary_key=True),
                 Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))


class User(Base):
    """
    Пользователь
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=False)

    posts = relationship('Post', back_populates='user')


class Tag(Base):
    """
    Тэг
    """
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    posts = relationship('Post', secondary=post_tag, back_populates='tags')


class Post(Base):
    """
    Пост
    """
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(200), nullable=False)
    text = Column(Text, nullable=False)
    published = Column(Boolean, nullable=False, default=False)

    user = relationship('User', back_populates='posts')
    tags = relationship('Tag', secondary=post_tag, back_populates='posts')

    def __repr__(self):
        return f'<#{self.id} {self.title}>'


def create_tables():
    """
    Создает таблицы
    """
    Base.metadata.create_all(engine)


def create_data():
    """
    Заполняет таблицы тестовыми данными
    """
    user1 = User(name='User1', fullname='User1 Full', email='user1@gmail.com')
    user2 = User(name='User2', fullname='User2 Full', email='user2@gmail.com')
    user3 = User(name='User3', fullname='User3 Full', email='user3@gmail.com')
    session.add_all([user1, user2, user3])

    tag1 = Tag(name='Tag1')
    tag2 = Tag(name='Tag2')
    tag3 = Tag(name='Tag3')
    session.add_all([tag1, tag2, tag3])

    session.flush()

    post1 = Post(title='Post1 title', text='Post1 text', user_id=user1.id, published=True)
    post2 = Post(title='Post2 title', text='Post2 text', user_id=user2.id)
    post3 = Post(title='Post3 title', text='Post3 text', user_id=user3.id)
    post4 = Post(title='Post4 title', text='Post4 text', user_id=user1.id)

    post1.tags = [tag1, tag2]
    post2.tags = [tag2]
    post3.tags = [tag2, tag3]

    session.add_all([post1, post2, post3, post4])

    session.commit()


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


engine = create_engine('sqlite:///blog.db')

if __name__ == '__main__':
    session = Session(bind=engine)
    create_tables()
    create_data()
    user_name = 'User1 Full'
    print(f'Posts of user "{user_name}" with 2 tags:')
    print('Version 1:')
    print_posts(get_posts_session_execute(user_name, 2))
    print('Version 2:')
    print_posts(get_posts_session_query(user_name, 2))
