"""End-to-end validation for LockIn's static exercise fallback system."""

from io import BytesIO
from pathlib import Path
import tempfile
from unittest.mock import patch

from PIL import Image

from app import create_app
from exercise_media import (
    EXERCISE_MEDIA,
    STATIC_EXERCISE_IMAGES,
    get_exercise_media,
)
from exercises import exercises


EXPECTED_STATIC_IDS = {
    128, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162,
    163, 164, 165, 166, 167, 169, 170, 172, 173, 174, 175, 176,
}


def main():
    project_dir = Path(__file__).resolve().parent
    assert set(STATIC_EXERCISE_IMAGES) == EXPECTED_STATIC_IDS
    assert not (set(STATIC_EXERCISE_IMAGES) & set(EXERCISE_MEDIA))

    for exercise_id, media in STATIC_EXERCISE_IMAGES.items():
        assert media["media_type"] == "jpg"
        assert media["representation_kind"] == "static_key_position"
        path = project_dir / "static" / media["media_path"]
        assert path.is_file(), path
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            assert image.format == "JPEG"
            assert image.size == (768, 768)

    active_ids = {exercise["id"] for exercise in exercises}
    valid_visual_ids = {
        exercise_id
        for exercise_id in active_ids
        if get_exercise_media(exercise_id) is not None
    }
    assert valid_visual_ids == active_ids

    # Existing animated media must retain priority over static fallbacks.
    assert get_exercise_media(168)["media_type"] == "gif"
    assert get_exercise_media(128)["representation_kind"] == "static_key_position"

    exercise_128 = next(exercise for exercise in exercises if exercise["id"] == 128)
    with tempfile.TemporaryDirectory() as temp_dir:
        app = create_app({
            "TESTING": True,
            "SECRET_KEY": "static-fallback-verification",
            "DATABASE": str(Path(temp_dir) / "fallbacks.db"),
        })
        client = app.test_client()
        response = client.post("/api/auth/register", json={
            "username": "fallback_verifier",
            "password": "test-password-123",
            "first_name": "Fallback",
            "last_name": "Verifier",
        })
        assert response.status_code == 201

        library = client.get("/api/library").get_json()["exercises"]
        assert len(library) == len(exercises)
        assert all(item["media_url"] for item in library)
        library_128 = next(item for item in library if item["id"] == 128)
        assert library_128["media_type"] == "jpg"
        assert library_128["instructions"] == exercise_128["instructions"]

        with patch("app.recommend_workout", return_value=[exercise_128]):
            response = client.post("/api/recommendations", json={
                "goal": exercise_128["goals"][0],
                "level": exercise_128["level"],
                "equipment": [],
                "duration": 30,
            })
        assert response.status_code == 200
        recommendation = response.get_json()["exercises"][0]
        assert recommendation["media_url"] == library_128["media_url"]
        assert recommendation["media_type"] == "jpg"
        assert recommendation["instructions"] == exercise_128["instructions"]

        image_response = client.get(library_128["media_url"])
        assert image_response.status_code == 200
        assert image_response.mimetype == "image/jpeg"
        with Image.open(BytesIO(image_response.data)) as image:
            assert image.format == "JPEG"

    print(
        "PASS: 155/155 active exercises have valid visuals; "
        "24 static fallbacks work in both API preview paths"
    )


if __name__ == "__main__":
    main()
