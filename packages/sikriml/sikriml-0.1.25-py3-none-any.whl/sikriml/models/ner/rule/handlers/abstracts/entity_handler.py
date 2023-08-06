from abc import ABC, abstractmethod
from typing import Match, Set

from sikriml.models.ner import ScoreEntity


class EntityHandler(ABC):
    @property
    def match_group(self) -> int:
        return 0

    @abstractmethod
    def get_label(self, match: Match[str]) -> str:
        pass

    @abstractmethod
    def process(self, text: str) -> Set[ScoreEntity]:
        pass

    def _append_entity(
        self, result: Set[ScoreEntity], value: Match[str]
    ) -> Set[ScoreEntity]:
        result.add(
            ScoreEntity(
                value.group(self.match_group),
                value.start(self.match_group),
                value.end(self.match_group),
                self.get_label(value),
            )
        )
        return result
