from pydantic import BaseModel, Field, field_validator, ConfigDict

from app.core.enums import StatusInfo
from app.core.exceptions import BusinessException


class LoginRequest(BaseModel):
    """
    登录请求模型
    """
    model_config = ConfigDict(extra="forbid") # 禁止额外字段
    
    username: str  = Field(..., description="用户名")
    password: str  = Field(..., description="密码")

    @field_validator("username", "password")
    @classmethod
    def validate_username_password(cls, v):
        # if not v:
        #     raise BusinessException(StatusInfo.LOGIN_EMPTY_CREDENTIALS)
        v = v.strip()
        if not v:
            # 用户名或密码不能为空
            raise BusinessException(StatusInfo.LOGIN_EMPTY_CREDENTIALS)

        if len(v) < 5 or len(v) > 12:
            # 用户名或密码长度必须在5-12之间
            raise BusinessException(StatusInfo.LOGIN_INVALID_LENGTH)
        return v
