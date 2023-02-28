from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import select

from app.chat.models import User, Message
from app.database.models import db, Users, Messages
from app.store.accessor import BaseAccessor

if TYPE_CHECKING:
    from app.chat.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self.engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[async_sessionmaker] = None

    def setup_db(self, app: 'Application') -> None:
        app.on_startup.append(self._on_connect)
        app.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, app: 'Application') -> None:
        self.config = app.config["postgres"]
        self.engine = create_async_engine(self.config["database_url"], echo=True, future=True)

        self._db = db

    async def _on_disconnect(self, _) -> None:
        if self._db is not None:
            await self.engine.dispose()


class DBAccessor(BaseAccessor):

    async def add_user(self, user: User) -> int:
        async_session = async_sessionmaker(self.database.engine, expire_on_commit=False)

        async with async_session() as session:
            async with session.begin():
                db_user = Users(nickname=user.nickname, password=user.password)
                session.add(db_user)
                session.refresh(db_user)
        self.logger.info(f'Added new user with id {db_user.user_id} to database')
        return db_user.user_id

    async def add_message(self, message: Message) -> int:
        async_session = async_sessionmaker(self.database.engine, expire_on_commit=False)

        async with async_session() as session:
            async with session.begin():
                db_message = Messages(user_id=message.user_id,
                                      content=message.content,
                                      datetime=datetime.fromisoformat(message.datetime))
                session.add(db_message)
                session.refresh(db_message)
        self.logger.info(f'Added new message with id {db_message.user_id} to database')
        return db_message.message_id

    async def check_user_and_get_id(self, user: User) -> (bool, int):
        async_session = async_sessionmaker(self.database.engine, expire_on_commit=False)

        async with async_session() as session:
            query = select(Users).where(Users.nickname == user.nickname)
            result = await session.execute(query)
            db_user = result.scalars().one()

        allowed = False if not db_user else db_user.password == user.password
        self.logger.info(f'Checked user with id {db_user.user_id} in database')
        return allowed, db_user.user_id

    async def get_all_messages(self) -> list[Message]:
        async_session = async_sessionmaker(self.database.engine, expire_on_commit=False)

        async with async_session() as session:
            query = select(Messages).order_by(Messages.datetime)
            result = await session.execute(query)
            db_messages = result.scalars().all()

        all_messages = [Message(message_id=r.message_id,
                                user_id=r.user_id,
                                content=r.content,
                                datetime=str(r.datetime)) for r in db_messages]
        self.logger.info(f'Got all messages from database')
        return all_messages
