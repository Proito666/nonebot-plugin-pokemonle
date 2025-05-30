from nonebot import get_plugin_config
from pydantic import BaseModel

class Config(BaseModel):
    #猜宝可梦最大尝试次数
    pokemonle_max_attempts: int = 10
    #世代选择，空代表都选
    pokemonle_gens: list = []
    #是否开启恶作剧
    pokemonle_cheat: bool = False

plugin_config = get_plugin_config(Config)