from typing import List

from spacy.tokens import Doc
from spacy.vocab import Vocab

from .abstracts import TokenizerBase
from .token_data import TokenData


class SpacyTokenizer:
    def __init__(self, vocab: Vocab, tokenizer: TokenizerBase):
        self.vocab = vocab
        self.tokenizer = tokenizer

    def __call__(self, text: str) -> Doc:
        tokens: List[TokenData] = self.tokenizer(text)
        words = [token.text for token in tokens]
        spaces = [token.space_after for token in tokens]
        return Doc(self.vocab, words=words, spaces=spaces)
