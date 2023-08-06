import re
from typing import List, Match, Optional, Tuple


class CardType:
    regex: str
    number_range: Optional[Tuple[int, int]]

    def __init__(self, regex: str, number_range: Tuple[int, int] = None):
        self.regex = regex
        self.number_range = number_range

    def __get_matches(
        self, regex: str, text: str, number_range: Tuple[int, int] = None
    ) -> List[Match]:
        iterator = re.finditer(regex, text)
        if not number_range:
            return list(iterator)

        matches = []
        for match in iterator:
            if not match.group(1) or (
                len(match.groups()) >= 2
                and match.group(2)
                and int(match.group(2).replace(" ", "").replace(".", ""))
                not in range(number_range[0], number_range[1] + 1)
            ):
                continue
            else:
                matches.append(match)
        return matches

    def match(self, text) -> List[Match]:
        return self.__get_matches(self.regex, text, self.number_range)
