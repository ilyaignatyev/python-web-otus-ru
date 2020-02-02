"""
Пользователь
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base


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

    def __repr__(self):
        return f'<#{self.id} {self.fullname}>'
