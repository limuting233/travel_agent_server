import asyncio

from langchain_core.messages import HumanMessage

from app.agents.mcp import create_mcp_client
from app.agents.resource_agent.agent import ResourceAgentBuilder


async def main():
    create_mcp_client()
    res_agent = await ResourceAgentBuilder().build()
    resp = await res_agent.ainvoke({
        "messages": [HumanMessage(content="去上海旅游三天两晚，都为晴天，我想要打卡网红景点，吃上海的美食")]
    })
    print(resp)

if __name__ == "__main__":
    asyncio.run(main())

