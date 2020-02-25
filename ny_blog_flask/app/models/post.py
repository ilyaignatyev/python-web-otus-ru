"""
Пост
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship

from app import db
from .post_tag import post_tag


class Post(db.Model):
    """
    Пост
    """
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(200), nullable=False)
    text = Column(Text, nullable=False)
    published_date_time = Column(DateTime)
    published = Column(Boolean, default=False)
    image_uuid = Column(String(36))
    image_name = Column(String(100))

    user = relationship('User', back_populates='posts')
    tags = relationship('Tag', secondary=post_tag, back_populates='posts')

    @property
    def short_text(self) -> str:
        """
        Возвращает бриф поста
        :return: Бриф
        """
        return self.text if len(self.text) < 300 else f'{self.text[:300]}...'

    @property
    def splited_text(self) -> list:
        """
        Разбивает пост на абзацы
        :return: Список абзацев
        """
        return self.text.split('\n\r')

    def __repr__(self):
        return f'<#{self.id} {self.title}>'
