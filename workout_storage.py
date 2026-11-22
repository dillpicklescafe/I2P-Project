
import json
import sqlite3
from contextlib import closing
from datetime import date, timedelta


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

            connection.execute("""
                CREATE TABLE IF NOT EXISTS active_workouts (
                    user_id INTEGER PRIMARY KEY,
                    session_id TEXT NOT NULL UNIQUE,
                    workout_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (user_id)
                        REFERENCES users(id)
                        ON DELETE CASCADE
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS paused_workouts (
                    user_id INTEGER NOT NULL,
                    session_id TEXT NOT NULL,
                    workout_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (user_id, session_id),
                    FOREIGN KEY (user_id)
                        REFERENCES users(id)
                        ON DELETE CASCADE
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


def save_active_workout(user_id, workout, db_path=DATABASE_NAME):
    """Create or replace the active workout for one account."""
    from datetime import datetime, timezone

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("User ID must be a positive integer.")
    if not isinstance(workout, dict):
        raise ValueError("Active workout must be an object.")
    session_id = workout.get("session_id")
    if not isinstance(session_id, str) or not session_id or len(session_id) > 128:
        raise ValueError("Active workout session ID is invalid.")
    try:
        workout_json = json.dumps(workout, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("Active workout must contain valid JSON data.") from error

    initialize_database(db_path)
    with closing(sqlite3.connect(db_path)) as connection:
        with connection:
            connection.execute("""
                INSERT INTO active_workouts (
                    user_id, session_id, workout_json, updated_at
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    session_id = excluded.session_id,
                    workout_json = excluded.workout_json,
                    updated_at = excluded.updated_at
            """, (
                user_id,
                session_id,
                workout_json,
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
            ))


def get_active_workout(user_id, db_path=DATABASE_NAME):
    """Retrieve the active workout for one account."""
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("User ID must be a positive integer.")

    initialize_database(db_path)
    with closing(sqlite3.connect(db_path)) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute("""
            SELECT workout_json
            FROM active_workouts
            WHERE user_id = ?
        """, (user_id,)).fetchone()

    if row is None:
        return None
    try:
        return json.loads(row["workout_json"])
    except json.JSONDecodeError as error:
        raise sqlite3.DatabaseError("Stored active workout is invalid.") from error


def pause_active_workout(user_id, session_id, db_path=DATABASE_NAME):
    """Move one account's active workout into its saved paused workouts."""
    from datetime import datetime, timezone

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("User ID must be a positive integer.")
    if not isinstance(session_id, str) or not session_id or len(session_id) > 128:
        raise ValueError("Workout session ID is invalid.")

    initialize_database(db_path)
    with closing(sqlite3.connect(db_path)) as connection:
        connection.row_factory = sqlite3.Row
        with connection:
            connection.execute("PRAGMA foreign_keys = ON")
            row = connection.execute("""
                SELECT workout_json
                FROM active_workouts
                WHERE user_id = ? AND session_id = ?
            """, (user_id, session_id)).fetchone()
            if row is None:
                return None
            try:
                workout = json.loads(row["workout_json"])
            except json.JSONDecodeError as error:
                raise sqlite3.DatabaseError(
                    "Stored active workout is invalid."
                ) from error

            updated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
            connection.execute("""
                INSERT INTO paused_workouts (
                    user_id, session_id, workout_json, updated_at
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id, session_id) DO UPDATE SET
                    workout_json = excluded.workout_json,
                    updated_at = excluded.updated_at
            """, (user_id, session_id, row["workout_json"], updated_at))
            deleted = connection.execute("""
                DELETE FROM active_workouts
                WHERE user_id = ? AND session_id = ?
            """, (user_id, session_id))
            if deleted.rowcount != 1:
                raise sqlite3.DatabaseError(
                    "Active workout changed while it was being saved."
                )
    return workout


def get_paused_workouts(user_id, db_path=DATABASE_NAME):
    """Retrieve saved paused workouts for one account, newest first."""
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("User ID must be a positive integer.")

    initialize_database(db_path)
    with closing(sqlite3.connect(db_path)) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("""
            SELECT workout_json
            FROM paused_workouts
            WHERE user_id = ?
            ORDER BY updated_at DESC
        """, (user_id,)).fetchall()

    try:
        return [json.loads(row["workout_json"]) for row in rows]
    except json.JSONDecodeError as error:
        raise sqlite3.DatabaseError("Stored paused workout is invalid.") from error


def resume_paused_workout(user_id, session_id, db_path=DATABASE_NAME):
    """Move a paused workout back into the account's active slot."""
    from datetime import datetime, timezone

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("User ID must be a positive integer.")
    if not isinstance(session_id, str) or not session_id or len(session_id) > 128:
        raise ValueError("Workout session ID is invalid.")

    initialize_database(db_path)
    with closing(sqlite3.connect(db_path)) as connection:
        connection.row_factory = sqlite3.Row
        with connection:
            connection.execute("PRAGMA foreign_keys = ON")
            active = connection.execute("""
                SELECT 1
                FROM active_workouts
                WHERE user_id = ?
            """, (user_id,)).fetchone()
            if active is not None:
                raise ValueError(
                    "Save and clear your current workout before resuming another."
                )

            row = connection.execute("""
                SELECT workout_json
                FROM paused_workouts
                WHERE user_id = ? AND session_id = ?
            """, (user_id, session_id)).fetchone()
            if row is None:
                return None
            try:
                workout = json.loads(row["workout_json"])
            except json.JSONDecodeError as error:
                raise sqlite3.DatabaseError(
                    "Stored paused workout is invalid."
                ) from error

            connection.execute("""
                INSERT INTO active_workouts (
                    user_id, session_id, workout_json, updated_at
                )
                VALUES (?, ?, ?, ?)
            """, (
                user_id,
                session_id,
                row["workout_json"],
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
            ))
            connection.execute("""
                DELETE FROM paused_workouts
                WHERE user_id = ? AND session_id = ?
            """, (user_id, session_id))
    return workout


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

            if user_id is not None:
                connection.execute("""
                    DELETE FROM active_workouts
                    WHERE user_id = ? AND session_id = ?
                """, (user_id, session["session_id"]))

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


from datetime import date, timedelta


def get_workout_stats(period="week", db_path=DATABASE_NAME, user_id=None):
    """Return workout totals and daily activity for the current week or month."""
    if period not in ("week", "month"):
        raise ValueError("Period must be 'week' or 'month'.")

    today = date.today()

    if period == "week":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=7)
    else:
        start_date = today.replace(day=1)
        if today.month == 12:
            end_date = date(today.year + 1, 1, 1)
        else:
            end_date = date(today.year, today.month + 1, 1)

    initialize_database(db_path)

    with closing(sqlite3.connect(db_path)) as connection:
        connection.row_factory = sqlite3.Row

        user_filter = ""
        parameters = [start_date.isoformat(), end_date.isoformat()]

        if user_id is not None:
            user_filter = " AND w.user_id = ?"
            parameters.append(user_id)

        totals = connection.execute("""
            SELECT
                COUNT(DISTINCT w.session_id) AS total_sessions,
                COUNT(DISTINCT date(w.date)) AS workout_days,
                COALESCE(SUM(e.duration_minutes), 0) AS total_duration,
                COALESCE(SUM(e.sets_completed), 0) AS total_sets
            FROM workouts w
            LEFT JOIN workout_exercises e
                ON w.session_id = e.session_id
            WHERE w.completed = 1
              AND date(w.date) >= date(?)
              AND date(w.date) < date(?)
        """ + user_filter, parameters).fetchone()

        activity = connection.execute("""
            SELECT
                date(w.date) AS workout_date,
                COUNT(DISTINCT w.session_id) AS sessions
            FROM workouts w
            WHERE w.completed = 1
              AND date(w.date) >= date(?)
              AND date(w.date) < date(?)
        """ + user_filter + """
            GROUP BY date(w.date)
            ORDER BY date(w.date)
        """, parameters).fetchall()

    return {
        "period": period,
        "start_date": start_date.isoformat(),
        "end_date": (end_date - timedelta(days=1)).isoformat(),
        "total_sessions": totals["total_sessions"],
        "workout_days": totals["workout_days"],
        "total_duration": round(totals["total_duration"], 2),
        "total_sets": totals["total_sets"],
        "activity": [
            {
                "date": row["workout_date"],
                "sessions": row["sessions"],
            }
            for row in activity
        ],
    }