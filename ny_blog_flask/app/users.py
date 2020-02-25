"""
Функции для работы с пользователями
"""

from hashlib import sha512
from os import urandom

from config import PASSWORD_SALT_LENGTH, POSTS_PER_PAGE
from app import db, login_manager
from app.models import User


def find_user(user_id: int):
    """
    Возвращает пользователя
    :param user_id: идентификатор пользователя
    :return: Пользователь
    """
    return db.session.query(User).filter_by(id=user_id).first()


def get_users(page: int = 1):
    """
    Список пользователей
    :param page: Страница навигации
    :return: Пользователи
    """
    return db.session.query(User).paginate(page, POSTS_PER_PAGE, False)


def authenticate_user(email: str, password: str) -> User or None:
    """
    Аутентификация
    :param email: Email
    :param password: Пароль
    :return: Пользователь, если найден
    """
    if not email or not password:
        return None

    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        return None

    if hash_password(password, user.password_salt) == user.password_hash:
        return user

    return None


def get_password_salt() -> bytes:
    """
    Возвращает случайную последовательность байт для хеширования пароля
    """
    return urandom(PASSWORD_SALT_LENGTH)


def hash_password(password: str, password_salt: bytes) -> str or None:
    """
    Хеширует пароль
    :param password: Пароль
    :param password_salt: "Соль"
    :return: Хеш
    """
    if not password or not password_salt:
        return None

    return sha512(password_salt + password.encode()).digest()


def register_user(name: str, email: str, password: str) -> str or None:
    """
    Регистрация пользователя
    :param name: Имя
    :param email: Email
    :param password: Пароль
    :return: Ошибка регистрации
    """
    if not name or not email or not password:
        return 'Введенные данные некорректны'

    if db.session.query(User).filter_by(email=email).first():
        return 'Пользователь уже существует'

    password_salt = get_password_salt()
    user = User(
        name=name,
        email=email,
        password_salt=password_salt,
        password_hash=hash_password(password, password_salt)
    )
    db.session.add(user)
    db.session.commit()
    return None


@login_manager.user_loader
def load_user(user_id: int) -> User:
    """
    Возвращает пользователя для авторизации
    :param user_id: Идентификатор пользователя
    :return: Пользователь
    """
    return find_user(user_id)
