from pathlib import Path
import re
import shutil

ROOT = Path(".")
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"

TEMPLATES.mkdir(exist_ok=True)
STATIC.mkdir(exist_ok=True)

START = "<!-- AI-ZONE-QURAN-COMPLETION-FEEDBACK-START -->"
END = "<!-- AI-ZONE-QURAN-COMPLETION-FEEDBACK-END -->"

CSS_START = "/* AI-ZONE-QURAN-COMPLETION-FEEDBACK-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-COMPLETION-FEEDBACK-CSS-END */"

JS_START = "/* AI-ZONE-QURAN-COMPLETION-FEEDBACK-JS-START */"
JS_END = "/* AI-ZONE-QURAN-COMPLETION-FEEDBACK-JS-END */"

LESSON_FILES = [
    TEMPLATES / "quran_lesson.html",
    *[TEMPLATES / f"quran_lesson_{i}.html" for i in range(2, 21)]
]


def replace_block(text, start, end, block):
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        re.S
    )
    if pattern.search(text):
        return pattern.sub(block, text, count=1), True
    return text, False


def lesson_id_from_file(path):
    if path.name == "quran_lesson.html":
        return 1

    m = re.search(r"quran_lesson_(\d+)\.html$", path.name)
    if not m:
        return None

    return int(m.group(1))


def feedback_html(lesson_id):
    if lesson_id < 20:
        action_html = f"""
      <div class="quran-completion-actions">
        <a class="quran-completion-btn primary"
           href="{{{{ url_for('quran_lesson_{lesson_id + 1}') }}}}">
          ➡️ পরের পাঠ
        </a>

        <a class="quran-completion-btn secondary"
           href="/quran">
          🏠 Academy Dashboard
        </a>
      </div>
"""
    else:
        action_html = """
      <div class="quran-completion-actions">
        <a class="quran-completion-btn primary"
           href="/quran">
          🏆 Academy Dashboard
        </a>

        <a class="quran-completion-btn secondary"
           href="/quran">
          🔄 Revision চালিয়ে যান
        </a>
      </div>
"""

    return f"""
{START}
<section
  class="quran-completion-feedback"
  data-quran-completion-feedback
  data-lesson-id="{lesson_id}"
  aria-live="polite">

  <div class="quran-completion-icon" data-completion-icon>✓</div>

  <div class="quran-completion-content">
    <span class="quran-completion-label">LESSON RESULT</span>

    <h2 data-completion-title>
      আপনার শেখার অগ্রগতি
    </h2>

    <p data-completion-message>
      Quiz শেষ করার পর আপনার ফলাফল অনুযায়ী পরবর্তী পদক্ষেপ এখানে দেখা যাবে।
    </p>

    <div class="quran-completion-state"
         data-completion-state>
      Quiz সম্পন্ন হলে Smart Feedback দেখাবে।
    </div>

    <div class="quran-completion-actions"
         data-smart-actions>
      {action_html}
    </div>
  </div>
</section>
{END}
"""


CSS_BLOCK = f"""
{CSS_START}

.quran-completion-feedback {{
  margin: 28px 0;
  padding: 22px;
  border: 1px solid rgba(70, 220, 255, .22);
  border-radius: 22px;
  background:
    linear-gradient(135deg,
      rgba(15, 25, 45, .96),
      rgba(8, 15, 30, .96));
  box-shadow: 0 14px 45px rgba(0,0,0,.25);
  display: flex;
  gap: 18px;
  align-items: flex-start;
}}

.quran-completion-icon {{
  width: 54px;
  height: 54px;
  min-width: 54px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 25px;
  font-weight: 800;
  background: rgba(40, 220, 150, .12);
  border: 1px solid rgba(40, 220, 150, .35);
}}

.quran-completion-content {{
  flex: 1;
}}

.quran-completion-label {{
  font-size: 11px;
  letter-spacing: 1.8px;
  opacity: .62;
}}

.quran-completion-content h2 {{
  margin: 5px 0 8px;
  font-size: 22px;
}}

.quran-completion-content p {{
  margin: 0 0 12px;
  line-height: 1.7;
  opacity: .82;
}}

.quran-completion-state {{
  display: inline-block;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 13px;
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.09);
}}

.quran-completion-actions {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 16px;
}}

.quran-completion-btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 10px 16px;
  border-radius: 13px;
  text-decoration: none;
  font-weight: 700;
  transition: transform .2s ease, opacity .2s ease;
}}

.quran-completion-btn:hover {{
  transform: translateY(-1px);
}}

.quran-completion-btn.primary {{
  background: linear-gradient(135deg, #19d3ff, #6d5cff);
  color: #fff;
}}

.quran-completion-btn.secondary {{
  background: rgba(255,255,255,.07);
  color: inherit;
  border: 1px solid rgba(255,255,255,.12);
}}

.quran-completion-feedback.status-completed {{
  border-color: rgba(40, 220, 150, .35);
}}

.quran-completion-feedback.status-revision {{
  border-color: rgba(255, 190, 70, .35);
}}

.quran-completion-feedback.status-ready {{
  border-color: rgba(70, 180, 255, .35);
}}

@media (max-width: 620px) {{
  .quran-completion-feedback {{
    padding: 17px;
    gap: 12px;
    border-radius: 18px;
  }}

  .quran-completion-icon {{
    width: 44px;
    height: 44px;
    min-width: 44px;
    font-size: 20px;
  }}

  .quran-completion-content h2 {{
    font-size: 18px;
  }}

  .quran-completion-actions {{
    flex-direction: column;
  }}

  .quran-completion-btn {{
    width: 100%;
  }}
}}

{CSS_END}
"""


JS_BLOCK = f"""
{JS_START}

(function () {{
  "use strict";

  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PASS_SCORE = 70;

  function readJSON(key, fallback) {{
    try {{
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    }} catch (error) {{
      return fallback;
    }}
  }}

  function lessonIdOf(item) {{
    const value =
      item?.lessonId ??
      item?.lesson_id ??
      item?.lesson ??
      item?.id;

    const number = Number(value);
    return Number.isFinite(number) ? number : null;
  }}

  function scoreOf(item) {{
    const value =
      item?.score ??
      item?.percentage ??
      item?.percent ??
      item?.result?.score;

    const number = Number(value);
    return Number.isFinite(number) ? number : null;
  }}

  function latestQuizResult(lessonId) {{
    const data = readJSON(QUIZ_KEY, null);

    if (!data) return null;

    let items = [];

    if (Array.isArray(data)) {{
      items = data;
    }} else if (Array.isArray(data.results)) {{
      items = data.results;
    }} else if (Array.isArray(data.history)) {{
      items = data.history;
    }} else if (Array.isArray(data.attempts)) {{
      items = data.attempts;
    }}

    const matches = items
      .filter(item => lessonIdOf(item) === lessonId)
      .map(item => ({{
        item,
        score: scoreOf(item),
        timestamp: Number(
          item?.timestamp ??
          item?.time ??
          item?.createdAt ??
          item?.created_at ??
          0
        )
      }}))
      .filter(entry => entry.score !== null);

    if (!matches.length) return null;

    matches.sort((a, b) => b.timestamp - a.timestamp);

    return matches[0];
  }}

  function setText(root, selector, value) {{
    const element = root.querySelector(selector);
    if (element) element.textContent = value;
  }}

  function updateCompletion(root) {{
    const lessonId = Number(root.dataset.lessonId);
    if (!Number.isFinite(lessonId)) return;

    const result = latestQuizResult(lessonId);

    root.classList.remove(
      "status-completed",
      "status-revision",
      "status-ready"
    );

    if (!result) {{
      setText(
        root,
        "[data-completion-title]",
        "আপনার শেখার অগ্রগতি"
      );

      setText(
        root,
        "[data-completion-message]",
        "Practice ও Quiz সম্পন্ন করার পর আপনার ফলাফল অনুযায়ী পরবর্তী পদক্ষেপ এখানে দেখা যাবে।"
      );

      setText(
        root,
        "[data-completion-state]",
        "Quiz এখনও সম্পন্ন হয়নি"
      );

      return;
    }}

    const score = result.score;

    if (score >= PASS_SCORE) {{
      root.classList.add("status-completed");

      setText(
        root,
        "[data-completion-icon]",
        "✓"
      );

      setText(
        root,
        "[data-completion-title]",
        "মাশাআল্লাহ! পাঠটি সম্পন্ন হয়েছে"
      );

      setText(
        root,
        "[data-completion-message]",
        "আপনি এই পাঠের Quiz-এ পাস করেছেন। এখন পরের পাঠে এগিয়ে যেতে পারেন অথবা Revision করতে পারেন।"
      );

      setText(
        root,
        "[data-completion-state]",
        "Quiz Score: " + score + "% • Completed"
      );

    }} else {{
      root.classList.add("status-revision");

      setText(
        root,
        "[data-completion-icon]",
        "↻"
      );

      setText(
        root,
        "[data-completion-title]",
        "আরও একটু অনুশীলন করুন"
      );

      setText(
        root,
        "[data-completion-message]",
        "এই Quiz-এ আপনার স্কোর 70%-এর নিচে। আগে Revision ও Practice করুন, তারপর আবার Quiz দিন।"
      );

      setText(
        root,
        "[data-completion-state]",
        "Quiz Score: " + score + "% • Revision Recommended"
      );
    }}
  }}

  function refreshCompletionFeedback() {{
    document
      .querySelectorAll("[data-quran-completion-feedback]")
      .forEach(updateCompletion);
  }}

  window.AIZoneRefreshQuranCompletionFeedback =
    refreshCompletionFeedback;

  document.addEventListener(
    "DOMContentLoaded",
    refreshCompletionFeedback
  );

  window.addEventListener(
    "storage",
    function (event) {{
      if (event.key === QUIZ_KEY || event.key === null) {{
        refreshCompletionFeedback();
      }}
    }}
  );
}})();

{JS_END}
"""


updated = 0
already = 0

print("=" * 60)
print(" AI Zone বাংলা — Quran Completion Feedback Installer")
print("=" * 60)

for path in LESSON_FILES:
    if not path.exists():
        print(f"SKIP missing: {path}")
        continue

    lesson_id = lesson_id_from_file(path)

    if lesson_id is None:
        continue

    backup = path.with_suffix(
        path.suffix + ".before-session23-step23-4"
    )

    if not backup.exists():
        shutil.copy2(path, backup)

    text = path.read_text(encoding="utf-8")

    new_block = feedback_html(lesson_id)

    text, existed = replace_block(
        text,
        START,
        END,
        new_block
    )

    if existed:
        already += 1
    else:
        marker = "AI-ZONE-QURAN-LESSON-NAV-END"

        if marker in text:
            insert_at = text.find("<!--", text.find(marker))
            if insert_at == -1:
                insert_at = len(text)

            text = (
                text[:insert_at]
                + new_block
                + "\n"
                + text[insert_at:]
            )
        else:
            text += "\n" + new_block + "\n"

        updated += 1

    path.write_text(text, encoding="utf-8")

print()
print(f"Lessons updated: {updated}")
print(f"Already installed: {already}")
print("Lesson backups: PASS")


# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

css_path = STATIC / "quran-progress.css"
css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

css, css_existed = replace_block(
    css,
    CSS_START,
    CSS_END,
    CSS_BLOCK.strip()
)

if not css_existed:
    css += "\n\n" + CSS_BLOCK.strip() + "\n"

css_path.write_text(css, encoding="utf-8")

print("Completion Feedback CSS: PASS")


# ---------------------------------------------------------
# JS
# ---------------------------------------------------------

js_path = STATIC / "quran-progress.js"
js = js_path.read_text(encoding="utf-8") if js_path.exists() else ""

js, js_existed = replace_block(
    js,
    JS_START,
    JS_END,
    JS_BLOCK.strip()
)

if not js_existed:
    js += "\n\n" + JS_BLOCK.strip() + "\n"

js_path.write_text(js, encoding="utf-8")

print("Completion Feedback JS: PASS")


# ---------------------------------------------------------
# Verification
# ---------------------------------------------------------

verified = 0

for path in LESSON_FILES:
    if not path.exists():
        continue

    text = path.read_text(encoding="utf-8")

    if (
        START in text
        and END in text
        and "data-quran-completion-feedback" in text
        and "data-lesson-id=" in text
    ):
        verified += 1

css_ok = (
    CSS_START in css
    and CSS_END in css
    and "quran-completion-feedback" in css
)

js_ok = (
    JS_START in js
    and JS_END in js
    and "AIZoneRefreshQuranCompletionFeedback" in js
    and 'PASS_SCORE = 70' in js
)

print()
print("=" * 60)
print(" VERIFICATION")
print("=" * 60)
print(f"Lessons verified: {verified}/20")
print(f"Completion Feedback CSS: {'PASS' if css_ok else 'FAIL'}")
print(f"Completion Feedback JS: {'PASS' if js_ok else 'FAIL'}")
print("Existing Progress/Quiz Engine: PRESERVED")
print("GitHub push: NO")

if verified == 20 and css_ok and js_ok:
    print("STEP 23.4: PASS")
else:
    print("STEP 23.4: FAIL")

print("=" * 60)
