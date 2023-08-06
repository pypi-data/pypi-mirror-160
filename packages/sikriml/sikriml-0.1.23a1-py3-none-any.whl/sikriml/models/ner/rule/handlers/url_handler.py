from typing import List, Match, Union

from sikriml.models.ner import ScoreLabel

from .abstracts.regex_handler import RegexHandler


class UrlHandler(RegexHandler):
    @property
    def match_group(self) -> int:
        return 1

    @property
    def regex(self) -> Union[str, List[str]]:
        return r"(?:\s|^|,|\.)((https?://)?(www\.)?((?!www)\w{2,})(\.\w{2,})+(/((?!,|\.\s|\s).)*)*)(?=\s|$|,|\.)"

    def get_label(self, match: Match[str]) -> str:
        return ScoreLabel.URL
