from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


engine = create_engine("", echo=True)
Base = declarative_base()


class User:
    __tablename__ = "Users"

    id_user = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    us_name = Column(String(250), nullable=False)
    us_sname = Column(String(250), nullable=False)
    rec = relationship("Records")


class Record:
    __tablename__ = "Records"

    id_rec = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id_user"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    rec_text = Column(String(500))
    user=relationship("User")


Base.metadata.create_all(engine)
