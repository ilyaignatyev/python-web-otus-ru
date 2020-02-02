"""
Тэг
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base
from .post_tag import post_tag


class Tag(Base):
    """
    Тэг
    """
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    posts = relationship('Post', secondary=post_tag, back_populates='tags')

    def __repr__(self):
        return f'<#{self.id} {self.name}>'
