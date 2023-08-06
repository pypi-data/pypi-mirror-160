from typing import List

from .abstracts.data_loader import DataLoaderBase


class FileLoader(DataLoaderBase):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self) -> List[str]:
        output: List[str] = []
        with open(self.file_path, "r", encoding="utf-8") as fh:
            for line in fh.read().split("\n"):
                output.append(line)
        return output
