"""Normalize generated static exercise fallbacks for web delivery."""

from pathlib import Path

from PIL import Image

from exercise_media import STATIC_EXERCISE_IMAGES


def main():
    static_dir = Path(__file__).resolve().parent / "static"
    for exercise_id, media in STATIC_EXERCISE_IMAGES.items():
        destination = static_dir / media["media_path"]
        source = destination.with_suffix(".png")
        if not source.is_file():
            raise FileNotFoundError(source)
        with Image.open(source) as image:
            normalized = image.convert("RGB")
            normalized.thumbnail((768, 768), Image.Resampling.LANCZOS)
            if normalized.size != (768, 768):
                raise ValueError(f"Expected square image for {exercise_id}: {normalized.size}")
            normalized.save(
                destination,
                format="JPEG",
                quality=88,
                optimize=True,
                progressive=True,
            )
        print(f"{exercise_id}: {destination.name}")


if __name__ == "__main__":
    main()
