import json
from typing import List

from sikriml.helpers.io.abstracts import ISerializable


class JsonFileHelper:
    @staticmethod
    def read(path: str, model: ISerializable) -> List[ISerializable]:
        with open(path, "r", encoding="utf-8") as file:
            return [model.from_dict(json.loads(line)) for line in file]

    @staticmethod
    def write(path: str, data: List[ISerializable]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            [f.write(json.dumps(item.to_dict())) for item in data]
