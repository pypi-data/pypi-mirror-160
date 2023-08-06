from abc import ABC, abstractmethod
from typing import List

from ..token_data import TokenData


class TokenizerBase(ABC):
    @abstractmethod
    def __call__(self, text: str) -> List[TokenData]:
        pass
