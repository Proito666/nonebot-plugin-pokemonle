import json
from pathlib import Path

root = Path(__file__).parent.parent


def FileGetter(path):
    with open(root / 'resources' / 'data' / f'{path}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def LabelGetter(path):
    with open(root / 'resources' / 'data' / 'label' / f'{path}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def PokeGetter(path):
    with open(root / 'resources' / 'data' / 'pokemon' / f'{path}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def SrcPath():
    return root