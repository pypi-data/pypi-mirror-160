import unittest

from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.rule.handlers import CardNumberHandler


class TestCardNumberHandler(unittest.TestCase):
    def test_process_mastercard(self):
        # Arrange
        text_with_numbers = (
            "Her er et Mastercard kontonummer: 2222400070000005."
        )
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("2222400070000005", 34, 50, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_mastercard_spaces(self):
        # Arrange
        text_with_numbers = (
            "Her er et Mastercard kontonummer: 2222 4000 7000 0005."
        )
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("2222 4000 7000 0005", 34, 53, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_mastercard_dots(self):
        # Arrange
        text_with_numbers = (
            "Her er et Mastercard kontonummer: 2222.4000.7000.0005."
        )
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("2222.4000.7000.0005", 34, 53, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_mastercard_suffix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Mastercard kontonummer med ekstra tall bak: 2222400070000005354."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_mastercard_prefix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Mastercard kontonummer med ekstra tall foran: 002222400070000005."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_mastercard_range_success(self):
        # Arrange
        text_with_numbers = (
            "Her er et Mastercard kontonummer: 2720400070000005."
        )
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("2720400070000005", 34, 50, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_mastercard_range_fail(self):
        # Arrange
        text_with_numbers = (
            "Her er et Mastercard kontonummer: 2721400070000005."
        )
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_visa_16_digits(self):
        # Arrange
        text_with_numbers = "Her er et Visa kontonummer: 4111111145551142."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("4111111145551142", 28, 44, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_visa_16_digits_spaces(self):
        # Arrange
        text_with_numbers = "Her er et Visa kontonummer: 4111 1111 4555 1142."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("4111 1111 4555 1142", 28, 47, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_visa_16_digits_dots(self):
        # Arrange
        text_with_numbers = "Her er et Visa kontonummer: 4111.1111.4555.1142."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("4111.1111.4555.1142", 28, 47, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_visa_16_digits_suffix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Visa kontonummer med ekstra tall bak: 4111111145551142666."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_visa_16_digits_prefix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Visa kontonummer med ekstra tall foran: 4444111111145551142."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_visa_13_digits(self):
        # Arrange
        text_with_numbers = "Her er et Visa kontonummer: 4111111145551."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("4111111145551", 28, 41, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_visa_13_digits_spaces(self):
        # Arrange
        text_with_numbers = "Her er et Visa kontonummer: 4111 111 145 551."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("4111 111 145 551", 28, 44, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_visa_13_digits_dots(self):
        # Arrange
        text_with_numbers = "Her er et Visa kontonummer: 4111.111.145.551."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("4111.111.145.551", 28, 44, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_visa_13_digits_suffix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Visa kontonummer med ekstra tall bak: 411111114555133."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_visa_13_digits_prefix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Visa kontonummer med ekstra tall foran: 434111111145551."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_amex(self):
        # Arrange
        text_with_numbers = "Her er et Amex kontonummer: 370000000000002."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("370000000000002", 28, 43, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_amex_spaces_4443(self):
        # Arrange
        text_with_numbers = "Her er et Amex kontonummer: 3700 0000 0000 002."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("3700 0000 0000 002", 28, 46, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_amex_spaces_465(self):
        # Arrange
        text_with_numbers = "Her er et Amex kontonummer: 3700 000000 00002."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("3700 000000 00002", 28, 45, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_amex_dots_4443(self):
        # Arrange
        text_with_numbers = "Her er et Amex kontonummer: 3700.0000.0000.002"
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("3700.0000.0000.002", 28, 46, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_amex_dots_465(self):
        # Arrange
        text_with_numbers = "Her er et Amex kontonummer: 3700.000000.00002."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("3700.000000.00002", 28, 45, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_amex_suffix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Amex kontonummer med ekstra tall bak: 37000000000000299."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_amex_prefix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Amex kontonummer med ekstra tall foran: 00370000000000002."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_diners(self):
        # Arrange
        text_with_numbers = "Her er et Diners kontonummer: 30569309025904."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("30569309025904", 30, 44, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_diners_spaces_4442(self):
        # Arrange
        text_with_numbers = "Her er et Diners kontonummer: 3056 9309 0259 04."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("3056 9309 0259 04", 30, 47, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_diners_dots_4442(self):
        # Arrange
        text_with_numbers = "Her er et Diners kontonummer: 3056.9309.0259.04."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("3056.9309.0259.04", 30, 47, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_diners_spaces_464(self):
        # Arrange
        text_with_numbers = "Her er et Diners kontonummer: 3056 930902 5904."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("3056 930902 5904", 30, 46, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_diners_dots_464(self):
        # Arrange
        text_with_numbers = "Her er et Diners kontonummer: 3056.930902.5904."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("3056.930902.5904", 30, 46, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_diners_suffix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Diners kontonummer med ekstra tall bak: 3056930902590400."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_diners_prefix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Diners kontonummer med ekstra tall foran: 0030569309025904."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_discover(self):
        # Arrange
        text_with_numbers = "Her er et Discover kontonummer: 6011111111111117."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("6011111111111117", 32, 48, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_discover_spaces(self):
        # Arrange
        text_with_numbers = (
            "Her er et Discover kontonummer: 6011 1111 1111 1117."
        )
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("6011 1111 1111 1117", 32, 51, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_discover_dots(self):
        # Arrange
        text_with_numbers = (
            "Her er et Discover kontonummer: 6011.1111.1111.1117."
        )
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("6011.1111.1111.1117", 32, 51, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_discover_suffix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Discover kontonummer med ekstra tall bak: 6011111111111117111."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_discover_prefix_fail(self):
        # Arrange
        text_with_numbers = "Her er et fake Discover kontonummer med ekstra tall foran: 1116011111111111117."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_discover_range_success(self):
        # Arrange
        text_with_numbers = "Her er et Discover kontonummer: 6229251111111117."
        card_handler = CardNumberHandler()
        expected_entities = set(
            [ScoreEntity("6229251111111117", 32, 48, ScoreLabel.CARD_NR)]
        )
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_discover_range_fail(self):
        # Arrange
        text_with_numbers = "Her er et Discover kontonummer: 6229261111111117."
        card_handler = CardNumberHandler()
        # Act
        result = card_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())


if __name__ == "__main__":
    unittest.main(verbosity=2)
