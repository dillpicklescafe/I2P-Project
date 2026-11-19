import unittest
import tempfile
import os

from workout_log import start_workout, add_exercise, complete_workout

from workout_storage import (
    initialize_database,
    save_workout,
    get_workout_history,
    get_workout_by_id
)


class WorkoutStorageTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(
            self.temp_dir.name, "test_fitness.db"
        )

        initialize_database(self.db_path)

        self.session = start_workout(
            goal="upper_body_strength",
            notes="Test workout"
        )

        exercise = {
            "name": "Wall Push-up",
            "sets": 2,
            "reps": 10
        }

        add_exercise(
            self.session,
            exercise,
            sets_completed=2,
            reps_completed=10,
            duration_minutes=5
        )

        complete_workout(self.session)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_workout(self):
        result = save_workout(self.session, self.db_path)

        self.assertEqual(result, self.session["session_id"])

    def test_get_workout_history(self):
        save_workout(self.session, self.db_path)

        history = get_workout_history(self.db_path)

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["total_sets"], 2)
        self.assertEqual(history[0]["total_exercises"], 1)

    def test_get_workout_by_id(self):
        save_workout(self.session, self.db_path)

        result = get_workout_by_id(
            self.session["session_id"],
            self.db_path
        )

        self.assertIsNotNone(result)
        self.assertEqual(
            result["exercises"][0]["name"],
            "Wall Push-up"
        )

    def test_missing_workout(self):
        result = get_workout_by_id(
            "nonexistent",
            self.db_path
        )

        self.assertIsNone(result)

    def test_incomplete_workout_rejected(self):
        incomplete = start_workout(goal="cardio")

        with self.assertRaises(ValueError):
            save_workout(incomplete, self.db_path)


if __name__ == "__main__":
    unittest.main()
