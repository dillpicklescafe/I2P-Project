"""End-to-end verification for approved LockIn exercise media mappings."""

from __future__ import annotations

import tempfile
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageChops, ImageSequence

from app import create_app
from exercise_media import EXERCISE_MEDIA
from exercises import exercises


def main() -> None:
    exercise = next(item for item in exercises if item["id"] == 168)
    mapping = EXERCISE_MEDIA[168]
    assert mapping["media_path"] == "exercises/168.gif"
    assert mapping["media_type"] == "gif"

    with tempfile.TemporaryDirectory() as temp_dir:
        app = create_app({
            "TESTING": True,
            "SECRET_KEY": "media-verification",
            "DATABASE": str(Path(temp_dir) / "media-verification.db"),
        })
        client = app.test_client()
        registration = client.post("/api/auth/register", json={
            "username": "media_verifier",
            "password": "test-password-123",
            "first_name": "Media",
            "last_name": "Verifier",
        })
        assert registration.status_code == 201

        library_response = client.get("/api/library")
        assert library_response.status_code == 200
        library_item = next(
            item for item in library_response.get_json()["exercises"]
            if item["id"] == 168
        )
        assert library_item["media_url"] == "/static/exercises/168.gif"
        assert library_item["media_type"] == "gif"

        with patch("app.recommend_workout", return_value=[exercise]):
            plan_response = client.post("/api/recommendations", json={
                "goal": exercise["goals"][0],
                "level": exercise["level"],
                "equipment": [],
                "duration": 30,
            })
        assert plan_response.status_code == 200
        plan_item = plan_response.get_json()["exercises"][0]
        assert plan_item["media_url"] == "/static/exercises/168.gif"
        assert plan_item["media_type"] == "gif"

        media_response = client.get(library_item["media_url"])
        assert media_response.status_code == 200
        assert media_response.mimetype == "image/gif"
        assert media_response.data.startswith((b"GIF87a", b"GIF89a"))

        with Image.open(BytesIO(media_response.data)) as source:
            frames = [
                frame.convert("RGB")
                for frame in ImageSequence.Iterator(source)
            ]
            assert source.info.get("loop") == 0
        assert len(frames) == 6
        assert any(
            ImageChops.difference(first, second).getbbox() is not None
            for first, second in zip(frames, frames[1:])
        )

    print("PASS: exercise 168 is animated, served, and present in both API previews")


if __name__ == "__main__":
    main()
