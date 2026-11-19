import random
from exercises import exercises


VALID_LEVELS = ["beginner", "intermediate", "advanced"]
MIN_EXERCISES_FOR_LEVEL = 2


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
    """Return equipment names used by the active exercise database."""
    equipment_options = []

    for exercise in exercises:
        for item in exercise["equipment"]:
            if item not in equipment_options:
                equipment_options.append(item)

    return sorted(equipment_options)


def filter_exercises(goal, level, available_equipment):
    """Return matching exercises without changing the database."""
    if not isinstance(goal, str) or goal not in get_available_goals():
        return []
    if level not in VALID_LEVELS:
        return []
    if not isinstance(available_equipment, (list, tuple, set)):
        return []

    normalized_equipment = []
    for item in available_equipment:
        if not isinstance(item, str):
            return []
        normalized_item = item.strip().lower().replace(" ", "_")
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

    workout = []
    total_duration = 0
    used_body_areas = []
    candidates = filter_exercises(goal, level, available_equipment)

    if shuffle:
        random_generator = random.Random(random_seed)
        random_generator.shuffle(candidates)

    # Prefer a new main body area before adding another similar exercise.
    varied_candidates = []
    repeated_candidates = []

    for exercise in candidates:
        main_body_area = exercise["body_area"][0]
        if main_body_area not in used_body_areas:
            varied_candidates.append(exercise)
            used_body_areas.append(main_body_area)
        else:
            repeated_candidates.append(exercise)

    candidates = varied_candidates + repeated_candidates
    selected_names = []

    for exercise in candidates:
        if exercise["name"] in selected_names:
            continue

        # Easier and harder variations teach the same movement progression.
        # Use only one variation in a workout to avoid unnecessary repetition.
        is_progression_duplicate = False
        for selected_exercise in workout:
            selected_variations = [
                selected_exercise["easier_variation"],
                selected_exercise["harder_variation"]
            ]
            exercise_variations = [
                exercise["easier_variation"],
                exercise["harder_variation"]
            ]
            if exercise["name"] in selected_variations:
                is_progression_duplicate = True
            if selected_exercise["name"] in exercise_variations:
                is_progression_duplicate = True

        if is_progression_duplicate:
            continue

        if total_duration + exercise["duration"] <= duration:
            workout.append(exercise)
            selected_names.append(exercise["name"])
            total_duration += exercise["duration"]

    return workout


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
