import asyncio

from app.agents.mcp import create_mcp_client, get_xiaohongshu_mcp_tools


async def main():
    create_mcp_client()
    tools = await get_xiaohongshu_mcp_tools()
    # for tool in tools:
    #     print(tool.name)
    needed_tools=[]
    for t in tools:
        if t.name  in ["check_login_status", "get_feed_detail", "search_feeds"]:
            needed_tools.append(t)
    for t in needed_tools:
        print(t.name)


if __name__ == "__main__":
    asyncio.run(main())
