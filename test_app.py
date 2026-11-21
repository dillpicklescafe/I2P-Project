from contextlib import closing
import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import build_recommendation, create_app, save_completed_workout
from workout_storage import (
    get_user_by_id,
    get_workout_by_id,
    get_workout_history,
    initialize_database,
)


class WorkoutUiTests(unittest.TestCase):

    def test_build_recommendation_includes_existing_exercise_details(self):
        result = build_recommendation({
            "goal": "first_pushup",
            "level": "beginner",
            "equipment": [],
            "duration": 30,
        })

        self.assertTrue(result)
        self.assertTrue(all("instructions" in exercise for exercise in result))
        self.assertTrue(all("media_url" in exercise for exercise in result))
        self.assertTrue(all(exercise["duration"] <= 30 for exercise in result))

    def test_build_recommendation_rejects_unavailable_level(self):
        with self.assertRaises(ValueError):
            build_recommendation({
                "goal": "first_pushup",
                "level": "expert",
                "equipment": [],
                "duration": 20,
            })

    def test_build_recommendation_accepts_advanced_and_time_steps(self):
        result = build_recommendation({
            "goal": "first_pushup",
            "level": "advanced",
            "equipment": [],
            "duration": 15,
        })

        self.assertTrue(all(exercise["duration"] <= 15 for exercise in result))
        with self.assertRaises(ValueError):
            build_recommendation({
                "goal": "first_pushup",
                "level": "beginner",
                "equipment": [],
                "duration": 20,
            })

    def test_save_completed_workout_stores_only_marked_exercises(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = str(Path(temp_dir) / "workouts.db")
            session_id = save_completed_workout({
                "goal": "first_pushup",
                "completed_exercises": [1],
                "notes": "Felt good",
            }, db_path)

            history = get_workout_history(db_path)
            saved_workout = get_workout_by_id(session_id, db_path)

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["total_exercises"], 1)
        self.assertEqual(saved_workout["notes"], "Felt good")
        self.assertEqual(saved_workout["exercises"][0]["exercise_id"], 1)

    def test_save_completed_workout_requires_a_checked_exercise(self):
        with self.assertRaises(ValueError):
            save_completed_workout({
                "goal": "first_pushup",
                "completed_exercises": [],
            })

    def test_accounts_and_workout_history_are_private(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            app = create_app({
                "TESTING": True,
                "SECRET_KEY": "test-secret-key",
                "DATABASE": str(Path(temp_dir) / "accounts.db"),
            })
            first_client = app.test_client()
            second_client = app.test_client()

            missing_names = first_client.post("/api/auth/register", json={
                "username": "no_names",
                "password": "test-password-123",
            })
            self.assertEqual(missing_names.status_code, 400)

            response = first_client.post("/api/auth/register", json={
                "username": "Runner_1",
                "password": "test-password-123",
                "first_name": " Ada ",
                "last_name": " Runner ",
            })
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json()["user"]["username"], "runner_1")
            self.assertEqual(response.get_json()["user"]["first_name"], "Ada")
            self.assertEqual(response.get_json()["user"]["last_name"], "Runner")
            self.assertEqual(
                first_client.get("/api/auth/me").get_json()["user"]["first_name"],
                "Ada",
            )
            options = first_client.get("/api/options").get_json()
            self.assertEqual(
                options["levels"]["first_pushup"],
                ["beginner", "intermediate", "advanced"],
            )

            duplicate = second_client.post("/api/auth/register", json={
                "username": "RUNNER_1",
                "password": "another-password",
                "first_name": "Another",
                "last_name": "Runner",
            })
            self.assertEqual(duplicate.status_code, 409)
            second_registration = second_client.post("/api/auth/register", json={
                "username": "runner_2",
                "password": "second-password-123",
                "first_name": "Second",
                "last_name": "Runner",
            })
            self.assertEqual(second_registration.status_code, 201)

            saved = first_client.post("/api/workouts", json={
                "goal": "first_pushup",
                "completed_exercises": [1],
            })
            self.assertEqual(saved.status_code, 201)
            session_id = saved.get_json()["session_id"]

            self.assertEqual(len(first_client.get("/api/history").get_json()), 1)
            self.assertEqual(second_client.get("/api/history").get_json(), [])

            self.assertEqual(second_client.get("/api/history").get_json(), [])
            self.assertEqual(
                second_client.get("/api/history/" + session_id).status_code,
                404,
            )

            second_client.post("/api/auth/logout")
            login = second_client.post("/api/auth/login", json={
                "username": "runner_2",
                "password": "second-password-123",
            })
            self.assertEqual(login.status_code, 200)
            self.assertEqual(login.get_json()["user"]["first_name"], "Second")
            self.assertEqual(second_client.get("/api/history").get_json(), [])
            second_client.post("/api/auth/logout")
            self.assertEqual(
                second_client.post("/api/recommendations", json={}).status_code,
                401,
            )

    def test_existing_user_table_migrates_name_columns(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = str(Path(temp_dir) / "legacy-users.db")
            with closing(sqlite3.connect(db_path)) as connection:
                with connection:
                    connection.execute("""
                        CREATE TABLE users (
                            id INTEGER PRIMARY KEY,
                            username TEXT NOT NULL UNIQUE,
                            password_hash TEXT NOT NULL,
                            created_at TEXT NOT NULL
                        )
                    """)
                    connection.execute("""
                        INSERT INTO users (username, password_hash, created_at)
                        VALUES ('legacy', 'hash', '2026-01-01T00:00:00')
                    """)

            initialize_database(db_path)
            user = get_user_by_id(1, db_path)

        self.assertEqual(user["first_name"], "")
        self.assertEqual(user["last_name"], "")


if __name__ == "__main__":
    unittest.main()
