import random
from itertools import combinations
from math import ceil
from exercises import exercises


VALID_LEVELS = ["beginner", "intermediate", "advanced"]
MIN_EXERCISES_FOR_LEVEL = 1
MIN_EXERCISES_PER_WORKOUT = 3
TRANSITION_SECONDS = 30
MAX_SETS_PER_EXERCISE = 6
REP_SECONDS_BY_TYPE = {
    "strength": 4,
    "stability": 4,
    "balance": 4,
    "mobility": 4,
    "coordination": 4,
    "cardio": 3,
    "plyometric": 2,
}
REST_SECONDS_BY_TYPE = {
    "strength": {"beginner": 60, "intermediate": 90, "advanced": 120},
    "stability": 45,
    "balance": 45,
    "mobility": 15,
    "flexibility": 15,
    "coordination": 30,
    "cardio": 30,
    "plyometric": 90,
}
REP_RANGES_BY_LEVEL = {
    "beginner": (10, 12),
    "intermediate": (12, 16),
    "advanced": (15, 20),
}
SUPPORTED_EQUIPMENT = [
    "bar", "bench", "chair", "dumbbells", "resistance_band", "step", "wall"
]


def get_available_goals():
    """Return all fitness goals found in the exercise database."""
    goals = []

    for exercise in exercises:
        for goal in exercise["goals"]:
            if goal not in goals:
                goals.append(goal)

    return sorted(goals)


def get_available_levels(goal=None):
    """Return levels with enough exercises for a meaningful recommendation."""
    level_counts = {}

    for level in VALID_LEVELS:
        level_counts[level] = 0

    if goal is not None:
        for exercise in exercises:
            if goal in exercise["goals"]:
                level_counts[exercise["level"]] += 1
    else:
        # A general dropdown should only show a level that is meaningful for
        # at least one fitness goal.
        for available_goal in get_available_goals():
            goal_level_counts = {}
            for level in VALID_LEVELS:
                goal_level_counts[level] = 0
            for exercise in exercises:
                if available_goal in exercise["goals"]:
                    goal_level_counts[exercise["level"]] += 1
            for level in VALID_LEVELS:
                if goal_level_counts[level] > level_counts[level]:
                    level_counts[level] = goal_level_counts[level]

    ordered_levels = []
    for level in VALID_LEVELS:
        if level_counts[level] >= MIN_EXERCISES_FOR_LEVEL:
            ordered_levels.append(level)

    return ordered_levels


def get_available_equipment():
    """Return equipment choices supported by the planner UI."""
    return SUPPORTED_EQUIPMENT.copy()


def _rest_seconds(exercise):
    rest_seconds = exercise.get("rest_seconds")
    if rest_seconds is not None:
        return rest_seconds

    exercise_type = exercise["type"]
    if exercise_type == "strength":
        return REST_SECONDS_BY_TYPE[exercise_type][exercise["level"]]
    return REST_SECONDS_BY_TYPE.get(exercise_type, 30)


def _exercise_duration_seconds(exercise):
    """Estimate elapsed exercise time from its prescription and recovery."""
    sets = exercise["sets"]
    rest_seconds = _rest_seconds(exercise)

    if exercise["reps"] is not None:
        active_seconds = (
            sets
            * exercise["reps"]
            * REP_SECONDS_BY_TYPE.get(exercise["type"], 4)
        )
    elif exercise["hold_seconds"] is not None:
        active_seconds = sets * exercise["hold_seconds"]
    elif exercise["work_seconds"] is not None:
        active_seconds = sets * exercise["work_seconds"]
    else:
        active_seconds = sets * exercise["duration"] * 60

    between_set_rest = max(0, sets - 1) * rest_seconds
    return active_seconds + between_set_rest + TRANSITION_SECONDS


def _update_exercise_duration(exercise):
    exercise["duration"] = max(1, ceil(_exercise_duration_seconds(exercise) / 60))


def _prepare_exercise(exercise):
    """Copy an exercise and expose timed continuous cardio as a work interval."""
    prepared = exercise.copy()
    if prepared["reps"] is not None:
        min_reps, max_reps = REP_RANGES_BY_LEVEL[prepared["level"]]
        prepared["reps"] = min(max(prepared["reps"], min_reps), max_reps)
    if (
        prepared["type"] == "cardio"
        and prepared["reps"] is None
        and prepared["hold_seconds"] is None
        and prepared["work_seconds"] is None
    ):
        prepared["work_seconds"] = prepared["duration"] * 60
    if prepared["sets"] > 1 and prepared["rest_seconds"] is None:
        prepared["rest_seconds"] = _rest_seconds(prepared)
    _update_exercise_duration(prepared)
    return prepared


def _scale_exercise_volume(workout, duration):
    """Increase reps and sets in small steps without exceeding exercise limits."""
    duration_seconds = duration * 60
    total_seconds = sum(item["duration"] * 60 for item in workout)
    tolerance_seconds = max(2 * 60, round(duration_seconds * 0.05))
    if duration_seconds - total_seconds <= tolerance_seconds:
        return

    while True:
        changes = []
        for index, exercise in enumerate(workout):
            max_reps = REP_RANGES_BY_LEVEL[exercise["level"]][1]
            if exercise["reps"] is not None:
                next_reps = min(max_reps, exercise["reps"] + 2)
                if next_reps > exercise["reps"]:
                    candidate = exercise.copy()
                    candidate["reps"] = next_reps
                    candidate_seconds = ceil(_exercise_duration_seconds(candidate) / 60) * 60
                    changes.append((index, "reps", next_reps, candidate_seconds))

            if exercise["sets"] < MAX_SETS_PER_EXERCISE:
                candidate = exercise.copy()
                candidate["sets"] += 1
                if candidate["rest_seconds"] is None:
                    candidate["rest_seconds"] = _rest_seconds(candidate)
                candidate_seconds = ceil(_exercise_duration_seconds(candidate) / 60) * 60
                changes.append((index, "sets", candidate["sets"], candidate_seconds))

        fitting_changes = [
            change for change in changes
            if total_seconds - workout[change[0]]["duration"] * 60
            + change[3] <= duration_seconds
        ]
        if not fitting_changes:
            return

        index, field, value, candidate_seconds = max(
            fitting_changes,
            key=lambda change: (
                total_seconds
                - workout[change[0]]["duration"] * 60
                + change[3],
                change[1] == "sets",
                -change[0],
            ),
        )
        workout[index][field] = value
        if workout[index]["sets"] > 1 and workout[index]["rest_seconds"] is None:
            workout[index]["rest_seconds"] = _rest_seconds(workout[index])
        _update_exercise_duration(workout[index])
        total_seconds = sum(item["duration"] * 60 for item in workout)


def filter_exercises(goal, level, available_equipment):
    """Return matching exercises without changing the database."""
    if not isinstance(goal, str) or goal not in get_available_goals():
        return []
    if level not in VALID_LEVELS:
        return []
    if not isinstance(available_equipment, (list, tuple, set)):
        return []

    normalized_equipment = []
    valid_equipment = get_available_equipment()
    for item in available_equipment:
        if not isinstance(item, str):
            return []
        normalized_item = item.strip().lower().replace(" ", "_")
        if normalized_item not in valid_equipment:
            return []
        if normalized_item not in normalized_equipment:
            normalized_equipment.append(normalized_item)

    matches = []

    for exercise in exercises:
        if goal not in exercise["goals"]:
            continue
        if exercise["level"] != level:
            continue

        has_equipment = True
        for item in exercise["equipment"]:
            if item.lower().replace(" ", "_") not in normalized_equipment:
                has_equipment = False

        if has_equipment:
            matches.append(exercise.copy())

    return matches


def recommend_workout(goal, level, available_equipment, duration, shuffle=True,
                      random_seed=None):
    """Build a varied workout that does not exceed duration in minutes.

    Invalid inputs and valid searches with no matches both return an empty
    list, which is convenient for a Flask route to handle.
    """
    if not isinstance(duration, int) or isinstance(duration, bool):
        return []
    if duration <= 0:
        return []
    if not isinstance(shuffle, bool):
        return []

    candidates = filter_exercises(goal, level, available_equipment)

    if shuffle:
        random_generator = random.Random(random_seed)
        random_generator.shuffle(candidates)

    varied_candidates = []
    repeated_candidates = []
    used_body_areas = []

    for exercise in candidates:
        main_body_area = exercise["body_area"][0]
        if main_body_area not in used_body_areas:
            varied_candidates.append(exercise)
            used_body_areas.append(main_body_area)
        else:
            repeated_candidates.append(exercise)

    candidates = varied_candidates + repeated_candidates
    if available_equipment:
        candidates = [
            exercise for exercise in candidates
            if exercise["equipment"]
        ] + [
            exercise for exercise in candidates
            if not exercise["equipment"]
        ]

    def has_progression_conflict(first, second):
        first_variations = [first["easier_variation"], first["harder_variation"]]
        second_variations = [second["easier_variation"], second["harder_variation"]]
        return (
            first["name"] in second_variations
            or second["name"] in first_variations
        )

    def select_exercises(available_candidates):
        workout = []
        total_duration = 0
        # Reserve a varied three-exercise foundation before adding optional work.
        valid_foundations = []
        for foundation in combinations(
            available_candidates, MIN_EXERCISES_PER_WORKOUT
        ):
            if sum(exercise["duration"] for exercise in foundation) > duration:
                continue
            if any(
                has_progression_conflict(first, second)
                for first, second in combinations(foundation, 2)
            ):
                continue
            equipped_count = sum(
                bool(exercise["equipment"]) for exercise in foundation
            )
            body_area_count = len({
                exercise["body_area"][0] for exercise in foundation
            })
            valid_foundations.append(
                (equipped_count, body_area_count, foundation)
            )

        if valid_foundations:
            _, _, foundation = max(
                valid_foundations,
                key=lambda item: (item[0], item[1]),
            )
            workout.extend(foundation)
            total_duration = sum(exercise["duration"] for exercise in workout)

        selected_ids = {exercise["id"] for exercise in workout}
        for exercise in available_candidates:
            if exercise["id"] in selected_ids:
                continue
            if any(
                has_progression_conflict(exercise, selected_exercise)
                for selected_exercise in workout
            ):
                continue
            if total_duration + exercise["duration"] <= duration:
                workout.append(exercise)
                selected_ids.add(exercise["id"])
                total_duration += exercise["duration"]
        return workout

    workout = select_exercises(candidates)
    workout = [_prepare_exercise(exercise) for exercise in workout]
    if sum(exercise["duration"] for exercise in workout) > duration:
        prepared_candidates = [
            _prepare_exercise(exercise) for exercise in candidates
        ]
        workout = select_exercises(prepared_candidates)

    _scale_exercise_volume(workout, duration)
    for exercise in workout:
        _update_exercise_duration(exercise)
    return workout


def diagnose_empty_workout(goal, level, available_equipment, duration):
    """Classify why a request cannot produce a workout.

    The return value is ``None`` when actual plan generation succeeds.
    """
    if recommend_workout(
        goal, level, available_equipment, duration, shuffle=False
    ):
        return None
    if not isinstance(goal, str) or goal not in get_available_goals():
        return "no goal/difficulty match"
    if level not in VALID_LEVELS:
        return "no goal/difficulty match"
    if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
        return "duration constraints"
    if not isinstance(available_equipment, (list, tuple, set)):
        return "equipment filtering"

    goal_level_candidates = [
        exercise for exercise in exercises
        if goal in exercise["goals"] and exercise["level"] == level
    ]
    if not goal_level_candidates:
        return "no goal/difficulty match"
    equipped_candidates = filter_exercises(goal, level, available_equipment)
    if not equipped_candidates:
        return "equipment filtering"
    if not any(exercise["duration"] <= duration for exercise in equipped_candidates):
        return "duration constraints"
    if len(equipped_candidates) < 1:
        return "insufficient candidates"
    return "another issue"


def calculate_workout_duration(workout):
    total_duration = 0

    for exercise in workout:
        total_duration += exercise["duration"]

    return total_duration


def calculate_interval_seconds(exercise):
    """Return planned work and between-set rest time for timed cardio."""
    if exercise["work_seconds"] is None:
        return None

    work_time = exercise["sets"] * exercise["work_seconds"]
    rest_time = 0

    if exercise["sets"] > 1:
        rest_time = (exercise["sets"] - 1) * exercise["rest_seconds"]

    return work_time + rest_time


def display_workout(workout):

    if len(workout) == 0:
        print("No suitable exercises found.")
        return

    print("\nYour Recommended Workout")
    print("------------------------")

    for exercise in workout:
        print("Exercise:", exercise["name"])
        print("Sets:", exercise["sets"])

        if exercise["reps"] is not None:
            print("Reps:", exercise["reps"])
        elif exercise["hold_seconds"] is not None:
            print("Hold:", exercise["hold_seconds"], "seconds")
        elif exercise["work_seconds"] is not None:
            print("Work:", exercise["work_seconds"], "seconds per set")
            print("Rest:", exercise["rest_seconds"], "seconds between sets")
        else:
            print("Pace: Continuous for duration")

        print("Duration:", exercise["duration"], "minutes")
        print("------------------------")

    total_duration = calculate_workout_duration(workout)
    print("Total workout duration:", total_duration, "minutes")

if __name__ == "__main__":

    goal = "first_pushup"
    level = "beginner"
    available_equipment = []
    duration = 15

    workout = recommend_workout(
        goal,
        level,
        available_equipment,
        duration
    )

    display_workout(workout)
