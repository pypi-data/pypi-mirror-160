import unittest
from typing import List

from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.rule.handlers import WordListHandler
from sikriml.models.ner.rule.services import DataLoaderBase, NltkStemmer


class DummyLoader(DataLoaderBase):
    def load_data(self) -> List[str]:
        return [
            "hemmelig",
            "skade",
            "fullmakt",
            "sensitive opplysninger",
            "sykdom",
            "dom",
        ]


dummy_loader = DummyLoader()
stemmer = NltkStemmer()


class TestWordListHandler(unittest.TestCase):
    def test_tags_right_word(self):

        list_handler = WordListHandler(dummy_loader, stemmer)
        text = "dette er den hemmeligste texten"
        target = set([ScoreEntity("hemmeligste", 13, 24, ScoreLabel.LIST)])
        # Act
        output = list_handler.process(text)
        # Assert
        self.assertSetEqual(output, target)

    def test_space_string_starts_with_whitespace(self):
        list_handler = WordListHandler(dummy_loader, stemmer)
        text = " dette er den hemmeligste texten"
        target = set([ScoreEntity("hemmeligste", 14, 25, ScoreLabel.LIST)])
        # Act)
        output = list_handler.process(text)
        # Assert
        self.assertSetEqual(output, target)

    def test_string_with_punctuation(self):
        list_handler = WordListHandler(dummy_loader, stemmer)
        text = ".dette er den hemmeligste texten"
        target = set([ScoreEntity("hemmeligste", 14, 25, ScoreLabel.LIST)])
        # Act
        output = list_handler.process(text)
        # Assert
        self.assertSetEqual(output, target)

    def test_string_repating_words(self):
        list_handler = WordListHandler(dummy_loader, stemmer)
        text = "Av hemmlige texter som er hemmlige er dette er den hemmeligste texten"
        target = set(
            [
                ScoreEntity("hemmlige", 3, 11, ScoreLabel.LIST),
                ScoreEntity("hemmlige", 26, 34, ScoreLabel.LIST),
                ScoreEntity("hemmeligste", 51, 62, ScoreLabel.LIST),
            ]
        )
        # Act
        output = list_handler.process(text)
        # Assert
        self.assertSetEqual(output, target)

    def test_double_tagging(self):
        list_handler = WordListHandler(dummy_loader, stemmer)
        text = "sykdom"
        target = set([ScoreEntity("sykdom", 0, 6, ScoreLabel.LIST)])
        # Act
        output = list_handler.process(text)
        # Assert
        self.assertSetEqual(output, target)


if __name__ == "__main__":
    unittest.main(verbosity=2)
