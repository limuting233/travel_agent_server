from langchain_core.messages import HumanMessage

from app.agents.mcp import create_mcp_client
from app.agents.resource_agent.agent import ResourceAgentBuilder
import asyncio


async def main():
    create_mcp_client()
    resource_agent = await ResourceAgentBuilder().build()
    resp = await resource_agent.ainvoke({
        "messages": [HumanMessage(content="调用search_feeds工具，工具的参数keyword为小红书")]
    })
    print(resp)


if __name__ == '__main__':
    asyncio.run(main())
