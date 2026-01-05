from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from app.agents.resource_agent.prompt import RESOURCE_AGENT_SYSTEM_PROMPT
from app.core.config import settings


class ResourceAgentBuilder:
    """
    ResourceAgent构建器，用于构建ResourceAgent
    """

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4.1-mini", base_url=settings.OPENAI_API_BASE, api_key=settings.OPENAI_API_KEY)

    def build(self):
        """
        构建ResourceAgent
        :return: ResourceAgent实例
        """
        return create_agent(
            model=self.llm,
            tools=[],
            system_prompt=RESOURCE_AGENT_SYSTEM_PROMPT,
            debug=True,
        )
