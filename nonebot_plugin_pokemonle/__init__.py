from nonebot import on_message, require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from nonebot.adapters import Event
from nonebot.matcher import Matcher
from nonebot.rule import Rule
require("nonebot_plugin_alconna")
require("nonebot_plugin_uninfo")
require("nonebot_plugin_htmlrender")

from nonebot_plugin_uninfo import Uninfo
from nonebot_plugin_alconna import UniMessage, Image, on_alconna
from .config import Config

from .game import Pokemonle
from .render import render_result
__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-pokemonle",
    description="猜宝可梦",
    usage="""指令:
猜宝可梦 - 开始游戏
结束 - 结束游戏
直接输入宝可梦猜测""",
    homepage="https://github.com/Proito666/nonebot-plugin-pokemonle",
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna", "nonebot_plugin_uninfo"
    ),
    type="application",
    config=Config,
)
game = Pokemonle()

def is_playing() -> Rule:
    async def _checker(uninfo: Uninfo) -> bool:
        return bool(game.get_game(uninfo))
    return Rule(_checker)

start_cmd = on_alconna("猜宝可梦")
guess_matcher = on_message(rule=is_playing(), priority=15, block=False)

@start_cmd.handle()
async def handle_start(uninfo: Uninfo, matcher: Matcher):
    if game.get_game(uninfo):
        await matcher.finish("游戏已在进行中！")
    
    game.start_new_game(uninfo)
    await matcher.send(f"游戏开始！你有{game.max_attempts}次猜测机会，直接输入宝可梦名即可")

async def handle_end(uninfo: Uninfo):
    poke = game.get_game(uninfo)["poke"]
    ans = game.guess(uninfo, poke)
    game.end_game(uninfo)
    img = await render_result(ans)
    await UniMessage(Image(raw=img)).send()

@guess_matcher.handle()
async def handle_guess(uninfo: Uninfo, event: Event):
    guess_name = event.get_plaintext().strip()
    if guess_name in ("", "结束", "猜宝可梦"):
        if guess_name == "结束":
            await handle_end(uninfo)
        return
    # 检查游戏状态
    game_data = game.get_game(uninfo)
    if not game_data:
        return
    # 检查重复猜测
    if any(g == guess_name for g in game_data["guesses"]):
        await UniMessage.text(f"已经猜过【{guess_name}】了，请尝试其他宝可梦").send()
        return
        
    poke = game.getPokeByName(guess_name)
    if not poke:
        similar = game.find_similar(guess_name)
        if not similar:
            return
        err_msg = f"未找到宝可梦【{guess_name}】！\n尝试以下结果：" + "、".join(similar)
        await guess_matcher.finish(err_msg)

    ans = game.guess(uninfo, poke)
            
    if ans["answer"]:
        game.end_game(uninfo)
        img = await render_result(ans)
        await UniMessage([
            "猜对了！正确答案：",
            Image(raw=img)
        ]).send()
        return
    
    attempts_left = game.max_attempts - len(game_data["guesses"])
    # 检查尝试次数
    if attempts_left <= 0:
        poke = game.get_game(uninfo)["poke"]
        ans = game.guess(uninfo, poke)
        game.end_game(uninfo)
        img = await render_result(ans)
        await UniMessage([
            "尝试次数已用尽！正确答案：",
            Image(raw=img)
        ]).send()
        return
    
    img = await render_result(ans)
    await UniMessage(Image(raw=img)).send()
    