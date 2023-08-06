import json

import yaml


def json_load(path: str, encoding="utf-8") -> dict | list[dict]:
    with open(path, "r", encoding=encoding) as f:
        return json.load(f)


def yaml_load(path: str, encoding="utf-8") -> dict | list[dict]:
    with open(path, "r", encoding=encoding) as f:
        return yaml.safe_load(f)
