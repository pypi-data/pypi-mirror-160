import unittest

from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.rule.handlers import AccountNumberHandler


class TestAccountNumberHandler(unittest.TestCase):
    def test_process_account_numbers(self):
        # Arrange
        text_with_numbers = "Her er flere fake kontonumre: 60110011111, 12101122222, 12140011111."
        number_handler = AccountNumberHandler()
        expected_entities = set(
            [
                ScoreEntity("60110011111", 30, 41, ScoreLabel.ACC_NR),
                ScoreEntity("12101122222", 43, 54, ScoreLabel.ACC_NR),
                ScoreEntity("12140011111", 56, 67, ScoreLabel.ACC_NR),
            ]
        )
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_account_number_too_short(self):
        # Arrange
        text_with_numbers = "Her er et for kort kontonummer: 6011001111."
        number_handler = AccountNumberHandler()
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_account_number_too_long(self):
        # Arrange
        text_with_numbers = "Her er et for langt kontonummer: 601100111111."
        number_handler = AccountNumberHandler()
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_account_number_dot(self):
        # Arrange
        text_with_numbers = "Her er et fake kontonummer: 6011.00.11111."
        number_handler = AccountNumberHandler()
        expected_entities = set(
            [ScoreEntity("6011.00.11111", 28, 41, ScoreLabel.ACC_NR)]
        )
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_account_number_wrong_dot(self):
        # Arrange
        text_with_numbers = (
            "Her er et fake kontonummer oppdelt feil: 601.100.11111."
        )
        number_handler = AccountNumberHandler()
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_account_number_space(self):
        # Arrange
        text_with_numbers = "Her er et fake kontonummer: 6011 00 11111."
        number_handler = AccountNumberHandler()
        expected_entities = set(
            [ScoreEntity("6011 00 11111", 28, 41, ScoreLabel.ACC_NR)]
        )
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_account_number_wrong_space(self):
        # Arrange
        text_with_numbers = (
            "Her er et fake kontonummer oppdelt feil: 6011 00 11 111."
        )
        number_handler = AccountNumberHandler()
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_account_number_wrong_space2(self):
        # Arrange
        text_with_numbers = "Her er et fake kontonummer oppdelt som personnummer: 231156 24334."
        number_handler = AccountNumberHandler()
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_account_number_that_has_personal_number_digits_success(
        self,
    ):
        # Arrange
        text_with_numbers = "Her er et fake kontonummer: 2311 56 24334."
        number_handler = AccountNumberHandler()
        expected_entities = set(
            [ScoreEntity("2311 56 24334", 28, 41, ScoreLabel.ACC_NR)]
        )
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)


if __name__ == "__main__":
    unittest.main(verbosity=2)
