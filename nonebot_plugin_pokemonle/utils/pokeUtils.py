import random
import re

from .dataUtils import *

Types = ["一般", "火", "水", "电", "草", "冰", "格斗", "毒", "地面", "飞行", "超能力", "虫", "岩石", "幽灵", "龙", "恶",
         "钢", "妖精", "无"]
Gens = ["第一世代", "第二世代", "第三世代", "第四世代", "第五世代", "第六世代", "第七世代", "第八世代", "第九世代"]
Labels = [
    {
        "id": "Beginer",
        "name": "最初的伙伴",
        "weight": 30
    },
    {
        "id": "Dream",
        "name": "幻之宝可梦",
        "weight": 20
    },
    {
        "id": "Legend",
        "name": "传说的宝可梦",
        "weight": 30
    },
    {
        "id": "MaybeGod",
        "name": "大器晚成的宝可梦",
        "weight": 20
    },
    {
        "id": "Mouse",
        "name": "电气鼠宝可梦",
        "weight": 10
    },
    {
        "id": "Paradox",
        "name": "悖谬宝可梦",
        "weight": 10
    },
    {
        "id": "Stone",
        "name": "化石宝可梦",
        "weight": 5
    },
    {
        "id": "Yibu",
        "name": "伊布",
        "weight": 10
    },
    {
        "id": "ZMonster",
        "name": "究极异兽",
        "weight": 5
    },
    {
        "id": "Zskill",
        "name": "拥有专属Z招式",
        "weight": 5
    },
    {
        "id": "Mega",
        "name": "有Mega进化",
        "weight": 20
    },
    {
        "id": "Gmax",
        "name": "有超极巨化",
        "weight": 15
    }
]

Rows = [
    ["type"],          # 属性
    ["pow"],           # 种族值
    ["speed"],         # 速度
    ["attack", "defense"],  # 攻防
    ["gen"],           # 世代
    ["ability"],       # 特性
    ["stage", "evo"],  # 进化
    ["shape", "col"],  # 外形
    ["egg"],           # 蛋组
    ["catrate"],       # 捕获率
    ["label"],         # 其他
]

def TypeGet(Info):
    type = Info["forms"][0]["types"]
    t1 = type[0]
    if (len(type) == 1):
        t2 = "无"
    else:
        t2 = type[1]
    return [t1, t2]


def PowerSumGet(Info):
    state = Info["stats"][0]["data"]
    sum = 0
    for x in state.values():
        sum += int(x)
    return sum


def AbilityGet(Info):
    ability = Info["forms"][0]["ability"]
    ans = []
    for x in ability:
        ans.append(x["name"])
    return ans


def EvolutionGet(Info):
    EvolutionChain = Info["evolution_chains"][0]
    own = {}
    i = 0
    for Evolution in EvolutionChain:
        if (Evolution["name"] == Info["name"]):
            own = Evolution
            break
    if (own["stage"] == "不进化" or own["stage"] == "未进化" or own["stage"] == "幼年"):
        own["stage"] = "未进化/不进化"
    return own["stage"], own["text"]


def APTypeGet(Info):
    At = int(Info["stats"][0]["data"]["attack"])
    Pt = int(Info["stats"][0]["data"]["sp_attack"])
    Ad = int(Info["stats"][0]["data"]["defense"])
    Pd = int(Info["stats"][0]["data"]["sp_defense"])
    As = ""
    Ds = ""
    if (At == Pt):
        As = "物攻=特攻"
    elif (At > Pt):
        As = "物攻>特攻"
    elif (At < Pt):
        As = "物攻<特攻"

    if (Ad == Pd):
        Ds = "物防=特防"
    elif (Ad > Pd):
        Ds = "物防>特防"
    elif (Ad < Pd):
        Ds = "物防<特防"

    return As, Ds


def EggGroupGet(Info):
    return Info["forms"][0]["egg_groups"]


def checkLevelEvo(s):
    pattern = r'^等级.+以上.*$'
    return bool(re.fullmatch(pattern, s))


def isLabel(Info, Label):
    for x in Info["forms"]:
        if (Label in x["name"]):
            return True
    return False


def checkLabel(Info, Label):
    Group = LabelGetter(Label)
    return (Info["name"] in Group)


def getLabel(Info):
    Label = []
    if (isLabel(Info, "阿罗拉")):
        Label.append("有阿罗拉地区形态")
    if (isLabel(Info, "洗翠")):
        Label.append("有洗翠地区形态")
    if (isLabel(Info, "帕底亚")):
        Label.append("有帕底亚地区形态")
    if (isLabel(Info, "伽勒尔")):
        Label.append("有伽勒尔地区形态")
    for x in Labels:
        if (checkLabel(Info, x["id"])):
            Label.append(x["name"])
    return Label
