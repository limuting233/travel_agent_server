import json

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime

from app.agents.context import TravelAgentContext
from app.agents.environment_agent.agent import EnvironmentAgentBuilder
from app.agents.manager_agent.agent import ManagerAgentBuilder, ManagerAgentOutput
# from app.agents.mcp import create_mcp_client
from app.agents.memory import init_checkpointer
from app.agents.message import ManagerAgentMessage, EnvironmentAgentMessage, ResourceAgentMessage, PlannerAgentMessage
from app.agents.planner_agent.agent import PlannerAgentBuilder
from app.agents.resource_agent.agent import ResourceAgentBuilder
from app.agents.state import TravelAgentState

from loguru import logger

travel_agent = None


async def manager_agent_node(state: TravelAgentState, runtime: Runtime[TravelAgentContext]):
    """
    manager agent节点
    :param state: travel agent状态
    :param runtime: travel agent运行时
    :return: travel agent状态中需要更新的部分
    """
    logger.info("进入manager_agent_node")
    agent = ManagerAgentBuilder().build()
    is_just_start: bool = state["is_just_start"]
    context = runtime.context

    if is_just_start:
        # travel_agent 刚启动

        first_msg = _build_initial_message(context)

        resp = await agent.ainvoke(
            input={
                "messages": [SystemMessage(content=first_msg)]
            }
        )
        return {
            "current_phase": "manager_agent",
            "next_phase": resp["structured_response"].next_to,
            "is_just_start": False,
            "messages": [
                resp["messages"][0],
                ManagerAgentMessage(content=resp["structured_response"].model_dump_json())
            ]

            # "manager_agent_response": resp["structured_response"].model_dump(),
            # "messages": [{"role": "user", "content": first_msg}]
        }

    last_phase = state["current_phase"]  # travel agent运行的上一个阶段
    if last_phase == "environment_agent":
        weather_msg = state["messages"][-1].content
        msg = f"上一个阶段是environment_agent,environment_agent查询到的天气和生成的旅行建议如下：\n{weather_msg}\n\n，你现在要做的是对environment agent生成的内容进行质检。"
        resp = await agent.ainvoke(
            input={
                "messages": [SystemMessage(content=msg)]
            }
        )
        return {
            "current_phase": "manager_agent",
            "next_phase": resp["structured_response"].next_to,
            "is_need_correct": True if resp["structured_response"].next_to == "environment_agent" else False,
            "need_correct_content": weather_msg if resp["structured_response"].next_to == "environment_agent" else None,
            # "is_just_start": False,
            "messages": [
                resp["messages"][0],
                ManagerAgentMessage(content=resp["structured_response"].model_dump_json())
            ]
        }

    if last_phase == "resource_agent":
        candidates = json.loads(state["messages"][-1].content)  # 解析resource agent返回的poi列表
        # todo 对poi列表进行质检
        return {
            "current_phase": "manager_agent",
            "next_phase": "planner_agent",
            "is_need_correct": False,
            "need_correct_content": None,
            "messages": [
                SystemMessage(content="请对resource agent返回的poi列表进行质检"),
                ManagerAgentMessage(
                    content=ManagerAgentOutput(next_to="planner_agent", reason="质检通过").model_dump_json())
            ]
        }

    if last_phase == "planner_agent":
        planner_output = state["messages"][-1].content
        # todo 对最终规划结果进行质检
        return {
            "current_phase": "manager_agent",
            "next_phase": "finish",
            "is_need_correct": False,
            "need_correct_content": None,
            "messages": [
                SystemMessage(content="请对planner agent返回的最终规划结果进行质检"),
                ManagerAgentMessage(
                    content=ManagerAgentOutput(next_to="finish", reason="质检通过").model_dump_json()),
                ManagerAgentMessage(content=planner_output)
            ]
        }


def _build_initial_message(context: TravelAgentContext) -> str:
    """
    构建初始消息
    :param context: 旅行智能体上下文
    :return: 初始消息
    """
    location = context["location"]
    days = context["days"]
    start_date = context.get("start_date", None)
    end_date = context.get("end_date", None)
    preferences = context.get("preferences", None)

    parts = [f"用户想去{location}游玩{days}天"]
    if start_date and end_date:
        parts.append(f"游玩时间是从{start_date}到{end_date}")
    if preferences:
        parts.append(f"用户的旅游偏好是{"、".join(preferences)}")

    return ", ".join(parts) + "。" + "请根据用户的旅游信息和偏好，制定一个旅游计划。"


async def environment_agent_node(state: TravelAgentState, runtime: Runtime[TravelAgentContext]):
    """
    environment agent节点
    :param state: travel agent状态
    :param runtime: travel agent运行时
    :return: travel agent状态中需要更新的部分
    """
    logger.info("进入environment_agent_node")

    agent = EnvironmentAgentBuilder().build()

    context = runtime.context
    location = context["location"]
    start_date = context["start_date"]
    end_date = context["end_date"]
    is_need_correct = state["is_need_correct"]
    if not is_need_correct:
        # 不需要修正，直接查询天气
        msg = f"用户想去{location}旅游，请你查询{location}从{start_date}到{end_date}的天气情况。"
        resp = await agent.ainvoke(
            input={
                "messages": [SystemMessage(content=msg)]
            }
        )
        last_msg = resp["messages"][-1].model_dump()
        last_msg["type"] = "environment_agent"

        return {
            "current_phase": "environment_agent",
            "next_phase": "manager_agent",
            "messages": [
                resp["messages"][0],
                EnvironmentAgentMessage(**last_msg),
            ]
        }

    # 需要修正
    state_last_msg = json.loads(state["messages"][-1].content)
    reason = state_last_msg["reason"]
    raw_content = state["need_correct_content"]
    msg = f"你做的旅游建议存在以下问题：\n{reason}\n\n你生成的旅游建议和你查询到的天气信息如下：\n{raw_content}\n\n请根据天气信息和存在的问题，重新生成一个旅游建议。"
    resp = await agent.ainvoke(
        input={
            "messages": [SystemMessage(content=msg)]
        }
    )
    last_msg = resp["messages"][-1].model_dump()
    last_msg["type"] = "environment_agent"
    return {
        "current_phase": "environment_agent",
        "next_phase": "manager_agent",
        "is_need_correct": False,
        "need_correct_content": None,
        "messages": [
            resp["messages"][0],
            EnvironmentAgentMessage(**last_msg),
        ]
    }


async def resource_agent_node(state: TravelAgentState, runtime: Runtime[TravelAgentContext]):
    """
    resource agent节点
    :param state: travel agent状态
    :param runtime: travel agent运行时
    :return: travel agent状态中需要更新的部分
    """
    logger.info("进入resource_agent_node")

    agent = await ResourceAgentBuilder().build()

    context = runtime.context
    location = context["location"]
    days = context["days"]
    start_date = context.get("start_date", None)
    end_date = context.get("end_date", None)
    preferences = context.get("preferences", None)
    is_need_correct = state["is_need_correct"]
    if not is_need_correct:
        # 不需要修正，直接查询poi
        msg = f"用户想去{location}旅游{days}天{days - 1}晚"
        if start_date and end_date:
            msg += f"，游玩时间是从{start_date}到{end_date}"
        if preferences:
            msg += f"，用户的旅游偏好是{"、".join(preferences)}"
        msg += f"，请你查询{location}的poi。"
        resp = await agent.ainvoke(
            input={
                "messages": [SystemMessage(content=msg)]
            }
        )
        candidates = resp["structured_response"].model_dump()["candidates"]

        return {
            "current_phase": "resource_agent",
            "next_phase": "manager_agent",
            "messages": [
                resp["messages"][0],
                ResourceAgentMessage(content=json.dumps(candidates, ensure_ascii=False)),
            ]
        }
    # todo 对poi列表进行质检不通过，需要重新查询poi


async def planner_agent_node(state: TravelAgentState, runtime: Runtime[TravelAgentContext]):
    """
    planner agent节点
    :param state: travel agent状态
    :param runtime: travel agent运行时
    :return: travel agent状态中需要更新的部分
    """
    logger.info("进入planner_agent_node")
    agent = await PlannerAgentBuilder().build()
    context = runtime.context

    if not state["is_need_correct"]:
        base_info = f"用户想去{context['location']}旅游{context['days']}天{context['days'] - 1}晚"
        if context["start_date"] and context["end_date"]:
            base_info += f"，游玩时间是从{context['start_date']}到{context['end_date']}"
        if context["preferences"]:
            base_info += f"，用户的旅游偏好是{"、".join(context['preferences'])}"
        base_info += "。"

        if context["start_date"] and context["end_date"]:
            weather_info = f"environment_agent查询到的{context['location']}从{context['start_date']}到{context['end_date']}的天气情况以及旅游决策建议如下：\n"
            for msg in reversed(state["messages"]):
                if isinstance(msg, EnvironmentAgentMessage):
                    weather_info += msg.content
                    break
        else:
            weather_info = ""

        poi_info = f"resource_agent查询到的{context['location']}的poi如下：\n"
        for msg in reversed(state["messages"]):
            if isinstance(msg, ResourceAgentMessage):
                poi_info += msg.content
                break

        if weather_info:
            msg = f"{base_info}\n\n{weather_info}\n\n{poi_info}"
        else:
            msg = f"{base_info}\n\n{poi_info}"

        msg = msg + "\n\n请根据旅游基本信息、天气信息和poi信息，生成一个具体旅游计划。"

        resp = await agent.ainvoke(
            input={
                "messages": [SystemMessage(content=msg)]
            }
        )
        res = resp["structured_response"].model_dump_json()
        return {
            "current_phase": "planner_agent",
            "next_phase": "manager_agent",
            "messages": [
                resp["messages"][0],
                PlannerAgentMessage(content=res),
            ]
        }
    # todo 对planner_agent的输出进行质检不通过，需要重新规划


async def build_travel_agent():
    """
    构建旅行智能体
    :return: None
    """
    global travel_agent
    if travel_agent is None:
        logger.info("正在构建 TravelAgent ...")
        await init_checkpointer()

        # create_mcp_client()

        graph = StateGraph(state_schema=TravelAgentState, context_schema=TravelAgentContext)

        graph.add_node(manager_agent_node, "manager_agent_node")
        graph.add_node(environment_agent_node, "environment_agent_node")
        graph.add_node(resource_agent_node, "resource_agent_node")
        graph.add_node(planner_agent_node, "planner_agent_node")

        graph.add_edge(START, "manager_agent_node")
        graph.add_conditional_edges(
            "manager_agent_node",
            lambda state: state["next_phase"],
            {
                "environment_agent": "environment_agent_node",
                "resource_agent": "resource_agent_node",
                "planner_agent": "planner_agent_node",
                "finish": END,
            }

        )

        graph.add_edge("environment_agent_node", "manager_agent_node")
        graph.add_edge("resource_agent_node", "manager_agent_node")
        graph.add_edge("planner_agent_node", "manager_agent_node")
        from app.agents.memory import checkpointer

        travel_agent = graph.compile(checkpointer=checkpointer)

        logger.info("TravelAgent 构建完成")
