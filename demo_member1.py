"""Terminal demonstration of the LockIn Member 1 recommendation system."""

from recommendation import calculate_workout_duration, recommend_workout


EXAMPLES = [
    {
        "title": "Beginner cardio (no equipment)",
        "goal": "cardio",
        "level": "beginner",
        "equipment": [],
        "duration": 15,
    },
    {
        "title": "First push-up practice (no equipment)",
        "goal": "first_pushup",
        "level": "beginner",
        "equipment": [],
        "duration": 10,
    },
    {
        "title": "Intermediate lower-body strength (dumbbells)",
        "goal": "lower_body_strength",
        "level": "intermediate",
        "equipment": ["dumbbells"],
        "duration": 20,
    },
]


def exercise_plan(exercise):
    """Return a simple display string for reps, holds, or intervals."""
    sets = exercise["sets"]
    if exercise["reps"] is not None:
        return f"{sets} sets x {exercise['reps']} reps"
    if exercise["hold_seconds"] is not None:
        return f"{sets} sets x {exercise['hold_seconds']}-second hold"
    if exercise["work_seconds"] is not None:
        return (
            f"{sets} sets x {exercise['work_seconds']} seconds work, "
            f"{exercise['rest_seconds']} seconds rest between sets"
        )
    return f"{sets} set(s), continuous movement"


def display_example(number, example):
    """Request and print one example workout."""
    workout = recommend_workout(
        goal=example["goal"],
        level=example["level"],
        available_equipment=example["equipment"],
        duration=example["duration"],
        random_seed=number,
    )

    print(f"\nExample {number}: {example['title']}")
    print("-" * 60)
    print(f"Goal: {example['goal']}")
    print(f"Difficulty: {example['level']}")
    print("Available equipment:", ", ".join(example["equipment"]) or "none")
    print(f"Available time: {example['duration']} minutes")

    if not workout:
        print("No suitable exercises found.")
        return

    print("Recommended exercises:")
    for index, exercise in enumerate(workout, 1):
        equipment = ", ".join(exercise["equipment"]) or "none"
        print(f"  {index}. {exercise['name']}")
        print(f"     Plan: {exercise_plan(exercise)}")
        print(f"     Equipment: {equipment}")
        print(f"     Estimated time: {exercise['duration']} minutes")

    print(
        "Estimated total workout duration:",
        calculate_workout_duration(workout),
        "minutes",
    )


def main():
    print("LockIn - Member 1 Recommendation Demo")
    print("Member 2 can use recommend_workout(...) and display its returned list.")
    for number, example in enumerate(EXAMPLES, 1):
        display_example(number, example)


if __name__ == "__main__":
    main()
