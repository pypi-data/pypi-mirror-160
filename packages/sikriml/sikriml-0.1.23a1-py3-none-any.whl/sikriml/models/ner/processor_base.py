from abc import ABC, abstractmethod
from string import punctuation
from typing import List, Set

import pydash as py_

from .score_entity import ScoreEntity


class ProcessorBase(ABC):
    @abstractmethod
    def process(self, text: str) -> Set[ScoreEntity]:
        pass


def process_text(
    text: str, processors: List[ProcessorBase]
) -> Set[ScoreEntity]:
    trimmed_text = text.rstrip(punctuation)
    return py_.reduce_(
        processors,
        lambda total, x: total.union(x.process(trimmed_text)),
        set(),
    )
