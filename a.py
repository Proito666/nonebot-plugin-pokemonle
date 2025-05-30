import json
import os

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

def check_json_files(directory):
    problem_files = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    stage, text = EvolutionGet(data)
                    if stage is None:  # 表示出现了问题
                        problem_files.append(filename)
                        
            except json.JSONDecodeError:
                print(f"JSON解析错误: {filename}")
                problem_files.append(filename)
            except Exception as e:
                print(f"处理{filename}时出错: {e}")
                problem_files.append(filename)
    
    print("\n有问题的文件列表:")
    for file in problem_files:
        print(file)
    
    return problem_files

# 使用示例
directory_path = "D:\\devtools\\workSpace\\nonebot-plugin-pokemonle\\nonebot_plugin_pokemonle\\resources\\data\\pokemon"
problem_files = check_json_files(directory_path)