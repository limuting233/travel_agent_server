import httpx
from loguru import logger


async def search_poi_by_amap(keywords: str, adcode: str):
    """
    根据关键词和区域代码搜索POI
    :param keywords: 搜索关键词
    :param adcode: 区域代码
    :return: 搜索到的POI列表
    """



    async with httpx.AsyncClient() as client:
        try:


        except Exception:
            logger.exception(f"搜索POI失败")
            return f"搜索POI失败"
