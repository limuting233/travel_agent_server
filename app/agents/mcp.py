from typing import List

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.core.config import settings

from loguru import logger

mcp_client: MultiServerMCPClient | None = None


def create_mcp_client():
    """
    创建MCP客户端
    :return: MCP客户端
    """
    global mcp_client
    if mcp_client is not None:
        logger.info("MCP客户端已存在")
        return
    logger.info("正在创建MCP客户端 ...")
    mcp_config = {
        # 小红书MCP配置
        "xiaohongshu_mcp": {
            "transport": "http",
            "url": settings.XHS_MCP_URL,
        }
    }

    mcp_client = MultiServerMCPClient(mcp_config)
    logger.info("MCP客户端创建完成")


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


async def get_xiaohongshu_mcp_tools() -> List[BaseTool]:
    global mcp_client
    # if mcp_client is None:
    #     create_mcp_client()
    tools = await mcp_client.get_tools(server_name="xiaohongshu_mcp")
    return [fix_tool_schema(tool) for tool in tools]
