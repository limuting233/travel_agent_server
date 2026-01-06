from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    """
    数据库模型基类，所有数据库模型都应继承自该类
    """
    # id: Mapped[str] = mapped_column(String(36), primary_key=True, nullable=False, comment="主键ID")
