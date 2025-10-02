#!/usr/bin/python3
"""Association model linking places and amenities."""
from os import getenv

from models.base_model import Base


USE_DB_STORAGE = getenv('HBNB_TYPE_STORAGE') == 'db'

if USE_DB_STORAGE:
    class PlaceAmenity(object):
        def __init__(self, *args, **kwargs):
            self.place_id = kwargs.get('place_id')
            self.amenity_id = kwargs.get('amenity_id')

        def __repr__(self):
            return f"<PlaceAmenity place_id={self.place_id} amenity_id={self.amenity_id}>"
else:
    class PlaceAmenity(object):
        def __init__(self, *args, **kwargs):
            self.place_id = kwargs.get('place_id')
            self.amenity_id = kwargs.get('amenity_id')

        def save(self):
            from models import storage
            storage.new(self)
            storage.save()

        def to_dict(self):
            return {
                '__class__': self.__class__.__name__,
                'place_id': self.place_id,
                'amenity_id': self.amenity_id
            }

        def __repr__(self):
            return f"<PlaceAmenity place_id={self.place_id} amenity_id={self.amenity_id}>"
