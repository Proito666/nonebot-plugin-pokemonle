import random
import difflib
from pypinyin import lazy_pinyin
from typing import Dict, List, Optional, Tuple
from nonebot_plugin_uninfo import Uninfo
from .config import plugin_config
from .utils.dataUtils import *
from .utils.pokeUtils import *

class Pokemonle:
    def __init__(self):
        self.games: Dict[str, Dict] = {}
        self.max_attempts = plugin_config.pokemonle_max_attempts
        self.pokeList = self._load_and_filter_poke()
        self.nameList = [m["name"] for m in self.pokeList]
        self.pinyin_name = [''.join(lazy_pinyin(name)) for name in self.nameList]  # 预加载宝可梦名称拼音列表

    def _load_and_filter_poke(self):
        pokeList = FileGetter('pokemon_full_list')
        newPokeList = []
        las = ""
        for x in pokeList:
            if (x["index"] != las):
                newPokeList.append(x)
            las = x["index"]
        if not plugin_config.pokemonle_gens:
            return newPokeList    
        return [p for p in newPokeList if p.get('generation') in plugin_config.pokemonle_gens]

    def get_session_id(self, uninfo) -> str:
        return f"{uninfo.scope}_{uninfo.self_id}_{uninfo.scene_path}"

    def get_game(self, uninfo: Uninfo) -> Optional[Dict]:
        return self.games.get(self.get_session_id(uninfo))

    def start_new_game(self, uninfo: Uninfo) -> Dict:
        session_id = self.get_session_id(uninfo)
        self.games[session_id] = random.randrange(len(self.pokeList))
        self.games[session_id] = {
            "poke": random.randrange(len(self.pokeList)),
            "guesses": []
        }
        return self.games[session_id]

    def getPokeByName(self, name: str) -> int:
        return next((i for i, x in enumerate(self.pokeList) if x["name"] == name), None)

    def guess(self, uninfo: Uninfo, guessed: int) -> Tuple[bool, Optional[Dict], Dict]:
        game = self.get_game(uninfo)

        game["guesses"].append(self.nameList[guessed])
        current = game["poke"]

        # 检查尝试次数
        attempts_left = self.max_attempts - len(game["guesses"])
        if attempts_left <= 0:
            guessed = current
        
        ans = {"name": self.pokeList[guessed]["name"], "index": int(self.pokeList[guessed]["index"])}
        ans["answer"] = self.pokeList[guessed]["name"] == self.pokeList[current]["name"]

        currentPath = self.pokeList[current]["index"] + '-' + self.pokeList[current]["name"]
        guessedPath = self.pokeList[guessed]["index"] + '-' + self.pokeList[guessed]["name"]
        currentInfo = PokeGetter(currentPath)
        guessedInfo = PokeGetter(guessedPath)

        # 属性检查
        types = []
        currentType = TypeGet(currentInfo)
        guessedType = TypeGet(guessedInfo)

        s1 = (currentType[0] == guessedType[0]) + (currentType[1] == guessedType[1])
        s2 = (currentType[0] == guessedType[1]) + (currentType[1] == guessedType[0])
        if (s2 > s1):
            currentType[0], currentType[1] = currentType[1], currentType[0]

        for i in range(0, 2):
            types.append({"key": guessedType[i], "value": currentType[i] == guessedType[i]})
        ans["type"] = types

        #种族值检查
        currentPow = PowerSumGet(currentInfo)
        guessedPow = PowerSumGet(guessedInfo)
        if (guessedPow == currentPow):
            ans["pow"] = {"key": guessedPow, "value": "equiv"}
        elif (guessedPow > currentPow):
            ans["pow"] = {"key": guessedPow, "value": "low"}
        else:
            ans["pow"] = {"key": guessedPow, "value": "high"}
        if (currentPow == guessedPow):
            ans["pow"]["dis"] = "equiv"
        if (abs(currentPow - guessedPow) <= 10):
            ans["pow"]["dis"] = "near"
        else:
            ans["pow"]["dis"] = "far"

        # 速度检查
        currentSpd = int(currentInfo["stats"][0]["data"]["speed"])
        guessedSpd = int(guessedInfo["stats"][0]["data"]["speed"])
        if (guessedSpd == currentSpd):
            ans["speed"] = {"key": guessedSpd, "value": "equiv"}
        elif (guessedSpd > currentSpd):
            ans["speed"] = {"key": guessedSpd, "value": "low"}
        else:
            ans["speed"] = {"key": guessedSpd, "value": "high"}         
        if (currentSpd == guessedSpd):
            ans["speed"]["dis"] = "equiv"
        if (abs(currentSpd - guessedSpd) <= 10):
            ans["speed"]["dis"] = "near"
        else:
            ans["speed"]["dis"] = "far"

        # 攻防检查
        currentAt, currentDF = APTypeGet(currentInfo)
        guessedAt, guessedDF = APTypeGet(guessedInfo)
        ans["attack"] = {"key": guessedAt, "value": currentAt == guessedAt}
        ans["defense"] = {"key": guessedDF, "value": currentDF == guessedDF}

        # 蛋组/捕获率检查
        currentEggGroup = EggGroupGet(currentInfo)
        guessedEggGroup = EggGroupGet(guessedInfo)
        abt = []
        for x in guessedEggGroup:
            flag = False
            for y in currentEggGroup:
                if (x == y):
                    flag = True
                    break
            abt.append({"key": x, "value": flag})
        ans["egg"] = abt

        currentCatRate = int(currentInfo["forms"][0]["catch_rate"]["number"])
        guessedCatRate = int(guessedInfo["forms"][0]["catch_rate"]["number"])
        if ( guessedCatRate == currentCatRate):
            ans["catrate"] = {"key":  guessedCatRate, "value": "equiv"}
        elif ( guessedCatRate > currentCatRate):
            ans["catrate"] = {"key":  guessedCatRate, "value": "low"}
        else:
            ans["catrate"] = {"key":  guessedCatRate, "value": "high"}

        # 外形检查
        currentShape = currentInfo["forms"][0]["shape"]
        guessedShape = guessedInfo["forms"][0]["shape"]
        currentCol = currentInfo["forms"][0]["color"]
        guessedCol = guessedInfo["forms"][0]["color"]
        ans["shape"] = {"key": guessedShape, "value": currentShape == guessedShape}
        ans["col"] = {"key": guessedCol, "value": currentCol == guessedCol}

        # 世代检查
        currentGen = Gens.index(self.pokeList[current]["generation"])
        guessedGen = Gens.index(self.pokeList[guessed]["generation"])
        if (currentGen == guessedGen):
            ans["gen"] = {"key": self.pokeList[guessed]["generation"], "value": "equiv"}
        elif (currentGen < guessedGen):
            ans["gen"] = {"key": self.pokeList[guessed]["generation"], "value": "low"}
        else:
            ans["gen"] = {"key": self.pokeList[guessed]["generation"], "value": "high"}
        if (currentGen == guessedGen):
            ans["gen"]["dis"] = "equiv"
        if (abs(currentGen - guessedGen) <= 1):
            ans["gen"]["dis"] = "near"
        else:
            ans["gen"]["dis"] = "far"
        
        # 特性信息
        currentAbility = AbilityGet(currentInfo)
        guessedAbility = AbilityGet(guessedInfo)
        abt = []
        for x in guessedAbility:
            flag = False
            for y in currentAbility:
                if (x == y):
                    flag = True
                    break
            abt.append({"key": x, "value": flag})
        ans["ability"] = abt

        # 进化信息
        currentStage, currentEVO = EvolutionGet(currentInfo)
        guessedStage, guessedEVO = EvolutionGet(guessedInfo)
        ans["stage"] = {"key": guessedStage, "value": currentStage == guessedStage}

        if (currentEVO == guessedEVO):
            ans["evo"] = {"key": guessedEVO, "value": "equiv"}
        elif (currentEVO == None or guessedEVO == None):
            ans["evo"] = {"key": guessedEVO, "value": "far"}
        elif ("使用" in currentEVO and "使用" in guessedEVO):
            ans["evo"] = {"key": guessedEVO, "value": "near"}
        elif ("来到" in currentEVO and "来到" in guessedEVO):
            ans["evo"] = {"key": guessedEVO, "value": "near"}
        elif (checkLevelEvo(currentEVO) and checkLevelEvo(guessedEVO)):
            ans["evo"] = {"key": guessedEVO, "value": "near"}
        elif ("亲密度" in currentEVO and "亲密度" in guessedEVO):
            ans["evo"] = {"key": guessedEVO, "value": "near"}
        else:
            ans["evo"] = {"key": guessedEVO, "value": "far"}      

        currentLabel = getLabel(currentInfo)
        guessedLabel = getLabel(guessedInfo)
        Label = []
        # 检查两只宝可梦是否都有形态变化
        currentFormLabels = [l for l in currentLabel if "形态" in l or any(region in l for region in ["阿罗拉", "伽勒尔", "洗翠", "帕底亚"])]
        guessedFormLabels = [l for l in guessedLabel if "形态" in l or any(region in l for region in ["阿罗拉", "伽勒尔", "洗翠", "帕底亚"])]
        
        currentHasForm = len(currentFormLabels) > 0
        guessedHasForm = len(guessedFormLabels) > 0
        
        for x in guessedLabel:
            exact_match = x in currentLabel
            
            # 检查是否是形态标签
            is_form_label = "形态" in x or any(region in x for region in ["阿罗拉", "伽勒尔", "洗翠", "帕底亚"])
            
            if exact_match:
                # 完全匹配，前端会渲染为绿色
                Label.append({"key": x, "value": True})
            else:
                # 不完全匹配，检查是否是形态标签且双方都有形态变化
                if is_form_label and currentHasForm and guessedHasForm:
                    Label.append({"key": x, "value": False, "col": "warning"})
                else:
                    # 其他情况
                    Label.append({"key": x, "value": False})
        
        ans["label"] = Label

        ans["attempts_left"] = self.max_attempts - len(game["guesses"])

        if not ans["answer"] and plugin_config.pokemonle_cheat:
            ans = self.cheat(ans)
        return ans

    def cheat(self, ans):
        # 随机选择一行
        random_row = random.choice(Rows)
        # 选择一个覆盖图标[耿鬼，勾魂眼，风妖精，胡帕]
        random_value = random.choice([94, 302, 547, 720])
        cheatIcon = f"<img src='https://pokeimg.oss-cn-beijing.aliyuncs.com/pokemon_images/{random_value}.webp' class='cheat-icon'>"
        if len(random_row) == 1:
            # 单字段行（如种族值、速度）
            field = random_row[0]
            if isinstance(ans[field], list):
                # 多值字段（如属性、特性）：替换整个列表为一个数字
                ans[field] = [{"key": cheatIcon, "value": None}]
            else:
                # 单值字段（如种族值）：直接替换 key
                ans[field] = {"key": cheatIcon, "value": None}
        else:
            # 多字段行（如攻防、外形）：合并成一个数字，清空其他字段
            for field in random_row:
                ans[field] = {"key": "", "value": None}  # 清空其他字段
            ans[random_row[0]] = {"key": cheatIcon, "value": None}  # 第一个字段显示数字
        return ans

    def find_similar(self, name: str, n: int = 3) -> List[str]:
        # 使用difflib找到相似的宝可梦名称
        difflib_matches = difflib.get_close_matches(
            name,
            self.nameList,
            n=n,
            cutoff=0.6  # 相似度阈值（0-1之间）
        )
        # 通过拼音精确匹配读音一样的宝可梦名称
        name_pinyin = ''.join(lazy_pinyin(name))  # 转换输入名称为拼音
        pinyin_matches = [self.nameList[i] for i, pinyin in enumerate(self.pinyin_name) if
                          pinyin == name_pinyin]

        all_matches = list(dict.fromkeys(pinyin_matches + difflib_matches))
        return all_matches

    def _compare_attributes(self, guess_attr: str, target_attr: str) -> Dict:
        guess_attrs = guess_attr.split("/") if guess_attr else []
        target_attrs = target_attr.split("/") if target_attr else []
        common = set(guess_attrs) & set(target_attrs)
        return {
            "guess": guess_attr,
            "target": target_attr,
            "common": list(common) if common else []
        }

    def end_game(self, uninfo: Uninfo):
        try:
            self.games.pop(self.get_session_id(uninfo))
        except (AttributeError, KeyError):
            pass
