import asyncio

from app.agents.manager_agent.agent import ManagerAgentBuilder, ManagerAgentOutput


async def main():
    agent = ManagerAgentBuilder().build()
    resp = await agent.ainvoke(
        input={
            "messages": [{"role": "system",
                          "content": "用户想去北京游玩3天,时间是从2026-02-15到2026-02-17，用户喜欢网红景点、美食。请你根据用户的需求，规划一个3天的旅游行程，当前的日期是2026-02-15"}]
        },
    )
    output = ManagerAgentOutput.parse_response(resp)
    print(output)


if __name__ == "__main__":
    asyncio.run(main())
