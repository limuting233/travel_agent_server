import asyncio
import uuid
from datetime import date

import httpx
from langchain_core.messages import SystemMessage

from app.agents.context import TravelAgentContext

from app.core.config import settings
from app.schemas.request.travel import PlanTravelRequest
from loguru import logger
import time

from app.schemas.response.stream import StreamResponse, StartEvent, LoadingEvent, MessageEvent, DoneEvent


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

        thread_id = f"thread_{str(uuid.uuid4()).replace('-', '')}"
        logger.info(f"本次旅游规划thread_id: {thread_id}")
        yield StreamResponse(
            event="start",
            data=StartEvent(thread_id=thread_id, start_at=int(time.time())),
        )
        yield StreamResponse(
            event="loading",
            data=LoadingEvent(loading_at=int(time.time())),
        )
        from app.agents.graph import travel_agent
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
            # print(f"chunk: {chunk}")
            # chunk 格式: {"node_name": {state_update}}
            for node_name, state_update in chunk.items():
                # 打印节点名称和状态更新
                logger.info(f"当前node: {node_name}, 更新的state: {state_update}")
                if node_name == "manager_agent_node":
                    next_phase = state_update["next_phase"]  # 下一个阶段
                    if next_phase == "finish":
                        # 规划完成
                        logger.info("本轮规划完成")

                        # 获取规划结果
                        final_output = state_update["messages"][-1].content
                        logger.info(f"规划结果: {final_output}")
                        # 分批返回规划结果
                        for c in final_output:
                            yield StreamResponse(
                                event="message",
                                data=MessageEvent(
                                    content=c
                                ),
                            )

                            await asyncio.sleep(0.05)  # 等待0.05s

                        yield StreamResponse(
                            event="done",
                            data=DoneEvent(
                                # usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                                thread_id=thread_id,
                                end_at=int(time.time()),
                            ),
                        )

                        # todo 规划完成后需要加本次规划结果存放进数据库
