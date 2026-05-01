import asyncio
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_mcp_adapters.tools import load_mcp_tools

from app.agents.mcp import create_xhc_mcp_session, is_xhs_mcp_enabled


async def main():
    """
    最简单的小红书 MCP 测试脚本：
    1. 建立连接
    2. 打印工具列表
    3. 优先测试 check_login_status
    4. 若存在 search_feeds，再跑一个固定关键词示例
    """
    if not is_xhs_mcp_enabled():
        print("小红书 MCP 当前已关闭，请先将 ENABLE_XHS_MCP 打开后再测试。")
        return

    async with create_xhc_mcp_session():
        from app.agents.mcp import xhs_mcp_session

        tools = await load_mcp_tools(session=xhs_mcp_session)
        print(f"已加载 {len(tools)} 个小红书 MCP 工具")

        tool_map = {}
        for tool in tools:
            tool_map[tool.name] = tool
            print(f"- {tool.name}")

        login_tool = tool_map.get("check_login_status")
        if login_tool is not None:
            print("\n[check_login_status] 开始测试")
            login_result = await login_tool.ainvoke({})
            print(login_result)
        else:
            print("\n未找到 check_login_status 工具，跳过登录状态测试")

        search_tool = tool_map.get("search_feeds")
        if search_tool is not None:
            print("\n[search_feeds] 开始测试")
            search_input = {"keyword": "上海 外滩 攻略"}
            print(f"入参: {json.dumps(search_input, ensure_ascii=False)}")
            search_result = await search_tool.ainvoke(search_input)
            print(search_result)
        else:
            print("\n未找到 search_feeds 工具，跳过搜索测试")


if __name__ == "__main__":
    asyncio.run(main())
