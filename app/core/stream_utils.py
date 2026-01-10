import json
from typing import AsyncGenerator

from loguru import logger
from pydantic import BaseModel


async def sse_generator(generator: AsyncGenerator[BaseModel | dict | str, None]):
    """
    [中间件] 将业务生成器转换为 SSE 协议流
    功能：
    1. 自动识别 Pydantic 模型并序列化
    2. 自动识别 Dict 并序列化
    3. 统一异常捕获和错误格式输出
    """

    try:
        async for chunk in generator:
            # payload = ""
            if isinstance(chunk, BaseModel):
                # model_dump_json() 比 json.dumps(model.dict()) 性能更好
                # payload = chunk.model_dump_json()
                event = chunk.event
                data = chunk.data

            # elif isinstance(chunk, dict):
            #     payload = json.dumps(chunk, check_circular=False)
            #
            # else:
            #     payload = json.dumps({"data": chunk}, check_circular=False)

            yield f"event: {event}\ndata: {data.model_dump_json()}\n\n"
    except Exception as e:
        logger.error(f"[sse_generator] 异常: {str(e)}")
        # payload = json.dumps({"error": str(e)}, check_circular=False)
