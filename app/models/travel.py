from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.models.base import Base


# class TouristPOI(Base):
#     """
#     旅游兴趣点模型
#     """
#     __tablename__ = "tourist_poi"
#     __table_args__ = {"comment": "旅游兴趣点表"}

#     id: Mapped[str] = mapped_column(String(36), primary_key=True, nullable=False, comment="主键ID")
#     name: Mapped[str] = mapped_column(String(255), nullable=False, comment="兴趣点名称")
#     location: Mapped[str] = mapped_column(String(255), nullable=False, comment="经度纬度,格式:经度,纬度")
#     type: Mapped[str] = mapped_column(String(255), nullable=False, comment="兴趣点类型")

