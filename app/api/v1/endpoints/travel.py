from fastapi import APIRouter

from loguru import logger
from fastapi.responses import StreamingResponse

from app.core.stream_utils import sse_generator
from app.schemas.request.travel import PlanTravelRequest
from app.services.travel import TravelService

router = APIRouter()


@router.post("/plan")
async def plan_travel(request: PlanTravelRequest):
    """
    旅行规划接口
    :param request: 旅行规划请求模型
    :return:
    """
    logger.info(f"[旅行规划接口] 请求参数: {request}")

    travel_service = TravelService()
    return StreamingResponse(
        content=sse_generator(travel_service.plan_travel(request)),
        media_type="text/event-stream"
    )
