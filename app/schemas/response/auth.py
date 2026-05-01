from pydantic import BaseModel, Field


class CurrentUserResponse(BaseModel):
    """
    当前登录用户响应模型
    """

    id: str = Field(description="用户ID")
    username: str = Field(description="用户名")
    nickname: str = Field(description="用户昵称")
