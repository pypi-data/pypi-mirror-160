import unittest
from unittest.mock import Mock

from sikriml.models.ner import ScoreEntity, ScoreLabel, process_text


class ProcessorBaseTest(unittest.TestCase):
    def test_process_text_correct_result(self):
        # Arrange
        text = "Tom is 23"
        name_mock = ScoreEntity("Tom", 0, 3, ScoreLabel.PER)
        name_handler = Mock()
        name_handler.process = Mock(return_value=set([name_mock]))
        number_mock = ScoreEntity("23", 7, 9, ScoreLabel.NUMB)
        number_handler = Mock()
        number_handler.process = Mock(return_value=set([number_mock]))
        # Act
        result = process_text(text, [number_handler, name_handler])
        # Assert
        expected_result = set([name_mock, number_mock])
        self.assertSetEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
