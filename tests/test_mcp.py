import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools

from app.agents.mcp import create_amap_mcp_session


async def main():
    async with create_amap_mcp_session():
        from app.agents.mcp import amap_mcp_session
        tools = await load_mcp_tools(session=amap_mcp_session)
        for tool in tools:
            print(tool)


if __name__ == "__main__":
    asyncio.run(main())
