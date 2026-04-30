from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from app.agents.environment_agent.prompt import ENVIRONMENT_AGENT_SYSTEM_PROMPT
from app.agents.environment_agent.tools.weather import search_weather_tool
from app.core.config import settings


class EnvironmentAgentBuilder:
    """
    EnvironmentAgent构建器，用于构建EnvironmentAgent
    """

    def __init__(self):
        # self.llm = ChatOllama(
        #     model="qwen3:8b",
        #     # base_url=settings.OLLAMA_API_BASE,
        #
        # )
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini", base_url=settings.OPENAI_API_BASE, api_key=settings.OPENAI_API_KEY)

    def build(self):
        """
        构建EnvironmentAgent
        :return: EnvironmentAgent实例
        """
        return create_agent(
            model=self.llm,
            tools=[search_weather_tool],
            system_prompt=ENVIRONMENT_AGENT_SYSTEM_PROMPT,
            debug=True,
        )
