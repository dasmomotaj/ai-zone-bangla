from pathlib import Path
import re

TEMPLATES = Path("templates")
TOTAL = 20

START = "<!-- AI-ZONE-QURAN-PRACTICE-MODE-START -->"
END = "<!-- AI-ZONE-QURAN-PRACTICE-MODE-END -->"

def build_block(lesson_id):
    next_lesson = lesson_id + 1 if lesson_id < TOTAL else None

    if next_lesson:
        next_html = f'''
        <a class="practice-next-btn"
           href="/quran/lesson/{next_lesson}">
            ➡️ Lesson {next_lesson}-এ যান
        </a>
'''
    else:
        next_html = '''
        <a class="practice-next-btn"
           href="/quran">
            🏆 Academy Dashboard
        </a>
'''

    return f'''
{START}
<section class="quran-practice-mode"
         data-practice-mode
         data-lesson-id="{lesson_id}">

    <div class="practice-mode-header">
        <span class="practice-mode-icon">🧠</span>
        <div>
            <h2>Practice Mode</h2>
            <p>এবার নিজে অনুশীলন করুন</p>
        </div>
    </div>

    <div class="practice-mode-instructions">
        <strong>📌 কী করবেন?</strong>
        <ol>
            <li>এই Lesson-এর বিষয়টি ধীরে ধীরে আবার পড়ুন।</li>
            <li>যা শিখেছেন তা নিজের মতো করে অনুশীলন করুন।</li>
            <li>তিনটি ধাপ শেষ হলে Practice Complete হবে।</li>
        </ol>
    </div>

    <div class="practice-steps">

        <label class="practice-step">
            <input type="checkbox"
                   data-practice-step="1">
            <span>
                <strong>ধাপ ১ — বুঝেছি</strong>
                <small>Lesson-এর মূল বিষয় বুঝেছি।</small>
            </span>
        </label>

        <label class="practice-step">
            <input type="checkbox"
                   data-practice-step="2">
            <span>
                <strong>ধাপ ২ — পড়েছি</strong>
                <small>Lesson-এর উদাহরণ/নিয়ম পড়ে দেখেছি।</small>
            </span>
        </label>

        <label class="practice-step">
            <input type="checkbox"
                   data-practice-step="3">
            <span>
                <strong>ধাপ ৩ — অনুশীলন করেছি</strong>
                <small>নিজে অন্তত কয়েকবার অনুশীলন করেছি।</small>
            </span>
        </label>

    </div>

    <div class="practice-mode-status"
         data-practice-status>
        0 / 3 ধাপ সম্পন্ন
    </div>

    <div class="practice-mode-progress">
        <div data-practice-progress></div>
    </div>

    <div class="practice-mode-result"
         data-practice-result>
        🔒 তিনটি ধাপ সম্পন্ন করলে পরবর্তী Lesson-এর জন্য প্রস্তুত হবেন।
    </div>

    <div class="practice-mode-next">
        {next_html}
    </div>

</section>

<style>
.quran-practice-mode {{
    margin: 30px auto;
    max-width: 760px;
    padding: 22px;
    border-radius: 22px;
    border: 1px solid rgba(0,220,255,.22);
    background:
        linear-gradient(
            145deg,
            rgba(0,220,255,.08),
            rgba(80,40,180,.08)
        );
    box-shadow: 0 12px 40px rgba(0,0,0,.15);
}}

.practice-mode-header {{
    display:flex;
    align-items:center;
    gap:14px;
    margin-bottom:18px;
}}

.practice-mode-icon {{
    font-size:34px;
}}

.practice-mode-header h2 {{
    margin:0;
}}

.practice-mode-header p {{
    margin:4px 0 0;
    opacity:.72;
}}

.practice-mode-instructions {{
    padding:15px;
    border-radius:16px;
    background:rgba(255,255,255,.05);
    margin-bottom:18px;
}}

.practice-mode-instructions ol {{
    margin:10px 0 0;
    padding-left:22px;
}}

.practice-steps {{
    display:grid;
    gap:12px;
}}

.practice-step {{
    display:flex;
    align-items:flex-start;
    gap:12px;
    padding:16px;
    border-radius:16px;
    border:1px solid rgba(255,255,255,.12);
    cursor:pointer;
    transition:.2s ease;
}}

.practice-step:hover {{
    transform:translateY(-1px);
}}

.practice-step input {{
    width:20px;
    height:20px;
    margin-top:2px;
    flex:none;
    opacity:1;
    pointer-events:auto;
    appearance:auto;
}}

.practice-step span {{
    display:flex;
    flex-direction:column;
    gap:4px;
}}

.practice-step small {{
    opacity:.7;
}}

.practice-step:has(input:checked) {{
    border-color:rgba(0,220,255,.5);
    background:rgba(0,220,255,.08);
}}

.practice-mode-status {{
    margin-top:18px;
    font-weight:700;
    text-align:center;
}}

.practice-mode-progress {{
    height:9px;
    margin-top:10px;
    border-radius:20px;
    overflow:hidden;
    background:rgba(255,255,255,.1);
}}

.practice-mode-progress div {{
    height:100%;
    width:0%;
    border-radius:20px;
    background:linear-gradient(90deg,#00d9ff,#7c4dff);
    transition:width .3s ease;
}}

.practice-mode-result {{
    margin-top:16px;
    padding:14px;
    border-radius:14px;
    text-align:center;
}}

.practice-mode-result.complete {{
    background:rgba(0,200,120,.12);
    border:1px solid rgba(0,200,120,.3);
}}

.practice-next-btn {{
    display:inline-block;
    margin-top:16px;
    padding:12px 18px;
    border-radius:14px;
    text-decoration:none;
    font-weight:700;
    background:rgba(0,220,255,.12);
}}

.practice-mode-next {{
    text-align:center;
}}

@media (max-width:600px) {{
    .quran-practice-mode {{
        margin:24px 10px;
        padding:18px;
    }}
}}
</style>

<script>
(function() {{
    const root = document.querySelector(
        '[data-practice-mode][data-lesson-id="{lesson_id}"]'
    );

    if (!root) return;

    const steps = Array.from(
        root.querySelectorAll('[data-practice-step]')
    );

    const status = root.querySelector('[data-practice-status]');
    const progress = root.querySelector('[data-practice-progress]');
    const result = root.querySelector('[data-practice-result]');

    function updatePractice() {{
        const completed = steps.filter(step => step.checked).length;
        const percent = Math.round((completed / 3) * 100);

        status.textContent =
            completed + " / 3 ধাপ সম্পন্ন";

        progress.style.width = percent + "%";

        if (completed === 3) {{
            result.textContent =
                "✅ Practice Complete — এবার Quiz দিন!";

            result.classList.add("complete");

            try {{
                localStorage.setItem(
                    "ai_zone_quran_practice_{lesson_id}",
                    JSON.stringify({{
                        completed: true,
                        updatedAt: Date.now()
                    }})
                );
            }} catch (e) {{}}
        }} else {{
            result.textContent =
                "🔒 তিনটি ধাপ সম্পন্ন করলে Practice Complete হবে।";

            result.classList.remove("complete");
        }}
    }}

    steps.forEach(step => {{
        step.addEventListener("change", updatePractice);
    }});

    try {{
        const saved = JSON.parse(
            localStorage.getItem(
                "ai_zone_quran_practice_{lesson_id}"
            ) || "null"
        );

        if (saved && saved.completed) {{
            steps.forEach(step => {{
                step.checked = true;
            }});
        }}
    }} catch (e) {{}}

    updatePractice();
}})();
</script>
{END}
'''

updated = 0

for lesson_id in range(1, TOTAL + 1):
    if lesson_id == 1:
        path = TEMPLATES / "quran_lesson.html"
    else:
        path = TEMPLATES / f"quran_lesson_{lesson_id}.html"

    if not path.exists():
        print(f"Lesson {lesson_id}: FILE MISSING")
        continue

    content = path.read_text(encoding="utf-8")

    # Remove any previous Practice Mode block only.
    content = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        "",
        content,
        flags=re.S
    )

    block = build_block(lesson_id)

    # Put Practice Mode before Quiz.
    if "<!-- AI-ZONE-QURAN-QUIZ-START -->" in content:
        content = content.replace(
            "<!-- AI-ZONE-QURAN-QUIZ-START -->",
            block + "\n<!-- AI-ZONE-QURAN-QUIZ-START -->",
            1
        )
    elif "<!-- AI-ZONE-QURAN-PROGRESS-START -->" in content:
        content = content.replace(
            "<!-- AI-ZONE-QURAN-PROGRESS-START -->",
            block + "\n<!-- AI-ZONE-QURAN-PROGRESS-START -->",
            1
        )
    else:
        content += "\n" + block + "\n"

    path.write_text(content, encoding="utf-8")
    updated += 1

print()
print("==========================================")
print(" QURAN PRACTICE MODE INSTALLER")
print("==========================================")
print(f"Updated lessons: {updated}/{TOTAL}")

print()
print("=== TEMPLATE VERIFICATION ===")

required = [
    START,
    "quran-practice-mode",
    "practice-mode-instructions",
    "practice-steps",
    "practice-mode-progress",
    "practice-mode-result",
    END,
]

all_ok = True

for lesson_id in range(1, TOTAL + 1):
    if lesson_id == 1:
        path = TEMPLATES / "quran_lesson.html"
    else:
        path = TEMPLATES / f"quran_lesson_{lesson_id}.html"

    content = path.read_text(encoding="utf-8")

    ok = all(x in content for x in required)

    print(
        f"Lesson {lesson_id}: "
        + ("PASS" if ok else "FAIL")
    )

    if not ok:
        all_ok = False

print()
print(
    "Practice Mode: "
    + ("PASS" if all_ok else "FAIL")
)

if not all_ok:
    raise SystemExit(1)

print()
print("Practice Mode installation complete.")
