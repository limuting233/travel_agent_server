import asyncio
import json

from langchain_core.messages import HumanMessage

from app.agents.mcp import create_xhc_mcp_session, create_amap_mcp_session
from app.agents.planner_agent.agent import PlannerAgentBuilder
from app.agents.resource_agent.agent import ResourceAgentBuilder


async def main():
    # create_mcp_client()
    # res_agent = await ResourceAgentBuilder().build()
    # resp = await res_agent.ainvoke({
    #     "messages": [HumanMessage(content="去上海旅游一天，都为晴天，我想要吃上海的美食")]
    # })
    # print(resp)
    # async for agent in ResourceAgentBuilder().build():
    #     resp = await agent.ainvoke({
    #         "messages": [HumanMessage(content="去上海旅游一天，都为晴天，我想要吃上海的美食")]
    #     })
    #     print(resp)
    data = {
        "candidates": [
            {"id": "B00155LZQ0", "name": "上海美食城(南京路步行街店)", "category": "LOCAL_GASTRONOMY", "tags": [],
             "location": "121.485456,31.236800", "rating": 4.4, "price": 8.0, "open_time": "",
             "suggested_duration": 1.0, "photo": "",
             "recommend_reason": "高德评分4.4；小红书笔记中无明显避雷信息，部分笔记提及该店特色美食。"},
            {"id": "B0J131PAZS", "name": "黎巴嫩美食(上海商城店)", "category": "LOCAL_GASTRONOMY",
             "tags": ["羊肉", "烤肉"], "location": "121.451441,31.226487", "rating": 4.5, "price": 153.0,
             "open_time": "11:00-22:30", "suggested_duration": 1.5, "photo": "",
             "recommend_reason": "高德评分4.5，小红书笔记多称赞其羊肉和烤肉，口碑较好。"},
            {"id": "B0FFJDLZMV", "name": "新疆美食烧烤(上海大学店)第5分店", "category": "LOCAL_GASTRONOMY",
             "tags": ["羊肉", "烤串"], "location": "121.388234,31.320912", "rating": 4.0, "price": 65.0,
             "open_time": "17:00-24:00", "suggested_duration": 1.5, "photo": "",
             "recommend_reason": "高德评分4.0，部分小红书笔记称赞烤串，但无避雷标题。"},
            {"id": "B0LR17T3J5", "name": "邢老三肉丸糊辣汤·非遗美食(上海店)", "category": "LOCAL_GASTRONOMY",
             "tags": ["单人餐"], "location": "121.518840,31.228745", "rating": 4.6, "price": 29.0,
             "open_time": "07:00-22:00", "suggested_duration": 1.0, "photo": "",
             "recommend_reason": "高德评分4.6，小红书多篇热门笔记标题推荐其非遗肉丸汤，口碑良好。"},
            {"id": "B0G257X85E", "name": "巴奴毛肚火锅(上海人广来福士店)", "category": "LOCAL_GASTRONOMY",
             "tags": ["火锅", "双人餐"], "location": "121.477150,31.232142", "rating": 4.7, "price": 157.0,
             "open_time": "00:00-24:00", "suggested_duration": 2.0, "photo": "",
             "recommend_reason": "高德评分4.7，小红书笔记多含'必吃'和高点赞推荐，热度极高。"},
            {"id": "B0K64HQF9I", "name": "费大厨辣椒炒肉(人广来福士店)", "category": "LOCAL_GASTRONOMY",
             "tags": ["辣椒炒肉"], "location": "121.476678,31.232310", "rating": 4.6, "price": 81.0,
             "open_time": "11:00-21:00", "suggested_duration": 1.5, "photo": "",
             "recommend_reason": "高德评分4.6，小红书笔记含'推荐'关键词，口碑正面。"},
            {"id": "B0K6UZO9NN", "name": "3号仓库·创意中国菜(新世界城店)", "category": "LOCAL_GASTRONOMY",
             "tags": ["创意菜", "烤鸭"], "location": "121.473875,31.234825", "rating": 4.8, "price": 158.0,
             "open_time": "10:00-21:30", "suggested_duration": 1.5, "photo": "",
             "recommend_reason": "高德评分4.8，小红书好评多，推荐创意中餐体验。"}
        ]
    }
    str = json.dumps(data,ensure_ascii=False)
    async with create_amap_mcp_session():
        agent = await PlannerAgentBuilder().build()
        resp = await agent.ainvoke({
            "messages": [HumanMessage(content=f"候选poi:{str}。一天的上海旅游，天气为晴天，偏好美食")]
        })
        print(resp)
        # async with ResourceAgentBuilder().build() as res_agent:
        #     resp = await res_agent.ainvoke({
        #         "messages": [HumanMessage(content="去上海旅游一天，都为晴天，我想要吃上海的美食")]
        #     })
        #     print(resp)


if __name__ == "__main__":
    asyncio.run(main())
