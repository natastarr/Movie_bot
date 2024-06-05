import json
import typing as tp


def load_keys() -> tp.Dict[str, str]:
    with open('./src/keys.json') as file:
        data = json.load(file)
        return data


keys = load_keys()
