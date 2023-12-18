import abc
import sqlite3
import traceback
from typing import *
from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from config import config_db_engine, config_db_connection

logger = logging.getLogger(__name__)

Base = declarative_base()


class DBType(str, Enum):
    """
    list the database that we support
    """
    sqlite = "sqlite"
    async_sqlite = "async_sqlite"
    postgresql = "postgresql"
    mysql = "mysql"
    exception = None

    @classmethod
    def _missing_(cls, name):
        return cls.exception


class DBEngine(metaclass=abc.ABCMeta):
    """
    base class of database engine
    """
    _db_type = None
    SUBCLASSES = {}

    def __init__(self, **kwargs):
        self.connect_info = {}
        self.engine = None

    def __init_subclass__(cls, **kwargs):
        """
        child hook
        """
        super().__init_subclass__(**kwargs)
        cls.SUBCLASSES[cls._db_type] = cls

    def get_db(self):
        """
        get database session
        :return:
        """
        pass

    def get_conn(self):
        """
        get database conn, no usage for now
        :return:
        """
        pass

    def test_conn(self) -> bool:
        """
        test databses connection
        :return: is connection success
        """
        pass


class SQLiteEngine(DBEngine):
    _db_type = DBType('sqlite')

    def __init__(self, database_url: str = None):
        super().__init__()
        logger.info(f"initial sqlite")
        self.inited = True
        self.database_url = database_url  # if database_url else config_db_connection.get('database_url', None)
        self.connect_info[database_url] = self.database_url
        logger.info(self.connect_info)
        if not self.database_url:
            raise
        self.engine = create_engine(url=self.database_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        """
        yield a database session
        :return: generator
        """
        db = None
        try:
            db = self.SessionLocal()
            yield db
        finally:
            db.close()

    def get_conn(self):
        """
        get database conn, no usage for now
        :return: a connection
        """
        _conn = sqlite3.connect(self.database_url)
        return _conn

    def test_conn(self) -> bool:
        """
        test databses connection
        :return: is connection success
        """
        try:
            conn = self.get_conn()
            conn.cursor()
            return True
        except Exception as e:
            logger.info(e)
            return False


class AsyncSQLiteEngine(DBEngine):
    """
    # async database engine, not finished yet
    """
    _db_type = DBType('async_sqlite')

    def __init__(self, database_url):
        super().__init__()
        self.async_engine = create_async_engine(database_url, connect_args={"check_same_thread": False})
        self.async_session_maker = async_sessionmaker(bind=self.async_engine, autocommit=False, autoflush=False,
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


def get_db_engine(**kwargs) -> DBEngine:
    """
    get database engine, the engine is defined in config.py
    :param kwargs: might have connection info
    :return: DBEngine object
    """
    try:
        _cls = DBEngine()
        _scls = _cls.SUBCLASSES.get(DBType(config_db_engine))
        # try getting connect url
        database_url = kwargs.get('database_url', None)
        if not database_url:
            database_url = config_db_connection.get("database_url", None)
        if not database_url:
            raise
        # database_url = kwargs.get('database_url', config_db_connection.get("database_url", None))
        instance = _scls(database_url=database_url)
        logger.info(f"db_instance={instance}")
        return instance
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(e)
        raise e


if __name__ == "__main__":
    pass
