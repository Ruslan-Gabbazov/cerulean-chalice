from dataclasses import dataclass


@dataclass
class User:
    nickname: str
    password: str
    user_id: int or None = None  # -> autoincrement in db


@dataclass
class Event:
    kind: str
    payload: dict


@dataclass
class Message:
    content: str
    datetime: str
    message_id: int or None = None  # -> autoincrement in db
    user_id: int or None = None
