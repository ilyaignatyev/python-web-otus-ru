"""
Инициализация таблиц
"""

from .db import Base, engine


def create_tables():
    """
    Создает таблицы
    """
    Base.metadata.create_all(engine)
