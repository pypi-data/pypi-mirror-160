import unittest

from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.rule.handlers import UrlHandler

url_handler = UrlHandler()


class TestUrlHandler(unittest.TestCase):
    def test_process_url_correct(self):
        # Arrange
        text_with_url = "Urler: https://www.vg.no, https://www.yahoo.com, www.biznes.gov.pl, https://stat.gov.pl, https://nrksuper.no, Nrk.no, https://www.finn.no/bap/forsale/ad.html?finnkode=174781820, stuff.no,more_stuff.no. De var alle riktige."
        expected_entities = set(
            [
                ScoreEntity("https://www.vg.no", 7, 24, ScoreLabel.URL),
                ScoreEntity("https://www.yahoo.com", 26, 47, ScoreLabel.URL),
                ScoreEntity("www.biznes.gov.pl", 49, 66, ScoreLabel.URL),
                ScoreEntity("https://stat.gov.pl", 68, 87, ScoreLabel.URL),
                ScoreEntity("https://nrksuper.no", 89, 108, ScoreLabel.URL),
                ScoreEntity("Nrk.no", 110, 116, ScoreLabel.URL),
                ScoreEntity(
                    "https://www.finn.no/bap/forsale/ad.html?finnkode=174781820",
                    118,
                    176,
                    ScoreLabel.URL,
                ),
                ScoreEntity("stuff.no", 178, 186, ScoreLabel.URL),
                ScoreEntity("more_stuff.no", 187, 200, ScoreLabel.URL),
            ]
        )
        # Act
        result = url_handler.process(text_with_url)
        # Assert
        self.assertSetEqual(result, expected_entities)

    def test_process_url_incorrect(self):
        # Arrange
        text_with_urls = "Ikke urler: http://wer, Stuff, stuff, 0853jg4e56_($)/ert654.935yua, ad.html?finnkode=174781820, www.jik www.jik.c www.www.www "
        # Act
        result = url_handler.process(text_with_urls)
        # Assert
        self.assertSetEqual(result, set())


if __name__ == "__main__":
    unittest.main(verbosity=2)
