from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime,  Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class PriceData(Base):
    __tablename__ = 'price_data'

    id = Column(Integer, primary_key=True)
    commodity_id = Column(String)
    commodity_name = Column(String)
    json_data = Column(JSON)
    date_created = Column(DateTime, default=datetime.now)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    new_sector_name = Column(String)
    new_sub_sector_name = Column(String)
    new_industry_name = Column(String)
    new_sub_industry_name = Column(String)
    sector_name = Column(String)
    sub_sector_name = Column(String)
    board_recording = Column(Integer)
    head_office = Column(String)
    phone = Column(String)
    representative_name = Column(String)
    website_url = Column(String)
    address = Column(String)
    total_employees = Column(String)
    exchange_administration = Column(String)
    npwp = Column(String)
    npkp = Column(String)
    is_active = Column(Boolean)
    listing_date = Column(String)
    annual_dividend = Column(Float)
    general_information = Column(String)
    fax = Column(String)
    founding_date = Column(String)
    company_email = Column(String)


class Directors(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True)
    fk_profile_id = Column(Integer)
    name = Column(String)
    role = Column(String)
    affiliated = Column(String)
    id_field = Column(String)


class StockHolders(Base):
    __tablename__ = "stock_holders"

    id = Column(Integer, primary_key=True)
    fk_profile_id = Column(Integer)
    name = Column(String)
    holding_type = Column(String)
    amount = Column(Float)
    percentage = Column(Float)
    id_field = Column(Integer)