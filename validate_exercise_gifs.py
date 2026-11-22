"""Technical checks and contact sheets for LockIn exercise GIF review.

This script is intentionally read-only with respect to source media. It writes
temporary contact sheets to a caller-selected directory so a reviewer can
inspect representative frames before any mapping is approved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageOps, ImageSequence


def frame_digest(frame: Image.Image) -> str:
    normalized = frame.convert("RGB").resize((128, 128))
    return hashlib.sha256(normalized.tobytes()).hexdigest()


def inspect_gif(path: Path, sheet_path: Path, sample_count: int = 12) -> dict:
    with Image.open(path) as source:
        frames = [frame.convert("RGB") for frame in ImageSequence.Iterator(source)]
        durations = [
            frame.info.get("duration", source.info.get("duration", 0))
            for frame in ImageSequence.Iterator(source)
        ]
        loop = source.info.get("loop")

    digests = [frame_digest(frame) for frame in frames]
    distinct_exact = len(set(digests))
    changed_pairs = 0
    for previous, current in zip(frames, frames[1:]):
        difference = ImageChops.difference(previous, current)
        if difference.getbbox() is not None:
            changed_pairs += 1

    if len(frames) <= sample_count:
        indexes = list(range(len(frames)))
    else:
        indexes = sorted({
            round(position * (len(frames) - 1) / (sample_count - 1))
            for position in range(sample_count)
        })

    tile_size = (280, 280)
    columns = 4
    rows = (len(indexes) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_size[0], rows * 320), "white")
    draw = ImageDraw.Draw(sheet)
    for slot, frame_index in enumerate(indexes):
        frame = ImageOps.contain(frames[frame_index], (260, 260))
        x = (slot % columns) * tile_size[0] + (tile_size[0] - frame.width) // 2
        y = (slot // columns) * 320 + 10
        sheet.paste(frame, (x, y))
        draw.text(
            ((slot % columns) * tile_size[0] + 10, (slot // columns) * 320 + 278),
            f"frame {frame_index + 1}/{len(frames)}",
            fill="black",
        )
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(sheet_path)

    return {
        "path": str(path),
        "format": "GIF",
        "width": frames[0].width,
        "height": frames[0].height,
        "frame_count": len(frames),
        "distinct_exact_frames": distinct_exact,
        "changed_adjacent_pairs": changed_pairs,
        "loop": loop,
        "duration_ms": sum(duration for duration in durations if duration),
        "technical_pass": len(frames) > 1 and distinct_exact > 1 and changed_pairs > 0,
        "contact_sheet": str(sheet_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    results = []
    for path in args.paths:
        result = inspect_gif(
            path,
            args.output_dir / f"{path.stem}-contact-sheet.jpg",
        )
        results.append(result)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
