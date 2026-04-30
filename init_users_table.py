import asyncio

from app.core.db import async_engine
from app.models.base import Base
from app.models.user import User


async def init_users_table() -> None:
    """
    初始化 users 表
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: Base.metadata.create_all(
                sync_conn,
                tables=[User.__table__],
            )
        )


if __name__ == "__main__":
    asyncio.run(init_users_table())
