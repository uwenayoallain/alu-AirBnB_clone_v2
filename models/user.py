#!/usr/bin/python3
"""Define the User model for both storage engines."""
from os import getenv

from models.base_model import BaseModel, Base


USE_DB_STORAGE = getenv('HBNB_TYPE_STORAGE') == 'db'

if USE_DB_STORAGE:
    from sqlalchemy import Column, String
    from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Represent a user instance."""

    __tablename__ = 'users'

    if USE_DB_STORAGE:
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship('Place', backref='user', cascade='all, delete')
        reviews = relationship('Review', backref='user', cascade='all, delete')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
