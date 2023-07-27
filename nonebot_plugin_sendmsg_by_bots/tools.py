import nonebot
from nonebot.adapters.onebot.v11.adapter import Adapter
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.adapters.onebot.v11.bot import Bot

async def is_in_group(bot:Bot,group_id:int) -> bool:
    group_list = await bot.get_group_list()
    if group_id not in [group_num["group_id"] for group_num in group_list]:
        return False
    return True

async def is_in_friend(bot:Bot,user_id:int) -> bool:
    friend_list = await bot.get_friend_list()
    if user_id not in [friend_id["user_id"] for friend_id in friend_list]:
        return False
    return True

async def send_group_forward_msg_by_bots(group_id:int,node_msg:list) -> bool:
    '''group_id：尝试发送到的群号\n
    msg：尝试发送的node列表\n
    不在bot群列表的群不会尝试发送'''
    bots = nonebot.get_adapter(Adapter).bots
    for bot in bots:
        if await is_in_group(bots[bot],int(group_id)):
            await bots[bot].send_group_forward_msg(group_id=int(group_id), messages=node_msg)
            return True
        return False
        
async def send_private_forward_msg_by_bots(user_id:int,node_msg:list) -> bool:
    '''user_id：尝试发送到的好友qq号\n
    msg：尝试发送的node列表\n
    不在bot好友列表的qq不会尝试发送'''
    bots = nonebot.get_adapter(Adapter).bots
    for bot in bots:
        if await is_in_friend(bots[bot],int(user_id)):
            await bots[bot].send_private_forward_msg(user_id=int(user_id), messages=node_msg)
            return True
        return False
            
async def send_group_msg_by_bots(group_id:int,msg:Message|MessageSegment|str) -> bool:
    '''group_id：尝试发送到的群号\n
    msg：尝试发送的消息\n
    不在bot群列表的群不会尝试发送'''
    bots = nonebot.get_adapter(Adapter).bots
    for bot in bots:
        if await is_in_group(bots[bot],int(group_id)):
            await bots[bot].send_group_msg(group_id=int(group_id),message=msg)
            return True
        return False

async def send_private_msg_by_bots(user_id:int,msg:Message|MessageSegment|str) -> bool:
    '''user_id：尝试发送到的好友qq号\n
    msg：尝试发送的消息\n
    不在bot好友列表的qq不会尝试发送'''
    bots = nonebot.get_adapter(Adapter).bots
    for bot in bots:
        if await is_in_friend(bots[bot],int(user_id)):
            await bots[bot].send_private_msg(user_id=int(user_id),message=msg)
            return True
        return False
               
        
        