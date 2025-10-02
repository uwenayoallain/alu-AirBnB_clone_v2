#!/usr/bin/python3
"""State model definition supporting both storage engines."""
from os import getenv

from models.base_model import BaseModel, Base
from models import storage


USE_DB_STORAGE = getenv('HBNB_TYPE_STORAGE') == 'db'

if USE_DB_STORAGE:
    from sqlalchemy import Column, String
    from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """State class."""

    __tablename__ = 'states'

    if USE_DB_STORAGE:
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        name = ""

        @property
        def cities(self):
            from models.city import City
            return [obj for obj in storage.all(City).values()
                    if obj.state_id == self.id]
