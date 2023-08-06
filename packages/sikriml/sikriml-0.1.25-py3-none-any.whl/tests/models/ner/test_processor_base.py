import unittest
from typing import Any, Callable
from unittest.mock import Mock

from sikriml.models.ner import ScoreEntity, ScoreLabel, process_text

key_func: Callable[[ScoreEntity], Any] = lambda x: x.label


class ProcessorBaseTest(unittest.TestCase):
    def test_process_text_multiple_processors_correct_result(self):
        # Arrange
        text = "Tom is 23"
        name_entity_mock = ScoreEntity("Tom", 0, 3, ScoreLabel.PER)
        spacy_processor_mock = Mock()
        spacy_processor_mock.process = Mock(return_value=set([name_entity_mock]))
        number_entity_mock = ScoreEntity("23", 7, 9, ScoreLabel.NUMB)
        rule_processor_mock = Mock()
        rule_processor_mock.process = Mock(return_value=set([number_entity_mock]))
        # Act
        result = process_text(text, [rule_processor_mock, spacy_processor_mock])
        # Assert
        expected_result = sorted([name_entity_mock, number_entity_mock], key=key_func)
        self.assertListEqual(sorted(result, key=key_func), expected_result)

    def test_process_text_enveloped_tags_should_take_longest(self):
        # Arrange
        text = "Khalifa bin Zayed al Nahyan studied at Universitetet i Oslo"
        entities = [
            ScoreEntity("Khalifa", 0, 7, ScoreLabel.PER),
            ScoreEntity("Zayed", 12, 17, ScoreLabel.PER),
            ScoreEntity("Oslo", 55, 59, ScoreLabel.LOC),
            ScoreEntity("Nahyan", 21, 27, ScoreLabel.PER),
            ScoreEntity("Khalifa bin Zayed al Nahyan", 0, 27, ScoreLabel.PER),
            ScoreEntity("Universitetet i Oslo", 39, 59, ScoreLabel.ORG),
            ScoreEntity("Zayed al Nahyan", 12, 27, ScoreLabel.PER),
        ]
        spacy_processor_mock = Mock()
        spacy_processor_mock.process = Mock(return_value=set(entities))
        # Act
        result = process_text(text, [spacy_processor_mock])
        # Assert
        expected_result = [
            ScoreEntity("Khalifa bin Zayed al Nahyan", 0, 27, ScoreLabel.PER),
            ScoreEntity("Universitetet i Oslo", 39, 59, ScoreLabel.ORG),
        ]
        self.assertListEqual(
            sorted(result, key=key_func), sorted(expected_result, key=key_func)
        )

    def test_process_text_overlapped_tags_should_take_longest(self):
        # Arrange
        text = "Khalifa bin Zayed al Nahyan"
        entities = [
            ScoreEntity("Khalifa bin Zayed", 0, 17, ScoreLabel.PER),
            ScoreEntity("Zayed al Nahyan", 12, 27, ScoreLabel.PER),
        ]
        spacy_processor_mock = Mock()
        spacy_processor_mock.process = Mock(return_value=set(entities))
        # Act
        result = process_text(text, [spacy_processor_mock])
        # Assert
        expected_result = [ScoreEntity("Khalifa bin Zayed", 0, 17, ScoreLabel.PER)]
        self.assertListEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
