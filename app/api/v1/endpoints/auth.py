from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.schemas.request.auth import LoginRequest, RegisterRequest
from app.schemas.response.base import success
from app.services.auth import AuthService
from loguru import logger

router = APIRouter()


@router.post("/register")
async def register(request: RegisterRequest, db_session: AsyncSession = Depends(get_db)):
    """
    注册接口
    :param request: 注册请求模型
    :param db_session: 数据库会话
    :return:
    """
    logger.info(f"[注册接口] username={request.username}")
    auth_service = AuthService(db_session)
    await auth_service.register(request)
    return success()


@router.post("/login")
async def login(request: LoginRequest, db_session: AsyncSession = Depends(get_db)):
    """
    登录接口
    :param request: 登录请求模型
    :param db_session: 数据库会话
    :return:
    """
    logger.info(f"[登录接口] username={request.username}")
    auth_service = AuthService(db_session)
    data = await auth_service.login(request)
    return success(data)
