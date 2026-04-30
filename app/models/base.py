from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    数据库模型基类，所有数据库模型都应继承自该类
    """
