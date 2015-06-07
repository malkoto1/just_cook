__author__ = 'Vojda'

import sqlite3
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

conn = sqlite3.connect('just_cook_db.db')

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250))
    password = Column(String(250))
    # TODO user_type

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))

engine = create_engine('sqlite:///just_cook_db.db')

Base.metadata.create_all(engine)
