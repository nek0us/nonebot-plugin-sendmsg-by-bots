import nonebot
from nonebot.adapters.onebot.v11.adapter import Adapter
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import ActionFailed
from nonebot import logger

async def get_all_group_info(group_id:int):
    '''从所有bot账号中检索群信息 return {"group_name":"未获取到群名","group_id":group_id}'''
    bots = nonebot.get_adapter(Adapter).bots
    for bot in bots:
        try:
            group_info = await bots[bot].get_group_info(group_id=group_id)
            return group_info
        except ActionFailed:
            pass
        except Exception as e:
            pass
    logger.debug(f"没有检测到有关群{group_id}的信息，也许所有bot均已退群。")
    return {"group_name":"未获取到群名","group_id":group_id}
        
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
    status = False
    for bot in bots:
        if await is_in_group(bots[bot],int(group_id)):
            await bots[bot].send_group_forward_msg(group_id=int(group_id), messages=node_msg)
            status = True
    return status
        
async def send_private_forward_msg_by_bots(user_id:int,node_msg:list) -> bool:
    '''user_id：尝试发送到的好友qq号\n
    msg：尝试发送的node列表\n
    不在bot好友列表的qq不会尝试发送'''
    bots = nonebot.get_adapter(Adapter).bots
    status = False
    for bot in bots:
        if await is_in_friend(bots[bot],int(user_id)):
            await bots[bot].send_private_forward_msg(user_id=int(user_id), messages=node_msg)
            status = True
    return status

async def send_group_forward_msg_by_bots_once(group_id:int,node_msg:list) -> bool:
    '''group_id：尝试发送到的群号\n
    msg：尝试发送的node列表\n
    不在bot群列表的群不会尝试发送'''
    bots = nonebot.get_adapter(Adapter).bots
    status = False
    for bot in bots:
        if await is_in_group(bots[bot],int(group_id)):
            await bots[bot].send_group_forward_msg(group_id=int(group_id), messages=node_msg)
            status = True
            return status
    return status
        
async def send_private_forward_msg_by_bots_once(user_id:int,node_msg:list) -> bool:
    '''user_id：尝试发送到的好友qq号\n
    msg：尝试发送的node列表\n
    不在bot好友列表的qq不会尝试发送'''
    bots = nonebot.get_adapter(Adapter).bots
    status = False
    for bot in bots:
        if await is_in_friend(bots[bot],int(user_id)):
            await bots[bot].send_private_forward_msg(user_id=int(user_id), messages=node_msg)
            status = True
            return status
    return status            
async def send_group_msg_by_bots(group_id:int,msg:Message|MessageSegment|str) -> bool:
    '''group_id：尝试发送到的群号\n
    msg：尝试发送的消息\n
    不在bot群列表的群不会尝试发送'''
    bots = nonebot.get_adapter(Adapter).bots
    status = False
    for bot in bots:
        if await is_in_group(bots[bot],int(group_id)):
            await bots[bot].send_group_msg(group_id=int(group_id),message=msg)
            status = True
    return status

async def send_group_msg_by_bots_once(group_id:int,msg:Message|MessageSegment|str) -> bool:
    '''group_id：尝试发送到的群号\n
    msg：尝试发送的消息\n
    不在bot群列表的群不会尝试发送'''
    bots = nonebot.get_adapter(Adapter).bots
    status = False
    for bot in bots:
        if await is_in_group(bots[bot],int(group_id)):
            await bots[bot].send_group_msg(group_id=int(group_id),message=msg)
            status = True
            return status
    return status

async def send_private_msg_by_bots(user_id:int,msg:Message|MessageSegment|str) -> bool:
    '''user_id：尝试发送到的好友qq号\n
    msg：尝试发送的消息\n
    不在bot好友列表的qq不会尝试发送'''
    bots = nonebot.get_adapter(Adapter).bots
    status = False
    for bot in bots:
        if await is_in_friend(bots[bot],int(user_id)):
            await bots[bot].send_private_msg(user_id=int(user_id),message=msg)
            status = True
    return status

async def send_private_msg_by_bots_once(user_id:int,msg:Message|MessageSegment|str) -> bool:
    '''user_id：尝试发送到的好友qq号\n
    msg：尝试发送的消息\n
    不在bot好友列表的qq不会尝试发送'''
    bots = nonebot.get_adapter(Adapter).bots
    status = False
    for bot in bots:
        if await is_in_friend(bots[bot],int(user_id)):
            await bots[bot].send_private_msg(user_id=int(user_id),message=msg)
            status = True
            return status
    return status               
        
        
async def get_group_member_list(group_id: int) -> list:
    '''根据群号检索群成员列表'''
    bots = nonebot.get_adapter(Adapter).bots
    group_member = []
    for bot in bots:
        if await is_in_group(bots[bot],int(group_id)):
            group_member = await bots[bot].call_api('get_group_member_list',**{"group_id":group_id})
    return group_member