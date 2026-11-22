from datetime import date
import unittest
import tempfile
import os
import sqlite3
from contextlib import closing
from unittest.mock import patch

from workout_log import (
    start_workout,
    add_exercise,
    complete_workout
)

from workout_storage import (
    initialize_database,
    save_workout,
    get_workout_history,
    get_workout_by_id,
    get_workout_stats,
)


class WorkoutStorageTests(unittest.TestCase):

    def setUp(self):
        # Create a temporary database for each test
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(
            self.temp_dir.name,
            "test_fitness.db"
        )

        initialize_database(self.db_path)

        # Create a sample workout session
        self.session = start_workout(
            goal="upper_body_strength",
            notes="Test workout"
        )

        # Exercise must include its original exercise ID
        exercise = {
            "id": 1,
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
        # Remove the temporary database after each test
        self.temp_dir.cleanup()

    def test_save_workout(self):
        result = save_workout(
            self.session,
            self.db_path
        )

        self.assertEqual(
            result,
            self.session["session_id"]
        )

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

        self.assertEqual(
            result["exercises"][0]["exercise_id"],
            1
        )

    def test_missing_workout(self):
        result = get_workout_by_id(
            "nonexistent",
            self.db_path
        )

        self.assertIsNone(result)

    def test_stats_return_weekdays_and_monthly_buckets(self):
        workouts = [
            ("monday", "2026-11-23"),
            ("sunday", "2026-11-29"),
            ("march", "2026-03-15"),
            ("november", "2026-11-22"),
            ("last_year", "2025-12-31"),
        ]
        with closing(sqlite3.connect(self.db_path)) as connection:
            with connection:
                connection.executemany("""
                    INSERT INTO workouts (session_id, date, goal, completed)
                    VALUES (?, ?, 'cardio', 1)
                """, workouts)

        class FixedDate(date):
            @classmethod
            def today(cls):
                return cls(2026, 11, 23)

        with patch("workout_storage.date", FixedDate):
            weekly = get_workout_stats("week", self.db_path)
            monthly = get_workout_stats("month", self.db_path)

        self.assertEqual(
            [bucket["date"] for bucket in weekly["activity"]],
            [
                "2026-11-23",
                "2026-11-24",
                "2026-11-25",
                "2026-11-26",
                "2026-11-27",
                "2026-11-28",
                "2026-11-29",
            ],
        )
        self.assertEqual(
            [bucket["sessions"] for bucket in weekly["activity"]],
            [1, 0, 0, 0, 0, 0, 1],
        )
        self.assertEqual(weekly["total_sessions"], 2)
        self.assertEqual(len(monthly["activity"]), 12)
        self.assertEqual(monthly["activity"][2]["date"], "2026-03-01")
        self.assertEqual(monthly["activity"][2]["sessions"], 1)
        self.assertEqual(monthly["activity"][10]["date"], "2026-11-01")
        self.assertEqual(monthly["activity"][10]["sessions"], 2)
        self.assertEqual(monthly["total_sessions"], 3)
        self.assertEqual(monthly["end_date"], "2026-11-23")

    def test_incomplete_workout_rejected(self):
        incomplete = start_workout(goal="cardio")

        with self.assertRaises(ValueError):
            save_workout(incomplete, self.db_path)

    def test_exercise_id_is_required(self):
        session = start_workout(goal="cardio")

        exercise = {
            "name": "Jumping Jack",
            "sets": 2,
            "reps": 10
        }

        with self.assertRaises(ValueError):
            add_exercise(
                session,
                exercise,
                sets_completed=2,
                reps_completed=10,
                duration_minutes=5
            )


if __name__ == "__main__":
    unittest.main()
