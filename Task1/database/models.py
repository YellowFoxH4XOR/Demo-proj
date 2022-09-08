from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from database.db import Base


class User(Base):
    """User Db model class

    Args:
        Base (_type_)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Tweet(Base):
    """Tweet Db model class

    Args:
        Base (_type_)
    """
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tweet = Column(String(150), index=True)
    likes = Column(JSON, default=[])
    retweet = Column(JSON, default=[])
    owner_id = Column(Integer, ForeignKey("users.id"))
