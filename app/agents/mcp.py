from contextlib import asynccontextmanager
from typing import List

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession

from app.core.config import settings

from loguru import logger

# mcp_client: MultiServerMCPClient | None = None

_active_session: ClientSession | None = None
_session_tools: List[BaseTool] | None = None


def _create_mcp_client():
    """
    创建MCP客户端
    :return: MCP客户端
    """
    # global mcp_client

    logger.info("正在创建MCP客户端 ...")
    mcp_config = {
        # 小红书MCP配置
        "xiaohongshu_mcp": {
            "transport": "http",
            "url": settings.XHS_MCP_URL,
            "timeout": settings.XHS_MCP_TIMEOUT,
        }
    }
    mcp_client = MultiServerMCPClient(mcp_config)
    logger.info("MCP客户端创建完成")

    return mcp_client


def fix_tool_schema(tool) -> BaseTool:
    """
    修复工具的 schema，确保符合 OpenAI function calling 的要求
    :param tool: 原始工具
    :return: 修复后的工具
    """
    if isinstance(tool.args_schema, dict):
        if "properties" not in tool.args_schema:
            tool.args_schema["properties"] = {}
            tool.args_schema["required"] = []

    return tool


@asynccontextmanager
async def xhs_mcp_session():
    """
    创建小红书MCP持久会话（上下文管理器）

    使用方式：
        async with xiaohongshu_session() as (session, tools):
            # 在此块内，会话保持连接
            agent = create_agent(model=llm, tools=tools)
            result = await agent.ainvoke(...)

    :yield: (ClientSession, tools列表) 元组
    """
    client = _create_mcp_client()  # 创建MCP客户端
    logger.info(f"正在创建小红书MCP持久会话 ...")

    async with client.session(server_name="xiaohongshu_mcp") as session:
        logger.info("小红书MCP会话创建完成")
        tools = await load_mcp_tools(session=session)
        fixed_tools = [fix_tool_schema(t) for t in tools]
        logger.info(f"已加载 {len(fixed_tools)} 个小红书MCP工具")

        try:
            yield session, fixed_tools
        finally:
            logger.info("小红书MCP会话已关闭")

#
# def create_mcp_client():
#     """
#     创建MCP客户端
#     :return: None
#     """
#     global mcp_client
#     if mcp_client is not None:
#         logger.info("MCP客户端已存在")
#         return
#     logger.info("正在创建MCP客户端 ...")
#     mcp_config = {
#         # 小红书MCP配置
#         "xiaohongshu_mcp": {
#             "transport": "http",
#             "url": settings.XHS_MCP_URL,
#             "timeout": settings.XHS_MCP_TIMEOUT,
#         }
#     }
#
#     mcp_client = MultiServerMCPClient(mcp_config)
#     logger.info("MCP客户端创建完成")
#
#
# async def get_xiaohongshu_mcp_tools() -> List[BaseTool]:
#     """
#     获取小红书MCP的工具列表
#     :return: 小红书MCP的工具列表
#     """
#     global mcp_client
#     if mcp_client is None:
#         create_mcp_client()
#     tools = await mcp_client.get_tools(server_name="xiaohongshu_mcp")
#     return [fix_tool_schema(tool) for tool in tools]
