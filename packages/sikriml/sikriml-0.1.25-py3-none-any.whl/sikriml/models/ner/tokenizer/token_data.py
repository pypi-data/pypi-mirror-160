from dataclasses import dataclass


@dataclass
class TokenData:
    index: int
    text: str
    char_start: int
    char_end: int
    space_after: bool = False
