<div align="center">x
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-sendmsg-by-bots

_✨ NoneBot 多bot发送消息 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/nek0us/nonebot-plugin-sendmsg-by-bots.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-sendmsg-by-bots">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-sendmsg-by-bots.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>

## 📖 介绍

让连接的每个bot发送消息，如无好友或群则跳过

## 💿 安装

<details open>
<summary>使用 pip 安装</summary>

    pip install nonebot-plugin-sendmsg-by-bots
</details>
<details open>
<summary>使用 conda 安装</summary>

    conda install nonebot-plugin-sendmsg-by-bots
</details>



## 🎉 使用
### 指令表

```bash
from nonebot_plugin_sendmsg_by_bots import tools
# 发送群消息（能发都发）：
await tools.send_group_msg_by_bots(group_id: int,node_msg: Message|MessageSegment|str)
# 发送群消息（只发成功一次）：
await tools.send_group_msg_by_bots_once(group_id: int,node_msg: Message|MessageSegment|str)
# 发送群合并消息（能发都发）：
await tools.send_group_forward_msg_by_bots(group_id: int,node_msg: list)
# 发送群合并消息（一次收手）：
await tools.send_group_forward_msg_by_bots_once(group_id: int,node_msg: list)
# 发送私聊消息（能发都发）：
await tools.send_private_msg_by_bots(user_id: int,msg: Message|MessageSegment|str)
# 发送私聊消息（只发成功一次收手）：
await tools.send_private_msg_by_bots_once(user_id: int,msg: Message|MessageSegment|str)
# 发送私聊合并消息（能发都发）：
await tools.send_private_forward_msg_by_bots(user_id: int,msg: list)
# 发送私聊合并消息（一次收手）：
await tools.send_private_forward_msg_by_bots_once(user_id: int,msg: list)
# 被动回复消息，以拉格兰md形式发送
await tools.send_text2md(text: str):

# group_id : 群号
# user_id : 好友qq号
# node_msg : 合并转发消息列表
# msg : 消息

# 发送成功会返回True，否则会返回False

# 从所有bot的群列表检索群信息
# 未检索到会返回 {"group_name":"未获取到群名","group_id":group_id}
group_info = await tools.get_all_group_info(group_id:int)
# 从所有bot的群列表检索群成员列表
member_list = await get_group_member_list(group_id: int)

```
