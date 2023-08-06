import unittest

from sikriml.models.ner.tokenizer import TokenData, Tokenizer

email = "arnenilsen28@gmail.com"
custom_tokenizer = Tokenizer()


class TokenizerTest(unittest.TestCase):
    def test_tokenizer_words_with_whitespace(self):
        # Arrange
        text = "Michael og Justin"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "Michael", 0, 7, True),
            TokenData(1, "og", 8, 10, True),
            TokenData(2, "Justin", 11, 17, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_words_with_hyphen(self):
        # Arrange
        text = "Jan-Arne Nilsen"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "Jan", 0, 3, False),
            TokenData(1, "-", 3, 4, False),
            TokenData(2, "Arne", 4, 8, True),
            TokenData(3, "Nilsen", 9, 15, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_words_with_slash(self):
        # Arrange
        text = "USA/Amerika"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "USA", 0, 3, False),
            TokenData(1, "/", 3, 4, False),
            TokenData(2, "Amerika", 4, 11, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_numbers_with_hyphen(self):
        # Arrange
        text = "2005-2006"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "2005", 0, 4, False),
            TokenData(1, "-", 4, 5, False),
            TokenData(2, "2006", 5, 9, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_numbers_with_slash(self):
        # Arrange
        text = "2005/2006"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "2005", 0, 4, False),
            TokenData(1, "/", 4, 5, False),
            TokenData(2, "2006", 5, 9, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_text_and_numbers_with_hyphen(self):
        # Arrange
        text = "24-åring"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "24", 0, 2, False),
            TokenData(1, "-", 2, 3, False),
            TokenData(2, "åring", 3, 8, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_numbers_with_dot(self):
        # Arrange
        text = "2005.2006"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [TokenData(0, "2005.2006", 0, 9, False)]
        self.assertEqual(result, expected_result)

    def test_tokenizer_numbers_with_comma(self):
        # Arrange
        text = "2005,2006"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [TokenData(0, "2005,2006", 0, 9, False)]
        self.assertEqual(result, expected_result)

    def test_tokenizer_numbers_with_dot_and_comma(self):
        # Arrange
        text = "2.205,200"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [TokenData(0, "2.205,200", 0, 9, False)]
        self.assertEqual(result, expected_result)

    def test_tokenizer_numbers_with_comma_and_dot(self):
        # Arrange
        text = "2,205.200"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [TokenData(0, "2,205.200", 0, 9, False)]
        self.assertEqual(result, expected_result)

    def test_tokenizer_number_with_dot_trailing_dot(self):
        # Arrange
        text = "200."
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "200", 0, 3, False),
            TokenData(1, ".", 3, 4, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_email(self):
        # Arrange
        # Act
        result = custom_tokenizer(email)
        # Assert
        expected_result = [TokenData(0, email, 0, 22, False)]
        self.assertEqual(result, expected_result)

    def test_tokenizer_email_trailing_dot(self):
        # Arrange
        text = f"{email}."
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, email, 0, 22, False),
            TokenData(1, ".", 22, 23, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_text_with_comma(self):
        # Arrange
        text = "epler, bananer"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "epler", 0, 5, False),
            TokenData(1, ",", 5, 6, True),
            TokenData(2, "bananer", 7, 14, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_number_with_parentheses(self):
        # Arrange
        text = "(13)"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "(", 0, 1, False),
            TokenData(1, "13", 1, 3, False),
            TokenData(2, ")", 3, 4, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_text_with_parentheses(self):
        # Arrange
        text = "(stuff)"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "(", 0, 1, False),
            TokenData(1, "stuff", 1, 6, False),
            TokenData(2, ")", 6, 7, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_text_with_guillemets(self):
        # Arrange
        text = "«Queer as Folk»-serien"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "«", 0, 1, False),
            TokenData(1, "Queer", 1, 6, True),
            TokenData(2, "as", 7, 9, True),
            TokenData(3, "Folk", 10, 14, False),
            TokenData(4, "»", 14, 15, False),
            TokenData(5, "-", 15, 16, False),
            TokenData(6, "serien", 16, 22, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_url(self):
        # Arrange
        text = "https://www.youtube.com/watch?v=5RwhyZnVRS8&ab_channel=IAmTimCorey"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(
                0,
                "https://www.youtube.com/watch?v=5RwhyZnVRS8&ab_channel=IAmTimCorey",
                0,
                len(text),
                False,
            )
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_url_slash_at_the_end(self):
        # Arrange
        text = "https://www.youtube.com/"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(
                0,
                "https://www.youtube.com/",
                0,
                len(text),
                False,
            )
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_url_punctuation_at_the_end(self):
        # Arrange
        text = "Aftenposten.no:"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(
                0,
                "Aftenposten.no",
                0,
                14,
                False,
            ),
            TokenData(
                1,
                ":",
                14,
                15,
                False,
            ),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_text_beginning_with_hashtag(self):
        # Arrange
        text = "#norge"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "#", 0, 1, False),
            TokenData(1, "norge", 1, 6, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_text_beginning_with_space(self):
        # Arrange
        text = " Norge"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, " ", 0, 1, False),
            TokenData(1, "Norge", 1, 6, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_text_beginning_with_multiple_spaces(self):
        # Arrange
        text = "   Norge"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "   ", 0, 3, False),
            TokenData(1, "Norge", 3, 8, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_multiple_spaces_after_word(self):
        # Arrange
        text = "Norge  er best"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "Norge", 0, 5, True),
            TokenData(1, " ", 6, 7, False),
            TokenData(2, "er", 7, 9, True),
            TokenData(3, "best", 10, 14, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_ellipsis(self):
        # Arrange
        text = "Ok..."
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "Ok", 0, 2, False),
            TokenData(1, "...", 2, 5, False),
        ]
        self.assertEqual(result, expected_result)

    def test_tokenizer_date_with_parentheses(self):
        # Arrange
        text = "(08.05.2006 12:16)"
        # Act
        result = custom_tokenizer(text)
        # Assert
        expected_result = [
            TokenData(0, "(", 0, 1, False),
            TokenData(1, "08.05.2006", 1, 11, True),
            TokenData(2, "12", 12, 14, False),
            TokenData(3, ":", 14, 15, False),
            TokenData(4, "16", 15, 17, False),
            TokenData(5, ")", 17, 18, False),
        ]
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
