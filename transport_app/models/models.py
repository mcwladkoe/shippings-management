# -*- coding: utf-8 -*-

from pyramid.security import Allow, Everyone

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    String,
    Boolean,
    ForeignKey,
    DateTime,
)

from sqlalchemy.orm import relationship, backref, class_mapper

from . import DBSession, Base


class Driver(Base):
    __tablename__ = 'driver'

    uid = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)

    experience = Column(Integer, doc="Стаж", nullable=False)
    
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)

    @property
    def full_name(self):
        return u'{} {} {}'.format(
            self.first_name,
            self.patronymic,
            self.last_name
        )

    @classmethod
    def options(cls, second=False):
        items = DBSession.query(cls).order_by(cls.created)

        result = []
        if second:
            result.append((0, 'Нет'))
        for i in items:
            result.append((i.uid, i.full_name))
        return result


class Route(Base):
    __tablename__ = 'route'

    uid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    distance = Column(Float, nullable=False)
    base_price = Column(Float, nullable=False)

    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    
    @classmethod
    def options(cls):
        items = DBSession.query(cls).order_by(cls.created)
        result = []
        for i in items:
            result.append((i.uid, i.name))
        return result


class Shipping(Base):
    
    __tablename__ = 'shipping'

    uid = Column(Integer, primary_key=True)
    
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    
    award = Column(Float, nullable=True)

    # driver_1_id = Column(Integer, ForeignKey('driver.uid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, index=True)
    # driver_2_id = Column(Integer, ForeignKey('driver.uid', onupdate='CASCADE', ondelete='CASCADE'), nullable=True, index=True)

    # driver_1 = relationship(Driver, backref=backref('tasks', cascade='all, delete-orphan', passive_deletes=True, doc='Documents'), doc='Driver')
    # driver_2 = relationship(Driver, backref=backref('tasks', cascade='all, delete-orphan', passive_deletes=True, doc='Documents'), doc='Driver')
    
    route_id = Column(Integer, ForeignKey('route.uid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, index=True)
    
    route = relationship(Route, backref=backref('shippings', cascade='all, delete-orphan', passive_deletes=True, doc='Shippings'), doc='Route')
    
    price = Column(Float, nullable=True)


class DriverShipping(Base):
    __tablename__ = 'driver_shipping'

    driver_id = Column(Integer, ForeignKey('driver.uid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, index=True, primary_key=True)
    shipping_id = Column(Integer, ForeignKey('shipping.uid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, index=True, primary_key=True)
    
    price = Column(Float, nullable=False)
    
    driver = relationship(Driver, backref=backref('shippings', cascade='all, delete-orphan', passive_deletes=True, doc='Shippings'), doc='Driver')
    shipping = relationship(Shipping, backref=backref('drivers', cascade='all, delete-orphan', passive_deletes=True, doc='Drivers'), doc='Shipping')
