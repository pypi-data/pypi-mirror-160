import unittest

from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.rule.handlers import NumberHandler

handler = NumberHandler()


class NumberHandlerTest(unittest.TestCase):
    def test_number_handler_int_number(self):
        # Arrange
        number = "223"
        # Act
        result = handler.process(f"Text with {number}")
        # Assert
        expected_result = set([ScoreEntity(number, 10, 13, ScoreLabel.NUMB)])
        self.assertSetEqual(result, expected_result)

    def test_number_handler_float_number(self):
        # Arrange
        number = "15.6"
        # Act
        result = handler.process(f"Text with {number}")
        # Assert
        expected_result = set([ScoreEntity(number, 10, 14, ScoreLabel.NUMB)])
        self.assertSetEqual(result, expected_result)

    def test_number_handler_range_of_numbers(self):
        # Arrange
        number = "20-30"
        # Act
        result = handler.process(f"Text with {number}")
        # Assert
        expected_result = set(
            [
                ScoreEntity("20", 10, 12, ScoreLabel.NUMB),
                ScoreEntity("30", 13, 15, ScoreLabel.NUMB),
            ]
        )
        self.assertSetEqual(result, expected_result)

    def test_number_handler_number_with_letter(self):
        # Arrange
        number = "11A"
        # Act
        result = handler.process(f"Text with {number}")
        # Assert
        expected_result = set([ScoreEntity("11", 10, 12, ScoreLabel.NUMB)])
        self.assertSetEqual(result, expected_result)

    def test_number_handler_returns_empty_set(self):
        # Act
        result = handler.process("Text without number")
        # Assert
        self.assertSetEqual(result, set())


if __name__ == "__main__":
    unittest.main(verbosity=2)
