
import sqlite3
from contextlib import closing


DATABASE_NAME = "fitness_tracker.db"


def initialize_database(db_path=DATABASE_NAME):
    """Create or update the workout database."""

    with closing(sqlite3.connect(db_path)) as connection:
        with connection:
            connection.execute("PRAGMA foreign_keys = ON")

            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    first_name TEXT NOT NULL DEFAULT '',
                    last_name TEXT NOT NULL DEFAULT ''
                )
            """)

            user_columns = connection.execute(
                "PRAGMA table_info(users)"
            ).fetchall()
            user_column_names = [column[1] for column in user_columns]
            if "first_name" not in user_column_names:
                connection.execute("""
                    ALTER TABLE users
                    ADD COLUMN first_name TEXT NOT NULL DEFAULT ''
                """)
            if "last_name" not in user_column_names:
                connection.execute("""
                    ALTER TABLE users
                    ADD COLUMN last_name TEXT NOT NULL DEFAULT ''
                """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS workouts (
                    session_id TEXT PRIMARY KEY,
                    date TEXT NOT NULL,
                    goal TEXT,
                    notes TEXT,
                    completed INTEGER NOT NULL,
                    completed_at TEXT,
                    user_id INTEGER REFERENCES users(id)
                )
            """)

            workout_columns = connection.execute(
                "PRAGMA table_info(workouts)"
            ).fetchall()
            if "user_id" not in [column[1] for column in workout_columns]:
                connection.execute("""
                    ALTER TABLE workouts
                    ADD COLUMN user_id INTEGER REFERENCES users(id)
                """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS workout_exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    exercise_id INTEGER,
                    name TEXT NOT NULL,
                    sets_completed INTEGER NOT NULL,
                    reps_completed INTEGER,
                    duration_minutes REAL NOT NULL,
                    notes TEXT,
                    FOREIGN KEY (session_id)
                        REFERENCES workouts(session_id)
                        ON DELETE CASCADE
                )
            """)

            # Migrate existing databases that don't have exercise_id.
            columns = connection.execute(
                "PRAGMA table_info(workout_exercises)"
            ).fetchall()

            column_names = [column[1] for column in columns]

            if "exercise_id" not in column_names:
                connection.execute("""
                    ALTER TABLE workout_exercises
                    ADD COLUMN exercise_id INTEGER
                """)


def create_user(
    username,
    password_hash,
    db_path=DATABASE_NAME,
    first_name="",
    last_name=""
):
    """Create an account and return its database ID."""
    from datetime import datetime, timezone

    initialize_database(db_path)

    with closing(sqlite3.connect(db_path)) as connection:
        with connection:
            cursor = connection.execute("""
                INSERT INTO users (
                    username, password_hash, created_at, first_name, last_name
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                username,
                password_hash,
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                first_name,
                last_name,
            ))

    return cursor.lastrowid


def get_user_by_username(username, db_path=DATABASE_NAME):
    """Retrieve an account by username, including its password hash."""
    initialize_database(db_path)

    with closing(sqlite3.connect(db_path)) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute("""
            SELECT id, username, password_hash, first_name, last_name
            FROM users
            WHERE username = ?
        """, (username,)).fetchone()

    return dict(row) if row is not None else None


def get_user_by_id(user_id, db_path=DATABASE_NAME):
    """Retrieve public account details by ID."""
    initialize_database(db_path)

    with closing(sqlite3.connect(db_path)) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute("""
            SELECT id, username, first_name, last_name
            FROM users
            WHERE id = ?
        """, (user_id,)).fetchone()

    return dict(row) if row is not None else None


def save_workout(session, db_path=DATABASE_NAME, user_id=None):
    """Save a completed workout and its exercises to SQLite."""

    if not session.get("completed"):
        raise ValueError("Only completed workouts can be saved.")

    if not session.get("exercises"):
        raise ValueError("Workout must contain at least one exercise.")
    if user_id is not None and (
        not isinstance(user_id, int)
        or isinstance(user_id, bool)
        or user_id <= 0
    ):
        raise ValueError("User ID must be a positive integer.")

    # Validate exercise records before saving.
    for exercise in session["exercises"]:
        exercise_id = exercise.get("exercise_id")

        if (
            not isinstance(exercise_id, int)
            or isinstance(exercise_id, bool)
            or exercise_id <= 0
        ):
            raise ValueError("Every exercise must have a valid exercise ID.")

    initialize_database(db_path)

    with closing(sqlite3.connect(db_path)) as connection:
        with connection:
            connection.execute("PRAGMA foreign_keys = ON")

            connection.execute("""
                INSERT INTO workouts (
                    session_id, date, goal, notes,
                    completed, completed_at, user_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session["session_id"],
                session["date"],
                session["goal"],
                session["notes"],
                int(session["completed"]),
                session.get("completed_at"),
                user_id
            ))

            for exercise in session["exercises"]:
                connection.execute("""
                    INSERT INTO workout_exercises (
                        session_id, exercise_id, name,
                        sets_completed, reps_completed,
                        duration_minutes, notes
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    session["session_id"],
                    exercise["exercise_id"],
                    exercise["name"],
                    exercise["sets_completed"],
                    exercise["reps_completed"],
                    exercise["duration_minutes"],
                    exercise["notes"]
                ))

    return session["session_id"]


def get_workout_history(db_path=DATABASE_NAME, user_id=None):
    """Retrieve all saved workouts with progress summaries."""

    initialize_database(db_path)

    with closing(sqlite3.connect(db_path)) as connection:
        with connection:
            connection.row_factory = sqlite3.Row

            query = """
                SELECT
                    w.session_id,
                    w.date,
                    w.goal,
                    w.completed,
                    COUNT(e.id) AS total_exercises,
                    COALESCE(SUM(e.sets_completed), 0) AS total_sets,
                    COALESCE(SUM(e.duration_minutes), 0)
                        AS total_duration
                FROM workouts w
                LEFT JOIN workout_exercises e
                    ON w.session_id = e.session_id
            """
            parameters = ()
            if user_id is not None:
                query += " WHERE w.user_id = ?"
                parameters = (user_id,)
            query += " GROUP BY w.session_id ORDER BY w.date DESC"
            rows = connection.execute(query, parameters).fetchall()

    return [dict(row) for row in rows]


def get_workout_by_id(session_id, db_path=DATABASE_NAME, user_id=None):
    """Retrieve one workout and all its recorded exercises."""

    initialize_database(db_path)

    with closing(sqlite3.connect(db_path)) as connection:
        with connection:
            connection.row_factory = sqlite3.Row

            query = """
                SELECT *
                FROM workouts
                WHERE session_id = ?
            """
            parameters = (session_id,)
            if user_id is not None:
                query += " AND user_id = ?"
                parameters = (session_id, user_id)
            workout = connection.execute(query, parameters).fetchone()

            if workout is None:
                return None

            exercises = connection.execute("""
                SELECT
                    exercise_id,
                    name,
                    sets_completed,
                    reps_completed,
                    duration_minutes,
                    notes
                FROM workout_exercises
                WHERE session_id = ?
                ORDER BY id
            """, (session_id,)).fetchall()

    result = dict(workout)
    result["completed"] = bool(result["completed"])
    result["exercises"] = [dict(row) for row in exercises]

    return result