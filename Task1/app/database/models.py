from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON

from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tweet = Column(String(150), index=True)
    likes = Column(JSON, default=[])
    retweet = Column(JSON, default=[])
    owner_id = Column(Integer, ForeignKey("users.id"))
