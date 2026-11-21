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
    recommend_workout,
)
from workout_log import add_exercise, complete_workout, start_workout
from workout_storage import (
    DATABASE_NAME,
    create_user,
    get_user_by_id,
    get_user_by_username,
    get_workout_by_id,
    get_workout_history,
    initialize_database,
    save_workout,
)


PROJECT_DIR = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_DIR / "static"
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 32
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128


def build_recommendation(data):
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

    recommendations = recommend_workout(goal, level, equipment, duration)
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


def save_completed_workout(data, db_path=DATABASE_NAME, user_id=None):
    """Save checked exercises as a completed workout for one account."""
    goal = data.get("goal")
    if not isinstance(goal, str) or goal not in get_available_goals():
        raise ValueError("Choose a valid fitness goal.")

    notes = data.get("notes", "")
    if not isinstance(notes, str):
        raise ValueError("Workout notes must be text.")

    completed_ids = data.get("completed_exercises")
    if not isinstance(completed_ids, list) or not completed_ids:
        raise ValueError("Mark at least one exercise as complete before saving.")

    exercise_by_id = {exercise["id"]: exercise for exercise in exercises}
    if any(
        not isinstance(exercise_id, int)
        or isinstance(exercise_id, bool)
        or exercise_id not in exercise_by_id
        for exercise_id in completed_ids
    ):
        raise ValueError("The completed exercises contain an invalid exercise.")
    if len(set(completed_ids)) != len(completed_ids):
        raise ValueError("An exercise can only be recorded once per workout.")

    session_data = start_workout(goal=goal, notes=notes)
    for exercise_id in completed_ids:
        exercise = exercise_by_id[exercise_id]
        add_exercise(
            session_data,
            exercise,
            sets_completed=exercise["sets"],
            reps_completed=exercise.get("reps"),
            duration_minutes=exercise["duration"],
        )

    complete_workout(session_data)
    return save_workout(session_data, db_path, user_id=user_id)


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

    @app.post("/api/recommendations")
    @authenticated_api
    def recommendations():
        try:
            return jsonify(exercises=build_recommendation(json_body()))
        except ValueError as error:
            return jsonify(error=str(error)), 400

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

    @app.post("/api/workouts")
    @authenticated_api
    def save_user_workout():
        try:
            session_id = save_completed_workout(
                json_body(),
                app.config["DATABASE"],
                user_id=session["user_id"],
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
