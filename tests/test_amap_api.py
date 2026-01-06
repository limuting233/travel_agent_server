import httpx

from app.agents.environment_agent.tools.weather import search_weather

import asyncio

from app.core.config import settings


async def main():
    # await search_weather(
    #     location="浙江省杭州市西湖区", start_date="2026-01-6", end_date="2026-01-7")

    async with httpx.AsyncClient() as client:
        resp=await client.get(
            url=f"{settings.AMAP_API_BASE}/v5/place/text",
            params={
                "key":settings.AMAP_API_KEY,
                "keywords":"网红",
                "types":"",
                "region":"320583",
                "citylimit":"true",
                "show_fields":"business,navi,photos"
            }
        )
        pois = resp.json().get("pois", [])
        for p in pois:
            print(p["name"])

if __name__ == "__main__":
    asyncio.run(main())
