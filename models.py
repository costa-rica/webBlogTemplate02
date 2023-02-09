from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

from config import config
import os
from datetime import datetime

Base = declarative_base()
engine = create_engine(config.SQL_URI, echo = False, connect_args={"check_same_thread": False})
Session = sessionmaker(bind = engine)
sess = Session()


class Blogposts(Base):
    __tablename__ = 'blogposts'
    id = Column(Integer, primary_key = True)
    title = Column(Text)
    word_doc_name = Column(Text)
    images_folder_name = Column(Text)
    date_published = Column(DateTime, nullable=False, default=datetime.now)



if 'blogposts' in inspect(engine).get_table_names():
    print("db already exists")
else:

    Base.metadata.create_all(engine)
    print("NEW db created.")