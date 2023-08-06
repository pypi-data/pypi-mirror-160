from abc import ABC, abstractmethod


class StemmerBase(ABC):
    @abstractmethod
    def stem(self, str) -> str:
        pass
