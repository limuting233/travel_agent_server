from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from app.agents.mcp import create_mcp_client, get_xiaohongshu_mcp_tools
from app.agents.resource_agent.prompt import RESOURCE_AGENT_SYSTEM_PROMPT
from app.core.config import settings


class ResourceAgentBuilder:
    """
    ResourceAgent构建器，用于构建ResourceAgent
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            base_url=settings.OPENAI_API_BASE,
            api_key=settings.OPENAI_API_KEY
        )

    async def build(self):
        """
        构建ResourceAgent
        :return: ResourceAgent实例
        """
        # mcp_client = create_mcp_client()
        # tools = await get_mcp_tools()
        tools = await get_xiaohongshu_mcp_tools()

        return create_agent(
            model=self.llm,
            tools=tools,
            system_prompt=RESOURCE_AGENT_SYSTEM_PROMPT,
            debug=True,
        )
