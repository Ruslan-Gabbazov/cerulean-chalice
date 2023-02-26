from dataclasses import dataclass


@dataclass
class User:
    user_id: int  # from db ?
    nickname: str
    password: str


@dataclass
class Event:
    kind: str
    payload: dict


@dataclass
class Message:
    message_id: int  # from db ?
    user_id: int
    content: str
    datetime: str
