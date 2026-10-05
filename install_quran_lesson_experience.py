from pathlib import Path
import re

TOTAL = 20

BASE = Path("templates")

START = "<!-- AI-ZONE-QURAN-EXPERIENCE-START -->"
END = "<!-- AI-ZONE-QURAN-EXPERIENCE-END -->"

BLOCK = f"""
{START}

<section class="quran-learning-experience"
         data-quran-experience>

    <div class="quran-experience-header">
        <span class="quran-experience-kicker">
            📖 LESSON EXPERIENCE
        </span>

        <h2>শুনুন → পড়ুন → অনুশীলন করুন</h2>

        <p>
            এই পাঠটি ধীরে ধীরে শিখুন। আগে বুঝুন,
            তারপর পড়ে অনুশীলন করুন এবং শেষে Quiz দিন।
        </p>
    </div>

    <div class="quran-experience-grid">

        <article class="quran-experience-card">
            <div class="quran-experience-icon">🎧</div>

            <h3>শুনুন</h3>

            <p>
                সঠিক উচ্চারণ শেখার জন্য শিক্ষক বা
                নির্ভরযোগ্য ক্বারির তিলাওয়াত শুনুন।
            </p>

            <div class="quran-audio-placeholder">
                <span>🎧 Audio lesson</span>
                <small>Audio source যুক্ত হলে এখানে Player দেখা যাবে</small>
            </div>
        </article>

        <article class="quran-experience-card">
            <div class="quran-experience-icon">📖</div>

            <h3>পড়ুন</h3>

            <p>
                পাঠের উদাহরণ ধীরে ধীরে পড়ুন।
                প্রয়োজন হলে আবার আগের অংশে ফিরে আসুন।
            </p>

            <button type="button"
                    class="quran-practice-focus"
                    data-quran-focus>
                ✨ Practice Mode
            </button>
        </article>

        <article class="quran-experience-card">
            <div class="quran-experience-icon">🧠</div>

            <h3>অনুশীলন</h3>

            <p>
                ভুল হলে তাড়াহুড়া না করে আবার শুনুন,
                দেখুন এবং ধীরে ধীরে পুনরায় পড়ুন।
            </p>

            <div class="quran-practice-checklist">
                <label>
                    <input type="checkbox"
                           data-practice-check="listen">
                    শুনেছি
                </label>

                <label>
                    <input type="checkbox"
                           data-practice-check="read">
                    পড়েছি
                </label>

                <label>
                    <input type="checkbox"
                           data-practice-check="practice">
                    অনুশীলন করেছি
                </label>
            </div>
        </article>

    </div>

    <div class="quran-practice-progress"
         data-practice-progress>
        Practice: 0 / 3
    </div>

</section>

<style>
.quran-learning-experience {{
    margin:32px 0;
    padding:24px;
    border-radius:24px;
    border:1px solid rgba(255,255,255,.10);
    background:
        linear-gradient(
            145deg,
            rgba(59,130,246,.08),
            rgba(255,255,255,.025)
        );
}}

.quran-experience-header {{
    margin-bottom:20px;
}}

.quran-experience-kicker {{
    font-size:.72rem;
    font-weight:800;
    letter-spacing:.12em;
    opacity:.72;
}}

.quran-experience-header h2 {{
    margin:8px 0;
}}

.quran-experience-header p {{
    margin:0;
    opacity:.72;
    line-height:1.7;
}}

.quran-experience-grid {{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:14px;
}}

.quran-experience-card {{
    padding:18px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,.09);
    background:rgba(255,255,255,.035);
}}

.quran-experience-icon {{
    font-size:1.8rem;
    margin-bottom:8px;
}}

.quran-experience-card h3 {{
    margin:0 0 7px;
}}

.quran-experience-card p {{
    line-height:1.65;
    opacity:.74;
}}

.quran-audio-placeholder {{
    display:flex;
    flex-direction:column;
    gap:4px;
    padding:12px;
    margin-top:12px;
    border-radius:14px;
    border:1px dashed rgba(255,255,255,.16);
    background:rgba(0,0,0,.12);
}}

.quran-audio-placeholder small {{
    opacity:.55;
}}

.quran-practice-focus {{
    width:100%;
    padding:11px 14px;
    border:0;
    border-radius:12px;
    cursor:pointer;
    font-weight:700;
}}

.quran-practice-checklist {{
    display:flex;
    flex-direction:column;
    gap:9px;
    margin-top:12px;
}}

.quran-practice-checklist label {{
    display:flex;
    align-items:center;
    gap:9px;
    cursor:pointer;
}}

.quran-practice-checklist input {{
    width:18px;
    height:18px;
}}

.quran-practice-progress {{
    margin-top:18px;
    padding:12px 14px;
    border-radius:14px;
    background:rgba(34,197,94,.07);
    border:1px solid rgba(34,197,94,.20);
    font-weight:700;
    text-align:center;
}}

@media (max-width:760px) {{
    .quran-experience-grid {{
        grid-template-columns:1fr;
    }}

    .quran-learning-experience {{
        padding:18px;
        border-radius:20px;
    }}
}}
</style>

<script>
(function () {{
    const checks =
        document.querySelectorAll(
            "[data-practice-check]"
        );

    const progress =
        document.querySelector(
            "[data-practice-progress]"
        );

    const focusButton =
        document.querySelector(
            "[data-quran-focus]"
        );

    function updatePractice() {{
        let done = 0;

        checks.forEach(function (check) {{
            if (check.checked) {{
                done++;
            }}
        }});

        if (progress) {{
            progress.textContent =
                "Practice: " + done + " / " + checks.length;

            if (done === checks.length) {{
                progress.textContent =
                    "✓ Practice Complete — এখন Quiz দিন";
            }}
        }}
    }}

    checks.forEach(function (check) {{
        check.addEventListener(
            "change",
            updatePractice
        );
    }});

    if (focusButton) {{
        focusButton.addEventListener("click", function () {{
            const target =
                document.querySelector(
                    ".quran-lesson-content, .lesson-content, main"
                );

            if (target) {{
                target.scrollIntoView({{
                    behavior:"smooth",
                    block:"start"
                }});
            }}
        }});
    }}

    updatePractice();
}})();
</script>

{END}
"""

def lesson_file(lesson_id):
    if lesson_id == 1:
        return BASE / "quran_lesson.html"
    return BASE / f"quran_lesson_{lesson_id}.html"

updated = 0

for lesson_id in range(1, TOTAL + 1):
    path = lesson_file(lesson_id)

    if not path.exists():
        print(f"Lesson {lesson_id}: FILE MISSING")
        continue

    text = path.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(START) + r".*?" + re.escape(END),
        re.S
    )

    if START in text:
        text = pattern.sub(BLOCK.strip(), text)
        print(f"Lesson {lesson_id}: experience refreshed")
    else:
        # Put the experience before the first Quiz section.
        quiz_marker = "<!-- AI-ZONE-QURAN-QUIZ-START -->"

        if quiz_marker in text:
            text = text.replace(
                quiz_marker,
                BLOCK.strip() + "\n\n" + quiz_marker,
                1
            )
        else:
            # Fallback: insert before </main>, then </body>.
            if "</main>" in text:
                text = text.replace(
                    "</main>",
                    BLOCK.strip() + "\n</main>",
                    1
                )
            elif "</body>" in text:
                text = text.replace(
                    "</body>",
                    BLOCK.strip() + "\n</body>",
                    1
                )
            else:
                text += "\n" + BLOCK

        print(f"Lesson {lesson_id}: experience installed")

    path.write_text(text, encoding="utf-8")
    updated += 1

print()
print(f"Updated lesson templates: {updated}/{TOTAL}")
