from abc import ABC, abstractmethod


class ISerializable(ABC):
    @staticmethod
    @abstractmethod
    def from_dict(fields: dict) -> "ISerializable":
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass
