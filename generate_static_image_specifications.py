"""Generate the reviewed static-fallback specification document."""

from pathlib import Path

from exercise_media import STATIC_EXERCISE_IMAGES
from exercises import exercises


def main():
    by_id = {exercise["id"]: exercise for exercise in exercises}
    lines = [
        "# LockIn static exercise fallback specifications",
        "",
        "These are static key-position illustrations, not animated demonstrations. "
        "The complete database instructions must remain visible beside each image.",
        "",
        "## Shared visual specification",
        "",
        "- One consistent adult woman instructor with a dark-brown ponytail, charcoal sleeveless athletic top, deep-teal leggings, and white training shoes.",
        "- Polished semi-realistic fitness-instruction illustration on a plain pale studio background with soft, even lighting.",
        "- Square 768×768 JPEG, complete relevant anatomy visible, no text, arrows, captions, borders, logos, watermarks, or extra people.",
        "- Each image shows only the approved key position named below; it must not be described as showing the complete movement sequence.",
        "",
    ]
    for exercise_id, media in STATIC_EXERCISE_IMAGES.items():
        exercise = by_id[exercise_id]
        lines.extend([
            f"## {exercise_id} — {exercise['name']}",
            "",
            f"- Final file: `static/{media['media_path']}`",
            f"- Approved key position: {media['key_position']}",
            "- Original instructions:",
            "",
        ])
        for index, instruction in enumerate(exercise["instructions"], start=1):
            lines.append(f"  {index}. {instruction}")
        lines.extend([
            "- Review status: visually reviewed and approved as an accurate static key-position fallback.",
            "",
        ])
    Path("STATIC_EXERCISE_IMAGE_SPECIFICATIONS.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
