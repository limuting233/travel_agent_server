import asyncio

from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.mcp import create_xhc_mcp_session
from app.agents.resource_agent.agent import ResourceAgentBuilder, Candidate, ResourceAgentOutput


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

    # async with create_xhc_mcp_session():
    #     agent = await ResourceAgentBuilder().build()
    #     resp = await agent.ainvoke({
    #         "messages": [SystemMessage(content="用户想去上海旅游4天3晚，游玩时间是从2026-01-10到2026-01-13，用户的旅游偏好是网红打卡、美食打卡，请你查询上海的poi。")]
    #     })
    #
    #     print("\nresp['structured_response']:")
    #     print(resp["structured_response"])
    # async with ResourceAgentBuilder().build() as res_agent:
    #     resp = await res_agent.ainvoke({
    #         "messages": [HumanMessage(content="去上海旅游一天，都为晴天，我想要吃上海的美食")]
    #     })
    #     print(resp)
    resp = ResourceAgentOutput(candidates=[
        Candidate(id='B00155FXB3', name='外滩', category='CORE_SIGHTSEEING', tags=['室外', '亲子'],
                  location='121.492127,31.233516', rating=4.9, price=None, open_time='00:00-24:00',
                  suggested_duration=2.0, photo='',
                  recommend_reason='高德评分4.9。小红书多篇热评笔记标题表现出对外滩夜景和历史建筑的赞美，热度和口碑较好。'),
        Candidate(id='B00155MF55', name='上海豫园', category='CORE_SIGHTSEEING', tags=['室外', '历史', '文化'],
                  location='121.492497,31.227714', rating=4.8, price=None, open_time='09:00-16:30',
                  suggested_duration=2.0, photo='',
                  recommend_reason='高德评分4.8，小红书笔记多推荐豫园与城隍庙游玩，口碑较优。'),
        Candidate(id='B00157917M', name='上海人民广场', category='CITY_LEISURE', tags=['室外'],
                  location='121.475213,31.228827', rating=4.7, price=None, open_time='00:00-24:00',
                  suggested_duration=1.5, photo='',
                  recommend_reason='高德评分4.7，小红书笔记中有丰富的市区游玩和美食推荐，网民认可度高。'),
        Candidate(id='B00155FHOA', name='上海城隍庙', category='CORE_SIGHTSEEING', tags=['室外', '历史', '文化'],
                  location='121.492466,31.225879', rating=4.8, price=None, open_time='08:30-16:30',
                  suggested_duration=1.5, photo='',
                  recommend_reason='高德评分4.8，小红书笔记多提及城隍庙的特色和历史底蕴，评价积极。'),
        Candidate(id='B00156Y4J9', name='农家菜老大(松江店)', category='LOCAL_GASTRONOMY', tags=['室内', '老字号'],
                  location='121.259257,31.038399', rating=4.8, price=93.0, open_time='10:30-14:30,16:30-20:30',
                  suggested_duration=1.5, photo='',
                  recommend_reason='高德评分4.8，部分小红书笔记提及菜品受欢迎，但有避雷贴需注意口味差异。'),
        Candidate(id='B0H01HNRB6', name='四季民福烤鸭店(外滩外白渡桥店)', category='LOCAL_GASTRONOMY',
                  tags=['室内', '老字号'], location='121.490444,31.247145', rating=4.8, price=184.0,
                  open_time='10:30-22:30', suggested_duration=1.5, photo='',
                  recommend_reason='高德评分4.8，小红书多篇笔记提到烤鸭好吃，口味正宗，适合尝试。'),
        Candidate(id='B0FFJBZBG2', name='点都德(环宇荟店)', category='LOCAL_GASTRONOMY',
                  tags=['室内', '老字号', '需预约'], location='121.476543,31.211745', rating=4.8, price=104.0,
                  open_time='09:00-21:30', suggested_duration=1.5, photo='',
                  recommend_reason='高德评分4.8，小红书中多篇测评和攻略推荐点都德，热度高，适合早茶体验。'),
        Candidate(id='B0H0OSXDUD', name='Gate M西岸梦中心', category='CITY_LEISURE', tags=['室外', '商场'],
                  location='121.465465,31.161190', rating=4.9, price=None, open_time='10:00-24:00',
                  suggested_duration=2.0, photo='',
                  recommend_reason='高德评分4.9，小红书多篇笔记称西岸梦中心是上海最chill的街区，氛围佳。')])
    print(resp.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
