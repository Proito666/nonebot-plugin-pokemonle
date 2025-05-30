<div align="center">

# nonebot-plugin-pokemonle

_✨ <猜宝可梦> ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Proito666/nonebot-plugin-pokemonle" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_pokemonle">
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/nonebot_plugin_pokemonle">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
</div>

nonebot插件版的猜宝可梦，修改自[pokemonle](https://github.com/QuantAskk/pokemonle/tree/main)

## 💿 安装
<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-pokemonle

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-pokemonle
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-pokemonle
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-pokemonle
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-pokemonle
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_pokemonle"]

</details>

## ⚙️ 配置

在 nonebot2 项目的 env 文件中添加配置

| 配置项 | 必填 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| pokemonle_max_attempts | 否 | int | 10 | 最大尝试次数 |
| pokemonle_gens | 否 | list | [] | 世代选择，例如：["第一世代", "第三世代", "第五世代"]，空代表都选 |
| pokemonle_cheat | 否 | bool | False | 是否开启恶作剧 |

## 🎉 使用
猜宝可梦: 开始游戏

直接输入怪物名称进行猜测

结束：结束游戏

## 📖 说明

### 游戏目标
通过输入宝可梦名称进行猜测，找出目标宝可梦。每次猜测后，你将获得输入宝可梦的相关信息，帮助你逐步接近答案。

### 提示颜色说明

<span style="color:#67c23a;background-color:#f0f9eb;border-color:#e1f3d8;padding: 2px 5px;border-radius: 4px;">绿色高亮</span> 表示该信息与目标宝可梦完全相同。  

<span style="color:#e6a23c;background-color:#fdf6ec;border-color:#faecd8;padding: 2px 5px;border-radius: 4px;">黄色高亮</span>  表示该信息与目标宝可梦接近但不完全相同。

### 黄色高亮的触发条件

**种族值总和**：`与目标宝可梦的差值 ≤ 50`  
**速度**：`与目标宝可梦的差值 ≤ 10`  
**世代**：`与目标世代相邻（差值 ≤ 1）`  
**进化方式**：`不完全相同但属于相似进化方式（例如使用物品、特定地点、等级、亲密度等）`  
**形态标签**：`两只宝可梦都有地区形态，特殊形态所属地区不同`


### 上下箭头的作用

在种族值总和、速度、世代等数值类信息中，箭头提示你猜测的方向是否正确：

↑：表示你输入的宝可梦的该数值低于目标宝可梦，建议下次猜测选择数值更高的宝可梦。

↓：表示你输入的宝可梦的该数值高于目标宝可梦，建议下次猜测选择数值更低的宝可梦。