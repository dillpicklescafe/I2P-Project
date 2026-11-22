"""Flask application for the LockIn workout planner."""

import os
import secrets
import sqlite3
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    current_app,
    jsonify,
    request,
    send_from_directory,
    session,
)
from werkzeug.security import check_password_hash, generate_password_hash

from exercise_media import get_exercise_media
from exercises import exercises
from recommendation import (
    VALID_LEVELS,
    get_available_equipment,
    get_available_goals,
    filter_exercises,
    recommend_workout,
)
from workout_log import add_exercise, complete_workout, start_workout
from workout_storage import (
    DATABASE_NAME,
    create_user,
    get_user_by_id,
    get_user_by_username,
    get_active_workout,
    get_paused_workouts,
    get_workout_by_id,
    get_workout_history,
    get_workout_stats,
    initialize_database,
    pause_active_workout,
    resume_paused_workout,
    save_active_workout,
    save_workout,
)


PROJECT_DIR = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_DIR / "static"
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 32
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128


def get_exercise_keywords(exercise):
    """Collect concise focus terms from an exercise's existing metadata."""
    keywords = []
    candidates = exercise.get("keywords") or [
        *exercise["goals"],
        *exercise["body_area"],
        exercise["type"],
    ]
    for keyword in candidates:
        if keyword not in keywords:
            keywords.append(keyword)
    return keywords


def build_recommendation(data, random_seed=None):
    """Validate form selections and return recommended exercises for the UI."""
    goal = data.get("goal")
    level = data.get("level")
    equipment = data.get("equipment")
    duration = data.get("duration")

    if not isinstance(goal, str) or goal not in get_available_goals():
        raise ValueError("Choose a fitness goal from the available options.")
    if not isinstance(level, str) or level not in VALID_LEVELS:
        raise ValueError("Choose beginner, intermediate, or advanced difficulty.")
    if not isinstance(equipment, list) or any(
        not isinstance(item, str) or item not in get_available_equipment()
        for item in equipment
    ):
        raise ValueError("Choose equipment from the available options.")
    if (
        not isinstance(duration, int)
        or isinstance(duration, bool)
        or duration not in range(15, 181, 15)
    ):
        raise ValueError(
            "Choose a time from 15 minutes to 3 hours in 15-minute increments."
        )

    recommendations = recommend_workout(
        goal,
        level,
        equipment,
        duration,
        random_seed=random_seed,
    )
    result = []

    for exercise in recommendations:
        media = get_exercise_media(exercise["id"])
        media_url = None
        media_type = None
        if media and (STATIC_DIR / media["media_path"]).is_file():
            media_url = "/static/" + media["media_path"].replace("\\", "/")
            media_type = media["media_type"]

        result.append({
            "id": exercise["id"],
            "name": exercise["name"],
            "goals": exercise["goals"],
            "body_area": exercise["body_area"],
            "keywords": get_exercise_keywords(exercise),
            "level": exercise["level"],
            "sets": exercise["sets"],
            "reps": exercise.get("reps"),
            "hold_seconds": exercise.get("hold_seconds"),
            "work_seconds": exercise.get("work_seconds"),
            "rest_seconds": exercise.get("rest_seconds"),
            "duration": exercise["duration"],
            "instructions": exercise["instructions"],
            "equipment": exercise["equipment"],
            "media_url": media_url,
            "media_type": media_type,
        })

    return result


def save_completed_workout(
    data,
    db_path=DATABASE_NAME,
    user_id=None,
    session_id=None,
):
    """Save completed exercise sets as a workout for one account."""
    goal = data.get("goal")
    if not isinstance(goal, str) or goal not in get_available_goals():
        raise ValueError("Choose a valid fitness goal.")

    notes = data.get("notes", "")
    if not isinstance(notes, str):
        raise ValueError("Workout notes must be text.")

    exercise_by_id = {exercise["id"]: exercise for exercise in exercises}
    if "completed_sets" in data:
        completed_sets = data["completed_sets"]
        if not isinstance(completed_sets, list) or not completed_sets:
            raise ValueError("Mark at least one set as complete before saving.")

        completed_records = []
        for record in completed_sets:
            if not isinstance(record, dict):
                raise ValueError("The completed sets contain an invalid exercise.")
            exercise_id = record.get("exercise_id")
            sets_completed = record.get("sets_completed")
            if (
                not isinstance(exercise_id, int)
                or isinstance(exercise_id, bool)
                or exercise_id not in exercise_by_id
                or not isinstance(sets_completed, int)
                or isinstance(sets_completed, bool)
                or sets_completed < 1
                or sets_completed > exercise_by_id[exercise_id]["sets"]
            ):
                raise ValueError("The completed sets contain an invalid exercise or set count.")
            completed_records.append((exercise_id, sets_completed))
        if len({exercise_id for exercise_id, _ in completed_records}) != len(completed_records):
            raise ValueError("An exercise can only be recorded once per workout.")
    else:
        completed_ids = data.get("completed_exercises")
        if not isinstance(completed_ids, list) or not completed_ids:
            raise ValueError("Mark at least one exercise as complete before saving.")
        if any(
            not isinstance(exercise_id, int)
            or isinstance(exercise_id, bool)
            or exercise_id not in exercise_by_id
            for exercise_id in completed_ids
        ):
            raise ValueError("The completed exercises contain an invalid exercise.")
        if len(set(completed_ids)) != len(completed_ids):
            raise ValueError("An exercise can only be recorded once per workout.")
        completed_records = [
            (exercise_id, exercise_by_id[exercise_id]["sets"])
            for exercise_id in completed_ids
        ]

    session_data = start_workout(goal=goal, notes=notes)
    if session_id is not None:
        if not isinstance(session_id, str) or not session_id or len(session_id) > 128:
            raise ValueError("Workout session ID is invalid.")
        session_data["session_id"] = session_id
    for exercise_id, sets_completed in completed_records:
        exercise = exercise_by_id[exercise_id]
        add_exercise(
            session_data,
            exercise,
            sets_completed=sets_completed,
            reps_completed=exercise.get("reps"),
            duration_minutes=exercise["duration"],
        )

    complete_workout(session_data)
    return save_workout(session_data, db_path, user_id=user_id)


def recommendation_empty_message(data):
    matching_exercises = filter_exercises(
        data["goal"],
        data["level"],
        data["equipment"],
    )
    if matching_exercises:
        return (
            "Matching exercises exist, but they don't fit the "
            "selected time. Choose more time and try again."
        )
    return (
        "No exercises in the current library match all of "
        "these selections. Try another goal or difficulty; "
        "we won't substitute a different level or equipment."
    )


def build_active_workout(data, db_path=DATABASE_NAME, user_id=None):
    """Create and persist a server-owned active workout."""
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("User ID must be a positive integer.")

    recommendation_seed = data.get("recommendation_seed")
    if recommendation_seed is None:
        recommendation_seed = secrets.randbits(64)
    if (
        not isinstance(recommendation_seed, int)
        or isinstance(recommendation_seed, bool)
        or not 0 <= recommendation_seed < 2**64
    ):
        raise ValueError("Workout recommendation seed is invalid.")
    exercises_for_workout = build_recommendation(data, recommendation_seed)
    if not exercises_for_workout:
        return None

    structure_mode = data.get("structure_mode", "block")
    if structure_mode not in ("block", "stagger"):
        raise ValueError("Choose block or stagger workout structure.")

    active_workout = {
        "version": 1,
        "session_id": secrets.token_urlsafe(24),
        "goal": data["goal"],
        "level": data["level"],
        "duration": data["duration"],
        "equipment": data["equipment"],
        "exercises": exercises_for_workout,
        "structure_mode": structure_mode,
        "completed_set_keys": [],
        "saved": False,
        "notes": "",
    }
    save_active_workout(user_id, active_workout, db_path)
    return active_workout


def build_redo_workout(session_id, db_path=DATABASE_NAME, user_id=None):
    """Create a fresh active workout from a previously completed workout."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("User ID must be a positive integer.")

    # Do not overwrite an unfinished workout.
    existing_active = get_active_workout(user_id, db_path)
    if existing_active is not None:
        raise ValueError(
            "You already have an unfinished workout. Finish it before redoing another workout."
        )

    # Retrieve the original completed workout.
    original = get_workout_by_id(
        session_id,
        db_path,
        user_id=user_id,
    )

    if original is None or not original["completed"]:
        raise ValueError("Completed workout not found.")

    exercise_by_id = {
        exercise["id"]: exercise
        for exercise in exercises
    }

    rebuilt_exercises = []

    for record in original["exercises"]:
        exercise = exercise_by_id.get(record["exercise_id"])

        if exercise is None:
            raise ValueError(
                f"Exercise ID {record['exercise_id']} is no longer available."
            )

        media = get_exercise_media(exercise["id"])
        media_url = None
        media_type = None

        if media and (STATIC_DIR / media["media_path"]).is_file():
            media_url = "/static/" + media["media_path"].replace("\\", "/")
            media_type = media["media_type"]

        rebuilt_exercises.append({
            "id": exercise["id"],
            "name": exercise["name"],
            "keywords": get_exercise_keywords(exercise),
            "level": exercise["level"],
            "sets": exercise["sets"],
            "reps": exercise.get("reps"),
            "hold_seconds": exercise.get("hold_seconds"),
            "work_seconds": exercise.get("work_seconds"),
            "rest_seconds": exercise.get("rest_seconds"),
            "duration": exercise["duration"],
            "instructions": exercise["instructions"],
            "equipment": exercise["equipment"],
            "media_url": media_url,
            "media_type": media_type,
        })

    if not rebuilt_exercises:
        raise ValueError("This workout has no exercises to redo.")

    active_workout = {
        "version": 1,
        "session_id": secrets.token_urlsafe(24),
        "goal": original["goal"],
        "level": rebuilt_exercises[0]["level"],
        "duration": min(
            180,
            max(
                15,
                ((sum(exercise["duration"] for exercise in rebuilt_exercises) + 14) // 15) * 15
        )
),
        "equipment": list(dict.fromkeys(
            item
            for exercise in rebuilt_exercises
            for item in exercise["equipment"]
        )),
        "exercises": rebuilt_exercises,
        "structure_mode": "block",
        "completed_set_keys": [],
        "saved": False,
        "notes": "",
    }

    save_active_workout(user_id, active_workout, db_path)

    return active_workout

def update_active_workout_progress(active_workout, data):
    """Validate and apply progress updates to a user's active workout."""
    if data.get("session_id") != active_workout["session_id"]:
        raise ValueError("This active workout has changed. Reload the page and try again.")

    structure_mode = data.get("structure_mode")
    if structure_mode not in ("block", "stagger"):
        raise ValueError("Choose a valid workout structure.")

    notes = data.get("notes", "")
    if not isinstance(notes, str):
        raise ValueError("Workout notes must be text.")

    completed_set_keys = data.get("completed_set_keys")
    if not isinstance(completed_set_keys, list):
        raise ValueError("Completed sets must be a list.")
    valid_set_keys = {
        f"{exercise['id']}:{set_number}"
        for exercise in active_workout["exercises"]
        for set_number in range(1, exercise["sets"] + 1)
    }
    if (
        any(not isinstance(key, str) or key not in valid_set_keys for key in completed_set_keys)
        or len(set(completed_set_keys)) != len(completed_set_keys)
    ):
        raise ValueError("The completed sets don't match this workout.")

    updated_workout = dict(active_workout)
    updated_workout["structure_mode"] = structure_mode
    updated_workout["completed_set_keys"] = completed_set_keys
    updated_workout["notes"] = notes
    return updated_workout


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        static_folder=str(STATIC_DIR),
        static_url_path="/static",
    )
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32),
        DATABASE=str(PROJECT_DIR / DATABASE_NAME),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        MAX_CONTENT_LENGTH=1024 * 1024,
    )
    if test_config:
        app.config.update(test_config)
    initialize_database(app.config["DATABASE"])

    def authenticated_api(handler):
        @wraps(handler)
        def wrapped(*args, **kwargs):
            user_id = session.get("user_id")
            if not isinstance(user_id, int):
                return jsonify(error="Please log in to continue."), 401
            return handler(*args, **kwargs)
        return wrapped

    def json_body():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            raise ValueError("Request body must be a JSON object.")
        return data

    def database_error():
        current_app.logger.exception("Workout database request failed")
        return jsonify(error="A database error occurred. Please try again."), 500

    @app.get("/")
    def home():
        return send_from_directory(STATIC_DIR, "index.html")

    @app.get("/api/auth/me")
    def current_user():
        user_id = session.get("user_id")
        user = get_user_by_id(user_id, app.config["DATABASE"]) if isinstance(user_id, int) else None
        if user is None:
            session.clear()
            return jsonify(user=None)
        return jsonify(user={
            "id": user["id"],
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
        })

    @app.post("/api/auth/register")
    def register():
        try:
            data = json_body()
            username = data.get("username")
            password = data.get("password")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            if not isinstance(first_name, str) or not first_name.strip():
                raise ValueError("Enter your first name.")
            if not isinstance(last_name, str) or not last_name.strip():
                raise ValueError("Enter your last name.")
            first_name = first_name.strip()
            last_name = last_name.strip()
            if len(first_name) > 50 or len(last_name) > 50:
                raise ValueError("Names must be 50 characters or fewer.")
            if not isinstance(username, str):
                raise ValueError("Enter a username.")
            username = username.strip().lower()
            if (
                not USERNAME_MIN_LENGTH <= len(username) <= USERNAME_MAX_LENGTH
                or not username.replace("_", "").isalnum()
            ):
                raise ValueError(
                    "Username must be 3–32 letters, numbers, or underscores."
                )
            if not isinstance(password, str) or not (
                PASSWORD_MIN_LENGTH <= len(password) <= PASSWORD_MAX_LENGTH
            ):
                raise ValueError("Password must be 8–128 characters.")
            user_id = create_user(
                username,
                generate_password_hash(password),
                app.config["DATABASE"],
                first_name=first_name,
                last_name=last_name,
            )
        except ValueError as error:
            return jsonify(error=str(error)), 400
        except sqlite3.IntegrityError:
            return jsonify(error="That username is already taken."), 409
        except sqlite3.Error:
            return database_error()

        session.clear()
        session["user_id"] = user_id
        return jsonify(user={
            "id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }), 201

    @app.post("/api/auth/login")
    def login():
        try:
            data = json_body()
        except ValueError as error:
            return jsonify(error=str(error)), 400
        username = data.get("username")
        password = data.get("password")
        if (
            not isinstance(username, str)
            or not isinstance(password, str)
            or len(username) > USERNAME_MAX_LENGTH
            or len(password) > PASSWORD_MAX_LENGTH
        ):
            return jsonify(error="Username or password is incorrect."), 401

        try:
            user = get_user_by_username(
                username.strip().lower(),
                app.config["DATABASE"],
            )
        except sqlite3.Error:
            return database_error()
        if user is None or not check_password_hash(user["password_hash"], password):
            return jsonify(error="Username or password is incorrect."), 401

        session.clear()
        session["user_id"] = user["id"]
        return jsonify(user={
            "id": user["id"],
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
        })

    @app.post("/api/auth/logout")
    def logout():
        session.clear()
        return jsonify(ok=True)

    @app.get("/api/options")
    @authenticated_api
    def options():
        goals = get_available_goals()
        return jsonify(
            goals=goals,
            levels={goal: list(VALID_LEVELS) for goal in goals},
            equipment=get_available_equipment(),
        )

    @app.get("/api/library")
    @authenticated_api
    def exercise_library():
        library_exercises = []
        targets = []
        for exercise in exercises:
            media = get_exercise_media(exercise["id"])
            media_url = None
            media_type = None
            if media and (STATIC_DIR / media["media_path"]).is_file():
                media_url = "/static/" + media["media_path"].replace("\\", "/")
                media_type = media["media_type"]

            library_exercises.append({
                "id": exercise["id"],
                "name": exercise["name"],
                "goals": exercise["goals"],
                "level": exercise["level"],
                "body_area": exercise["body_area"],
                "equipment": exercise["equipment"],
                "type": exercise["type"],
                "duration": exercise["duration"],
                "sets": exercise["sets"],
                "reps": exercise.get("reps"),
                "hold_seconds": exercise.get("hold_seconds"),
                "work_seconds": exercise.get("work_seconds"),
                "rest_seconds": exercise.get("rest_seconds"),
                "instructions": exercise["instructions"],
                "media_url": media_url,
                "media_type": media_type,
            })
            for target in exercise["body_area"]:
                if target not in targets:
                    targets.append(target)
            if exercise["type"] == "cardio" and "cardio" not in targets:
                targets.append("cardio")

        return jsonify(
            exercises=library_exercises,
            equipment=get_available_equipment(),
            targets=targets,
        )

    @app.post("/api/recommendations")
    @authenticated_api
    def recommendations():
        try:
            data = json_body()
            recommendation_seed = secrets.randbits(64)
            workout = build_recommendation(data, recommendation_seed)
            empty_message = recommendation_empty_message(data) if not workout else None
            return jsonify(
                exercises=workout,
                empty_message=empty_message,
                recommendation_seed=recommendation_seed,
            )
        except ValueError as error:
            return jsonify(error=str(error)), 400

    @app.get("/api/active-workout")
    @authenticated_api
    def active_workout():
        try:
            workout = get_active_workout(
                session["user_id"],
                app.config["DATABASE"],
            )
            if workout is not None:
                exercises_by_id = {exercise["id"]: exercise for exercise in exercises}
                for planned_exercise in workout["exercises"]:
                    source = exercises_by_id.get(planned_exercise["id"])
                    if source is not None and "goals" not in planned_exercise:
                        planned_exercise["goals"] = source["goals"]
                    if source is not None and "body_area" not in planned_exercise:
                        planned_exercise["body_area"] = source["body_area"]
                    if "keywords" not in planned_exercise:
                        if source is not None:
                            planned_exercise["keywords"] = get_exercise_keywords(source)
            return jsonify(active_workout=workout)
        except sqlite3.Error:
            return database_error()

    @app.get("/api/paused-workouts")
    @authenticated_api
    def paused_workouts():
        try:
            return jsonify(
                paused_workouts=get_paused_workouts(
                    session["user_id"],
                    app.config["DATABASE"],
                )
            )
        except sqlite3.Error:
            return database_error()

    @app.post("/api/active-workout/pause")
    @authenticated_api
    def pause_user_workout():
        try:
            data = json_body()
            workout = get_active_workout(
                session["user_id"],
                app.config["DATABASE"],
            )
            if workout is None:
                return jsonify(error="There is no active workout to save."), 404
            updated_workout = update_active_workout_progress(workout, data)
            save_active_workout(
                session["user_id"],
                updated_workout,
                app.config["DATABASE"],
            )
            paused_workout = pause_active_workout(
                session["user_id"],
                updated_workout["session_id"],
                app.config["DATABASE"],
            )
            if paused_workout is None:
                return jsonify(
                    error="The active workout changed. Reload the page and try again."
                ), 409
            return jsonify(paused_workout=paused_workout), 201
        except (ValueError, TypeError) as error:
            return jsonify(error=str(error)), 400
        except sqlite3.Error:
            return database_error()

    @app.post("/api/paused-workouts/<session_id>/resume")
    @authenticated_api
    def resume_user_workout(session_id):
        try:
            workout = resume_paused_workout(
                session["user_id"],
                session_id,
                app.config["DATABASE"],
            )
            if workout is None:
                return jsonify(error="Saved unfinished workout was not found."), 404
            return jsonify(active_workout=workout)
        except ValueError as error:
            return jsonify(error=str(error)), 409
        except sqlite3.Error:
            return database_error()

    @app.post("/api/active-workout")
    @authenticated_api
    def start_user_workout():
        try:
            data = json_body()
            if get_active_workout(
                session["user_id"],
                app.config["DATABASE"],
            ) is not None:
                return jsonify(
                    error="Save and clear your current workout before starting another."
                ), 409
            workout = build_active_workout(
                data,
                app.config["DATABASE"],
                user_id=session["user_id"],
            )
            if workout is None:
                return jsonify(
                    active_workout=None,
                    empty_message=recommendation_empty_message(data),
                )
            return jsonify(active_workout=workout), 201
        except (ValueError, TypeError) as error:
            return jsonify(error=str(error)), 400
        except sqlite3.Error:
            return database_error()

    @app.put("/api/active-workout")
    @authenticated_api
    def update_user_workout():
        try:
            data = json_body()
            workout = get_active_workout(
                session["user_id"],
                app.config["DATABASE"],
            )
            if workout is None:
                return jsonify(error="There is no active workout to update."), 404
            updated_workout = update_active_workout_progress(workout, data)
            save_active_workout(
                session["user_id"],
                updated_workout,
                app.config["DATABASE"],
            )
            return jsonify(active_workout=updated_workout)
        except (ValueError, TypeError) as error:
            return jsonify(error=str(error)), 400
        except sqlite3.Error:
            return database_error()

    @app.get("/api/history")
    @authenticated_api
    def workout_history():
        try:
            history = get_workout_history(
                app.config["DATABASE"],
                user_id=session["user_id"],
            )
            return jsonify(history)
        except sqlite3.Error:
            return database_error()

    @app.get("/api/history/<session_id>")
    @authenticated_api
    def workout_detail(session_id):
        try:
            workout = get_workout_by_id(
                session_id,
                app.config["DATABASE"],
                user_id=session["user_id"],
            )
        except sqlite3.Error:
            return database_error()
        if workout is None:
            return jsonify(error="Workout not found."), 404
        return jsonify(workout)

    
    @app.post("/api/history/<session_id>/redo")
    @authenticated_api
    def redo_user_workout(session_id):
        try:
            # Check whether the user already has an unfinished workout.
            active_workout = get_active_workout(
                session["user_id"],
                app.config["DATABASE"],
            )

            if active_workout is not None:
                return jsonify(
                    error="Finish your current workout before redoing another one."
                ), 409

            workout = build_redo_workout(
                session_id,
                app.config["DATABASE"],
                user_id=session["user_id"],
            )

            return jsonify(active_workout=workout), 201

        except ValueError as error:
            return jsonify(error=str(error)), 404

        except sqlite3.Error:
            return database_error()

    @app.get("/api/stats")
    @authenticated_api
    def workout_statistics():
        period = request.args.get("period", "week")

        try:
            stats = get_workout_stats(
                period=period,
                db_path=app.config["DATABASE"],
                user_id=session["user_id"],
            )
            return jsonify(stats)
        except ValueError as error:
            return jsonify(error=str(error)), 400
        except sqlite3.Error:
            return database_error()

        
    @app.post("/api/workouts")
    @authenticated_api
    def save_user_workout():
        try:
            data = json_body()
            active_workout = get_active_workout(
                session["user_id"],
                app.config["DATABASE"],
            )
            session_id = None

            if active_workout is not None:
                progress = update_active_workout_progress(active_workout, data)
                completed_counts = {}

                for key in progress["completed_set_keys"]:
                    exercise_id, _ = key.split(":", 1)
                    exercise_id = int(exercise_id)
                    completed_counts[exercise_id] = (
                        completed_counts.get(exercise_id, 0) + 1
                    )

                data = {
                    "goal": active_workout["goal"],
                    "completed_sets": [
                        {
                            "exercise_id": exercise_id,
                            "sets_completed": sets_completed,
                        }
                        for exercise_id, sets_completed in completed_counts.items()
                    ],
                    "notes": progress["notes"],
                }
                session_id = active_workout["session_id"]

            elif "session_id" in data:
                return jsonify(
                    error="This active workout no longer exists. Reload the page."
                ), 409

            session_id = save_completed_workout(
                data,
                app.config["DATABASE"],
                user_id=session["user_id"],
                session_id=session_id,
            )

        except (ValueError, TypeError) as error:
            return jsonify(error=str(error)), 400
        except sqlite3.Error:
            return database_error()

        return jsonify(session_id=session_id), 201


    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
