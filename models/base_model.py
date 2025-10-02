#!/usr/bin/python3
"""Define the shared behaviour for all models."""
import uuid
from datetime import datetime
from os import getenv

try:
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, String, DateTime
except ImportError:  # SQLAlchemy might not be installed for file storage tests
    declarative_base = None
    Column = String = DateTime = None


USE_DB_STORAGE = getenv('HBNB_TYPE_STORAGE') == 'db'


if USE_DB_STORAGE and declarative_base is not None:
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""

    TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

    def __init__(self, *args, **kwargs):
        """Instantiate a new model or rehydrate from stored data."""
        if kwargs:
            payload = dict(kwargs)
            payload.pop('__class__', None)

            missing = {'id', 'created_at', 'updated_at'} - payload.keys()
            if missing:
                raise KeyError(next(iter(missing)))

            created = payload['created_at']
            updated = payload['updated_at']
            if isinstance(created, str):
                payload['created_at'] = datetime.strptime(
                    created, self.TIME_FORMAT)
            if isinstance(updated, str):
                payload['updated_at'] = datetime.strptime(
                    updated, self.TIME_FORMAT)

            for key, value in payload.items():
                setattr(self, key, value)
        else:
            from models import storage

            self.id = str(uuid.uuid4())
            now = datetime.utcnow()
            self.created_at = now
            self.updated_at = now
            storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    if USE_DB_STORAGE and Column is not None:
        # SQLAlchemy-mapped columns (as mixin attributes)
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def delete(self):
        from models import storage
        storage.delete(self)
