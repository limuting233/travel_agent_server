from typing import Literal, Union, Optional

from pydantic import BaseModel, Field


class StartEvent(BaseModel):
    """
    工作流开始事件数据
    """
    session_id: str = Field(..., description="聊天会话ID")
    start_at: int = Field(..., description="本次对话开始时间,毫秒时间戳")


class StepEvent(BaseModel):
    """
    工作流步骤事件数据
    """
    step: str = Field(..., description="当前的步骤")
    status: str = Field(..., description="当前步骤的状态")
    description: str = Field(..., description="当前步骤的描述")


class MessageEvent(BaseModel):
    """
    消息事件数据
    """
    content: str = Field(..., description="消息内容")


class CitationEvent(BaseModel):
    """
    引用事件数据
    """
    source: str = Field(..., description="引用来源")
    page: Optional[int] = Field(default=None, description="引用来源的页码")
    content: str = Field(..., description="具体引用内容")


class ErrorEvent(BaseModel):
    """
    错误事件数据
    """
    code: int = Field(..., description="错误码")
    error_message: str = Field(..., description="错误信息")


class DoneEvent(BaseModel):
    """
    完成事件数据
    """
    usage: dict = Field(..., description="使用统计信息")
    session_id: str = Field(..., description="聊天会话ID")
    end_at: int = Field(..., description="本次对话结束时间,毫秒时间戳")

class LoadingEvent(BaseModel):
    """
    加载事件数据
    """
    loading_at: int = Field(..., description="本次加载开始时间,毫秒时间戳")


class StreamResponse(BaseModel):
    """
    流式响应模型
    """
    event: Literal["start", "loading", "step", "message", "citation", "error", "done"] = Field(...,
                                                                                    description="事件类型")
    data: Union[StartEvent, LoadingEvent, StepEvent, MessageEvent, CitationEvent, ErrorEvent, DoneEvent] = Field(...,
                                                                                                   description="事件数据")
