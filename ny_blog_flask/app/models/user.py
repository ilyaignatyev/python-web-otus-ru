"""
Пользователь
"""

from sqlalchemy import Column, Integer, String, Binary
from sqlalchemy.orm import relationship

from app import db

from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    Пользователь
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(Binary, nullable=False)
    password_salt = Column(Binary, nullable=False)

    posts = relationship('Post', back_populates='user')

    def __repr__(self):
        return f'<#{self.id} {self.name}>'
