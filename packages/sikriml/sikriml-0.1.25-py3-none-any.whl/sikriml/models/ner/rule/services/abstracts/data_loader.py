from abc import ABC, abstractmethod
from typing import List


class DataLoaderBase(ABC):
    @abstractmethod
    def load_data(self) -> List[str]:
        pass
