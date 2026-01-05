from app.agents.environment_agent.tools.weather import search_weather

import asyncio


async def main():
    await search_weather(
        location="浙江省杭州市西湖区", start_date="2026-01-6", end_date="2026-01-7")


if __name__ == "__main__":
    asyncio.run(main())
