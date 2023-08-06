from db.common import Base
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, Text)
from sqlalchemy_serializer import SerializerMixin


class Place(Base, SerializerMixin):
    """ Represents a WOEID place from yahoo api
  'country': 'Japan',
  'countryCode': 'JP',
  'name': 'Okayama',
  'parentid': 23424856,
  'placeType': {'code': 7, 'name': 'Town'},
  'url': 'http://where.yahooapis.com/v1/place/90036018',
  'woeid': 90036018}
    """
    __tablename__ = 'regions_place'

    id = Column(Integer, primary_key=True)
    woeid = Column(Integer, unique=True, nullable=False, index=True)
    parent_id = Column(Integer, nullable=True)
    name = Column(String(length=90), nullable=False)
    country = Column(String(length=90), index=True)
    country_code = Column(String(length=4))
    type_code = Column(Integer)
    type_name = Column(String(), index=True)
