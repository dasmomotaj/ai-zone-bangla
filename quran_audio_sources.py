"""
AI Zone বাংলা — Quran Audio Source Registry

Purpose:
- Keep lesson audio sources in one place.
- Never invent or guess audio URLs.
- Empty source means the lesson is not connected to an audio file yet.
- Later, verified recitation sources can be added safely.
"""

TOTAL_LESSONS = 20


# Keep this dictionary intentionally empty for now.
# Example of the expected structure:
#
# AUDIO_SOURCES = {
#     1: {
#         "url": "VERIFIED_AUDIO_URL",
#         "title": "Lesson 1 Recitation",
#         "reciter": "Verified Reciter",
#         "language": "ar",
#     }
# }
#
# Do NOT add an unverified URL here.

AUDIO_SOURCES = {}


def get_audio_source(lesson_id):
    """Return a lesson's audio metadata or None."""
    try:
        lesson_id = int(lesson_id)
    except (TypeError, ValueError):
        return None

    if lesson_id < 1 or lesson_id > TOTAL_LESSONS:
        return None

    source = AUDIO_SOURCES.get(lesson_id)

    if not source:
        return None

    if not isinstance(source, dict):
        return None

    url = str(source.get("url", "")).strip()

    if not url:
        return None

    return {
        "url": url,
        "title": str(
            source.get("title", f"Lesson {lesson_id} Audio")
        ).strip(),
        "reciter": str(source.get("reciter", "")).strip(),
        "language": str(source.get("language", "ar")).strip(),
    }


def audio_source_count():
    """Return the number of configured audio sources."""
    return sum(
        1 for lesson_id in range(1, TOTAL_LESSONS + 1)
        if get_audio_source(lesson_id)
    )


if __name__ == "__main__":
    print("=" * 42)
    print(" AI Zone বাংলা — Quran Audio Registry")
    print("=" * 42)
    print(f"Lessons supported: {TOTAL_LESSONS}")
    print(f"Configured sources: {audio_source_count()}")
    print("Registry status: PASS")
