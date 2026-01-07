from app.agents.resource_agent.tools.poi import search_poi


async def main():
    r = await search_poi("北京", "0", "美食")
    print(r)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
