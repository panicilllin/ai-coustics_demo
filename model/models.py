from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from model.database import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)


class Audio(Base):
    __tablename__ = "audio_files"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_md5 = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    create_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
