import re
from typing import List, Match, Optional, Set

import pydash as py_
from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.rule.services import DataLoaderBase, StemmerBase

from .abstracts.entity_handler import EntityHandler


class WordListHandler(EntityHandler):
    screen_list: List[str]

    def __init__(
        self, data_loader: DataLoaderBase, stemmer: StemmerBase
    ) -> None:
        self.stemmer = stemmer
        self.screen_list = [
            self.stemmer.stem(word) for word in data_loader.load_data()
        ]

    def get_label(self, match: Match[str]) -> str:
        return ScoreLabel.LIST

    def process(self, text: str) -> Set[ScoreEntity]:
        stemmed_text = self.stemmer.stem(text)
        matches = [
            re.search(word, stemmed_text, re.IGNORECASE)
            for word in self.screen_list
        ]
        return py_.reduce_(
            matches,
            lambda res, val: self.__extend_entities(res, val, text),
            set(),
        )

    def __extend_entities(
        self, result: Set[ScoreEntity], match: Optional[Match[str]], text: str
    ) -> Set[ScoreEntity]:
        if not match:
            return result

        matches = re.finditer(f"(\\w*{match.group()}\\w*)", text)
        return result.union(py_.reduce_(matches, self._append_entity, set()))
