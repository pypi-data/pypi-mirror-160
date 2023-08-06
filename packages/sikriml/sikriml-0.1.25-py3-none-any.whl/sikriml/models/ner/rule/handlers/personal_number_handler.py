from datetime import datetime
from typing import List, Match, Union

from sikriml.models.ner import ScoreLabel

from .abstracts.regex_handler import RegexHandler


class PersonalNumberHandler(RegexHandler):
    @property
    def match_group(self) -> int:
        return 1

    @property
    def regex(self) -> Union[str, List[str]]:
        return r"(?:[^\w.]|^)(\d{6}[.|\s]?\d{5})(?:[^\w]|$)"

    def get_label(self, match: Match[str]) -> str:
        return ScoreLabel.PER_NR

    def validator(self, match: Match[str]) -> bool:
        personal_number = match.group(1).replace(" ", "").replace(".", "")
        is_valid_date = self.__has_valid_date(personal_number)
        if len(personal_number) != 11 or not is_valid_date:
            return False
        if (
            self.__get_control_numbers(personal_number[:9])
            == personal_number[9:]
        ):
            return True
        return False

    def __has_valid_date(self, per_nr: str) -> bool:
        card_date = f"{per_nr[:2]}/{per_nr[2:4]}/{per_nr[4:6]}"
        try:
            datetime.strptime(card_date, "%d/%m/%y")
            return True
        except ValueError:
            return False

    def __get_control_numbers(self, digits: str) -> str:
        weights1 = [3, 7, 6, 1, 8, 9, 4, 5, 2]
        weights2 = [5, 4, 3, 2, 7, 6, 5, 4, 3]
        control_number1 = (
            self.__multiply_digits_and_weights(digits, weights1) % 11
        )
        # if the obtained number is 0, control_number1 is set to 0, not 11 (according to the rules)
        control_number1 = (
            11 - control_number1 if control_number1 != 0 else control_number1
        )
        control_number2 = (
            self.__multiply_digits_and_weights(digits, weights2)
            + (2 * control_number1)
        ) % 11
        control_number2 = (
            11 - control_number2 if control_number2 != 0 else control_number2
        )
        return f"{control_number1}{control_number2}"

    def __multiply_digits_and_weights(
        self, digits: str, weights: List[int]
    ) -> int:
        result = 0
        for digit, weight in zip(digits, weights):
            result += int(digit) * weight
        return result
