import nonebot
from nonebot.adapters.onebot.v11.adapter import Adapter
from nonebot.adapters.onebot.v11 import Message,MessageSegment,GroupMessageEvent
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import ActionFailed
from nonebot.exception import FinishedException,ActionFailed
from nonebot.matcher import current_bot,current_event
from nonebot import logger,require,get_bots
from typing import Union,Optional
from more_itertools import chunked
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import text_to_pic,md_to_pic
import inspect

class MessageSegment(MessageSegment):
    """重构消息段，使其支持拉格兰"""

    @classmethod
    def node_custom_lgr(
        cls, node: Union[list[MessageSegment],Message,MessageSegment]
        ) -> Message:
        if isinstance(node,list):
            return Message( cls(
            "node", {"uin": str(msg.data["user_id"]), "name": msg.data["nickname"], "content": msg.data["content"]}
        ) for msg in node)
        else:
            return Message(cls(
                "node", {"uin": str(node.data["user_id"]), "name": node.data["nickname"], "content": node.data["content"]}
            ))
        
async def send_forward_msg_chunk(bot: Bot,id: int,msg: list,msg_type: str = "group"):
    try:
        if len(msg) > 200:
            chunks = list(chunked(msg,200))
            for list_value in chunks: 
                if msg_type == "group":
                    await bot.send_group_forward_msg(group_id=int(id), messages=list_value)
                else:
                    await bot.send_private_forward_msg(user_id=int(id), messages=list_value)
        else:
            if msg_type == "group":
                await bot.send_group_forward_msg(group_id=int(id), messages=msg)
            else:
                await bot.send_private_forward_msg(user_id=int(id), messages=msg)
    except Exception as e:
        raise e

async def send_forward_msg(bot: Bot,id: int,msg: list,msg_type: str = "group"):
    try:
        await send_forward_msg_chunk(bot, id, msg, msg_type)
    except FinishedException:
        pass
    except ActionFailed as e:
        # 拉格兰兼容
        if e.info["status"] == "failed" and e.info["retcode"] == 200 and e.info["data"] == None: # type: ignore
            msg = MessageSegment.node_custom_lgr(msg)
            await send_forward_msg_chunk(bot, id, msg, msg_type)
        else:
            pic_list = [await md_to_pic(text.data['content'][0].data['text']) for text in msg]
            md_msg_list = [MessageSegment.node_custom(user_id=int(bot.self_id),nickname=str(index + 1),content=Message(MessageSegment.image(x))) for index,x in enumerate(pic_list)]
            await send_forward_msg_chunk(bot, id, md_msg_list, msg_type)
    except Exception as e:
        logger.warning(f"发送合并消息失败：{e}")

def log():
    
    try:
        caller_name = inspect.stack()[1].function
        caller_name_origin = inspect.stack()[2].function
        logger.debug(f"""bot列表调用链: {caller_name} {caller_name_origin} 获取适配器
从适配器获取 {nonebot.get_adapter(Adapter)} {nonebot.get_adapter(Adapter).bots}
从驱动器获取 {nonebot.get_bots()}""")
    except Exception as e:
        logger.warning(f"获取适配器出错 {e}")

async def get_all_group_info(group_id:int):
    '''从所有bot账号中检索群信息 return {"group_name":"未获取到群名","group_id":group_id}'''
    # bots = nonebot.get_adapter(Adapter).bots
    bots = get_bots()
    log()
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
    log()
    # bots = nonebot.get_adapter(Adapter).bots
    bots = get_bots()
    status = False
    for bot in bots:
        if await is_in_group(bots[bot],int(group_id)):
            await send_forward_msg(bots[bot],int(group_id),node_msg)
            status = True
    return status
        
async def send_private_forward_msg_by_bots(user_id:int,node_msg:list) -> bool:
    '''user_id：尝试发送到的好友qq号\n
    msg：尝试发送的node列表\n
    不在bot好友列表的qq不会尝试发送'''
    log()
    # bots = nonebot.get_adapter(Adapter).bots
    bots = get_bots()
    status = False
    for bot in bots:
        if await is_in_friend(bots[bot],int(user_id)):
            await send_forward_msg(bots[bot],int(user_id),node_msg,msg_type="private")
            status = True
    return status

async def send_group_forward_msg_by_bots_once(group_id:int,node_msg:list,bot_id: Optional[str] = None) -> bool:
    '''group_id：尝试发送到的群号\n
    msg：尝试发送的node列表\n
    不在bot群列表的群不会尝试发送'''
    log()
    # bots = nonebot.get_adapter(Adapter).bots
    bots = get_bots()
    status = False
    
    if bot_id:
        try:
            await send_forward_msg(bots[bot_id],int(group_id),node_msg)
            status = True
            return status
        except Exception as e:
            pass
        
    for bot in bots:
        if await is_in_group(bots[bot],int(group_id)):
            await send_forward_msg(bots[bot],int(group_id),node_msg)
            status = True
            return status
    return status
        
async def send_private_forward_msg_by_bots_once(user_id:int,node_msg:list,bot_id: Optional[str] = None) -> bool:
    '''user_id：尝试发送到的好友qq号\n
    msg：尝试发送的node列表\n
    不在bot好友列表的qq不会尝试发送'''
    log()
    # bots = nonebot.get_adapter(Adapter).bots
    bots = get_bots()
    status = False
    
    if bot_id:
        try:
            await send_forward_msg(bots[bot_id],int(user_id),node_msg,msg_type="private")
            status = True
            return status
        except Exception as e:
            pass
    
    for bot in bots:
        if await is_in_friend(bots[bot],int(user_id)):
            await send_forward_msg(bots[bot],int(user_id),node_msg,msg_type="private")
            status = True
            return status
    return status            

async def send_group_msg_by_bots(group_id:int,msg:Message|MessageSegment|str) -> bool:
    '''group_id：尝试发送到的群号\n
    msg：尝试发送的消息\n
    不在bot群列表的群不会尝试发送'''
    log()
    # bots = nonebot.get_adapter(Adapter).bots
    bots = get_bots()
    status = False
    for bot in bots:
        if await is_in_group(bots[bot],int(group_id)):
            await bots[bot].send_group_msg(group_id=int(group_id),message=msg)
            status = True
    return status

async def send_group_msg_by_bots_once(group_id:int,msg:Message|MessageSegment|str,self_id: Optional[str] = None) -> bool:
    '''group_id：尝试发送到的群号\n
    msg：尝试发送的消息\n
    不在bot群列表的群不会尝试发送'''
    log()
    # bots = nonebot.get_adapter(Adapter).bots
    bots = get_bots()
    status = False
    if self_id:
        try:
            await bots[self_id].send_group_msg(group_id=int(group_id),message=msg)
            return True
        except Exception as e:
            logger.warning(f"传入的bot id似乎不正确{self_id}")
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
    log()
    # bots = nonebot.get_adapter(Adapter).bots
    bots = get_bots()
    status = False
    for bot in bots:
        if await is_in_friend(bots[bot],int(user_id)):
            await bots[bot].send_private_msg(user_id=int(user_id),message=msg)
            status = True
    return status

async def send_private_msg_by_bots_once(user_id:int,msg:Message|MessageSegment|str,self_id: Optional[str] = None) -> bool:
    '''user_id：尝试发送到的好友qq号\n
    msg：尝试发送的消息\n
    不在bot好友列表的qq不会尝试发送'''
    log()
    # bots = nonebot.get_adapter(Adapter).bots
    bots = get_bots()
    status = False
    if self_id:
        try:
            await bots[self_id].send_private_msg(user_id=int(user_id),message=msg)
            return True
        except Exception as e:
            logger.warning(f"传入的bot id似乎不正确{self_id}")
    for bot in bots:
        if await is_in_friend(bots[bot],int(user_id)):
            await bots[bot].send_private_msg(user_id=int(user_id),message=msg)
            status = True
            return status
    return status               
        
        
async def get_group_member_list(group_id: int) -> list:
    '''根据群号检索群成员列表'''
    # bots = nonebot.get_adapter(Adapter).bots
    bots = get_bots()
    log()
    group_member = []
    for bot in bots:
        if await is_in_group(bots[bot],int(group_id)):
            group_member = await bots[bot].call_api('get_group_member_list',**{"group_id":group_id})
    return group_member


async def send_text2md(text: str,bot_id: Optional[str] = None):
    '''转为拉格兰markdown消息发生'''
    md_text = {
             "type": "markdown",
             "data": {
               "content": '{"content":"' + repr(text)[1:-1].replace('\"','\\"').replace("\'","\\'") + '"}'
             }
           }
    
    md_node = MessageSegment.node_custom(user_id=int(bot_id),nickname="咩",content=[md_text])
    bot = current_bot.get()
    res_id = await bot.call_api("send_forward_msg", messages=[md_node])
    node = {
                "type": "node",
                "data": {
                    "name": "咩",
                    "uin":str(bot_id),
                    "content":MessageSegment.forward(res_id)
                }
            }
    
    res_id2 = await bot.call_api("send_forward_msg", messages=[node])
    node2 = {
                "type": "node",
                "data": {
                    "name": "咩",
                    "uin":str(bot_id),
                    "content":MessageSegment.forward(res_id2)
                }
            }
    
    res_id3 = await bot.call_api("send_forward_msg", messages=[node2])
    lmsg = {
            "type": "longmsg",
            "data": {
                "id": res_id3
            }
        }
    
    # md_node = MessageSegment.node_custom(user_id=10000,nickname="测试",content=[md_text])
    # md = MessageSegment.node_custom_lgr(md_node)
    # bot = current_bot.get()
    # res_id = await bot.call_api("send_forward_msg", messages=md)
    # lmsg = {
    #         "type": "longmsg",
    #         "data": {
    #             "id": res_id
    #         }
    #     }
    event = current_event.get()
    bots = get_bots()
    log()
    for botid in bots:
        if isinstance(event,GroupMessageEvent):
            if await is_in_group(bots[botid],int(event.group_id)):
            # await send_group_msg_by_bots_once(group_id=event.group_id,msg=MessageSegment.forward(res_id2),self_id=bot_id)
                await bots[botid].call_api("send_group_msg",group_id=event.group_id,message=[lmsg])
                return
        else:
            if await is_in_friend(bots[botid],int(event.user_id)):
            # await send_private_msg_by_bots_once(user_id=event.user_id,msg=MessageSegment.forward(res_id2),self_id=bot_id)
                await bots[botid].call_api("send_private_msg",user_id=event.user_id,message=[lmsg])
                return