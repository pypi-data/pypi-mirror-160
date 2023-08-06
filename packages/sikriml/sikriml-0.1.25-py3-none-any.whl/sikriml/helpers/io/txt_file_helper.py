from typing import List


class TxtFileHelper:
    @staticmethod
    def write(path: str, data: List[object]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            [f.write(str(item)) for item in data]
