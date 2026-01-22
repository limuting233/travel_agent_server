from typing import Literal

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.agents.manager_agent.prompt import MANAGER_AGENT_SYSTEM_PROMPT
from app.agents.manager_agent.tools import is_need_search_weather_tool
from app.core.config import settings


class ManagerAgentOutput(BaseModel):
    next_to: Literal["environment_agent", "resource_agent", "planner_agent", "finish"] = Field(
        description="下一个要调用的智能体，必须是以下值之一: environment_agent, resource_agent, planner_agent, finish"
    )
    reason: str = Field(description="调用下一个智能体的原因，必须是简明的中文说明")


class ManagerAgentBuilder:
    def __init__(self):
        self.llm = ChatOllama(
            model="qwen3:8b",
            # base_url=settings.OLLAMA_API_BASE,

        )
        # self.llm = ChatOpenAI(
        #     model="gpt-4.1-mini", base_url=settings.OPENAI_API_BASE, api_key=settings.OPENAI_API_KEY)

    def build(self):
        return create_agent(
            model=self.llm,
            tools=[is_need_search_weather_tool],
            system_prompt=MANAGER_AGENT_SYSTEM_PROMPT,
            response_format=ToolStrategy(ManagerAgentOutput),
            debug=True,
        )
