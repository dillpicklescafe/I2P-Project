"""Generate Markdown and CSV checklists for exercises without approved media."""

import csv
from pathlib import Path

from exercise_media import get_exercise_media
from exercises import exercises


PROJECT_DIR = Path(__file__).resolve().parent
MARKDOWN_PATH = PROJECT_DIR / "MISSING_MEDIA_CHECKLIST.md"
CSV_PATH = PROJECT_DIR / "MISSING_MEDIA_CHECKLIST.csv"
EXPECTED_MISSING_COUNT = 27
LEVELS = ("beginner", "intermediate", "advanced")
REJECTED_SAVED_MEDIA = {
    103: "Saved 103.gif shows a moving bear crawl, not the instructed stationary hover hold",
    124: "Saved 124.gif omits the complete 12/3/6 clock sequence and required leg switch",
}


def media_status(exercise):
    return REJECTED_SAVED_MEDIA.get(exercise["id"], "Not found")


def expected_filename(exercise):
    suffix = "-replacement" if exercise["id"] in REJECTED_SAVED_MEDIA else ""
    return f'{exercise["id"]}{suffix}.gif'


def missing_exercises():
    return [
        exercise for exercise in exercises
        if get_exercise_media(exercise["id"]) is None
    ]


def search_keywords(exercise):
    equipment = (
        " ".join(item.replace("_", " ") for item in exercise["equipment"])
        if exercise["equipment"] else "bodyweight no equipment"
    )
    return (
        f'{exercise["name"]} {exercise["position"]} {equipment} '
        "exercise proper form demonstration GIF video"
    )


def numbered_instructions(exercise):
    return "\n".join(
        f"{number}. {step}"
        for number, step in enumerate(exercise["instructions"], start=1)
    )


def generate_markdown(records):
    counts = {
        level: sum(exercise["level"] == level for exercise in records)
        for level in LEVELS
    }
    lines = [
        "# LockIn Missing Media Checklist",
        "",
        f"Exercises currently missing approved media: **{len(records)}**.",
        "",
        "Save GIFs with the listed `.gif` filename. If the matching demonstration is a video, "
        "keep the same numeric ID and use its real extension, such as `31.mp4`.",
        "",
        "Difficulty breakdown: "
        + ", ".join(f"{level.title()} **{counts[level]}**" for level in LEVELS)
        + ".",
        "",
    ]

    for level in LEVELS:
        lines.extend([f"## {level.title()}", ""])
        for exercise in records:
            if exercise["level"] != level:
                continue
            equipment = ", ".join(exercise["equipment"]) or "None"
            goals = ", ".join(exercise["goals"])
            lines.extend([
                f"### [ ] #{exercise['id']} — {exercise['name']}",
                "",
                f"- **Status:** {media_status(exercise)}",
                f"- **Difficulty:** {exercise['level']}",
                f"- **Required equipment:** {equipment}",
                f"- **Fitness goals:** {goals}",
                f"- **Suggested search keywords:** `{search_keywords(exercise)}`",
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

    MARKDOWN_PATH.write_text("\n".join(lines), encoding="utf-8")


def generate_csv(records):
    fieldnames = [
        "Found", "Status", "Exercise ID", "Exercise name", "Difficulty",
        "Required equipment", "Fitness goals", "Exact instructions",
        "Suggested search keywords", "Expected filename",
    ]
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for level in LEVELS:
            for exercise in records:
                if exercise["level"] != level:
                    continue
                writer.writerow({
                    "Found": "☐",
                    "Status": media_status(exercise),
                    "Exercise ID": exercise["id"],
                    "Exercise name": exercise["name"],
                    "Difficulty": exercise["level"],
                    "Required equipment": ", ".join(exercise["equipment"]) or "None",
                    "Fitness goals": ", ".join(exercise["goals"]),
                    "Exact instructions": numbered_instructions(exercise),
                    "Suggested search keywords": search_keywords(exercise),
                    "Expected filename": expected_filename(exercise),
                })


def main():
    records = missing_exercises()
    if len(records) != EXPECTED_MISSING_COUNT:
        raise RuntimeError(
            f"Expected {EXPECTED_MISSING_COUNT} missing exercises, found {len(records)}. "
            "Review exercise_media.py and MISSING_EXERCISE_MEDIA.md before regenerating."
        )
    generate_markdown(records)
    generate_csv(records)
    print(f"Generated {MARKDOWN_PATH.name} with {len(records)} exercises.")
    print(f"Generated {CSV_PATH.name} with {len(records)} exercises.")


if __name__ == "__main__":
    main()
