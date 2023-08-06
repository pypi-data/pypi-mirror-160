from json import JSONEncoder
from typing import List


class ScoreEntity:
    text: str
    start: int
    end: int
    label: str

    def __init__(self, text: str, start: int, end: int, label: str) -> None:
        self.text = text
        self.start = start
        self.end = end
        self.label = label

    def to_list(self) -> List:
        return [self.text, self.label, self.start, self.end]

    def __eq__(self, other):
        if not isinstance(other, ScoreEntity):
            return False
        return (
            self.text == other.text
            and self.start == other.start
            and self.end == other.end
            and self.label == other.label
        )

    def __hash__(self) -> int:
        return hash((self.text, self.start, self.end, self.label))


class ScoreEntityEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__


def score_entity_decoder(fields: dict) -> ScoreEntity:
    return ScoreEntity(**fields)
