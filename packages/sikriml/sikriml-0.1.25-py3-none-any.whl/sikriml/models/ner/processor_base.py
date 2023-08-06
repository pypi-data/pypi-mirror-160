from abc import ABC, abstractmethod
from string import punctuation
from typing import Any, Callable, List, Set

import pydash as py_
from intervaltree import Interval, IntervalTree
from sortedcontainers import SortedSet

from .score_entity import ScoreEntity


class ProcessorBase(ABC):
    @abstractmethod
    def process(self, text: str) -> Set[ScoreEntity]:
        pass


def process_text(text: str, processors: List[ProcessorBase]) -> List[ScoreEntity]:
    trimmed_text = text.rstrip(punctuation)

    def set_iteratee(result: SortedSet, current: ProcessorBase) -> SortedSet:
        return result.union(current.process(trimmed_text))

    def tree_iteratee(result: IntervalTree, current: ScoreEntity) -> IntervalTree:
        result.remove_overlap(current.start, current.end)
        result.addi(current.start, current.end, current)
        return result

    sort_key_func: Callable[[ScoreEntity], Any] = lambda x: x.end - x.start
    map_iteratee: Callable[[Interval], ScoreEntity] = lambda x: x.data

    entities = py_.reduce_(processors, set_iteratee, SortedSet(key=sort_key_func))
    tree = py_.reduce_(entities, tree_iteratee, IntervalTree())
    return py_.map_(tree.items(), map_iteratee)
