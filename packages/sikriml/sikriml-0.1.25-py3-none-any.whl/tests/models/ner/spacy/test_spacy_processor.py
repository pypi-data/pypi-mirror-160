import unittest
from unittest.mock import Mock

from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.spacy import SpacyProcessor

from .helpers.spacy_models import Doc, Span


class SpacyProcessorTest(unittest.TestCase):
    def test_process_correct_result(self):
        # Arrange
        start = 12
        name = "George"
        text = f"His name is {name}"
        span = Span(name, 12, 18, ScoreLabel.PER)
        doc = Doc(tuple([span]))
        spacy_model = Mock(return_value=doc)
        processor = SpacyProcessor(spacy_model)
        # Act
        result = processor.process(text)
        # Assert
        expected_result = set(
            [ScoreEntity(name, start, len(name) + start, ScoreLabel.PER)]
        )
        self.assertSetEqual(result, expected_result)

    def test_process_empty_text_should_return_empty_set(self):
        # Arrange
        model_mock = Mock()
        processor = SpacyProcessor(model_mock)
        # Act
        result = processor.process("")
        # Assert
        self.assertSetEqual(result, set([]))
        self.assertFalse(model_mock.called)


if __name__ == "__main__":
    unittest.main(verbosity=2)
