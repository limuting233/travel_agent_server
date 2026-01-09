from typing import TypedDict, List


class TravelAgentContext(TypedDict):
    """
    旅行智能体上下文
    """
    location: str  # 目的地
    days: int  # 计划天数
    start_date: str | None  # 计划开始日期
    end_date: str | None  # 计划结束日期
    preferences: List[str] | None  # 计划偏好
