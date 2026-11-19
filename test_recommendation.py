import unittest

from exercises import exercises
from recommendation import calculate_interval_seconds
from recommendation import calculate_workout_duration
from recommendation import filter_exercises
from recommendation import get_available_equipment
from recommendation import get_available_goals
from recommendation import get_available_levels
from recommendation import recommend_workout


REQUIRED_FIELDS = [
    "id", "name", "goals", "level", "body_area", "exercise_type",
    "equipment", "position", "sets", "reps", "hold_seconds",
    "work_seconds", "rest_seconds", "duration", "instructions",
    "easier_variation", "harder_variation", "video_url"
]


class ExerciseDatabaseTests(unittest.TestCase):
    def test_original_source_ids_are_preserved(self):
        ids = []
        for exercise in exercises:
            ids.append(exercise["id"])
        excluded_ids = {
            31, 38, 41, 44, 45, 48, 50, 54, 55, 57,
            58, 59, 62, 63, 64, 67, 69, 72, 73, 74,
            75, 77, 84, 87, 90, 97, 103, 104, 112, 113,
            114, 117, 119, 124, 126, 128, 132, 133, 135, 136
        }
        expected_ids = []
        for source_id in range(1, 151):
            if source_id not in excluded_ids:
                expected_ids.append(source_id)
        self.assertEqual(ids, expected_ids)

    def test_names_are_unique(self):
        names = []
        for exercise in exercises:
            names.append(exercise["name"])
        self.assertEqual(len(names), len(set(names)))

    def test_required_fields_and_types(self):
        for exercise in exercises:
            for field in REQUIRED_FIELDS:
                self.assertIn(field, exercise)
            self.assertIsInstance(exercise["id"], int)
            self.assertIsInstance(exercise["name"], str)
            self.assertIsInstance(exercise["goals"], list)
            self.assertIsInstance(exercise["body_area"], list)
            self.assertIsInstance(exercise["equipment"], list)
            self.assertIsInstance(exercise["instructions"], list)
            self.assertIn(exercise["level"], ["beginner", "intermediate", "advanced"])
            self.assertGreater(exercise["duration"], 0)

    def test_variations_exist_when_provided(self):
        names = []
        for exercise in exercises:
            names.append(exercise["name"])
        for exercise in exercises:
            for field in ["easier_variation", "harder_variation"]:
                variation = exercise[field]
                self.assertTrue(variation is None or variation in names)

    def test_video_url_formats(self):
        for exercise in exercises:
            video_url = exercise["video_url"]
            self.assertTrue(
                video_url is None or
                video_url.startswith("https://www.youtube.com/embed/")
            )

    def test_cardio_interval_fields(self):
        timed_cardio_names = [
            "Jumping Jack", "High Knees", "Butt Kicks", "Mountain Climber",
            "Elevated Mountain Climber", "Shadow Boxing", "Speed Skater",
            "Invisible Jump Rope"
        ]

        for exercise in exercises:
            if exercise["name"] in timed_cardio_names:
                self.assertIsInstance(exercise["work_seconds"], int)
                self.assertIsInstance(exercise["rest_seconds"], int)
                self.assertGreater(exercise["work_seconds"], 0)
                self.assertGreaterEqual(exercise["rest_seconds"], 0)
            else:
                self.assertIsNone(exercise["work_seconds"])
                self.assertIsNone(exercise["rest_seconds"])

    def test_cardio_intervals_fit_duration_estimates(self):
        for exercise in exercises:
            interval_seconds = calculate_interval_seconds(exercise)
            if interval_seconds is not None:
                self.assertLessEqual(
                    interval_seconds,
                    exercise["duration"] * 60
                )


class RecommendationTests(unittest.TestCase):
    def test_equipment_filtering(self):
        results = filter_exercises("upper_body_strength", "beginner", [])
        for exercise in results:
            self.assertEqual(exercise["equipment"], [])

    def test_difficulty_filtering(self):
        results = filter_exercises("cardio", "intermediate", [])
        for exercise in results:
            self.assertEqual(exercise["level"], "intermediate")

    def test_goal_filtering(self):
        goal = get_available_goals()[0]
        results = filter_exercises(goal, "beginner", [
            "bench", "chair", "dumbbells", "resistance_band", "wall"
        ])
        for exercise in results:
            self.assertIn(goal, exercise["goals"])

    def test_duration_and_no_duplicates(self):
        workout = recommend_workout("cardio", "beginner", [], 15,
                                    random_seed=10)
        self.assertLessEqual(calculate_workout_duration(workout), 15)
        names = []
        for exercise in workout:
            names.append(exercise["name"])
        self.assertEqual(len(names), len(set(names)))

    def test_invalid_inputs_do_not_crash(self):
        self.assertEqual(recommend_workout("not_a_goal", "beginner", [], 10), [])
        self.assertEqual(recommend_workout("mobility", "expert", [], 10), [])
        self.assertEqual(recommend_workout("mobility", "beginner", None, 10), [])
        self.assertEqual(recommend_workout(
            "mobility", "beginner", ["not_equipment"], 10
        ), [])
        self.assertEqual(recommend_workout("mobility", "beginner", [], -1), [])
        self.assertEqual(recommend_workout("mobility", "beginner", [], "ten"), [])

    def test_empty_result_is_handled(self):
        workout = recommend_workout("first_pushup", "advanced", [], 1)
        self.assertEqual(workout, [])

    def test_database_is_not_changed(self):
        original_first_name = exercises[0]["name"]
        workout = recommend_workout("first_pushup", "beginner", [], 10)
        if workout:
            workout[0]["name"] = "Changed only in result"
        self.assertEqual(exercises[0]["name"], original_first_name)

    def test_progression_variations_are_not_repeated(self):
        workout = recommend_workout("first_pushup", "beginner", [], 20,
                                    shuffle=False)
        names = []
        for exercise in workout:
            names.append(exercise["name"])
        self.assertFalse("Wall Push-up" in names and "Incline Push-up" in names)
        self.assertFalse("Wall Push-up" in names and "Knee Push-up" in names)

    def test_option_helpers_return_database_values(self):
        self.assertIn("cardio", get_available_goals())
        self.assertEqual(get_available_levels("first_pushup"), ["beginner"])
        self.assertEqual(get_available_levels(), ["beginner", "intermediate"])
        self.assertNotIn("advanced", get_available_levels("cardio"))
        self.assertIn("dumbbells", get_available_equipment())


if __name__ == "__main__":
    unittest.main()
