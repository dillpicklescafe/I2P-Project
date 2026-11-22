"""Generate the dated LockIn missing-media audit from project source data."""

from __future__ import annotations

import re
from pathlib import Path

from exercise_media import EXERCISE_MEDIA
from exercises import exercises


INITIAL_MISSING_IDS = {
    128, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163,
    164, 165, 166, 167, 168, 169, 170, 172, 173, 174, 175, 176,
}

CANDIDATE_REVIEW = {
    156: "Rejected: shows only one side; instructions require alternating sides.",
    157: "Rejected: depicts a seated reach flow, not Complex Mobility Flow.",
    162: "Rejected: depicts a kneeling recovery flow, not a seated reach matrix.",
    163: "Rejected: depicts a V-sit toe-reach exercise, not the instructed sequence.",
    164: "Unvalidated: existing MP4 could not be decoded for frame review locally.",
    165: "Rejected: does not clearly demonstrate alternating both sides.",
    166: "Rejected: does not clearly demonstrate the required both-side sequence.",
    167: "Rejected: ordinary push-ups; omits the knee-down reset stage.",
    168: "Approved and integrated: exact small high-plank forward/back shift.",
    176: "Rejected: demonstrates only one side; instructions require both sides.",
}


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main() -> None:
    source_by_id = {exercise["id"]: exercise for exercise in exercises}
    lines = [
        "# LockIn active exercise media audit — 2026-11-22",
        "",
        "Baseline: 155 active exercises; 25 initially had no registered media mapping. "
        "The checklist is ordered by the source database. Exact instructions are copied "
        "verbatim from `exercises.py`.",
        "",
        "Current result: one existing repository GIF (ID 168) passed technical and visual "
        "review and was integrated; 24 exercises still intentionally show `Demo coming "
        "soon`. The built-in image generator returned a static PNG when explicitly asked "
        "for an animated GIF, so no generated asset was registered.",
        "",
    ]
    for exercise_id in sorted(INITIAL_MISSING_IDS):
        exercise = source_by_id[exercise_id]
        mapping = EXERCISE_MEDIA.get(exercise_id)
        existing = sorted(
            path.name
            for path in Path("static/exercises").glob(f"{exercise_id}.*")
        )
        if mapping:
            status = (
                f"Integrated: `{mapping['media_path']}` ({mapping['media_type']}); "
                + CANDIDATE_REVIEW.get(exercise_id, "approved")
            )
            expected = Path(mapping["media_path"]).name
            checkbox = "x"
        else:
            candidate = CANDIDATE_REVIEW.get(exercise_id)
            if candidate:
                status = f"Existing candidate(s): {', '.join(existing)}. {candidate}"
            elif existing:
                status = f"Existing but unreviewed candidate(s): {', '.join(existing)}."
            else:
                status = "No file and no mapping; displays `Demo coming soon`."
            expected = f"{exercise_id}-{slugify(exercise['name'])}.gif"
            checkbox = " "

        lines.extend([
            f"## [{checkbox}] {exercise_id} — {exercise['name']}",
            "",
            f"- Difficulty: `{exercise['level']}`",
            f"- Existing media status: {status}",
            f"- Expected output filename: `{expected}`",
            "- Exact instructions:",
            "",
        ])
        for step, instruction in enumerate(exercise["instructions"], start=1):
            lines.append(f"  {step}. {instruction}")
        lines.append("")

    Path("MEDIA_AUDIT_2026-11-22.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
