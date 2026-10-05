from pathlib import Path
import shutil

ROOT = Path(".")
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"

START = "<!-- AI-ZONE-QURAN-SMART-STATUS-START -->"
END = "<!-- AI-ZONE-QURAN-SMART-STATUS-END -->"

CSS_START = "/* AI-ZONE-QURAN-SMART-STATUS-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-SMART-STATUS-CSS-END */"

JS_START = "/* AI-ZONE-QURAN-SMART-STATUS-JS-START */"
JS_END = "/* AI-ZONE-QURAN-SMART-STATUS-JS-END */"

TOTAL = 20


def get_lesson_number(path):
    if path.name == "quran_lesson.html":
        return 1

    prefix = "quran_lesson_"
    suffix = ".html"

    if path.name.startswith(prefix) and path.name.endswith(suffix):
        value = path.name[len(prefix):-len(suffix)]

        try:
            number = int(value)
        except ValueError:
            return None

        if 2 <= number <= TOTAL:
            return number

    return None


def build_status_block(lesson_id):
    return f'''
{START}
<div
  class="quran-smart-status"
  data-quran-smart-status
  data-lesson-id="{lesson_id}">

  <div class="quran-smart-status-icon" data-status-icon>
    ○
  </div>

  <div class="quran-smart-status-content">
    <span class="quran-smart-status-label">LESSON STATUS</span>

    <strong data-status-title>
      শেখা শুরু করুন
    </strong>

    <p data-status-message>
      এই পাঠটি শুরু করার জন্য প্রস্তুত।
    </p>
  </div>

  <span
    class="quran-smart-status-badge"
    data-status-badge>
    Not Started
  </span>

</div>
{END}
'''


def install_template(path, lesson_id):
    text = path.read_text(encoding="utf-8")

    if START in text and END in text:
        print(f"Lesson {lesson_id}: already installed")
        return False

    backup = path.with_name(
        path.name + ".before-session23-step23-3"
    )

    if not backup.exists():
        shutil.copy2(path, backup)

    block = build_status_block(lesson_id)

    # Place immediately after Journey Header.
    journey_end = text.find(
        "<!-- AI-ZONE-QURAN-JOURNEY-HEADER-END -->"
    )

    if journey_end != -1:
        insert_at = journey_end + len(
            "<!-- AI-ZONE-QURAN-JOURNEY-HEADER-END -->"
        )

        text = (
            text[:insert_at]
            + "\n"
            + block
            + "\n"
            + text[insert_at:]
        )

    else:
        # Safe fallback: insert before first quran experience block.
        experience_start = text.find(
            "<!-- AI-ZONE-QURAN-EXPERIENCE-START -->"
        )

        if experience_start != -1:
            text = (
                text[:experience_start]
                + block
                + "\n"
                + text[experience_start:]
            )
        else:
            body_end = text.lower().find("</body>")

            if body_end == -1:
                print(
                    f"Lesson {lesson_id}: no safe insertion point"
                )
                return False

            text = (
                text[:body_end]
                + block
                + "\n"
                + text[body_end:]
            )

    path.write_text(text, encoding="utf-8")

    print(f"Lesson {lesson_id}: UPDATED")
    return True


def install_css():
    path = STATIC / "quran-progress.css"

    if path.exists():
        css = path.read_text(encoding="utf-8")
    else:
        css = ""

    if CSS_START in css and CSS_END in css:
        print("Smart status CSS: already installed")
        return

    block = f'''
{CSS_START}

.quran-smart-status {{
  display: flex;
  align-items: center;
  gap: 14px;
  margin: 0 auto 22px;
  padding: 15px 17px;
  border: 1px solid rgba(34, 211, 238, 0.18);
  border-radius: 18px;
  background: rgba(8, 18, 38, 0.72);
}}

.quran-smart-status-icon {{
  width: 40px;
  height: 40px;
  flex: 0 0 40px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.14);
  font-size: 1.05rem;
  font-weight: 900;
}}

.quran-smart-status-content {{
  min-width: 0;
  flex: 1;
}}

.quran-smart-status-label {{
  display: block;
  margin-bottom: 3px;
  font-size: 0.62rem;
  letter-spacing: 0.14em;
  opacity: 0.55;
}}

.quran-smart-status-content strong {{
  display: block;
  font-size: 0.96rem;
}}

.quran-smart-status-content p {{
  margin: 3px 0 0;
  font-size: 0.78rem;
  line-height: 1.45;
  opacity: 0.64;
}}

.quran-smart-status-badge {{
  flex: 0 0 auto;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.12);
  font-size: 0.67rem;
  font-weight: 800;
  white-space: nowrap;
}}

.quran-smart-status.status-not-started .quran-smart-status-icon {{
  opacity: 0.65;
}}

.quran-smart-status.status-practice .quran-smart-status-icon {{
  border-color: rgba(96,165,250,0.55);
}}

.quran-smart-status.status-quiz .quran-smart-status-icon {{
  border-color: rgba(34,211,238,0.65);
}}

.quran-smart-status.status-completed .quran-smart-status-icon {{
  border-color: rgba(74,222,128,0.65);
}}

.quran-smart-status.status-completed .quran-smart-status-badge {{
  border-color: rgba(74,222,128,0.35);
}}

@media (max-width: 620px) {{
  .quran-smart-status {{
    align-items: flex-start;
    padding: 13px;
  }}

  .quran-smart-status-icon {{
    width: 36px;
    height: 36px;
    flex-basis: 36px;
  }}

  .quran-smart-status-badge {{
    font-size: 0.62rem;
    padding: 5px 8px;
  }}
}}

{CSS_END}
'''

    css = css.rstrip() + "\n\n" + block.strip() + "\n"
    path.write_text(css, encoding="utf-8")

    print("Smart status CSS: INSTALLED")


def install_js():
    path = STATIC / "quran-progress.js"

    if path.exists():
        js = path.read_text(encoding="utf-8")
    else:
        js = ""

    if JS_START in js and JS_END in js:
        print("Smart status JS: already installed")
        return

    block = f'''
{JS_START}

(function () {{
  "use strict";

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PRACTICE_PREFIX = "quran_practice_";

  function readJSON(key, fallback) {{
    try {{
      const raw = localStorage.getItem(key);
      if (!raw) return fallback;
      return JSON.parse(raw);
    }} catch (error) {{
      return fallback;
    }}
  }}

  function isCompleted(progress, lessonId) {{
    if (!progress) return false;

    if (Array.isArray(progress)) {{
      return progress.map(Number).includes(lessonId);
    }}

    if (progress.completed) {{
      if (Array.isArray(progress.completed)) {{
        return progress.completed.map(Number).includes(lessonId);
      }}

      if (typeof progress.completed === "object") {{
        return Boolean(
          progress.completed[lessonId] ||
          progress.completed[String(lessonId)]
        );
      }}
    }}

    if (typeof progress === "object") {{
      const value =
        progress[lessonId] ??
        progress[String(lessonId)];

      if (typeof value === "boolean") {{
        return value;
      }}
    }}

    return false;
  }}

  function practiceDone(lessonId) {{
    const data = readJSON(
      PRACTICE_PREFIX + lessonId,
      null
    );

    if (!data || typeof data !== "object") {{
      return false;
    }}

    return Boolean(
      (data.bujhechi || data.understood) &&
      (data.porechi || data.read) &&
      (data.onushilon || data.practice)
    );
  }}

  function hasPassedQuiz(quiz, lessonId) {{
    if (!quiz) return false;

    const source = Array.isArray(quiz)
      ? quiz
      : Array.isArray(quiz.results)
        ? quiz.results
        : [];

    const matching = source.filter(item => {{
      if (!item || typeof item !== "object") return false;

      const id =
        item.lessonId ??
        item.lesson_id ??
        item.lesson;

      return Number(id) === lessonId;
    }});

    if (!matching.length) return false;

    const latest = matching[matching.length - 1];

    const score = Number(
      latest.score ??
      latest.percentage ??
      latest.percent ??
      -1
    );

    return score >= 70;
  }}

  function updateStatus(root) {{
    const lessonId = Number(
      root.getAttribute("data-lesson-id")
    );

    if (!lessonId) return;

    const progress = readJSON(
      PROGRESS_KEY,
      null
    );

    const quiz = readJSON(
      QUIZ_KEY,
      null
    );

    const completed = isCompleted(
      progress,
      lessonId
    );

    const practiced = practiceDone(
      lessonId
    );

    const quizPassed = hasPassedQuiz(
      quiz,
      lessonId
    );

    let status = "not-started";

    if (completed || quizPassed) {{
      status = "completed";
    }} else if (practiced) {{
      status = "quiz";
    }} else {{
      status = "practice";
    }}

    const icon =
      root.querySelector("[data-status-icon]");

    const title =
      root.querySelector("[data-status-title]");

    const message =
      root.querySelector("[data-status-message]");

    const badge =
      root.querySelector("[data-status-badge]");

    root.classList.remove(
      "status-not-started",
      "status-practice",
      "status-quiz",
      "status-completed"
    );

    root.classList.add(
      "status-" + status
    );

    if (status === "completed") {{
      if (icon) icon.textContent = "✓";
      if (title) title.textContent = "পাঠ সম্পন্ন";
      if (message) {{
        message.textContent =
          "এই পাঠটি সম্পন্ন হয়েছে। পরের পাঠ বা Revision চালিয়ে যান।";
      }}
      if (badge) badge.textContent = "Completed";

    }} else if (status === "quiz") {{
      if (icon) icon.textContent = "3";
      if (title) title.textContent = "Quiz-এর জন্য প্রস্তুত";
      if (message) {{
        message.textContent =
          "Practice শেষ হয়েছে। এখন Quiz দিয়ে নিজের শেখা যাচাই করুন।";
      }}
      if (badge) badge.textContent = "Ready for Quiz";

    }} else if (status === "practice") {{
      if (icon) icon.textContent = "→";
      if (title) title.textContent = "শেখা চালিয়ে যান";
      if (message) {{
        message.textContent =
          "Lesson content দেখুন, শুনুন এবং Practice সম্পন্ন করুন।";
      }}
      if (badge) badge.textContent = "Continue";

    }} else {{
      if (icon) icon.textContent = "○";
      if (title) title.textContent = "শেখা শুরু করুন";
      if (message) {{
        message.textContent =
          "এই পাঠটি শুরু করার জন্য প্রস্তুত।";
      }}
      if (badge) badge.textContent = "Not Started";
    }}
  }}

  function refresh() {{
    document
      .querySelectorAll("[data-quran-smart-status]")
      .forEach(updateStatus);
  }}

  window.AIZoneRefreshQuranSmartStatus = refresh;

  if (
    document.readyState === "loading"
  ) {{
    document.addEventListener(
      "DOMContentLoaded",
      refresh
    );
  }} else {{
    refresh();
  }}

  window.addEventListener(
    "storage",
    function (event) {{
      if (
        event.key === PROGRESS_KEY ||
        event.key === QUIZ_KEY ||
        (
          event.key &&
          event.key.startsWith(PRACTICE_PREFIX)
        )
      ) {{
        refresh();
      }}
    }}
  );

}})();

{JS_END}
'''

    js = js.rstrip() + "\n\n" + block.strip() + "\n"
    path.write_text(js, encoding="utf-8")

    print("Smart status JS: INSTALLED")


def main():
    print("=" * 60)
    print(" AI Zone বাংলা — Quran Academy")
    print(" Session 23 — Step 23.3")
    print(" Smart Lesson Status")
    print("=" * 60)

    if not TEMPLATES.exists():
        print("ERROR: templates directory missing")
        raise SystemExit(1)

    lessons = []

    for path in TEMPLATES.glob("quran_lesson*.html"):
        n = get_lesson_number(path)

        if n is not None:
            lessons.append((n, path))

    lessons.sort()

    print()
    print("=== Updating Lessons ===")

    updated = 0
    already = 0

    for n, path in lessons:
        changed = install_template(path, n)

        if changed:
            updated += 1
        else:
            already += 1

    print()
    print("=== Shared CSS ===")
    install_css()

    print()
    print("=== Shared JS ===")
    install_js()

    print()
    print("=== Verification ===")

    verified = 0

    for n, path in lessons:
        text = path.read_text(encoding="utf-8")

        if (
            START in text
            and END in text
            and 'data-quran-smart-status' in text
            and f'data-lesson-id="{n}"' in text
        ):
            print(f"Lesson {n}: PASS")
            verified += 1
        else:
            print(f"Lesson {n}: FAIL")

    css_text = (
        STATIC / "quran-progress.css"
    ).read_text(encoding="utf-8")

    js_text = (
        STATIC / "quran-progress.js"
    ).read_text(encoding="utf-8")

    css_ok = (
        CSS_START in css_text
        and CSS_END in css_text
        and "quran-smart-status" in css_text
    )

    js_ok = (
        JS_START in js_text
        and JS_END in js_text
        and "AIZoneRefreshQuranSmartStatus" in js_text
        and "ai_zone_quran_progress_v1" in js_text
        and "ai_zone_quran_quiz_v1" in js_text
    )

    print()
    print("============================================================")
    print(" SESSION 23 — STEP 23.3 RESULT")
    print("============================================================")
    print(f"Lessons verified: {verified}/{len(lessons)}")
    print(f"Updated this run: {updated}")
    print(f"Already installed: {already}")
    print(f"Smart Status CSS: {'PASS' if css_ok else 'FAIL'}")
    print(f"Smart Status JS: {'PASS' if js_ok else 'FAIL'}")
    print("Existing progress/quiz engine: PRESERVED")
    print("GitHub push: NO")
    print("============================================================")

    if verified != 20 or not css_ok or not js_ok:
        raise SystemExit(1)

    print("STEP 23.3: PASS")


if __name__ == "__main__":
    main()
