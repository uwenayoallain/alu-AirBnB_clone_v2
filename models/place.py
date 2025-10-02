#!/usr/bin/python3
"""Place model supporting both storage engines."""
from os import getenv

from models.base_model import BaseModel, Base
from models import storage


USE_DB_STORAGE = getenv('HBNB_TYPE_STORAGE') == 'db'

if USE_DB_STORAGE:
    from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
    from sqlalchemy.orm import relationship

    place_amenity = Table(
        'place_amenity', Base.metadata,
        Column('place_id', String(60), ForeignKey('places.id'),
               primary_key=True, nullable=False),
        Column('amenity_id', String(60), ForeignKey('amenities.id'),
               primary_key=True, nullable=False)
    )
else:
    place_amenity = None


class Place(BaseModel, Base):
    """Represent a place available for booking."""

    __tablename__ = 'places'

    if USE_DB_STORAGE:
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            'Review', backref='place', cascade='all, delete')
        amenities = relationship(
            'Amenity', secondary=place_amenity, viewonly=False,
            back_populates='place_amenities')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            from models.review import Review
            return [obj for obj in storage.all(Review).values()
                    if obj.place_id == self.id]

        @property
        def amenities(self):
            from models.amenity import Amenity
            return [obj for obj in storage.all(Amenity).values()
                    if obj.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            from models.amenity import Amenity
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
