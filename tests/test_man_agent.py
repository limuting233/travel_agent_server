import asyncio

from app.agents.manager_agent.agent import ManagerAgentBuilder


async def main():
    agent = ManagerAgentBuilder().build()
    resp = await agent.ainvoke(
        input={
            "messages": [{"role": "system",
                          "content": "用户想去北京游玩三天,时间是2026-12-01到2026-12-03，用户喜欢网红景点、美食。请你根据用户的需求，规划一个三天的旅游行程。"}]
        },
    )
    print(resp["structured_response"])


if __name__ == "__main__":
    asyncio.run(main())
