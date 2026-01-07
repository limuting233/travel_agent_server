import asyncio

from langchain_core.messages import HumanMessage

from app.agents.mcp import create_xhc_mcp_session
from app.agents.resource_agent.agent import ResourceAgentBuilder


async def main():
    # create_mcp_client()
    # res_agent = await ResourceAgentBuilder().build()
    # resp = await res_agent.ainvoke({
    #     "messages": [HumanMessage(content="去上海旅游一天，都为晴天，我想要吃上海的美食")]
    # })
    # print(resp)
    # async for agent in ResourceAgentBuilder().build():
    #     resp = await agent.ainvoke({
    #         "messages": [HumanMessage(content="去上海旅游一天，都为晴天，我想要吃上海的美食")]
    #     })
    #     print(resp)

    async with create_xhc_mcp_session():
        agent = await ResourceAgentBuilder().build()
        resp = await agent.ainvoke({
            "messages": [HumanMessage(content="去上海旅游一天，都为晴天，我想要吃上海的美食")]
        })
        print(resp)
        # async with ResourceAgentBuilder().build() as res_agent:
        #     resp = await res_agent.ainvoke({
        #         "messages": [HumanMessage(content="去上海旅游一天，都为晴天，我想要吃上海的美食")]
        #     })
        #     print(resp)


if __name__ == "__main__":
    asyncio.run(main())
