from typing import List

import yaml
from sikriml.helpers.io.abstracts import ISerializable


class YamlFileHelper:
    @staticmethod
    def read(path: str, model: ISerializable) -> List[ISerializable]:
        with open(path, "r", encoding="utf-8") as f:
            return [model.from_dict(fields) for fields in yaml.safe_load_all(f)]

    @staticmethod
    def write(path: str, data: List[ISerializable]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump_all([item.to_dict() for item in data], f)
