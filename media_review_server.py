"""Local-only server for the LockIn missing-media review tool.

This module is intentionally separate from app.py and never writes media
mappings or review decisions. Decisions live in the browser's localStorage.
"""

import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from exercise_media import get_exercise_media
from exercises import exercises


PROJECT_DIR = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8766


def repdb_candidate(name, slug, warning, *, equipment="", position="", movement=""):
    root = "static/exercises/repdb_review/"
    main_path = PROJECT_DIR / root / f"{slug}-main.webp"
    media = []
    if main_path.is_file():
        media.append({"path": root + f"{slug}-main.webp", "kind": "image", "label": "Main pose"})
    else:
        for pose in ("start", "peak"):
            path = PROJECT_DIR / root / f"{slug}-{pose}.webp"
            if path.is_file():
                media.append({"path": root + f"{slug}-{pose}.webp", "kind": "image", "label": f"{pose.title()} pose"})
    return {
        "source_type": "RepDB free-tier dataset",
        "original_name": name,
        "source_id": slug,
        "media": media,
        "warning": warning,
        "mismatches": {
            "equipment": equipment,
            "body_position": position,
            "movement": movement,
        },
    }


def local_candidate(name, path, kind, warning, *, source, equipment="", position="", movement=""):
    return {
        "source_type": source,
        "original_name": name,
        "source_id": path,
        "media": [{"path": path, "kind": kind, "label": "Local preview"}],
        "warning": warning,
        "mismatches": {
            "equipment": equipment,
            "body_position": position,
            "movement": movement,
        },
    }


# These are deliberately possible matches, not approvals. Candidates were
# limited to files already present in the RepDB review set or local review
# assets. Similar names were excluded when the movement was unrelated.
CANDIDATES = {
    31: [repdb_candidate(
        "Push-Up", "push-up",
        "A standard push-up is related, but it does not verify the required wide hand placement.",
        movement="Candidate uses standard hand width; LockIn requires hands wider than shoulder-width.",
    )],
    48: [repdb_candidate(
        "Superman", "superman",
        "Likely movement match; confirm the candidate lifts and lowers rather than holding the peak.",
        movement="RepDB supplies two poses; review whether they communicate a dynamic repetition.",
    )],
    59: [repdb_candidate(
        "Superman", "superman",
        "Related prone back exercise, but the arm position and isometric emphasis differ.",
        position="Candidate arms extend overhead; LockIn uses a prone cobra arm position.",
        movement="Candidate depicts a full superman lift rather than scapular retraction in a cobra hold.",
    )],
    62: [repdb_candidate(
        "Dumbbell Bicep Curl", "bicep-curl",
        "The curl path is related, but the RepDB demonstration is standing rather than seated.",
        position="RepDB candidate is standing; LockIn exercise is seated.",
    )],
    63: [repdb_candidate(
        "Dumbbell Bicep Curl", "bicep-curl",
        "Generic standing curl does not show the elbow braced against the inner thigh.",
        position="Candidate is standing; LockIn concentration curl is seated.",
        movement="Candidate does not demonstrate the concentration-curl arm brace.",
    )],
    64: [repdb_candidate(
        "Dumbbell Bicep Curl", "bicep-curl",
        "The exercise family matches, but the images may show both arms moving together.",
        movement="LockIn alternates arms; candidate may depict a bilateral curl.",
    )],
    69: [local_candidate(
        "Chair Triceps Dip", "static/review_previews/pexels-4159114-chair-dip.mp4", "video",
        "Local Pexels preview demonstrates a chair dip, not the specified bench variation.",
        source="Local licensed candidate library (Pexels)",
        equipment="Candidate uses a chair; LockIn requires a bench.",
    )],
    75: [repdb_candidate(
        "Close Grip Push Ups", "close-grip-push-ups",
        "Close-grip form is related, but it may not show the diamond hand shape.",
        movement="LockIn requires thumbs and index fingers close in a diamond; candidate is only close-grip.",
    )],
    77: [repdb_candidate(
        "Bodyweight Squat", "bodyweight-squat",
        "Standard squat is related but does not verify the wide, toes-out sumo stance.",
        position="Candidate stance is narrower than the LockIn sumo stance.",
        movement="Hip and knee action is similar, but stance changes the exercise emphasis.",
    )],
    84: [repdb_candidate(
        "Bodyweight Calf Raise", "bodyweight-calf-raise",
        "The ankle movement matches, but the candidate is standing rather than seated.",
        position="RepDB candidate is standing; LockIn exercise is seated.",
    )],
    87: [local_candidate(
        "Donkey Kick", "static/review_previews/pexels-6303430-donkey-kick.jpg", "image",
        "Both begin on hands and knees, but the leg travels backward instead of out to the side.",
        source="Local licensed candidate library (Pexels)",
        movement="Donkey kick is hip extension; fire hydrant requires lateral hip abduction.",
    )],
    97: [repdb_candidate(
        "Russian Twist", "russian-twist",
        "Possible close match; verify bent knees, torso angle, and equipment-free rotation.",
    )],
    103: [repdb_candidate(
        "Plank", "plank",
        "A plank is related, but it does not show knees hovering in the bear-crawl position.",
        position="Candidate uses a straight-leg plank; LockIn requires bent knees hovering below the hips.",
        movement="Candidate does not demonstrate the quadruped bear-crawl hold.",
    )],
    112: [local_candidate(
        "Shadow Boxing", "static/review_previews/pexels-6296438-shadow-boxing.mp4", "video",
        "The punches match, but the local demonstration is standing rather than seated.",
        source="Local licensed candidate library (Pexels)",
        position="Candidate is standing; LockIn requires a seated position.",
    )],
    113: [repdb_candidate(
        "Jumping Jacks", "jumping-jacks",
        "Arm pattern is related, but jumping jacks do not show the required low-impact side step.",
        movement="Candidate jumps both feet; LockIn steps laterally one side at a time.",
    )],
    117: [local_candidate(
        "Speed Skater", "static/exercises/118.gif", "image",
        "The lateral pattern is related, but speed skaters may hop rather than use a controlled step.",
        source="Local user-provided exercise asset (license unreviewed)",
        movement="Candidate may be a hopping skater; LockIn specifies a lower-impact skater step.",
    )],
    124: [local_candidate(
        "Single-leg Reach", "static/exercises/123.gif", "image",
        "Related balance reach, but it may not demonstrate the full clock-direction sequence.",
        source="Local user-provided exercise asset (license unreviewed)",
        movement="LockIn reaches to multiple clock points; candidate may show only one reach direction.",
    )],
    126: [local_candidate(
        "Standing Tree Pose", "static/review_previews/pexels-6323275-tree-pose.mp4", "video",
        "The pose matches, but the demonstration does not use the required support.",
        source="Local licensed candidate library (Pexels)",
        equipment="LockIn permits chair support; candidate is unsupported.",
    )],
    128: [local_candidate(
        "Weight Shift Side-to-Side", "static/exercises/127.gif", "image",
        "This local asset shifts laterally, while LockIn requires forward-to-back weight transfer.",
        source="Local user-provided exercise asset (license unreviewed)",
        movement="Candidate moves side-to-side; LockIn moves front-to-back.",
    )],
    135: [repdb_candidate(
        "Heel-to-Toe Walk", "heel-to-toe-walk",
        "The narrow-base walking pattern is related, but it does not show lateral tightrope steps.",
        movement="Candidate travels forward; LockIn travels sideways.",
    )],
    136: [local_candidate(
        "Neck Rotation", "static/exercises/137.gif", "image",
        "Neck mobility is related, but turning left/right is not the same as lateral neck tilt.",
        source="Local user-provided exercise asset (license unreviewed)",
        movement="Candidate rotates the head; LockIn tilts the ear toward the shoulder.",
    )],
    153: [local_candidate(
        "Single-leg Reach", "static/exercises/123.gif", "image",
        "Potential component match, but the LockIn flow requires forward, side, and rear reaches.",
        source="Local user-provided exercise asset (license unreviewed)",
        movement="Candidate may show one reach direction rather than the three-direction flow.",
    )],
    154: [repdb_candidate(
        "Push-Up", "push-up",
        "Base movement matches, but still poses cannot verify a three-second lower and bottom pause.",
        movement="LockIn adds a prescribed eccentric tempo and pause not visible in the candidate.",
    )],
    156: [repdb_candidate(
        "Reverse Lunge", "reverse-lunge",
        "Only one component matches; the candidate omits torso rotation and overhead arm sweep.",
        equipment="RepDB pose appears to use dumbbells; LockIn requires no equipment.",
        movement="Candidate shows a reverse lunge, not the complete mobility flow.",
    )],
    160: [repdb_candidate(
        "Superman", "superman",
        "Related prone posture work, but it does not show the overhead-to-W arm sweep.",
        movement="LockIn requires a controlled Y-to-W-style arm path; candidate shows a superman lift.",
    )],
    161: [repdb_candidate(
        "Bodyweight Squat", "bodyweight-squat",
        "Squat component matches, but the forward and overhead reach sequence is absent.",
        movement="Candidate demonstrates a squat only; LockIn adds coordinated arm reaches.",
    )],
    166: [repdb_candidate(
        "Child's Pose", "childs-pose",
        "The base kneeling position is related, but it does not show side walking for a lat stretch.",
        movement="Candidate is a centered static pose; LockIn walks both hands laterally.",
    )],
    167: [repdb_candidate(
        "Push-Up", "push-up",
        "Related movement, but the candidate does not verify slow eccentric-only repetitions with a knee reset.",
        movement="LockIn emphasizes lowering only and resets from the knees.",
    )],
    168: [repdb_candidate(
        "Plank", "plank",
        "Starting position matches, but the static image does not show forward/back shoulder shifting.",
        movement="Candidate is static; LockIn repeatedly shifts shoulders beyond and behind the wrists.",
    )],
    171: [local_candidate(
        "Speed Skater", "static/exercises/118.gif", "image",
        "Lateral travel is similar, but confirm the candidate lands on one leg and visibly sticks the landing.",
        source="Local user-provided exercise asset (license unreviewed)",
        movement="LockIn requires a deliberate balance hold after every bound.",
    )],
    172: [local_candidate(
        "Basic Burpee", "static/review_previews/pexels-8858142-burpee.mp4", "video",
        "A burpee is related, but confirm it includes the required push-up and does not force an extra jump.",
        source="Local licensed candidate library (Pexels)",
        movement="Candidate may omit the push-up or add a jump that LockIn deliberately excludes.",
    )],
    173: [repdb_candidate(
        "Side Lunge", "side-lunge",
        "Related lateral squat, but a Cossack squat keeps the opposite leg straight and transitions side-to-side.",
        position="Candidate depth and straight-leg position may differ from a Cossack squat.",
        movement="Candidate may return to standing between reps rather than flow across a wide stance.",
    )],
}


def review_records():
    records = []
    for exercise in exercises:
        if get_exercise_media(exercise["id"]) is not None:
            continue
        candidates = []
        for candidate in CANDIDATES.get(exercise["id"], []):
            available_media = [
                media for media in candidate["media"]
                if (PROJECT_DIR / media["path"]).is_file()
            ]
            if available_media:
                candidate = {**candidate, "media": available_media}
                candidates.append(candidate)
        records.append({
            "id": exercise["id"],
            "name": exercise["name"],
            "difficulty": exercise["level"],
            "equipment": exercise["equipment"],
            "position": exercise["position"],
            "instructions": exercise["instructions"],
            "candidates": candidates,
            "no_candidate_note": (
                "No suitable candidate found in the available RepDB free-tier poses "
                "or local review assets. No match has been invented."
            ),
        })
    return records


class ReviewHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path in ("/", "/media_review_66.html"):
            return self.send_file(PROJECT_DIR / "media_review_66.html")
        if path == "/api/review-data":
            payload = json.dumps({"exercises": review_records()}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)
            return
        if path.startswith("/static/"):
            target = (PROJECT_DIR / path.lstrip("/")).resolve()
            static_root = (PROJECT_DIR / "static").resolve()
            if target == static_root or static_root not in target.parents:
                return self.send_error(403)
            return self.send_file(target)
        self.send_error(404)

    def send_file(self, path):
        if not path.is_file():
            return self.send_error(404)
        content = path.read_bytes()
        media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", media_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        print("[media review] " + format % args)


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), ReviewHandler)
    print(f"LockIn media review: http://{HOST}:{PORT}/media_review_66.html")
    print("Press Ctrl+C to stop. Decisions remain in this browser's local storage.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping media review server.")
    finally:
        server.server_close()
