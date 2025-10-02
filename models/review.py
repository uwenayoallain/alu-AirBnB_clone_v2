#!/usr/bin/python3
"""Review model definition."""
from os import getenv

from models.base_model import BaseModel, Base


USE_DB_STORAGE = getenv('HBNB_TYPE_STORAGE') == 'db'

if USE_DB_STORAGE:
    from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Store review details."""

    __tablename__ = 'reviews'

    if USE_DB_STORAGE:
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        text = ""
        place_id = ""
        user_id = ""
