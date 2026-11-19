from datetime import datetime


def start_workout(goal=None, notes=""):
    """
    Create a new workout session.
    """

    session = {
        "session_id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "date": datetime.now().isoformat(timespec="seconds"),
        "goal": goal,
        "notes": notes,
        "exercises": [],
        "completed": False
    }

    return session


def add_exercise(session, exercise, sets_completed,
                 reps_completed=None, duration_minutes=0, notes=""):
    """
    Add an exercise that the user has actually completed.
    """

    if not isinstance(sets_completed, int) or isinstance(sets_completed, bool) or sets_completed <= 0:
        raise ValueError("Sets completed must be a positive integer.")

    if reps_completed is not None:
        if not isinstance(reps_completed, int) or isinstance(reps_completed, bool) or reps_completed <= 0:
            raise ValueError("Repetitions must be a positive integer.")

    if not isinstance(duration_minutes, (int, float)) or isinstance(duration_minutes, bool) or duration_minutes < 0:
        raise ValueError("Duration must be a non-negative number.")

    if not isinstance(exercise, dict) or not exercise.get("name"):
        raise ValueError("A valid exercise dictionary is required.")

    completed_exercise = {
        "name": exercise["name"],
        "sets_completed": sets_completed,
        "reps_completed": reps_completed,
        "duration_minutes": duration_minutes,
        "notes": notes
    }

    session["exercises"].append(completed_exercise)

    return completed_exercise


def calculate_total_duration(session):
    """
    Calculate the total actual exercise duration.
    """

    total = 0

    for exercise in session["exercises"]:
        total += exercise["duration_minutes"]

    return total


def complete_workout(session):
    """
    Mark a workout session as completed.
    """

    if not session["exercises"]:
        raise ValueError("Cannot complete an empty workout.")

    session["completed"] = True
    session["completed_at"] = datetime.now().isoformat(timespec="seconds")

    return session


def get_workout_summary(session):
    """
    Generate a summary of a workout session.
    """

    total_exercises = len(session["exercises"])
    total_sets = sum(
        exercise["sets_completed"]
        for exercise in session["exercises"]
    )

    total_duration = calculate_total_duration(session)

    return {
        "session_id": session["session_id"],
        "date": session["date"],
        "goal": session["goal"],
        "total_exercises": total_exercises,
        "total_sets": total_sets,
        "total_duration": total_duration,
        "completed": session["completed"]
    }
