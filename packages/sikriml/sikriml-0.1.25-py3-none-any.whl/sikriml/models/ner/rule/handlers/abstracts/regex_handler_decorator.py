from typing import Optional, Set

import pydash as py_
from sikriml.models.ner import ScoreEntity

from .regex_handler import RegexHandler


class RegexHandlerDecorator(RegexHandler):
    def __init__(self, handler: Optional[RegexHandler]):
        self._handler = handler
        super().__init__()

    def process(self, text: str) -> Set[ScoreEntity]:
        regexes = self.regex if not self._handler else self._handler.regex
        matches = self._match_regexes(text, regexes)
        validated_matches = py_.filter_(matches, self.validator)
        return py_.reduce_(validated_matches, self._append_entity, set())
