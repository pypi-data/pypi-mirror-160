import unittest

from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.rule.handlers import PersonalNumberHandler


class TestPersonalNumberHandler(unittest.TestCase):
    def test_process_personal_numbers(self):
        # Arrange
        text_with_numbers = "Her er flere fake personnumre: 23115624334, 26040139973, 17090701541, 19033038332, 29050605793, 25081239862."
        number_handler = PersonalNumberHandler()
        expected_entities = set(
            [
                ScoreEntity("23115624334", 31, 42, ScoreLabel.PER_NR),
                ScoreEntity("26040139973", 44, 55, ScoreLabel.PER_NR),
                ScoreEntity("17090701541", 57, 68, ScoreLabel.PER_NR),
                ScoreEntity("19033038332", 70, 81, ScoreLabel.PER_NR),
                ScoreEntity("29050605793", 83, 94, ScoreLabel.PER_NR),
                ScoreEntity("25081239862", 96, 107, ScoreLabel.PER_NR),
            ]
        )
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_personal_number_too_short(self):
        # Arrange
        text_with_numbers = "Her er et for kort personnummer: 2311562433."
        number_handler = PersonalNumberHandler()
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_personal_number_too_long(self):
        # Arrange
        text_with_numbers = "Her er et for langt personnummer: 231156243341."
        number_handler = PersonalNumberHandler()
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_personal_number_wrong_date(self):
        # Arrange
        text_with_numbers = "Her er et personnummer som kunne vært lovlig hvis det fantes 53.11.56: 53115624357."
        number_handler = PersonalNumberHandler()
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_personal_number_dot(self):
        # Arrange
        text_with_numbers = "Her er et fake personnummer: 231156.24334."
        number_handler = PersonalNumberHandler()
        expected_entities = set(
            [ScoreEntity("231156.24334", 29, 41, ScoreLabel.PER_NR)]
        )
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_personal_number_wrong_dot(self):
        # Arrange
        text_with_numbers = (
            "Her er et fake personnummer oppdelt feil: 231.156.24334."
        )
        number_handler = PersonalNumberHandler()
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())

    def test_process_personal_number_space(self):
        # Arrange
        text_with_numbers = "Her er et fake personnummer: 231156 24334."
        number_handler = PersonalNumberHandler()
        expected_entities = set(
            [ScoreEntity("231156 24334", 29, 41, ScoreLabel.PER_NR)]
        )
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_personal_number_wrong_space(self):
        # Arrange
        text_with_numbers = (
            "Her er et fake personnummer oppdelt feil: 23 1156 243 34."
        )
        number_handler = PersonalNumberHandler()
        # Act
        result = number_handler.process(text_with_numbers)
        # Assert
        self.assertSetEqual(result, set())


if __name__ == "__main__":
    unittest.main(verbosity=2)
