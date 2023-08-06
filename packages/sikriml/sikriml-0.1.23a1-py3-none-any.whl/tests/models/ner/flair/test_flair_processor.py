import unittest
from unittest.mock import Mock, patch

from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.flair import FlairProcessor

from .helpers.flair_models import Span


class FlairProcessorTest(unittest.TestCase):
    @patch("sikriml.models.ner.flair.flair_processor.Sentence")
    def test_process_correct_result(self, mock_sentence: Mock):
        # Arrange
        start = 12
        end = 18
        name = "George"
        text = f"His name is {name}"
        # mock Sentence object
        sentence = Mock()
        span = Span(name, start, end, ScoreLabel.PER)
        sentence.get_spans.return_value = [span]
        mock_sentence.return_value = sentence
        # mock Flair model
        flair_model = Mock()
        flair_model.predict = Mock()
        processor = FlairProcessor(flair_model)
        # Act
        result = processor.process(text)
        # Assert
        expected_result = set([ScoreEntity(name, start, end, ScoreLabel.PER)])
        self.assertSetEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
