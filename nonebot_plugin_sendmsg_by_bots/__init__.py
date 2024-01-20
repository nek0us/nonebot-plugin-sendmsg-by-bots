from nonebot.plugin import PluginMetadata
from .config import Config,__version__

__plugin_meta__ = PluginMetadata(
    name="多bot发送消息",
    description="让连接的每个bot发送消息，如无好友或群则跳过",
    usage="""
from nonebot_plugin_sendmsg_by_bots import tools
# 发送群消息：
await tools.send_group_msg_by_bots(group_id: int,node_msg: Message|MessageSegment|str)
# 发送群合并消息：
await tools.send_group_forward_msg_by_bots(group_id: int,node_msg: list)
# 发送私聊消息：
await tools.send_private_msg_by_bots(user_id: int,msg: Message|MessageSegment|str)
# 发送私聊合并消息：
await tools.send_private_forward_msg_by_bots(user_id: int,msg: list)

# group_id : 群号
# user_id : 好友qq号
# node_msg : 合并转发消息列表
# msg : 消息

# 发送成功会返回True，否则会返回False

# 从所有bot的群列表检索群信息
# 未检索到会返回 {"group_name":"未获取到群名","group_id":group_id}
group_info = await tools.get_all_group_info(group_id:int)
    """,
    type="library",
    config=Config,
    homepage="https://github.com/nek0us/nonebot-plugin-sendmsg-by-bots",
    supported_adapters={"~onebot.v11"},
    extra={
        "author":"nek0us",
        "version":__version__
    }
)