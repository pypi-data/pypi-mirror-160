import json
import unittest

from sikriml.models.ner import (
    ScoreEntity,
    ScoreEntityEncoder,
    score_entity_decoder,
)

start = 0
end = 5
label = "LOC"
text = "London"
json_str = '{{"text": "{}", "start": {}, "end": {}, "label": "{}"}}'
invalid_json_str = '{"invalid_property": 0}'


class ScoreEntityTest(unittest.TestCase):
    def test_score_entity_encoder_correct_result(self):
        # Arrange
        score_entity = ScoreEntity(text, start, end, label)
        # Act
        result = json.dumps(score_entity, cls=ScoreEntityEncoder)
        # Assert
        json_score_entity = json_str.format(text, start, end, label)
        self.assertEqual(result, json_score_entity)

    def test_score_entity_decoder_correct_result(self):
        # Arrange
        json_score_entity = json_str.format(text, start, end, label)
        # Act
        entity: ScoreEntity = json.loads(
            json_score_entity, object_hook=score_entity_decoder
        )
        # Assert
        expected_entity = ScoreEntity(text, start, end, label)
        self.assertTrue(entity == expected_entity)

    def test_score_entity_decoder_invalid_type(self):
        # Assert
        self.assertRaises(
            TypeError,
            json.loads,
            invalid_json_str,
            object_hook=score_entity_decoder,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
