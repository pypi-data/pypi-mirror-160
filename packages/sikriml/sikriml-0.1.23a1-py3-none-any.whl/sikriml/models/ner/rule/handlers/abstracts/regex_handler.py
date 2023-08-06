import re
from abc import abstractproperty
from typing import List, Match, Set, Union

import pydash as py_
from sikriml.models.ner import ScoreEntity

from .entity_handler import EntityHandler


class RegexHandler(EntityHandler):
    @abstractproperty
    def regex(self) -> Union[str, List[str]]:
        pass

    def validator(self, match: Match[str]) -> bool:
        return True

    def process(self, text: str) -> Set[ScoreEntity]:
        matches = self._match_regexes(text, self.regex)
        validated_matches = py_.filter_(matches, self.validator)
        return py_.reduce_(validated_matches, self._append_entity, set())

    def _match_regexes(
        self, text: str, regex: Union[str, List[str]]
    ) -> List[Match[str]]:
        regexes = [regex] if isinstance(regex, str) else regex
        return py_.reduce_(
            regexes, lambda res, reg: self.__apply_regex(text, reg, res), []
        )

    def __apply_regex(
        self, text: str, regex: str, result: List[Match[str]]
    ) -> List[Match[str]]:
        result.extend(re.finditer(regex, text, re.IGNORECASE))
        return result
