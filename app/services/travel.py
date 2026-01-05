import httpx

from app.core.config import settings
from app.schemas.request.travel import PlanTravelRequest
from loguru import logger
from datetime import datetime, date


class TravelService:
    """
    旅行service,实现旅行相关功能
    """

    async def plan_travel(self, request: PlanTravelRequest):
        """
        旅行规划功能实现函数
        :param request: 旅行规划请求模型
        :return:
        """
        location = request.location  # 目的地
        days = request.days  # 计划天数
        start_date = request.start_date if request.start_date else None  # 计划开始日期
        end_date = request.end_date if request.end_date else None  # 计划结束日期
        preferences = request.preferences if request.preferences else None  # 用户偏好

        # weather_str: str | None = None  # 天气信息字符串,将来作为提示词传入travel_agent

        # if start_date and end_date and (datetime.strptime(end_date, "%Y-%m-%d").date() - date.today()).days + 1 <= 4:
        #     # today = date.today()
        #     # end = datetime.strptime(end_date, "%Y-%m-%d").date()
        #     # if (end-today).days+1 <= 4:
        #     async with httpx.AsyncClient() as client:
        #         try:
        #             # 获取该location对应的adcode
        #             adcode = await self._get_adcode(location, client)
        #             # 获取该adcode对应的天气信息
        #             weathers = await self._get_weather(adcode, client, start_date, end_date)
        #         except Exception as e:
        #             logger.error(f"{str(e)}")

    # async def _get_adcode(self, location: str, client: httpx.AsyncClient):
    #     """
    #     获取location对应的adcode
    #     :param location: 目的地
    #     :param client: httpx.AsyncClient
    #     :return: adcode
    #     """
    #     try:
    #         resp = await client.get(
    #             url=f"{settings.AMAP_API_BASE}/geocode/geo",
    #             params={
    #                 "key": settings.AMAP_API_KEY,
    #                 "address": location,
    #
    #             }
    #         )
    #         resp.raise_for_status()
    #         resp = resp.json()
    #         if resp["status"] == "0":
    #             raise Exception(resp["info"])
    #         adcode = resp["geocodes"][0]["adcode"]
    #         return adcode
    #     except Exception as e:
    #         logger.error(f"获取{location}的adcode失败,{str(e)}")
    #         # raise Exception()
    #
    # async def _get_weather(self, adcode: str, client: httpx.AsyncClient, start_date: str, end_date: str):
    #     """
    #     获取adcode对应的天气,只可查询未来4天的天气信息，包括当前日期
    #     :param adcode: 区域编码
    #     :param client: httpx.AsyncClient
    #     :param start_date: 计划开始日期
    #     :param end_date: 计划结束日期
    #     :return: 天气信息
    #     """
    #     try:
    #         resp = await client.get(
    #             url=f"{settings.AMAP_API_BASE}/weather/weatherInfo",
    #             params={
    #                 "key": settings.AMAP_API_KEY,
    #                 "city": adcode,
    #                 "extensions": "all"
    #             }
    #         )
    #         resp.raise_for_status()
    #         resp = resp.json()
    #         # print(resp["forecasts"][0]["casts"])
    #         if resp["status"] == "0":
    #             raise Exception(resp["info"])
    #         if resp["status"] == "1" and resp["info"] == "OK" and resp["infocode"] == "10000" and resp["count"] == "1":
    #             casts = resp["forecasts"][0]["casts"]  # 获取casts列表
    #
    #             # 过滤出指定日期范围内的天气信息
    #             filtered_casts = filter(
    #                 lambda x: datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(x["date"],
    #                                                                                          "%Y-%m-%d") <= datetime.strptime(
    #                     end_date, "%Y-%m-%d"), casts)
    #             # print(list(filtered_casts))
    #             # for cast in casts:
    #             #     if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(cast["date"],
    #             #                                                                       "%Y-%m-%d") <= datetime.strptime(
    #             #         end_date, "%Y-%m-%d"):
    #             #         filtered_casts.append(cast)
    #             return filtered_casts
    #
    #     except Exception as e:
    #         logger.error(f"查询{adcode}的天气失败, {str(e)}")
