"""
Связь поста с тэгом
"""

from sqlalchemy import Table, Column, ForeignKey, Integer

from ..db import Base

post_tag = Table('post_tag', Base.metadata,
                 Column('post_id', Integer, ForeignKey('post.id'), primary_key=True),
                 Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))
