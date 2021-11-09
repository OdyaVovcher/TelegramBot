from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

url = "mysql+mysqlconnector://vladimir:123@localhost/telegrambotdb"

engine = create_engine(url, echo=True)
Base = declarative_base()


class Record(Base):
    __tablename__ = "Records"

    id_rec = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id_user"))
    rec_date = Column(DateTime, nullable=False)
    rec_text = Column(Text)
    user = relationship("User")


class User(Base):
    __tablename__ = "Users"

    id_user = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    us_name = Column(String(250), nullable=False)
    us_sname = Column(String(250), nullable=False)
    rec = relationship("Record")

Base.metadata.create_all(engine)
