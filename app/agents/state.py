import operator
from typing import TypedDict, List, Annotated

from langchain.messages import AnyMessage


class TravelAgentState(TypedDict):
    """
    旅行智能体自定义状态
    """
    user_id: str  # 用户ID
    messages: Annotated[List[AnyMessage], operator.add]  # 消息列表
