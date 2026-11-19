
import unittest

from workout_log import (
    start_workout,
    add_exercise,
    calculate_total_duration,
    complete_workout,
    get_workout_summary
)


class WorkoutLogTests(unittest.TestCase):

    def setUp(self):
        self.session = start_workout(
            goal="upper_body_strength"
        )

        self.exercise = {
            "name": "Wall Push-up",
            "sets": 2,
            "reps": 10
        }

    def test_start_workout(self):
        self.assertEqual(self.session["exercises"], [])
        self.assertFalse(self.session["completed"])

    def test_add_exercise(self):
        add_exercise(
            self.session,
            self.exercise,
            sets_completed=2,
            reps_completed=10,
            duration_minutes=5
        )

        self.assertEqual(len(self.session["exercises"]), 1)

    def test_total_duration(self):
        add_exercise(
            self.session,
            self.exercise,
            2, 10, 5
        )

        self.assertEqual(
            calculate_total_duration(self.session), 5
        )

    def test_complete_workout(self):
        add_exercise(
            self.session,
            self.exercise,
            2, 10, 5
        )

        complete_workout(self.session)

        self.assertTrue(self.session["completed"])

    def test_workout_summary(self):
        add_exercise(
            self.session,
            self.exercise,
            2, 10, 5
        )

        summary = get_workout_summary(self.session)

        self.assertEqual(summary["total_exercises"], 1)
        self.assertEqual(summary["total_sets"], 2)
        self.assertEqual(summary["total_duration"], 5)

    def test_invalid_sets(self):
        with self.assertRaises(ValueError):
            add_exercise(
                self.session,
                self.exercise,
                0
            )


if __name__ == "__main__":
    unittest.main()
