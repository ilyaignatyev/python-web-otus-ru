"""
Пост
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from ..db import Base
from .post_tag import post_tag


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
