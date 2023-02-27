from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    String,
    DateTime,
)

db = declarative_base()


class Users(db):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    nickname = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    messages = relationship('Messages', back_populates='users')


class Messages(db):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    content = Column(Text, nullable=False)
    datetime = Column(DateTime, default=datetime.now)

    users = relationship('Users', back_populates='messages')
