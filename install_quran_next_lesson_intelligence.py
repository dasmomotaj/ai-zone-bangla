from pathlib import Path
import re
import shutil

ROOT = Path(".")
DASHBOARD = ROOT / "templates" / "quran.html"
CSS = ROOT / "static" / "quran-progress.css"
JS = ROOT / "static" / "quran-progress.js"

HTML_START = "AI-ZONE-QURAN-NEXT-LESSON-INTELLIGENCE-START"
HTML_END = "AI-ZONE-QURAN-NEXT-LESSON-INTELLIGENCE-END"

CSS_START = "AI-ZONE-QURAN-NEXT-LESSON-INTELLIGENCE-CSS-START"
CSS_END = "AI-ZONE-QURAN-NEXT-LESSON-INTELLIGENCE-CSS-END"

JS_START = "AI-ZONE-QURAN-NEXT-LESSON-INTELLIGENCE-JS-START"
JS_END = "AI-ZONE-QURAN-NEXT-LESSON-INTELLIGENCE-JS-END"

PROGRESS_KEY = "ai_zone_quran_progress_v1"
QUIZ_KEY = "ai_zone_quran_quiz_v1"
PASS_SCORE = 70
TOTAL_LESSONS = 20


def replace_block(text, start, end, block):
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        re.DOTALL
    )
    if pattern.search(text):
        return pattern.sub(block, text, count=1), "REPLACED"
    return text + "\n\n" + block + "\n", "ADDED"


def backup(path, suffix):
    if path.exists():
        target = Path(str(path) + suffix)
        shutil.copy2(path, target)
        return True
    return False


HTML_BLOCK = f"""<!-- {HTML_START} -->
<section
  class="quran-next-lesson-intelligence"
  data-quran-next-lesson-intelligence
  aria-label="পরবর্তী Quran Lesson"
>
  <div class="quran-next-lesson-head">
    <div>
      <span class="quran-next-lesson-kicker">NEXT LESSON</span>
      <h2 data-next-lesson-title>আপনার পরবর্তী Lesson</h2>
      <p data-next-lesson-message>
        আপনার শেখার অগ্রগতি অনুযায়ী পরবর্তী পাঠ নির্বাচন করা হবে।
      </p>
    </div>

    <div class="quran-next-lesson-count">
      <strong data-next-lesson-completed>0</strong>
      <span>/ {TOTAL_LESSONS} Completed</span>
    </div>
  </div>

  <div class="quran-next-lesson-card">
    <div class="quran-next-lesson-number">
      <span>LESSON</span>
      <strong data-next-lesson-number>—</strong>
    </div>

    <div class="quran-next-lesson-info">
      <strong data-next-lesson-name>পরবর্তী পাঠ প্রস্তুত হচ্ছে...</strong>
      <span data-next-lesson-status>Ready</span>
    </div>

    <a
      href="#"
      class="quran-next-lesson-button"
      data-next-lesson-button
    >
      Lesson শুরু করুন →
    </a>
  </div>

  <div class="quran-next-lesson-meta">
    <span data-next-lesson-score>Quiz Score: —</span>
    <span data-next-lesson-priority>Learning Status: —</span>
  </div>
</section>
<!-- {HTML_END} -->"""

CSS_BLOCK = f"""/* {CSS_START} */
.quran-next-lesson-intelligence {{
  margin: 24px 0;
  padding: 22px;
  border: 1px solid rgba(0, 220, 255, .22);
  border-radius: 22px;
  background:
    linear-gradient(145deg, rgba(8, 20, 38, .96), rgba(7, 13, 25, .94));
  box-shadow:
    0 14px 45px rgba(0, 0, 0, .25),
    0 0 30px rgba(0, 200, 255, .06);
}}

.quran-next-lesson-head {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}}

.quran-next-lesson-kicker {{
  display: inline-block;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: .16em;
  color: #67e8f9;
  margin-bottom: 6px;
}}

.quran-next-lesson-head h2 {{
  margin: 0;
  font-size: clamp(20px, 4vw, 30px);
}}

.quran-next-lesson-head p {{
  margin: 7px 0 0;
  opacity: .72;
  line-height: 1.6;
}}

.quran-next-lesson-count {{
  min-width: 100px;
  text-align: center;
  padding: 12px 14px;
  border-radius: 16px;
  background: rgba(0, 200, 255, .08);
  border: 1px solid rgba(0, 220, 255, .16);
}}

.quran-next-lesson-count strong {{
  display: block;
  font-size: 27px;
  color: #67e8f9;
}}

.quran-next-lesson-count span {{
  display: block;
  font-size: 10px;
  opacity: .65;
}}

.quran-next-lesson-card {{
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px;
  border-radius: 18px;
  background: rgba(255,255,255,.035);
  border: 1px solid rgba(255,255,255,.08);
}}

.quran-next-lesson-number {{
  width: 64px;
  height: 64px;
  flex: 0 0 64px;
  display: grid;
  place-items: center;
  align-content: center;
  border-radius: 18px;
  background: rgba(0, 220, 255, .10);
  border: 1px solid rgba(0, 220, 255, .20);
}}

.quran-next-lesson-number span {{
  font-size: 9px;
  opacity: .65;
}}

.quran-next-lesson-number strong {{
  font-size: 24px;
  color: #67e8f9;
}}

.quran-next-lesson-info {{
  flex: 1;
  min-width: 0;
}}

.quran-next-lesson-info strong {{
  display: block;
  margin-bottom: 5px;
  font-size: 17px;
}}

.quran-next-lesson-info span {{
  font-size: 12px;
  opacity: .65;
}}

.quran-next-lesson-button {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0 16px;
  border-radius: 13px;
  text-decoration: none;
  font-weight: 800;
  color: inherit;
  background: rgba(0, 220, 255, .13);
  border: 1px solid rgba(0, 220, 255, .25);
  transition: transform .18s ease, background .18s ease;
}}

.quran-next-lesson-button:hover {{
  transform: translateY(-2px);
  background: rgba(0, 220, 255, .20);
}}

.quran-next-lesson-meta {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 13px;
}}

.quran-next-lesson-meta span {{
  padding: 7px 10px;
  border-radius: 10px;
  font-size: 11px;
  opacity: .72;
  background: rgba(255,255,255,.035);
}}

.quran-next-lesson-intelligence.is-complete {{
  border-color: rgba(80, 220, 150, .30);
}}

.quran-next-lesson-intelligence.is-revision {{
  border-color: rgba(255, 190, 80, .30);
}}

@media (max-width: 620px) {{
  .quran-next-lesson-intelligence {{
    padding: 16px;
    border-radius: 18px;
  }}

  .quran-next-lesson-head {{
    align-items: flex-start;
  }}

  .quran-next-lesson-count {{
    min-width: 76px;
    padding: 9px;
  }}

  .quran-next-lesson-count strong {{
    font-size: 22px;
  }}

  .quran-next-lesson-card {{
    flex-wrap: wrap;
  }}

  .quran-next-lesson-info {{
    min-width: calc(100% - 82px);
  }}

  .quran-next-lesson-button {{
    width: 100%;
  }}
}}
/* {CSS_END} */"""


JS_BLOCK = f"""// {JS_START}
(function () {{
  "use strict";

  const PROGRESS_KEY = "{PROGRESS_KEY}";
  const QUIZ_KEY = "{QUIZ_KEY}";
  const PASS_SCORE = {PASS_SCORE};
  const TOTAL_LESSONS = {TOTAL_LESSONS};

  function readJSON(key, fallback) {{
    try {{
      const raw = localStorage.getItem(key);
      if (!raw) return fallback;
      return JSON.parse(raw);
    }} catch (error) {{
      return fallback;
    }}
  }}

  function lessonIdOf(item) {{
    if (!item || typeof item !== "object") return null;

    const value =
      item.lessonId ??
      item.lesson_id ??
      item.lesson ??
      item.id;

    const n = Number(value);
    return Number.isFinite(n) && n >= 1 && n <= TOTAL_LESSONS
      ? n
      : null;
  }}

  function scoreOf(item) {{
    if (item == null) return null;

    if (typeof item === "number") {{
      return Number.isFinite(item) ? item : null;
    }}

    if (typeof item !== "object") return null;

    const value =
      item.score ??
      item.quizScore ??
      item.percentage ??
      item.percent ??
      item.result;

    const n = Number(value);

    return Number.isFinite(n) ? n : null;
  }}

  function isCompleted(progress, lessonId) {{
    if (!progress) return false;

    if (Array.isArray(progress)) {{
      return progress.some(function (item) {{
        const id = lessonIdOf(item);
        return id === lessonId ||
          (typeof item === "number" && Number(item) === lessonId);
      }});
    }}

    if (typeof progress === "object") {{
      const direct = progress[String(lessonId)];

      if (direct === true) return true;

      if (direct && typeof direct === "object") {{
        return direct.completed === true ||
          direct.complete === true ||
          direct.status === "completed";
      }}

      if (Array.isArray(progress.completedLessons)) {{
        return progress.completedLessons.some(function (x) {{
          return Number(x) === lessonId;
        }});
      }}

      if (Array.isArray(progress.completed)) {{
        return progress.completed.some(function (x) {{
          return Number(x) === lessonId;
        }});
      }}

      if (Array.isArray(progress.lessons)) {{
        return progress.lessons.some(function (item) {{
          return lessonIdOf(item) === lessonId &&
            (item.completed === true || item.status === "completed");
        }});
      }}
    }}

    return false;
  }}

  function getQuizScore(quiz, lessonId) {{
    if (!quiz) return null;

    const sources = [];

    if (Array.isArray(quiz)) sources.push(quiz);
    if (Array.isArray(quiz.results)) sources.push(quiz.results);
    if (Array.isArray(quiz.history)) sources.push(quiz.history);
    if (Array.isArray(quiz.attempts)) sources.push(quiz.attempts);

    if (quiz[String(lessonId)] != null) {{
      const value = quiz[String(lessonId)];
      const score = scoreOf(value);
      if (score !== null) return score;
    }}

    let latest = null;
    let latestTime = -1;

    sources.forEach(function (list) {{
      list.forEach(function (item) {{
        if (!item || typeof item !== "object") return;

        if (lessonIdOf(item) !== lessonId) return;

        const score = scoreOf(item);
        if (score === null) return;

        const time = Number(
          item.timestamp ??
          item.time ??
          item.createdAt ??
          item.updatedAt ??
          0
        );

        if (time >= latestTime) {{
          latestTime = time;
          latest = score;
        }}
      }});
    }});

    return latest;
  }}

  function lessonURL(lessonId) {{
    if (lessonId === 1) {{
      return "/quran/lesson/1";
    }}

    return "/quran/lesson/" + lessonId;
  }}

  function refresh() {{
    const root = document.querySelector(
      "[data-quran-next-lesson-intelligence]"
    );

    if (!root) return;

    const progress = readJSON(PROGRESS_KEY, {{}});
    const quiz = readJSON(QUIZ_KEY, {{}});

    let completedCount = 0;

    for (let i = 1; i <= TOTAL_LESSONS; i++) {{
      if (isCompleted(progress, i)) {{
        completedCount++;
      }}
    }}

    const completedEl =
      root.querySelector("[data-next-lesson-completed]");
    const numberEl =
      root.querySelector("[data-next-lesson-number]");
    const nameEl =
      root.querySelector("[data-next-lesson-name]");
    const titleEl =
      root.querySelector("[data-next-lesson-title]");
    const messageEl =
      root.querySelector("[data-next-lesson-message]");
    const statusEl =
      root.querySelector("[data-next-lesson-status]");
    const scoreEl =
      root.querySelector("[data-next-lesson-score]");
    const priorityEl =
      root.querySelector("[data-next-lesson-priority]");
    const buttonEl =
      root.querySelector("[data-next-lesson-button]");

    if (completedEl) completedEl.textContent = completedCount;

    if (completedCount >= TOTAL_LESSONS) {{
      root.classList.add("is-complete");

      if (titleEl) titleEl.textContent = "মাশাআল্লাহ! Academy Complete";
      if (messageEl) {{
        messageEl.textContent =
          "সব ২০টি Lesson সম্পন্ন হয়েছে। এখন Revision ও নিয়মিত অনুশীলন চালিয়ে যান।";
      }}
      if (numberEl) numberEl.textContent = "✓";
      if (nameEl) nameEl.textContent = "Quran Academy সম্পন্ন";
      if (statusEl) statusEl.textContent = "Completed";
      if (scoreEl) scoreEl.textContent = "Lessons: 20 / 20";
      if (priorityEl) priorityEl.textContent = "Learning Status: Complete";

      if (buttonEl) {{
        buttonEl.href = "/quran";
        buttonEl.textContent = "Academy Dashboard →";
      }}

      return;
    }}

    root.classList.remove("is-complete");

    let nextLesson = null;

    for (let i = 1; i <= TOTAL_LESSONS; i++) {{
      if (!isCompleted(progress, i)) {{
        nextLesson = i;
        break;
      }}
    }}

    if (!nextLesson) return;

    const score = getQuizScore(quiz, nextLesson);
    const passed = score !== null && score >= PASS_SCORE;

    if (numberEl) numberEl.textContent = nextLesson;
    if (nameEl) nameEl.textContent = "Quran Lesson " + nextLesson;
    if (scoreEl) {{
      scoreEl.textContent =
        score === null
          ? "Quiz Score: —"
          : "Quiz Score: " + Math.round(score) + "%";
    }}

    if (passed) {{
      root.classList.remove("is-revision");
      if (titleEl) titleEl.textContent = "পরবর্তী Lesson প্রস্তুত";
      if (messageEl) {{
        messageEl.textContent =
          "আগের পাঠের Quiz ভালো হয়েছে। এবার পরবর্তী Lesson শুরু করুন।";
      }}
      if (statusEl) statusEl.textContent = "Ready";
      if (priorityEl) priorityEl.textContent = "Learning Status: Ready";
    }} else if (score !== null && score < PASS_SCORE) {{
      root.classList.add("is-revision");
      if (titleEl) titleEl.textContent = "Revision আগে করুন";
      if (messageEl) {{
        messageEl.textContent =
          "পরবর্তী Lesson-এ যাওয়ার আগে আগের শেখা বিষয়টি আবার অনুশীলন করুন।";
      }}
      if (statusEl) statusEl.textContent = "Revision Recommended";
      if (priorityEl) {{
        priorityEl.textContent =
          "Learning Status: Revision Recommended";
      }}
    }} else {{
      root.classList.remove("is-revision");
      if (titleEl) titleEl.textContent = "আপনার পরবর্তী Lesson";
      if (messageEl) {{
        messageEl.textContent =
          "আপনার অগ্রগতির ভিত্তিতে এই Lesson-টি এখন শেখার জন্য প্রস্তুত।";
      }}
      if (statusEl) statusEl.textContent = "Next";
      if (priorityEl) priorityEl.textContent = "Learning Status: Next";
    }}

    if (buttonEl) {{
      buttonEl.href = lessonURL(nextLesson);
      buttonEl.textContent = "Lesson " + nextLesson + " শুরু করুন →";
    }}
  }}

  window.AIZoneRefreshQuranNextLessonIntelligence = refresh;

  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", refresh);
  }} else {{
    refresh();
  }}
}})();
// {JS_END}"""


print("=" * 60)
print(" AI Zone বাংলা — STEP 24.2 NEXT LESSON INTELLIGENCE")
print("=" * 60)

if not DASHBOARD.exists():
    raise SystemExit("ERROR: templates/quran.html not found")

if not CSS.exists():
    raise SystemExit("ERROR: static/quran-progress.css not found")

if not JS.exists():
    raise SystemExit("ERROR: static/quran-progress.js not found")

print("\n=== Backups ===")
print("quran.html:", "PASS" if backup(
    DASHBOARD,
    ".before-session24-step24-2-fix"
) else "FAIL")

print("\n=== Dashboard ===")
dashboard_text = DASHBOARD.read_text(encoding="utf-8")
dashboard_text, html_status = replace_block(
    dashboard_text,
    HTML_START,
    HTML_END,
    HTML_BLOCK
)
DASHBOARD.write_text(dashboard_text, encoding="utf-8")
print("Next Lesson Intelligence HTML:", html_status)

print("\n=== CSS ===")
css_text = CSS.read_text(encoding="utf-8")
css_text, css_status = replace_block(
    css_text,
    CSS_START,
    CSS_END,
    CSS_BLOCK
)
CSS.write_text(css_text, encoding="utf-8")
print("Next Lesson Intelligence CSS:", css_status)

print("\n=== JavaScript ===")
js_text = JS.read_text(encoding="utf-8")
js_text, js_status = replace_block(
    js_text,
    JS_START,
    JS_END,
    JS_BLOCK
)
JS.write_text(js_text, encoding="utf-8")
print("Next Lesson Intelligence JS:", js_status)

print("\n=== Verification ===")

dashboard_check = DASHBOARD.read_text(encoding="utf-8")
css_check = CSS.read_text(encoding="utf-8")
js_check = JS.read_text(encoding="utf-8")

checks = [
    ("HTML marker", HTML_START in dashboard_check and HTML_END in dashboard_check),
    ("HTML data attribute", "data-quran-next-lesson-intelligence" in dashboard_check),
    ("CSS marker", CSS_START in css_check and CSS_END in css_check),
    ("JS marker", JS_START in js_check and JS_END in js_check),
    ("Refresh function", "AIZoneRefreshQuranNextLessonIntelligence" in js_check),
    ("Progress key", PROGRESS_KEY in js_check),
    ("Quiz key", QUIZ_KEY in js_check),
    ("PASS score", "PASS_SCORE = 70" in js_check),
    ("20 lessons", "TOTAL_LESSONS = 20" in js_check),
    ("Lesson URL", "/quran/lesson/" in js_check),
]

for name, ok in checks:
    print(f"{name}: {'PASS' if ok else 'FAIL'}")

print("\n=== Python Syntax ===")
import py_compile
py_compile.compile(
    str(ROOT / "app.py"),
    doraise=True
)
print("app.py: PASS")

py_compile.compile(
    str(ROOT / "install_quran_next_lesson_intelligence.py"),
    doraise=True
)
print("Installer: PASS")

print("\n=== GitHub ===")
print("GitHub push: NO")

print("\n" + "=" * 60)
print(" STEP 24.2 INSTALL COMPLETE")
print("=" * 60)
