from dataclasses import asdict, astuple
from pprint import pprint

from dathas.util import json_load, yaml_load


class Dathas:

    def __init__(self) -> None:
        pass

    @property
    def dict(self) -> dict:
        return asdict(self)

    @property
    def tuple(self) -> tuple:
        return astuple(self)

    def print(self):
        pprint(self.dict)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    @classmethod
    def from_json(cls, path: str):
        return cls.from_dict(json_load(path))

    @classmethod
    def from_yaml(cls, path: str):
        return cls.from_dict(yaml_load(path))
