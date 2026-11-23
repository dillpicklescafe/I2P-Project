# LockIn Member 1 Python Guide

The Member 1 files provide the exercise database, filtering, and rule-based
workout recommendations. They do not depend on Flask or SQLite.

## Main imports

```python
from exercises import exercises
from recommendation import filter_exercises
from recommendation import recommend_workout
from recommendation import calculate_workout_duration
from recommendation import calculate_interval_seconds
from recommendation import get_available_goals
from recommendation import get_available_levels
from recommendation import get_available_equipment
```

## Valid inputs

- `goal`: use a value returned by `get_available_goals()`.
- `level`: always use `get_available_levels(goal)` after a goal is selected.
  The helper only returns levels with at least two matching exercises. This
  prevents the dropdown from offering a level that only produces one exercise.
- `available_equipment`: a list, tuple, or set of equipment names. Use values
  returned by `get_available_equipment()`. An empty list means no equipment.
- `duration`: a positive whole number of minutes.
- `shuffle`: optional Boolean. It defaults to `True`.
- `random_seed`: optional value that makes shuffled examples repeatable.

The active equipment values are `bar`, `bench`, `chair`, `dumbbells`,
`resistance_band`, `step`, and `wall`. Spaces in supplied equipment names are
converted to underscores, but names such as `dumbbell` and `dumbbells` are not
treated as the same value.

## Recommendation example

```python
from recommendation import recommend_workout

workout = recommend_workout(
    goal="upper_body_strength",
    level="beginner",
    available_equipment=["dumbbells", "bench"],
    duration=20,
    random_seed=10
)

for exercise in workout:
    print(exercise["name"], exercise["sets"], exercise["reps"])
```

`recommend_workout()` returns a list of exercise dictionaries. Each dictionary
contains the database fields, including `name`, `sets`, `reps`,
`hold_seconds`, `work_seconds`, `rest_seconds`, `duration`, `equipment`,
`instructions`, and `video_url`.
Invalid inputs and valid searches with no matches return an empty list.

## Dropdown options

Build dropdowns from the helper functions instead of hard-coding options:

```python
goals = get_available_goals()
levels = get_available_levels(selected_goal)
equipment = get_available_equipment()
```

Beginner and intermediate are the meaningful recommendation levels currently
returned by the helpers. Advanced exercises remain in the database, but no
single goal has enough advanced exercises to offer a useful advanced dropdown
option yet.

## Displaying repetitions and timers

Member 2 can choose the display using these fields:

```python
if exercise["reps"] is not None:
    message = str(exercise["sets"]) + " sets x " + str(exercise["reps"]) + " reps"
elif exercise["hold_seconds"] is not None:
    message = str(exercise["sets"]) + " sets x " + str(exercise["hold_seconds"]) + " second hold"
elif exercise["work_seconds"] is not None:
    message = str(exercise["sets"]) + " sets x " + str(exercise["work_seconds"]) + " seconds"
    message += ", rest " + str(exercise["rest_seconds"]) + " seconds between sets"
else:
    message = "Continuous movement"
```

`work_seconds` and `rest_seconds` are LockIn planning estimates for continuous
cardio. They are not sourced performance facts. Rest is counted only between
sets, not after the final set.

## Filtering without building a workout

```python
from recommendation import filter_exercises

matches = filter_exercises(
    goal="cardio",
    level="beginner",
    available_equipment=[]
)
```

## Duration meaning

`duration` is a conservative whole-minute estimate for the complete exercise,
not a measured timer. For repetitions, it uses an estimated movement cadence
appropriate to the exercise type; for holds and intervals, it uses their
prescribed seconds. It adds rest between sets (using the exercise's rest value
or a type- and difficulty-based default) and a short setup/position-change
allowance for each exercise. Actual time varies with pace, rest needs, and
whether repetitions are performed on both sides.

The planning defaults are 4 seconds per controlled strength, stability,
balance, mobility, or coordination repetition; 3 seconds per cardio repetition;
and 2 seconds per plyometric repetition. Default rests are 60/90/120 seconds
for beginner/intermediate/advanced strength, 45 seconds for stability and
balance, 15 seconds for mobility and flexibility, 30 seconds for cardio and
coordination, and 90 seconds for plyometrics. The estimate includes a
30-second setup/position change per exercise. These are planning assumptions,
not measured exercise timings; an exercise's explicit rest value takes
precedence.

The recommendation system keeps the selected exercises when their calculated
time fits, then adds repetitions and sets in small steps to use the requested
time. Repetition ranges are 10–12 for beginners, 12–16 for intermediate, and
15–20 for advanced; each exercise is limited to six sets. If the selected
goal, difficulty, and equipment do not provide enough exercise variety to fill
the available time within those limits, the estimate will be shorter rather
than exceeding them.

For timed cardio, `calculate_interval_seconds(exercise)` returns work time plus
between-set rest. That interval total is validated to fit within the exercise's
whole-minute `duration`; remaining time allows for setup and transitions.

```python
from recommendation import calculate_workout_duration

estimated_minutes = calculate_workout_duration(workout)
```

## Notes for integration

- Do not change dictionaries returned by `exercises` directly.
- Recommended exercises are shallow copies, so changing top-level output fields
  does not change the main database.
- Easier and harder variations are not placed in the same workout.
- `video_url` is intentionally `None` until the team selects video sources.
- Advanced records are retained for future expansion but are not currently
  offered by `get_available_levels()` because coverage is too limited.

## Running tests

```powershell
py -m unittest -v test_recommendation.py
```
