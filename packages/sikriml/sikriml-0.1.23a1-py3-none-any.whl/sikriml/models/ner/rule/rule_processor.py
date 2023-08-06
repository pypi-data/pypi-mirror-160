from typing import List, Set

import pydash as py_
from sikriml.models.ner import ProcessorBase, ScoreEntity
from sikriml.models.ner.rule.handlers import EntityHandler


class RuleProcessor(ProcessorBase):
    def __init__(self, rules: List[EntityHandler] = None):
        self.rules = rules or []
        super().__init__()

    def process(self, text: str) -> Set[ScoreEntity]:
        return py_.reduce_(
            self.rules, lambda total, x: total.union(x.process(text)), set()
        )
