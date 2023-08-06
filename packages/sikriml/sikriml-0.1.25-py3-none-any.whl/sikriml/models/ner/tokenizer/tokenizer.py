import re
from typing import List

from .abstracts import TokenizerBase
from .token_data import TokenData


class Tokenizer(TokenizerBase):
    def __call__(self, text: str) -> List[TokenData]:
        tokens = []
        token_specification = [
            # Integer or decimal number
            ("NUMBER", r"\d+([\.,]\d+)*"),
            # Url or email (catches numbers like 20.3 too)
            ("URL", r"(http(s?)://)?[\w@]+(?:\.[^\r\n\t\f\v \.,]+)+(/|\w)"),
            # Any number of spaces at the start of a string, is a token
            ("BEGIN_SPACE", r"^\s+"),
            # A single space after another token, not a token
            ("SPACE_AFTER", r"(?<!(\s))\s"),
            # Any number of spaces following SPACE_AFTER, is a token
            ("MULTISPACE", r"\s+"),
            # Word
            ("WORD", r"\w+"),
            # Punctuation
            ("PUNCT", r"\.{3}|[+\-*/,\.]"),
            # Any other character
            ("OTHER", r"."),
        ]
        token_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
        token_index = 0
        for match in re.finditer(token_regex, text, re.UNICODE):
            kind = match.lastgroup
            value = match.group()
            # don't save single space as a token
            if kind != "SPACE_AFTER":
                tokens.append(TokenData(token_index, value, match.start(), match.end()))
                token_index += 1
                continue
            # other spaces are tokens, but space_after attribute is False
            if len(tokens) >= 1 and kind != "BEGIN_SPACE" and kind != "MULTISPACE":
                # update space_after attribute for previous token if current token is a space
                tokens[-1].space_after = True
        return tokens
