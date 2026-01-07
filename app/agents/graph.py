from langgraph.graph import StateGraph, START, END

# from app.agents.mcp import create_mcp_client
from app.agents.memory import  init_checkpointer
from app.agents.state import TravelAgentState

from loguru import logger

travel_agent = None


async def build_travel_agent():
    """
    构建旅行智能体
    :return: None
    """
    global travel_agent
    if travel_agent is not None:
        logger.info("TravelAgent 已构建")
        return

    logger.info("正在构建 TravelAgent ...")
    checkpointer = await init_checkpointer()

    # create_mcp_client()

    # TODO: 构建travel_agent的图
    graph = StateGraph(TravelAgentState)
    graph.add_edge(START, END)


    travel_agent = graph.compile(checkpointer=checkpointer)

    logger.info("TravelAgent 构建完成")
