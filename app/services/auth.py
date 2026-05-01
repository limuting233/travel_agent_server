from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import StatusInfo
from app.core.exceptions import BusinessException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.request.auth import LoginRequest, RegisterRequest


class AuthService:
    """
    认证服务
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def register(self, request: RegisterRequest) -> None:
        existing_user = await self._get_user_by_username(request.username)
        if existing_user is not None:
            raise BusinessException(StatusInfo.REGISTER_USERNAME_EXISTS)

        user = User(
            username=request.username,
            password_hash=hash_password(request.password),
        )
        self.db_session.add(user)
        await self.db_session.flush()
        await self.db_session.refresh(user)

    async def login(self, request: LoginRequest) -> dict:
        user = await self._get_user_by_username(request.username)
        if user is None or not verify_password(request.password, user.password_hash):
            raise BusinessException(StatusInfo.LOGIN_INVALID_CREDENTIALS)

        return create_access_token(user.id, user.username)

    async def _get_user_by_username(self, username: str) -> User | None:
        result = await self.db_session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
