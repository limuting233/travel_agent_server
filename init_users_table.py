import asyncio

from sqlalchemy import text

from app.core.db import async_engine
from app.models.base import Base
from app.models.user import User


async def init_users_table() -> None:
    """
    初始化 users 表，并为旧表补齐缺失字段
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: Base.metadata.create_all(
                sync_conn,
                tables=[User.__table__],
            )
        )
        await conn.execute(
            text(
                """
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS nickname VARCHAR(50) NOT NULL DEFAULT '旅行者'
                """
            )
        )
        await conn.execute(
            text(
                """
                UPDATE users
                SET nickname = '旅行者'
                WHERE nickname IS NULL OR nickname = ''
                """
            )
        )


if __name__ == "__main__":
    asyncio.run(init_users_table())
