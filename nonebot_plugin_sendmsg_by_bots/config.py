from pydantic import BaseModel
import sys

if sys.version_info < (3, 10):
    from importlib_metadata import version
else:
    from importlib.metadata import version

try:
    __version__ = version("nonebot_plugin_sendmsg_by_bots")
except Exception:
    __version__ = None

class Config(BaseModel):
    plugin_enabled: bool = True
    
