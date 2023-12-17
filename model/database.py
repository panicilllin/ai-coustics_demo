import abc
from typing import *
from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import logging
from config import config_db_engine, config_db_connection


logger = logging.getLogger(__name__)

Base = declarative_base()


class DBType(str, Enum):
    sqlite = "sqlite"
    async_sqlite = "async_sqlite"
    postgresql = "postgresql"
    mysql = "mysql"


class DBEngine(metaclass=abc.ABCMeta):
    _db_type = None
    SUBCLASSES = {}

    def __init__(self):
        pass

    def __init_subclass__(cls, **kwargs):
        """
        child hook
        """
        super().__init_subclass__(**kwargs)
        cls.SUBCLASSES[cls._db_type] = cls

    def get_db(self):
        pass


class SQLiteEngine(DBEngine):
    _db_type = DBType('sqlite')

    def __init__(self, database_url: str = None):
        super().__init__()
        logger.info(f"initial sqlite")
        self.inited = True
        database_url = database_url if database_url else config_db_connection.get("database_url", None)
        self.engine = create_engine(database_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        db = None
        try:
            db = self.SessionLocal()
            yield db
        finally:
            db.close()


class AsyncSQLiteEngine(DBEngine):
    """
    # async database engine, not finished yet
    """
    _db_type = DBType('async_sqlite')

    def __init__(self, database_url):
        super().__init__()
        async_engine = create_async_engine(database_url, connect_args={"check_same_thread": False})
        async_session_maker = async_sessionmaker(bind=async_engine, autocommit=False, autoflush=False,
                                                 expire_on_commit=False)

    async def create_db_and_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session


class PostgresEngine(DBEngine):
    pass


class MysqlEngine(DBEngine):
    pass


def get_db_engine() -> DBEngine or None:
    _cls = DBEngine()
    _scls = _cls.SUBCLASSES.get(DBType(config_db_engine))
    instance = _scls(database_url=config_db_connection.get("database_url", None))
    logger.info(f"db_instance={instance}")
    return instance


if __name__ == "__main__":
    pass
