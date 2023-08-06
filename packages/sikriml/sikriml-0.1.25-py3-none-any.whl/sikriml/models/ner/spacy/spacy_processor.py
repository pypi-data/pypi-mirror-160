from typing import Set

import pydash as py_
from sikriml.models.ner import ProcessorBase, ScoreEntity
from spacy.language import Language
from spacy.tokens import Span


class SpacyProcessor(ProcessorBase):
    def __init__(self, spacy_model: Language):
        self.spacy_model = spacy_model
        super().__init__()

    spacy_model: Language

    def __append_span(self, result: Set[ScoreEntity], value: Span) -> Set[ScoreEntity]:
        result.add(
            ScoreEntity(value.text, value.start_char, value.end_char, value.label_)
        )
        return result

    def process(self, text: str) -> Set[ScoreEntity]:
        if not text:
            return set([])

        doc = self.spacy_model(text)
        return py_.reduce_(doc.ents, self.__append_span, set())
