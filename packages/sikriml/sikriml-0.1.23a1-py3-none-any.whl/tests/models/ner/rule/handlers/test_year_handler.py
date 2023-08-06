import unittest

from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.rule.handlers import NumberHandler, YearHandler

handler = YearHandler()


class YearHandlerTest(unittest.TestCase):
    def test_year_handler_correct_result(self):
        # Arrange
        year = "1990"
        # Act
        result = handler.process(f"Was born in {year}")
        # Assert
        expected_result = set([ScoreEntity(year, 12, 16, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_with_apostrophe_return_only_digits(self):
        # Arrange
        year = "1990's"
        # Act
        result = handler.process(f"Was born in {year}")
        # Assert
        expected_result = set([ScoreEntity("1990", 12, 16, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_with_extra_chars_return_only_digits(self):
        # Arrange
        year = "1990th"
        # Act
        result = handler.process(f"Was born in {year}")
        # Assert
        expected_result = set([ScoreEntity("1990", 12, 16, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_time_period_correct(self):
        # Arrange
        year = "1990-årene"
        # Act
        result = handler.process(f"Det skjedde i {year}")
        # Assert
        expected_result = set([ScoreEntity(year, 14, 24, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_invalid_year(self):
        # Arrange
        year = "2990"
        # Act
        result = handler.process(f"Some random number {year}")
        # Assert
        self.assertSetEqual(result, set())

    def test_year_handler_valid_year_extra_digit_behind(self):
        # Arrange
        year = "19784"
        # Act
        result = handler.process(f"Some random number {year}")
        # Assert
        self.assertSetEqual(result, set())

    def test_year_handler_valid_year_extra_digit_front(self):
        # Arrange
        year = "11978"
        # Act
        result = handler.process(f"Some random number {year}")
        # Assert
        self.assertSetEqual(result, set())

    def test_year_handler_returns_empty_set(self):
        # Act
        result = handler.process("Date of birth is unknown")
        # Assert
        self.assertSetEqual(result, set())

    def test_year_handler_as_decorator(self):
        # Arrange
        number_handler = NumberHandler()
        year_decorator = YearHandler(number_handler)
        year = "2000"
        number = "22"
        # Act
        result = year_decorator.process(f"Was born in {year}. He is {number}")
        # Assert
        expected_result = set(
            [
                ScoreEntity(year, 12, 16, ScoreLabel.YEAR),
                ScoreEntity(number, 24, 26, ScoreLabel.NUMB),
            ]
        )
        self.assertSetEqual(result, expected_result)

    def test_year_handler_as_decorator_return_only_digits_for_year(self):
        # Arrange
        number_handler = NumberHandler()
        year_decorator = YearHandler(number_handler)
        year = "2000's"
        number = "22"
        # Act
        result = year_decorator.process(f"Was born in {year}. He is {number}")
        # Assert
        expected_result = set(
            [
                ScoreEntity("2000", 12, 16, ScoreLabel.YEAR),
                ScoreEntity(number, 26, 28, ScoreLabel.NUMB),
            ]
        )
        self.assertSetEqual(result, expected_result)

    def test_year_handler_as_decorator_time_period_return_whole_year_phrase(self):
        # Arrange
        number_handler = NumberHandler()
        year_decorator = YearHandler(number_handler)
        year = "1990-tallet"
        number = "28"
        # Act
        result = year_decorator.process(
            f"Jeg ble født på {year} og er {number} år gammel."
        )
        # Assert
        expected_result = set(
            [
                ScoreEntity(year, 16, 27, ScoreLabel.YEAR),
                ScoreEntity(number, 34, 36, ScoreLabel.NUMB),
            ]
        )
        self.assertSetEqual(result, expected_result)

    def test_year_handler_as_decorator_short_time_period_return_whole_year_phrase(self):
        # Arrange
        number_handler = NumberHandler()
        year_decorator = YearHandler(number_handler)
        year = "90-tallet"
        number = "28"
        # Act
        result = year_decorator.process(
            f"Jeg ble født på {year} og er {number} år gammel."
        )
        # Assert
        expected_result = set(
            [
                ScoreEntity(year, 16, 25, ScoreLabel.YEAR),
                ScoreEntity(number, 32, 34, ScoreLabel.NUMB),
            ]
        )
        self.assertSetEqual(result, expected_result)

    def test_year_handler_as_decorator_age_treat_whole_phrase_as_number(self):
        # Arrange
        number_handler = NumberHandler()
        year_decorator = YearHandler(number_handler)
        age = "90-årene"
        number = "98"
        # Act
        result = year_decorator.process(
            f"Jeg er en mann i {age}, jeg er {number} år gammel."
        )
        # Assert
        expected_result = set(
            [
                ScoreEntity(age, 17, 25, ScoreLabel.NUMB),
                ScoreEntity(number, 34, 36, ScoreLabel.NUMB),
            ]
        )
        self.assertSetEqual(result, expected_result)

    def test_year_handler_as_decorator_years_with_comma_and_dot(self):
        # Arrange
        number_handler = NumberHandler()
        year_decorator = YearHandler(number_handler)
        decimal = "1990,1991"
        decimal_dot = "1990.1991"
        # Act
        result = year_decorator.process(
            f"This is a decimal {decimal}, this too {decimal_dot}."
        )
        # Assert
        expected_result = set(
            [
                ScoreEntity(decimal, 18, 27, ScoreLabel.YEAR),
                ScoreEntity(decimal_dot, 38, 47, ScoreLabel.YEAR),
            ]
        )
        self.assertSetEqual(result, expected_result)

    def test_year_handler_as_decorator_year_range(self):
        # Arrange
        number_handler = NumberHandler()
        year_decorator = YearHandler(number_handler)
        year_range = "1990-1991"
        number = "19901991"
        # Act
        result = year_decorator.process(
            f"This is a year range {year_range} and this isn't {number}."
        )
        # Assert
        expected_result = set(
            [
                ScoreEntity("1990", 21, 25, ScoreLabel.YEAR),
                ScoreEntity("1991", 26, 30, ScoreLabel.YEAR),
                ScoreEntity(number, 46, 54, ScoreLabel.NUMB),
            ]
        )
        self.assertSetEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
