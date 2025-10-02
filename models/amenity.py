#!/usr/bin/python3
"""Amenity model definition."""
from os import getenv

from models.base_model import BaseModel, Base


USE_DB_STORAGE = getenv('HBNB_TYPE_STORAGE') == 'db'

if USE_DB_STORAGE:
    from sqlalchemy import Column, String
    from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Amenity linked to places."""

    __tablename__ = 'amenities'

    if USE_DB_STORAGE:
        name = Column(String(128), nullable=False)
        place_amenities = relationship('Place', secondary='place_amenity',
                                       viewonly=False)
    else:
        name = ""
