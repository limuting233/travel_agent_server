import uuid
from datetime import date

import httpx
from langchain_core.messages import SystemMessage

from app.agents.context import TravelAgentContext
from app.agents.graph import travel_agent
from app.core.config import settings
from app.schemas.request.travel import PlanTravelRequest
from loguru import logger


class TravelService:
    """
    旅行service,实现旅行相关功能
    """

    async def plan_travel(self, request: PlanTravelRequest):
        """
        旅行规划功能实现函数
        :param request: 旅行规划请求模型
        :return:
        """
        location = request.location  # 目的地
        days = request.days  # 计划天数
        start_date = request.start_date if request.start_date else None  # 计划开始日期
        end_date = request.end_date if request.end_date else None  # 计划结束日期
        preferences = request.preferences if request.preferences else None  # 用户偏好

        thread_id = f"thread_{uuid.uuid4()}"

        async for chunk in travel_agent.astream(
                {
                    "messages": [SystemMessage(content="开始规划")],
                    "is_just_start": True,
                    "is_need_correct": False,
                    "need_correct_content": None,

                },
                stream_mode="updates",
                config={"configurable": {"thread_id": thread_id}},
                context=TravelAgentContext(location=location, days=days,
                                           today=date.today().strftime("%Y-%m-%d") if start_date else None,
                                           preferences=preferences.split(",") if preferences else None,
                                           start_date=start_date, end_date=end_date)
        ):
            print(chunk)
