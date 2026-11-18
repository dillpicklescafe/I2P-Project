from exercises import exercises

def recommend_workout(goal, level, available_equipment, duration):

    workout = []
    total_duration = 0

    for exercise in exercises:

        if goal not in exercise["goals"]:
            continue

        if exercise["level"] != level:
            continue

        equipment_matches = True

        for item in exercise["equipment"]:
            if item not in available_equipment:
                equipment_matches = False

        if not equipment_matches:
            continue

        if total_duration + exercise["duration"] <= duration:

            workout.append(exercise)
            total_duration += exercise["duration"]

    return workout


def calculate_workout_duration(workout):

    total_duration = 0

    for exercise in workout:
        total_duration += exercise["duration"]

    return total_duration


def display_workout(workout):

    if len(workout) == 0:
        print("No suitable exercises found.")
        return

    print("\nYour Recommended Workout")
    print("------------------------")

    for exercise in workout:
        print("Exercise:", exercise["name"])
        print("Sets:", exercise["sets"])
        print("Reps:", exercise["reps"])
        print("Duration:", exercise["duration"], "minutes")
        print("------------------------")

    total_duration = calculate_workout_duration(workout)

    print("Total workout duration:", total_duration, "minutes")


# Test recommendation system
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