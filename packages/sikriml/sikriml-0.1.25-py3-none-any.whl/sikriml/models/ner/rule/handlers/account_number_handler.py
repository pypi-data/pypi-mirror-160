from typing import List, Match, Union

from sikriml.models.ner import ScoreLabel

from .personal_number_handler import PersonalNumberHandler


class AccountNumberHandler(PersonalNumberHandler):
    def __init__(self, check_per_nr: bool = False):
        self.check_per_nr = check_per_nr

    @property
    def regex(self) -> Union[str, List[str]]:
        return [
            r"(?:[^\d\w.]|^)(\d{11})(?:[^\d\w]|$)",
            r"(?:[^\d\w.]|^)(\d{4}[.|\s]\d{2}[.|\s]\d{5})(?:[^\d\w]|$)",
        ]

    def get_label(self, match: Match[str]) -> str:
        return ScoreLabel.ACC_NR

    def validator(self, match: Match[str]) -> bool:
        return super().validator(match) if self.check_per_nr else True
