import unittest

from exercise_media import get_exercise_media
from exercises import exercises
from media_review_server import PROJECT_DIR, review_records


class MediaReviewToolTests(unittest.TestCase):
    def test_review_records_cover_every_missing_media_exercise(self):
        records = review_records()
        expected = [
            exercise for exercise in exercises
            if get_exercise_media(exercise["id"]) is None
        ]
        self.assertEqual(len(records), 27)
        self.assertEqual(
            [record["id"] for record in records],
            [exercise["id"] for exercise in expected],
        )
        for record, exercise in zip(records, expected):
            self.assertEqual(record["name"], exercise["name"])
            self.assertEqual(record["difficulty"], exercise["level"])
            self.assertEqual(record["equipment"], exercise["equipment"])
            self.assertEqual(record["instructions"], exercise["instructions"])

    def test_every_candidate_has_existing_local_media_and_review_metadata(self):
        for record in review_records():
            for candidate in record["candidates"]:
                self.assertTrue(candidate["original_name"])
                self.assertTrue(candidate["source_type"])
                self.assertTrue(candidate["warning"])
                self.assertTrue(candidate["media"])
                for media in candidate["media"]:
                    self.assertTrue((PROJECT_DIR / media["path"]).is_file())

    def test_no_candidate_records_have_an_explicit_result(self):
        records_without_candidates = [
            record for record in review_records() if not record["candidates"]
        ]
        self.assertTrue(records_without_candidates)
        for record in records_without_candidates:
            self.assertIn("No suitable candidate found", record["no_candidate_note"])


if __name__ == "__main__":
    unittest.main()
