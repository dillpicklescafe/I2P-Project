"""Generate media worklists from the current active exercise/media state."""

import csv
from pathlib import Path

from exercise_media import get_exercise_media
from exercises import exercises
from generate_missing_media_checklist import (
    expected_filename,
    media_status,
    numbered_instructions,
)


PROJECT_DIR = Path(__file__).resolve().parent
MY_MD_PATH = PROJECT_DIR / "MY_REMAINING_MEDIA.md"
MY_CSV_PATH = PROJECT_DIR / "MY_REMAINING_MEDIA.csv"
TEAMMATE_MD_PATH = PROJECT_DIR / "TEAMMATE_MEDIA_CHECKLIST.md"


def missing_active_exercises():
    return [
        exercise for exercise in exercises
        if get_exercise_media(exercise["id"]) is None
    ]


def status(exercise):
    return media_status(exercise)


def append_exercise(lines, exercise):
    equipment = ", ".join(exercise["equipment"]) or "None"
    lines.extend([
        f"### [ ] #{exercise['id']} — {exercise['name']}",
        "",
        f"- **Status:** {status(exercise)}",
        f"- **Difficulty:** {exercise['level']}",
        f"- **Required equipment:** {equipment}",
        f"- **Expected filename:** `{expected_filename(exercise)}`",
        "",
        "**Instructions:**",
        "",
    ])
    lines.extend(
        f"{number}. {step}"
        for number, step in enumerate(exercise["instructions"], start=1)
    )
    lines.extend(["", "---", ""])


def generate_my_markdown(follow_up, remaining):
    lines = [
        "# My Remaining LockIn Media",
        "",
        "Only active Intermediate and Advanced exercises without approved media are included. "
        "Excluded records and unresolved Beginner media are not personal tasks.",
        "",
        f"- **Remaining assigned work in IDs 76–151:** {len(remaining)}",
        f"- **Total current tasks:** {len(remaining)}",
        "",
    ]
    lines.extend(["## My remaining work — IDs 76–151", ""])
    for exercise in remaining:
        append_exercise(lines, exercise)
    MY_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def generate_my_csv(follow_up, remaining):
    fieldnames = [
        "Section", "Found", "Status", "Exercise ID", "Exercise name",
        "Difficulty", "Required equipment", "Exact instructions",
        "Expected filename",
    ]
    with MY_CSV_PATH.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for section, records in (("My remaining IDs 76-151", remaining),):
            for exercise in records:
                writer.writerow({
                    "Section": section,
                    "Found": "☐",
                    "Status": status(exercise),
                    "Exercise ID": exercise["id"],
                    "Exercise name": exercise["name"],
                    "Difficulty": exercise["level"],
                    "Required equipment": ", ".join(exercise["equipment"]) or "None",
                    "Exact instructions": numbered_instructions(exercise),
                    "Expected filename": expected_filename(exercise),
                })


def generate_teammate_markdown(records):
    lines = [
        "# Teammate Media Checklist — IDs 152 and above",
        "",
        "Only active exercises without approved media are included. Excluded records are not tasks.",
        "",
        f"- **Total assigned exercises:** {len(records)}",
        "",
    ]
    for exercise in records:
        append_exercise(lines, exercise)
    TEAMMATE_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main():
    missing = missing_active_exercises()
    remaining = [
        exercise for exercise in missing
        if 76 <= exercise["id"] <= 151
        and exercise["level"] in ("intermediate", "advanced")
    ]
    teammate = [exercise for exercise in missing if exercise["id"] >= 152]
    unresolved_beginner = [
        exercise for exercise in missing
        if exercise["level"] == "beginner"
    ]
    if (
        len(remaining) != 2
        or len(teammate) != 24
        or [exercise["id"] for exercise in unresolved_beginner] != [128, 161]
    ):
        raise RuntimeError(
            "Responsibility counts changed; review the current media mappings before regenerating."
        )
    generate_my_markdown([], remaining)
    generate_my_csv([], remaining)
    generate_teammate_markdown(teammate)
    print("Generated worklists: 2 personal tasks, 24 teammate tasks; Beginner IDs 128 and 161 unresolved.")


if __name__ == "__main__":
    main()
