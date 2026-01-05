from fastapi import APIRouter

from app.schemas.request.auth import LoginRequest
from loguru import logger

router = APIRouter()


@router.post("/login")
async def login(request: LoginRequest):
    """
    登录接口
    :param request: 登录请求模型
    :return:
    """
    logger.info(f"[登录接口] 请求参数: {request}")
