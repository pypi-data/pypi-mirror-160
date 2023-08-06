from typing import Set

import pydash as py_
from flair.data import Sentence, Span
from flair.models import SequenceTagger
from sikriml.models.ner import ProcessorBase, ScoreEntity


class FlairProcessor(ProcessorBase):
    def __init__(self, flair_model: SequenceTagger):
        self.flair_model = flair_model
        super().__init__()

    flair_model: SequenceTagger

    def __apend_entity(self, result: Set[ScoreEntity], value: Span) -> Set[ScoreEntity]:
        result.add(
            ScoreEntity(value.text, value.start_position, value.end_position, value.tag)
        )
        return result

    def process(self, text: str) -> Set[ScoreEntity]:
        sentence = Sentence(text)
        self.flair_model.predict(sentence)
        return py_.reduce_(sentence.get_spans("ner"), self.__apend_entity, set())
