"""
Сессия
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import BASE_URI

engine = create_engine(BASE_URI, pool_pre_ping=True)
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine),
)
