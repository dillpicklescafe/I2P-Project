"""Exhaustive workout-plan coverage audit for LockIn's supported inputs."""

from collections import Counter
from itertools import combinations

from exercise_media import get_exercise_media
from exercises import exercises
from recommendation import (
    MIN_EXERCISES_PER_WORKOUT,
    VALID_LEVELS,
    calculate_workout_duration,
    filter_exercises,
    get_available_equipment,
    get_available_goals,
    recommend_workout,
)


SUPPORTED_TIMES = list(range(15, 181, 15))


def equipment_selections():
    equipment = get_available_equipment()
    return [
        list(selection)
        for size in range(len(equipment) + 1)
        for selection in combinations(equipment, size)
    ]


def run_coverage_audit():
    """Generate and assess plans for every supported input combination."""
    failures = []
    combinations_report = []
    coverage_by_goal_difficulty = {}
    tested = 0
    selections = equipment_selections()

    for goal in get_available_goals():
        for level in VALID_LEVELS:
            for duration in SUPPORTED_TIMES:
                for equipment in selections:
                    tested += 1
                    workout = recommend_workout(
                        goal, level, equipment, duration, shuffle=False
                    )
                    unique_count = len({exercise["id"] for exercise in workout})
                    actual_duration = calculate_workout_duration(workout)
                    eligible = filter_exercises(goal, level, equipment)
                    result = {
                        "goal": goal,
                        "level": level,
                        "duration": duration,
                        "equipment": equipment,
                        "eligible_count": len(eligible),
                        "unique_exercise_count": unique_count,
                        "actual_duration": actual_duration,
                    }
                    combinations_report.append(result)

                    group = coverage_by_goal_difficulty.setdefault(
                        (goal, level),
                        {
                            "tested": 0, "passing": 0,
                            "workout_0": 0, "workout_1": 0,
                            "workout_2": 0, "workout_3_or_more": 0,
                            "eligible_0": 0, "eligible_1": 0,
                            "eligible_2": 0, "eligible_3_or_more": 0,
                        },
                    )
                    group["tested"] += 1
                    workout_bucket = (
                        str(unique_count) if unique_count < 3 else "3_or_more"
                    )
                    eligible_bucket = (
                        str(len(eligible)) if len(eligible) < 3 else "3_or_more"
                    )
                    group["workout_" + workout_bucket] += 1
                    group["eligible_" + eligible_bucket] += 1

                    if unique_count < MIN_EXERCISES_PER_WORKOUT:
                        if len(eligible) < MIN_EXERCISES_PER_WORKOUT:
                            all_equipment = get_available_equipment()
                            unrestricted = filter_exercises(goal, level, all_equipment)
                            reason = (
                                "equipment filtering"
                                if len(unrestricted) >= MIN_EXERCISES_PER_WORKOUT
                                else "insufficient candidates"
                            )
                        elif sum(sorted(
                            exercise["duration"] for exercise in eligible
                        )[:MIN_EXERCISES_PER_WORKOUT]) > duration:
                            reason = "duration constraints"
                        else:
                            reason = "another issue"
                        failures.append({
                            **result,
                            "reason": reason,
                        })
                        continue

                    group["passing"] += 1
                    assert actual_duration <= duration
                    for exercise in workout:
                        assert goal in exercise["goals"]
                        assert exercise["level"] == level
                        assert set(exercise["equipment"]).issubset(equipment)

    return {
        "tested": tested,
        "passing": tested - len(failures),
        "failures": failures,
        "minimum_unique_exercises": min(
            result["unique_exercise_count"] for result in combinations_report
        ),
        "combinations": combinations_report,
        "coverage_by_goal_difficulty": coverage_by_goal_difficulty,
        "active_exercises": len(exercises),
        "difficulty_breakdown": dict(Counter(
            exercise["level"] for exercise in exercises
        )),
        "missing_media": [
            {"id": exercise["id"], "name": exercise["name"]}
            for exercise in exercises
            if get_exercise_media(exercise["id"]) is None
        ],
    }


if __name__ == "__main__":
    report = run_coverage_audit()
    print("Combinations tested:", report["tested"])
    print("Combinations passing:", report["passing"])
    print("Failing combinations:", len(report["failures"]))
    print("Failure reasons:", dict(Counter(
        failure["reason"] for failure in report["failures"]
    )))
    print("Minimum unique exercises:", report["minimum_unique_exercises"])
    print("Coverage by goal and difficulty:")
    for (goal, level), coverage in report["coverage_by_goal_difficulty"].items():
        print(" ", goal, level, coverage)
    print("Active exercises:", report["active_exercises"])
    print("Difficulty breakdown:", report["difficulty_breakdown"])
    print("Exercises lacking approved media:", len(report["missing_media"]))
    for exercise in report["missing_media"]:
        print("  {id}: {name}".format(**exercise))
