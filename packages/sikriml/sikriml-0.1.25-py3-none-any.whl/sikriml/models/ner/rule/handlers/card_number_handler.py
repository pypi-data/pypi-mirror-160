from typing import List, Match, Set

import pydash as py_
from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.rule.models import CardType

from .abstracts.entity_handler import EntityHandler

# catches 16 digit numbers starting with 51-55 or 2221–2720, optionally split with . or space at 4/4/4/4
mastercard_regex = (
    r"(?:[^\d\w.]|^)((?:5[1-5]\d{2}|(2\d{3}))(?:[.\s]?\d{4}){3})(?:[^\d\w]|$)"
)
# catches 13 and 16 digit numbers starting with 4, optionally split with . or space at 4/3/3/3 or 4/4/4/4 accordingly)
visa_regex = r"(?:[^\d\w.]|^)(4\d{3}(?:(?:[.\s]?\d{4}){3}|(?:[.\s]?\d{3}){3}))(?:[^\d\w]|$)"
# catches 15 digit numbers starting with 34 or 37, optionally split with . or space at 4/4/4/3 and 4/6/5
amex_regex = r"(?:[^\d\w.]|^)(3[4|7]\d{2}(?:(?:[.\s]?\d{4}){2}[.\s]?\d{3}|[.\s]?\d{6}[.\s]?\d{5}))(?:[^\d\w]|$)"
# catches 14 digit numbers starting with 300‑305, 309, 36 or 38‑39, optionally split with . or space at 4/4/4/2 or 4/6/4
diners_regex = r"(?:[^\d\w.]|^)(3(?:[689][.\s]?\d{2}|0[0-59]\d)(?:[.\s]?\d{6}[.\s]?\d{4}|(?:[.\s]?\d{4}){2}[.\s]?\d{2}))(?:[^\d\w]|$)"
# catches 16 digit numbers starting with 6011, 622126‑622925, 644‑649 or 65, optionally split with . or space at 4/4/4/4
discover_regex = r"(?:[^\d\w.]|^)(6(?:(?:011|5\d{2}|4[4-9]\d)(?:[.\s]?\d{4}){3}|22((?:[.\s]?\d){3})(?:[.\s]?\d{2})(?:[.\s]?\d{4}){2}))(?:[^\d\w]|$)"

DEFAULT_CARD_TYPES = [
    CardType(mastercard_regex, (2221, 2720)),
    CardType(visa_regex),
    CardType(amex_regex),
    CardType(diners_regex),
    CardType(discover_regex, (126, 925)),
]


class CardNumberHandler(EntityHandler):
    card_handlers: List[CardType]

    @property
    def match_group(self) -> int:
        return 1

    def get_label(self, match: Match[str]) -> str:
        return ScoreLabel.CARD_NR

    def __init__(self, card_handlers: List[CardType] = []):
        self.card_handlers = DEFAULT_CARD_TYPES + card_handlers

    def process(self, text: str) -> Set[ScoreEntity]:
        matches = []
        for card_handler in self.card_handlers:
            matches += card_handler.match(text)
        return py_.reduce_(matches, self._append_entity, set())
