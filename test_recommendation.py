import unittest

from audit_workout_coverage import run_coverage_audit
from exercises import all_exercises
from exercises import excluded_recommendation_ids
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
        for exercise in all_exercises:
            ids.append(exercise["id"])
        self.assertEqual(ids[:150], list(range(1, 151)))
        self.assertEqual(ids[150:], list(range(151, 177)))
        self.assertEqual(
            {exercise["id"] for exercise in all_exercises}
            - {exercise["id"] for exercise in exercises},
            set(excluded_recommendation_ids),
        )

    def test_names_are_unique(self):
        names = []
        for exercise in all_exercises:
            names.append(exercise["name"])
        self.assertEqual(len(names), len(set(names)))

    def test_required_fields_and_types(self):
        for exercise in all_exercises:
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
        for exercise in all_exercises:
            names.append(exercise["name"])
        for exercise in all_exercises:
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

    def test_recommendations_never_relax_selected_filters(self):
        requests = [
            ("first_pushup", "beginner", [], 30),
            ("upper_body_strength", "intermediate", ["dumbbells"], 30),
            (
                "cardio",
                "advanced",
                ["bar", "bench", "chair", "dumbbells", "resistance_band", "step", "wall"],
                30,
            ),
        ]
        for goal, level, equipment, duration in requests:
            workout = recommend_workout(
                goal,
                level,
                equipment,
                duration,
                random_seed=10,
            )
            for exercise in workout:
                self.assertIn(goal, exercise["goals"])
                self.assertEqual(exercise["level"], level)
                self.assertTrue(set(exercise["equipment"]).issubset(equipment))

        self.assertTrue(recommend_workout(
            "lower_body_strength",
            "advanced",
            ["bar", "bench", "chair", "dumbbells", "resistance_band", "step", "wall"],
            180,
        ))

    def test_selected_equipment_is_prioritized_over_bodyweight(self):
        workout = recommend_workout(
            "upper_body_strength",
            "beginner",
            ["dumbbells"],
            30,
            random_seed=10,
        )

        equipped_count = sum(bool(exercise["equipment"]) for exercise in workout)
        self.assertGreater(equipped_count, 0)
        self.assertTrue(all(exercise["equipment"] for exercise in workout[:equipped_count]))
        self.assertTrue(all(not exercise["equipment"] for exercise in workout[equipped_count:]))

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
        self.assertIn("advanced", get_available_levels("first_pushup"))
        self.assertEqual(get_available_levels(), ["beginner", "intermediate", "advanced"])
        self.assertIn("advanced", get_available_levels("cardio"))
        self.assertIn("dumbbells", get_available_equipment())
        self.assertNotIn("ball", get_available_equipment())

    def test_ball_exercise_is_preserved_but_never_recommended(self):
        source_record = next(
            exercise for exercise in all_exercises if exercise["id"] == 132
        )
        self.assertEqual(source_record["name"], "Single-leg Ball Pass")
        self.assertEqual(source_record["equipment"], ["ball"])
        self.assertNotIn(132, {exercise["id"] for exercise in exercises})
        for goal in get_available_goals():
            for level in ["beginner", "intermediate", "advanced"]:
                workout = recommend_workout(
                    goal, level, get_available_equipment(), 180, shuffle=False
                )
                self.assertNotIn(132, {exercise["id"] for exercise in workout})

    def test_every_supported_input_combination_generates_a_valid_plan(self):
        report = run_coverage_audit()
        self.assertEqual(report["tested"], 14 * 3 * 12 * (2 ** 7))
        self.assertEqual(report["failures"], [])
        self.assertEqual(report["passing"], report["tested"])
        self.assertGreaterEqual(report["minimum_unique_exercises"], 3)
        for result in report["combinations"]:
            self.assertGreaterEqual(result["unique_exercise_count"], 3)
            self.assertLessEqual(result["actual_duration"], result["duration"])

    def test_sparse_plans_have_three_distinct_ids_even_when_shuffled(self):
        requests = [
            ("posture", "advanced"),
            ("balance", "advanced"),
            ("first_pushup", "intermediate"),
            ("accessibility", "advanced"),
        ]
        for goal, level in requests:
            for seed in range(10):
                workout = recommend_workout(goal, level, [], 15, random_seed=seed)
                self.assertGreaterEqual(len({exercise["id"] for exercise in workout}), 3)
                self.assertLessEqual(calculate_workout_duration(workout), 15)


if __name__ == "__main__":
    unittest.main()
