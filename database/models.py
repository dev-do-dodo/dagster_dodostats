from sqlalchemy import (
    Column, Integer, Float, String, Text, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'stats_restaurant'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(100))
    name = Column(String(255))
    latin = Column(String(255))
    city = Column(String(150))
    address = Column(String(255))
    orientation = Column(Text, nullable=True)
    begin_date_work = Column(String(100))
    begin_date = Column(String(100), nullable=True)

    locations = relationship("Location", back_populates='restaurant')
    working_times = relationship("WorkingTime", back_populates='restaurant')
    revenue_current = relationship("RevenueCurrentMonth", back_populates='restaurant')
    operational_statistics = relationship("OperationalStatistics", back_populates='restaurant')


class Location(Base):
    __tablename__ = 'stats_location'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('stats_restaurant.id'))
    latitude = Column(Float)
    longitude = Column(Float)
    uuid = Column(String(100))
    name = Column(String(255))

    restaurant = relationship("Restaurant", back_populates='locations')


class WorkingTime(Base):
    __tablename__ = 'stats_workingtime'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('stats_restaurant.id'))
    day_index = Column(String(60))
    working_time_start = Column(String(60))
    working_time_end = Column(String(60))
    types = Column(String(20))

    restaurant = relationship("Restaurant", back_populates='working_times')


class CountRestaurant(Base):
    __tablename__ = 'stats_countrestaurant'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    count = Column(Integer)

    __table_args__ = (
        UniqueConstraint('year', 'month', name='unique_year_month'),
    )


class CountCity(Base):
    __tablename__ = 'stats_countcity'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class RevenueAllRestaurant(Base):
    __tablename__ = 'stats_revenueallrestaurant'

    id = Column(Integer, primary_key=True)
    current_year_progressive_total = Column(String(100))
    current_month_progressive_total = Column(String(100))
    current_time = Column(DateTime)


class RevenueCurrentMonth(Base):
    __tablename__ = 'stats_revenuecurrentmonth'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('stats_restaurant.id'))
    year = Column(Integer)
    month = Column(Integer)
    revenue = Column(String(100))

    restaurant = relationship("Restaurant", back_populates='revenue_current')

    __table_args__ = (
        UniqueConstraint('year', 'month', 'restaurant_id', name='unique_year_month_restaurant'),
    )


class OperationalStatistics(Base):
    __tablename__ = 'stats_operationalstatistics'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('stats_restaurant.id'))
    date = Column(DateTime, nullable=False)

    today_stationary_revenue = Column(String(100))
    today_stationary_order_count = Column(String(100))
    today_delivery_revenue = Column(String(100))
    today_delivery_order_count = Column(String(100))
    today_revenue = Column(String(100))
    today_order_count = Column(String(100))

    week_before_stationary_revenue = Column(String(100))
    week_before_stationary_order_count = Column(String(100))
    week_before_delivery_revenue = Column(String(100))
    week_before_delivery_order_count = Column(String(100))
    week_before_revenue = Column(String(100))
    week_before_order_count = Column(String(100))

    yesterday_to_this_time_stationary_revenue = Column(String(100))
    yesterday_to_this_time_stationary_order_count = Column(String(100))
    yesterday_to_this_time_delivery_revenue = Column(String(100))
    yesterday_to_this_time_delivery_order_count = Column(String(100))
    yesterday_to_this_time_revenue = Column(String(100))
    yesterday_to_this_time_order_count = Column(String(100))

    week_before_to_this_time_stationary_revenue = Column(String(100))
    week_before_to_this_time_stationary_order_count = Column(String(100))
    week_before_to_this_time_delivery_revenue = Column(String(100))
    week_before_to_this_time_delivery_order_count = Column(String(100))
    week_before_to_this_time_revenue = Column(String(100))
    week_before_to_this_time_order_count = Column(String(100))

    restaurant = relationship("Restaurant", back_populates='operational_statistics')
