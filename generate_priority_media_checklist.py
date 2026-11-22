"""Generate the protected and Intermediate/Advanced media priority lists."""

import csv
from pathlib import Path

from exercise_media import get_exercise_media
from exercises import exercises
from generate_missing_media_checklist import (
    expected_filename,
    media_status,
    numbered_instructions,
    search_keywords,
)


PROJECT_DIR = Path(__file__).resolve().parent
MEDIA_DIR = PROJECT_DIR / "static" / "exercises"
MARKDOWN_PATH = PROJECT_DIR / "PRIORITY_MEDIA_CHECKLIST.md"
CSV_PATH = PROJECT_DIR / "PRIORITY_MEDIA_CHECKLIST.csv"
PROTECTED_IDS = (38, 41, 45, 50, 57, 58, 59)
REGISTERED_PROTECTED_IDS = (38, 41, 45, 50, 57, 58, 59)
PENDING_PROTECTED_IDS = ()
PRIORITY_LEVELS = ("intermediate", "advanced")


def saved_media_name(exercise_id):
    matches = sorted(MEDIA_DIR.glob(f"{exercise_id}.*"))
    return matches[0].name if matches else None


def checklist_records():
    by_id = {exercise["id"]: exercise for exercise in exercises}
    protected = [by_id[exercise_id] for exercise_id in PENDING_PROTECTED_IDS]
    priority = {
        level: [
            exercise for exercise in exercises
            if exercise["level"] == level
            and get_exercise_media(exercise["id"]) is None
        ]
        for level in PRIORITY_LEVELS
    }
    return protected, priority


def metadata(exercise, section, protected=False):
    saved_name = saved_media_name(exercise["id"]) if protected else None
    return {
        "section": section,
        "found": "☐",
        "status": (
            "Saved file preserved; movement mismatch; replacement needed"
            if protected else media_status(exercise)
        ),
        "saved_file": saved_name or "",
        "expected_filename": (
            f'{exercise["id"]}-replacement.gif'
            if protected else expected_filename(exercise)
        ),
    }


def generate_markdown(protected, priority):
    lines = [
        "# LockIn Priority Media Checklist",
        "",
        "This checklist prioritizes every currently missing Intermediate and Advanced exercise. "
        "Validated protected work is already registered and must not be overwritten.",
        "",
        f"- **Intermediate media still needed:** {len(priority['intermediate'])}",
        f"- **Advanced media still needed:** {len(priority['advanced'])}",
        f"- **Total new GIFs/videos to find:** {sum(len(priority[level]) for level in PRIORITY_LEVELS)}",
        f"- **Protected saved files registered:** {len(REGISTERED_PROTECTED_IDS)}",
        f"- **Protected saved files needing a matching replacement:** {len(protected)}",
        "",
        "If a matching demonstration is an MP4 rather than a GIF, retain the numeric ID and "
        "use its real extension (for example, `167.mp4`).",
        "",
    ]

    sections = [(level.title(), priority[level], False) for level in PRIORITY_LEVELS]
    for heading, records, is_protected in sections:
        lines.extend([f"## {heading}", ""])
        for exercise in records:
            info = metadata(exercise, heading, is_protected)
            equipment = ", ".join(exercise["equipment"]) or "None"
            lines.extend([
                f"### [ ] #{exercise['id']} — {exercise['name']}",
                "",
                f"- **Status:** {info['status']}",
                f"- **Difficulty:** {exercise['level']}",
                f"- **Required equipment:** {equipment}",
                f"- **Suggested search keywords:** `{search_keywords(exercise)}`",
                f"- **Expected filename:** `{info['expected_filename']}`",
            ])
            if info["saved_file"]:
                lines.append(f"- **Existing saved file:** `static/exercises/{info['saved_file']}`")
            lines.extend(["", "**Instructions:**", ""])
            lines.extend(
                f"{number}. {step}"
                for number, step in enumerate(exercise["instructions"], start=1)
            )
            lines.extend(["", "---", ""])
    MARKDOWN_PATH.write_text("\n".join(lines), encoding="utf-8")


def generate_csv(protected, priority):
    fieldnames = [
        "Section", "Found", "Status", "Exercise ID", "Exercise name",
        "Difficulty", "Required equipment", "Exact instructions",
        "Suggested search keywords", "Expected filename", "Existing saved file",
    ]
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        sections = [(level.title(), priority[level], False) for level in PRIORITY_LEVELS]
        for section, records, is_protected in sections:
            for exercise in records:
                info = metadata(exercise, section, is_protected)
                writer.writerow({
                    "Section": section,
                    "Found": info["found"],
                    "Status": info["status"],
                    "Exercise ID": exercise["id"],
                    "Exercise name": exercise["name"],
                    "Difficulty": exercise["level"],
                    "Required equipment": ", ".join(exercise["equipment"]) or "None",
                    "Exact instructions": numbered_instructions(exercise),
                    "Suggested search keywords": search_keywords(exercise),
                    "Expected filename": info["expected_filename"],
                    "Existing saved file": (
                        f'static/exercises/{info["saved_file"]}'
                        if info["saved_file"] else ""
                    ),
                })


def main():
    protected, priority = checklist_records()
    missing_protected_files = [
        exercise["id"] for exercise in protected
        if saved_media_name(exercise["id"]) is None
    ]
    if missing_protected_files:
        raise RuntimeError(
            "Protected media files were not found for IDs: "
            + ", ".join(map(str, missing_protected_files))
        )
    if any(get_exercise_media(exercise_id) is None for exercise_id in REGISTERED_PROTECTED_IDS):
        raise RuntimeError("A validated protected exercise is missing its mapping.")
    if len(priority["intermediate"]) != 11 or len(priority["advanced"]) != 14:
        raise RuntimeError("Current priority counts differ from the audited 11/14 split.")
    generate_markdown(protected, priority)
    generate_csv(protected, priority)
    print("Generated priority checklist: 11 intermediate, 14 advanced.")


if __name__ == "__main__":
    main()
