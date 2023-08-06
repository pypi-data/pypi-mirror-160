from typing import List, Match, Union

from sikriml.models.ner import ScoreLabel

from .abstracts.regex_handler import RegexHandler


class NumberHandler(RegexHandler):
    @property
    def regex(self) -> Union[str, List[str]]:
        return r"\d+([.|,]\d+|-(tallet|årene|åra))?"

    def get_label(self, match: Match[str]) -> str:
        return ScoreLabel.NUMB
