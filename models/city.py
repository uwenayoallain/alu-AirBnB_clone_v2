#!/usr/bin/python3
"""City model definition."""
from os import getenv

from models.base_model import BaseModel, Base


USE_DB_STORAGE = getenv('HBNB_TYPE_STORAGE') == 'db'

if USE_DB_STORAGE:
    from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """City instances represent a location."""

    __tablename__ = 'cities'

    if USE_DB_STORAGE:
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    else:
        name = ""
        state_id = ""
