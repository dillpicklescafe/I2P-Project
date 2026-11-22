# LockIn

LockIn is a starter workout planner built on the existing exercise recommendation
and workout-history modules, with simple account login and registration.

## Run the UI

Install the requirements and start the Flask server from the project directory:

```powershell
py -m pip install -r requirements.txt
py app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in a browser. Stop the
server with `Ctrl+C`.

Create an account with your first and last name (up to 50 characters each),
username (3–32 letters, numbers, or underscores), and password (8–128
characters), or log in. Choose a goal, difficulty, available time, and
equipment to get a workout. Exercise cards show instructions and available
local demonstrations. Mark completed exercises and save them to your account's
history in the local `fitness_tracker.db` database.

After logging in, use the top navigation to switch between Build workout,
Exercise Library, Workout Tracker, and Profile. Exercise cards in the generated
plan and Exercise Library offer detailed previews by hover, click, or keyboard;
the Profile page remains a placeholder for future work.

Passwords are stored as one-way hashes, and each workout is associated with its
account. Existing workout rows from before accounts were added remain in the
database but are not shown in any account's history. Set `FLASK_SECRET_KEY` to a
long random value to keep login sessions valid across server restarts; if unset,
the app generates a temporary key on startup.

This is a local MVP, not a production-ready public authentication service. Use
HTTPS and configure a persistent secret key before deploying it for other users.
