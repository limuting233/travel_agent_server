import asyncio

from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.environment_agent.agent import EnvironmentAgentBuilder
from app.agents.mcp import create_xhc_mcp_session
from app.agents.message import EnvironmentAgentMessage
from app.agents.resource_agent.agent import ResourceAgentBuilder


async def main():
    agent = EnvironmentAgentBuilder().build()
    resp = await agent.ainvoke({
        "messages": [SystemMessage(
            content="请你查询上海从2026-1-10到2026-1-12的天气情况。")]
    })
    # print(resp["messages"][-1].model_dump())
    last_msg = resp["messages"][-1].model_dump()
    last_msg["type"] = "environment_agent"
    last_msg = EnvironmentAgentMessage(**last_msg)
    print(last_msg.content)


if __name__ == "__main__":
    asyncio.run(main())
