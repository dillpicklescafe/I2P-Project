from contextlib import closing
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import (
    build_recommendation,
    create_app,
    get_exercise_keywords,
    save_completed_workout,
)
from exercises import exercises
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
        self.assertTrue(all("goals" in exercise for exercise in result))
        self.assertTrue(all(exercise["keywords"] for exercise in result))
        self.assertTrue(all(exercise["level"] == "beginner" for exercise in result))
        self.assertTrue(all(exercise["duration"] <= 30 for exercise in result))
        source_by_id = {exercise["id"]: exercise for exercise in exercises}
        for exercise in result:
            self.assertEqual(exercise["goals"], source_by_id[exercise["id"]]["goals"])

    def test_replacement_gifs_are_attached_and_served(self):
        expected_paths = {
            103: "exercises/103-replacement.gif",
            124: "exercises/124-replacement.gif",
            151: "exercises/151-replacement.gif",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            client = create_app({
                "TESTING": True,
                "SECRET_KEY": "test-secret-key",
                "DATABASE": str(Path(temp_dir) / "media.db"),
            }).test_client()

            for exercise_id, media_path in expected_paths.items():
                with self.subTest(exercise_id=exercise_id):
                    exercise = next(
                        item for item in exercises if item["id"] == exercise_id
                    )
                    with patch("app.recommend_workout", return_value=[exercise]):
                        recommendation = build_recommendation({
                            "goal": exercise["goals"][0],
                            "level": exercise["level"],
                            "equipment": [],
                            "duration": 30,
                        })[0]

                    self.assertEqual(
                        recommendation["media_url"],
                        "/static/" + media_path,
                    )
                    self.assertEqual(recommendation["media_type"], "gif")
                    response = client.get(recommendation["media_url"])
                    try:
                        self.assertEqual(response.status_code, 200)
                        self.assertEqual(response.mimetype, "image/gif")
                        self.assertTrue(
                            response.data.startswith((b"GIF87a", b"GIF89a"))
                        )
                    finally:
                        response.close()

    def test_speed_skater_has_specific_display_keywords(self):
        speed_skater = next(
            exercise for exercise in exercises if exercise["name"] == "Speed Skater"
        )
        self.assertEqual(
            get_exercise_keywords(speed_skater),
            ["balance", "legs", "cardio"],
        )

    def test_exercise_library_returns_filterable_catalog_for_authenticated_users(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            app = create_app({
                "TESTING": True,
                "SECRET_KEY": "test-secret-key",
                "DATABASE": str(Path(temp_dir) / "library.db"),
            })
            client = app.test_client()
            self.assertEqual(client.get("/api/library").status_code, 401)

            registration = client.post("/api/auth/register", json={
                "username": "library_user",
                "password": "test-password-123",
                "first_name": "Library",
                "last_name": "User",
            })
            self.assertEqual(registration.status_code, 201)

            response = client.get("/api/library")
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(len(data["exercises"]), len(exercises))
            self.assertIn("dumbbells", data["equipment"])
            self.assertIn("core", data["targets"])
            self.assertIn("cardio", data["targets"])
            preview_fields = {
                "id", "name", "goals", "level", "body_area", "equipment",
                "type", "duration", "sets", "reps", "hold_seconds",
                "work_seconds", "rest_seconds", "instructions", "media_url",
                "media_type",
            }
            self.assertTrue(all(
                preview_fields <= exercise.keys()
                for exercise in data["exercises"]
            ))
            source_by_id = {exercise["id"]: exercise for exercise in exercises}
            for exercise in data["exercises"]:
                source = source_by_id[exercise["id"]]
                for field in (
                    "goals", "level", "duration", "sets", "reps",
                    "hold_seconds", "work_seconds", "rest_seconds",
                    "instructions",
                ):
                    self.assertEqual(exercise[field], source.get(field))

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

    def test_save_completed_workout_stores_completed_set_count(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = str(Path(temp_dir) / "workouts.db")
            session_id = save_completed_workout({
                "goal": "first_pushup",
                "completed_sets": [{"exercise_id": 1, "sets_completed": 1}],
            }, db_path)

            saved_workout = get_workout_by_id(session_id, db_path)

        self.assertEqual(saved_workout["exercises"][0]["exercise_id"], 1)
        self.assertEqual(saved_workout["exercises"][0]["sets_completed"], 1)

    def test_save_completed_workout_rejects_too_many_sets(self):
        with self.assertRaises(ValueError):
            save_completed_workout({
                "goal": "first_pushup",
                "completed_sets": [{"exercise_id": 1, "sets_completed": 3}],
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
            advanced_plan = first_client.post("/api/recommendations", json={
                "goal": "lower_body_strength",
                "level": "advanced",
                "equipment": [
                    "bar",
                    "bench",
                    "chair",
                    "dumbbells",
                    "resistance_band",
                    "step",
                    "wall",
                ],
                "duration": 180,
            })
            self.assertEqual(advanced_plan.status_code, 200)
            self.assertTrue(advanced_plan.get_json()["exercises"])
            self.assertIsNone(advanced_plan.get_json()["empty_message"])

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

    def test_active_workout_progress_survives_logout_and_moves_to_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            app = create_app({
                "TESTING": True,
                "SECRET_KEY": "test-secret-key",
                "DATABASE": str(Path(temp_dir) / "active-workout.db"),
            })
            client = app.test_client()
            registration = client.post("/api/auth/register", json={
                "username": "active_runner",
                "password": "test-password-123",
                "first_name": "Active",
                "last_name": "Runner",
            })
            self.assertEqual(registration.status_code, 201)

            preferences = {
                "goal": "first_pushup",
                "level": "beginner",
                "equipment": [],
                "duration": 30,
            }
            preview = client.post("/api/recommendations", json=preferences)
            self.assertEqual(preview.status_code, 200)
            preview_data = preview.get_json()
            started = client.post("/api/active-workout", json={
                **preferences,
                "structure_mode": "stagger",
                "recommendation_seed": preview_data["recommendation_seed"],
            })
            self.assertEqual(started.status_code, 201)
            active_workout = started.get_json()["active_workout"]
            self.assertEqual(
                [exercise["id"] for exercise in active_workout["exercises"]],
                [exercise["id"] for exercise in preview_data["exercises"]],
            )
            self.assertEqual(active_workout["structure_mode"], "stagger")
            exercise_id = active_workout["exercises"][0]["id"]
            progress = {
                "session_id": active_workout["session_id"],
                "structure_mode": "stagger",
                "completed_set_keys": [f"{exercise_id}:1"],
                "notes": "Keep going",
            }
            updated = client.put("/api/active-workout", json=progress)
            self.assertEqual(updated.status_code, 200)

            client.post("/api/auth/logout")
            self.assertEqual(client.get("/api/active-workout").status_code, 401)
            login = client.post("/api/auth/login", json={
                "username": "active_runner",
                "password": "test-password-123",
            })
            self.assertEqual(login.status_code, 200)
            restored = client.get("/api/active-workout").get_json()["active_workout"]
            self.assertEqual(restored["session_id"], active_workout["session_id"])
            self.assertEqual(restored["structure_mode"], "stagger")
            self.assertEqual(restored["completed_set_keys"], [f"{exercise_id}:1"])
            self.assertEqual(restored["notes"], "Keep going")

            saved = client.post("/api/workouts", json=progress)
            self.assertEqual(saved.status_code, 201)
            self.assertEqual(
                client.get("/api/active-workout").get_json()["active_workout"],
                None,
            )
            history = client.get("/api/history").get_json()
            self.assertEqual(len(history), 1)
            self.assertEqual(history[0]["total_sets"], 1)

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
