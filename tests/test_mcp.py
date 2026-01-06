import asyncio

from app.agents.mcp import create_mcp_client, get_xiaohongshu_mcp_tools


async def main():
    create_mcp_client()
    tools =await get_xiaohongshu_mcp_tools()
    print(tools)


if __name__ == "__main__":
    asyncio.run(main())
