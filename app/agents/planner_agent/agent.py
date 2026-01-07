from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from app.core.config import settings

from app.agents.planner_agent.prompt import PLANNER_AGENT_SYSTEM_PROMPT


class PlannerAgentBuilder:
    """
    旅游规划师智能体构建器，用于构建旅游规划师智能体。
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini", base_url=settings.OPENAI_API_BASE, api_key=settings.OPENAI_API_KEY)

    def build(self):
        """
        构建旅游规划师智能体
        :return: 旅游规划师智能体实例
        """
        return create_agent(
            model=self.llm,
            tools=[],
            system_prompt=PLANNER_AGENT_SYSTEM_PROMPT,
            debug=True,
        )
