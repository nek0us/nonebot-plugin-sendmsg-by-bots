import nonebot
from nonebot.adapters.onebot.v11.adapter import Adapter

async def send_group_forward_msg_by_bots(group_id:int,msg:list):
    bots = nonebot.get_adapter(Adapter).bots
    for bot in bots:
        await bots[bot].send_group_forward_msg(group_id=int(1231), messages=msg)