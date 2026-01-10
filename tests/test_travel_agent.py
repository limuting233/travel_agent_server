import asyncio

from langchain_core.messages import SystemMessage

from app.agents.context import TravelAgentContext
from app.agents.graph import build_travel_agent
from app.agents.mcp import create_xhc_mcp_session, create_amap_mcp_session
import time


async def main():
    async with create_xhc_mcp_session():
        async with create_amap_mcp_session():
            await build_travel_agent()

            from app.agents.graph import travel_agent

            # resp = await travel_agent.ainvoke(
            #     {
            #         "messages": [SystemMessage(content="开始规划")],
            #         "is_just_start": True,
            #         "is_need_correct": False,
            #         "need_correct_content": None,
            #     },
            #     config={"configurable": {"thread_id": "thread_1"}},
            #     context=TravelAgentContext(location="上海市", days=3, preferences=["经典必玩", "小众探索"],
            #                                start_date="2026-01-10", end_date="2026-01-12")
            # )
            # print(resp["messages"][-1].content)

            # 使用 updates 模式监听节点更新，只在最终质检通过后流式输出
            async for chunk in travel_agent.astream(
                    input={
                        "messages": [SystemMessage(content="开始规划")],
                        "is_just_start": True,
                        "is_need_correct": False,
                        "need_correct_content": None,
                    },
                    config={"configurable": {"thread_id": "thread_1"}},
                    context=TravelAgentContext(location="上海市", days=3, preferences=["经典必玩", "小众探索"],
                                               start_date="2026-01-10", end_date="2026-01-12"),
                    stream_mode="updates"  # updates 模式：监听节点状态更新
            ):
                # print(f"chunk: {chunk}")
                # chunk 格式: {"node_name": {state_update}}
                for node_name, state_update in chunk.items():
                    if node_name == "manager_agent_node":
                        # 检查是否是最终质检通过
                        next_phase = state_update.get("next_phase")
                        if next_phase == "finish":
                            # 获取manager agent的最后一条消息
                            messages = state_update.get("messages", [])
                            if messages:
                                final_output = messages[-1].content
                                print("\n" + "=" * 50)
                                print("✅ 质检通过！以下是您的行程规划：")
                                print("=" * 50 + "\n")
                                # 打字机效果：逐字符输出
                                for char in final_output:
                                    print(char, end="", flush=True)
                                    time.sleep(0.01)  # 控制打字速度
                                print("\n")


if __name__ == "__main__":
    asyncio.run(main())
