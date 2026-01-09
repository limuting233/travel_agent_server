import asyncio

from langchain_core.messages import SystemMessage

from app.agents.context import TravelAgentContext
from app.agents.graph import build_travel_agent
from app.agents.mcp import create_xhc_mcp_session, create_amap_mcp_session


async def main():
    async with create_xhc_mcp_session():
        async with create_amap_mcp_session():
            await build_travel_agent()
            yield

    from app.agents.graph import travel_agent

    resp = await travel_agent.ainvoke(
        {
            "messages": [SystemMessage(content="开始规划")],
            "is_just_start": True,
            "is_need_correct": False,
            "need_correct_content": None,
        },
        config={"configurable": {"thread_id": "thread_1"}},
        context=TravelAgentContext(location="上海市", days=3, preferences=["经典必玩", "小众探索"],
                                   start_date="2026-01-10", end_date="2026-01-12")
    )
    print(resp["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
