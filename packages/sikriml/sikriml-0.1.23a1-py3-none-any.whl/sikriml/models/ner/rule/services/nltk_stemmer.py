from nltk.stem import SnowballStemmer

from .abstracts.stemmer import StemmerBase


class NltkStemmer(StemmerBase):
    def __init__(self) -> None:
        self.stemmer = SnowballStemmer(language="norwegian")

    def stem(self, text: str):
        return " ".join([self.stemmer.stem(word) for word in text.split(" ")])
