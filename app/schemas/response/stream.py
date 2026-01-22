from typing import Literal, Union, Optional

from pydantic import BaseModel, Field


class StartEvent(BaseModel):
    """
    工作流开始事件数据
    """
    thread_id: str = Field(..., description="线程ID")
    start_at: int = Field(..., description="本次对话开始时间,秒时间戳")


class LoadingEvent(BaseModel):
    """
    加载事件数据
    """
    loading_at: int = Field(..., description="本次加载开始时间,秒时间戳")


class MessageEvent(BaseModel):
    """
    消息事件数据
    """
    content: str = Field(..., description="消息内容")


class DoneEvent(BaseModel):
    """
    完成事件数据
    """
    # usage: dict = Field(..., description="使用统计信息")
    thread_id: str = Field(..., description="聊天线程ID")
    end_at: int = Field(..., description="本次对话结束时间,秒时间戳")


class StreamResponse(BaseModel):
    """
    流式响应模型
    """
    event: Literal["start", "loading", "step", "message", "citation", "error", "done"] = Field(description="事件类型")
    data: Union[StartEvent, LoadingEvent, MessageEvent, DoneEvent] = Field(description="事件数据")
