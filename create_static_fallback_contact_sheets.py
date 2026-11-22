"""Create temporary contact sheets for final visual review."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from exercise_media import STATIC_EXERCISE_IMAGES


def main():
    project_dir = Path(__file__).resolve().parent
    output_dir = project_dir / ".static_fallback_review"
    output_dir.mkdir(exist_ok=True)
    entries = list(STATIC_EXERCISE_IMAGES.items())
    for sheet_index in range(3):
        sheet_entries = entries[sheet_index * 8:(sheet_index + 1) * 8]
        sheet = Image.new("RGB", (1200, 1200), "white")
        draw = ImageDraw.Draw(sheet)
        for slot, (exercise_id, media) in enumerate(sheet_entries):
            path = project_dir / "static" / media["media_path"]
            with Image.open(path) as source:
                thumbnail = ImageOps.contain(source.convert("RGB"), (560, 500))
            x = (slot % 2) * 600 + 20
            y = (slot // 2) * 300 + 10
            sheet.paste(thumbnail.resize((280, 280)), (x, y))
            draw.text((x + 290, y + 20), f"{exercise_id}", fill="black")
            draw.text((x + 290, y + 45), media["lockin_name"], fill="black")
            draw.text((x + 290, y + 80), media["key_position"], fill="black")
        sheet.save(output_dir / f"sheet-{sheet_index + 1}.jpg", quality=88)
        print(output_dir / f"sheet-{sheet_index + 1}.jpg")


if __name__ == "__main__":
    main()
