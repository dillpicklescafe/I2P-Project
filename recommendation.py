import random
from exercises import exercises


def recommend_workout(goal, level, available_equipment, duration, shuffle=True):

    workout = []
    total_duration = 0

    candidates = list(exercises)
    if shuffle:
        random.shuffle(candidates)

    for exercise in candidates:

        if goal not in exercise["goals"]:
            continue

        if exercise["level"] != level:
            continue

        equipment_matches = all(
            item in available_equipment for item in exercise["equipment"]
        )

        if not equipment_matches:
            continue

        if total_duration + exercise["duration"] <= duration:
            workout.append(exercise)
            total_duration += exercise["duration"]

    return workout


def calculate_workout_duration(workout):
    return sum(exercise["duration"] for exercise in workout)


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