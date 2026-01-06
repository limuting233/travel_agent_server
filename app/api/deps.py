from app.core.db import async_session_factory


async def get_db():
    """
    获取异步数据库会话
    :return: 异步数据库会话
    """
    async with async_session_factory() as db_session:
        try:
            yield db_session
            await db_session.commit()
        except Exception:
            await db_session.rollback()
            raise
