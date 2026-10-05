from pathlib import Path
import re

TOTAL = 20

path = Path("templates/quran.html")
text = path.read_text(encoding="utf-8")

START = "<!-- AI-ZONE-QURAN-CARD-STATUS-START -->"
END = "<!-- AI-ZONE-QURAN-CARD-STATUS-END -->"

block = f"""
{START}
<style>
.quran-live-status {{
    display:flex;
    flex-wrap:wrap;
    gap:7px;
    margin-top:12px;
}}

.quran-live-badge {{
    display:inline-flex;
    align-items:center;
    gap:5px;
    padding:6px 10px;
    border-radius:999px;
    font-size:.74rem;
    font-weight:700;
    border:1px solid rgba(255,255,255,.12);
    background:rgba(255,255,255,.055);
}}

.quran-live-badge.complete {{
    border-color:rgba(34,197,94,.45);
}}

.quran-live-badge.quiz {{
    border-color:rgba(59,130,246,.45);
}}

@media (max-width:640px) {{
    .quran-live-badge {{
        font-size:.69rem;
        padding:5px 8px;
    }}
}}
</style>

<script>
(function () {{
    const PROGRESS_KEY = "ai_zone_quran_progress_v1";
    const QUIZ_KEY = "ai_zone_quran_quiz_v1";

    function read(key) {{
        try {{
            return JSON.parse(localStorage.getItem(key) || "{{}}");
        }} catch (e) {{
            return {{}};
        }}
    }}

    function refreshLessonCards() {{
        const progress = read(PROGRESS_KEY);
        const quizzes = read(QUIZ_KEY);

        document.querySelectorAll("[data-quran-live-card]").forEach(card => {{
            const lessonId = Number(card.dataset.quranLiveCard);

            const completed =
                progress[String(lessonId)] === true ||
                progress[lessonId] === true;

            const quiz =
                quizzes[String(lessonId)] ||
                quizzes[lessonId];

            let status = card.querySelector(".quran-live-status");

            if (!status) {{
                status = document.createElement("div");
                status.className = "quran-live-status";
                card.appendChild(status);
            }}

            status.innerHTML = "";

            if (completed) {{
                const badge = document.createElement("span");
                badge.className = "quran-live-badge complete";
                badge.textContent = "✓ পাঠ সম্পন্ন";
                status.appendChild(badge);
            }}

            if (quiz && quiz.passed) {{
                const badge = document.createElement("span");
                badge.className = "quran-live-badge quiz";
                badge.textContent = "✓ Quiz Passed";
                status.appendChild(badge);
            }}
        }});
    }}

    window.AIZoneRefreshQuranLessonCards = refreshLessonCards;

    if (document.readyState === "loading") {{
        document.addEventListener("DOMContentLoaded", refreshLessonCards);
    }} else {{
        refreshLessonCards();
    }}

    window.addEventListener("storage", function (event) {{
        if (
            event.key === PROGRESS_KEY ||
            event.key === QUIZ_KEY
        ) {{
            refreshLessonCards();
        }}
    }});
}})();
</script>
{END}
"""

# Remove old block if present, then install exactly once.
pattern = re.compile(
    re.escape(START) + r".*?" + re.escape(END),
    re.S
)

if START in text:
    text = pattern.sub(block.strip(), text)
    print("Existing status block replaced.")
else:
    marker = "</body>"
    if marker in text:
        text = text.replace(marker, block + "\n" + marker, 1)
    else:
        text += "\n" + block
    print("Status block installed.")

# Add data marker to likely lesson cards.
added = 0

for lesson_id in range(1, TOTAL + 1):

    if f'data-quran-live-card="{lesson_id}"' in text:
        continue

    patterns = [
        rf'(<[^>]*data-lesson-id="{lesson_id}"[^>]*)',
        rf'(<[^>]*data-lesson="{lesson_id}"[^>]*)',
    ]

    found = False

    for pattern_text in patterns:
        match = re.search(pattern_text, text)

        if match:
            original = match.group(1)

            if "data-quran-live-card" not in original:
                replacement = (
                    original +
                    f' data-quran-live-card="{lesson_id}"'
                )

                text = (
                    text[:match.start(1)] +
                    replacement +
                    text[match.end(1):]
                )

                added += 1
                found = True

            break

    if found:
        print(f"Lesson {lesson_id}: marker added")
    else:
        print(f"Lesson {lesson_id}: existing card marker not detected")

path.write_text(text, encoding="utf-8")

print()
print(f"Card markers added: {added}")
print("Installer finished successfully.")
