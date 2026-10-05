from pathlib import Path
import re
import shutil

ROOT = Path(".")
DASHBOARD = ROOT / "templates" / "quran.html"
CSS = ROOT / "static" / "quran-progress.css"
JS = ROOT / "static" / "quran-progress.js"

MARK_START = "<!-- AI-ZONE-QURAN-DASHBOARD-FOCUS-START -->"
MARK_END = "<!-- AI-ZONE-QURAN-DASHBOARD-FOCUS-END -->"

CSS_START = "/* AI-ZONE-QURAN-DASHBOARD-FOCUS-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-DASHBOARD-FOCUS-CSS-END */"

JS_START = "/* AI-ZONE-QURAN-DASHBOARD-FOCUS-JS-START */"
JS_END = "/* AI-ZONE-QURAN-DASHBOARD-FOCUS-JS-END */"

BACKUP_SUFFIX = ".before-session23-step23-6"

assert DASHBOARD.exists(), "templates/quran.html not found"
assert CSS.exists(), "static/quran-progress.css not found"
assert JS.exists(), "static/quran-progress.js not found"

dashboard = DASHBOARD.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
js = JS.read_text(encoding="utf-8")

print("=" * 60)
print(" AI Zone বাংলা — Session 23 Step 23.6")
print(" SMART DASHBOARD LEARNING FOCUS")
print("=" * 60)

# ---------------------------------------------------------
# Backup
# ---------------------------------------------------------

backup = DASHBOARD.with_name(DASHBOARD.name + BACKUP_SUFFIX)

if not backup.exists():
    shutil.copy2(DASHBOARD, backup)
    print("Dashboard backup: PASS")
else:
    print("Dashboard backup: ALREADY EXISTS")

# ---------------------------------------------------------
# Dashboard HTML
# ---------------------------------------------------------

focus_html = f"""
{MARK_START}
<section
  class="quran-dashboard-focus"
  data-quran-dashboard-focus
  aria-label="Current Learning Focus">

  <div class="quran-focus-glow"></div>

  <div class="quran-focus-header">
    <div>
      <span class="quran-focus-kicker">SMART LEARNING FOCUS</span>
      <h2>🎯 এখন কী করবেন?</h2>
      <p>আপনার বর্তমান শেখার অবস্থার ভিত্তিতে পরবর্তী কাজটি এখানে দেখানো হবে।</p>
    </div>
    <div class="quran-focus-lesson" data-focus-lesson>
      Lesson 1
    </div>
  </div>

  <div class="quran-focus-body">

    <div class="quran-focus-icon" data-focus-icon>📖</div>

    <div class="quran-focus-content">
      <span class="quran-focus-label">YOUR NEXT ACTION</span>

      <h3 data-focus-title>শেখা শুরু করুন</h3>

      <p data-focus-message>
        আপনার Quran Academy journey শুরু করার জন্য প্রথম Lesson প্রস্তুত।
      </p>

      <div class="quran-focus-meta">
        <span data-focus-status>Not Started</span>
        <span data-focus-progress>0 / 20 Lessons</span>
      </div>

      <a
        class="quran-focus-button"
        data-focus-button
        href="/quran/lesson/1">
        Lesson 1 শুরু করুন →
      </a>
    </div>

  </div>
</section>
{MARK_END}
"""

if MARK_START in dashboard and MARK_END in dashboard:
    pattern = re.compile(
        re.escape(MARK_START) + r".*?" + re.escape(MARK_END),
        re.S
    )
    dashboard = pattern.sub(focus_html.strip(), dashboard, count=1)
    print("Dashboard Focus: REPLACED")
else:
    # Prefer insertion after hero/progress area.
    anchor_candidates = [
        "</header>",
        '<main',
        '<section class="quran-hero',
    ]

    inserted = False

    for anchor in anchor_candidates:
        if anchor in dashboard:
            dashboard = dashboard.replace(
                anchor,
                focus_html.strip() + "\n\n" + anchor,
                1
            )
            inserted = True
            break

    if not inserted:
        dashboard = dashboard.replace(
            "</body>",
            focus_html.strip() + "\n\n</body>",
            1
        )

    print("Dashboard Focus: ADDED")

DASHBOARD.write_text(dashboard, encoding="utf-8")

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

focus_css = f"""
{CSS_START}

.quran-dashboard-focus {{
  position: relative;
  overflow: hidden;
  margin: 24px 0;
  padding: 24px;
  border: 1px solid rgba(80, 220, 255, .20);
  border-radius: 24px;
  background:
    linear-gradient(135deg,
      rgba(10, 25, 48, .96),
      rgba(5, 12, 28, .98));
  box-shadow:
    0 18px 50px rgba(0, 0, 0, .28),
    inset 0 1px 0 rgba(255,255,255,.05);
}}

.quran-focus-glow {{
  position: absolute;
  width: 180px;
  height: 180px;
  right: -70px;
  top: -80px;
  border-radius: 50%;
  background: rgba(40, 210, 255, .16);
  filter: blur(45px);
  pointer-events: none;
}}

.quran-focus-header {{
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 22px;
}}

.quran-focus-kicker {{
  display: block;
  margin-bottom: 6px;
  font-size: .72rem;
  font-weight: 800;
  letter-spacing: .14em;
  opacity: .62;
}}

.quran-focus-header h2 {{
  margin: 0;
  font-size: clamp(1.35rem, 4vw, 1.8rem);
}}

.quran-focus-header p {{
  margin: 7px 0 0;
  opacity: .72;
  line-height: 1.6;
}}

.quran-focus-lesson {{
  flex: 0 0 auto;
  padding: 8px 12px;
  border: 1px solid rgba(80, 220, 255, .24);
  border-radius: 999px;
  font-size: .78rem;
  font-weight: 800;
  white-space: nowrap;
}}

.quran-focus-body {{
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 18px;
}}

.quran-focus-icon {{
  flex: 0 0 64px;
  width: 64px;
  height: 64px;
  display: grid;
  place-items: center;
  border-radius: 20px;
  background: rgba(80, 220, 255, .10);
  border: 1px solid rgba(80, 220, 255, .20);
  font-size: 1.8rem;
}}

.quran-focus-content {{
  min-width: 0;
  flex: 1;
}}

.quran-focus-label {{
  font-size: .68rem;
  font-weight: 800;
  letter-spacing: .12em;
  opacity: .58;
}}

.quran-focus-content h3 {{
  margin: 4px 0 5px;
  font-size: 1.25rem;
}}

.quran-focus-content p {{
  margin: 0;
  line-height: 1.6;
  opacity: .78;
}}

.quran-focus-meta {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 12px 0;
}}

.quran-focus-meta span {{
  display: inline-flex;
  padding: 5px 9px;
  border-radius: 999px;
  background: rgba(255,255,255,.055);
  border: 1px solid rgba(255,255,255,.08);
  font-size: .72rem;
  font-weight: 700;
}}

.quran-focus-button {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 10px 16px;
  border-radius: 13px;
  text-decoration: none;
  font-weight: 800;
  border: 1px solid rgba(80, 220, 255, .28);
  background: rgba(80, 220, 255, .10);
  transition: transform .2s ease, background .2s ease;
}}

.quran-focus-button:hover {{
  transform: translateY(-2px);
  background: rgba(80, 220, 255, .16);
}}

@media (max-width: 620px) {{
  .quran-dashboard-focus {{
    padding: 18px;
    border-radius: 20px;
  }}

  .quran-focus-header {{
    flex-direction: column;
    gap: 10px;
  }}

  .quran-focus-lesson {{
    align-self: flex-start;
  }}

  .quran-focus-body {{
    align-items: flex-start;
    flex-direction: column;
  }}

  .quran-focus-icon {{
    width: 54px;
    height: 54px;
    flex-basis: 54px;
    border-radius: 16px;
  }}

  .quran-focus-button {{
    width: 100%;
  }}
}}

{CSS_END}
"""

if CSS_START in css and CSS_END in css:
    pattern = re.compile(
        re.escape(CSS_START) + r".*?" + re.escape(CSS_END),
        re.S
    )
    css = pattern.sub(focus_css.strip(), css, count=1)
    print("Dashboard Focus CSS: REPLACED")
else:
    css += "\n\n" + focus_css.strip() + "\n"
    print("Dashboard Focus CSS: INSTALLED")

CSS.write_text(css, encoding="utf-8")

# ---------------------------------------------------------
# JavaScript
# ---------------------------------------------------------

focus_js = r"""
/* AI-ZONE-QURAN-DASHBOARD-FOCUS-JS-START */
(function () {
  "use strict";

  const TOTAL = 20;
  const PASS_SCORE = 70;

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PRACTICE_PREFIX = "quran_practice_";

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      if (!raw) return fallback;
      return JSON.parse(raw);
    } catch (e) {
      return fallback;
    }
  }

  function normalizeLessonId(value) {
    const n = Number(value);
    return Number.isInteger(n) && n >= 1 && n <= TOTAL ? n : null;
  }

  function isCompleted(progress, lessonId) {
    if (!progress) return false;

    if (Array.isArray(progress)) {
      return progress.some(function (x) {
        return Number(x) === lessonId;
      });
    }

    if (Array.isArray(progress.completed)) {
      return progress.completed.some(function (x) {
        return Number(x) === lessonId;
      });
    }

    if (progress.completed && typeof progress.completed === "object") {
      return Boolean(
        progress.completed[lessonId] ||
        progress.completed[String(lessonId)]
      );
    }

    if (progress[String(lessonId)] === true) return true;

    return false;
  }

  function practiceDone(lessonId) {
    const data = readJSON(
      PRACTICE_PREFIX + lessonId,
      null
    );

    if (!data) return false;

    if (data === true) return true;

    if (typeof data === "object") {
      const a = Boolean(data.bujhechi || data.understood);
      const b = Boolean(data.porechi || data.read);
      const c = Boolean(data.onushilon || data.practice);

      return a && b && c;
    }

    return false;
  }

  function quizEntries(quiz) {
    if (Array.isArray(quiz)) return quiz;

    if (!quiz || typeof quiz !== "object") return [];

    const keys = ["results", "history", "attempts", "quizzes"];

    for (const key of keys) {
      if (Array.isArray(quiz[key])) {
        return quiz[key];
      }
    }

    return [];
  }

  function latestQuiz(quiz, lessonId) {
    const entries = quizEntries(quiz)
      .filter(function (item) {
        if (!item || typeof item !== "object") return false;

        const id = Number(
          item.lessonId ??
          item.lesson_id ??
          item.lesson ??
          item.id
        );

        return id === lessonId;
      });

    if (!entries.length) return null;

    entries.sort(function (a, b) {
      const ta = Number(
        a.timestamp ??
        a.time ??
        a.createdAt ??
        a.date ??
        0
      );

      const tb = Number(
        b.timestamp ??
        b.time ??
        b.createdAt ??
        b.date ??
        0
      );

      return tb - ta;
    });

    return entries[0];
  }

  function quizScore(item) {
    if (!item || typeof item !== "object") return null;

    const raw =
      item.score ??
      item.percent ??
      item.percentage ??
      item.result;

    const score = Number(raw);

    return Number.isFinite(score) ? score : null;
  }

  function nextLessonURL(lessonId) {
    if (lessonId >= TOTAL) return "/quran";
    return "/quran/lesson/" + (lessonId + 1);
  }

  function lessonURL(lessonId) {
    return "/quran/lesson/" + lessonId;
  }

  function updateFocus(root) {
    const progress = readJSON(PROGRESS_KEY, null);
    const quiz = readJSON(QUIZ_KEY, null);

    let current = 1;

    for (let i = 1; i <= TOTAL; i++) {
      if (!isCompleted(progress, i)) {
        current = i;
        break;
      }

      if (i === TOTAL) {
        current = TOTAL;
      }
    }

    const completedCount = Array.from(
      { length: TOTAL },
      function (_, index) {
        return isCompleted(progress, index + 1);
      }
    ).filter(Boolean).length;

    const title = root.querySelector("[data-focus-title]");
    const message = root.querySelector("[data-focus-message]");
    const button = root.querySelector("[data-focus-button]");
    const icon = root.querySelector("[data-focus-icon]");
    const status = root.querySelector("[data-focus-status]");
    const lesson = root.querySelector("[data-focus-lesson]");
    const progressText = root.querySelector("[data-focus-progress]");

    if (!title || !message || !button || !icon) return;

    const completed = isCompleted(progress, current);
    const practice = practiceDone(current);
    const quizResult = latestQuiz(quiz, current);
    const score = quizScore(quizResult);

    lesson.textContent =
      "Lesson " + current + " / " + TOTAL;

    progressText.textContent =
      completedCount + " / " + TOTAL + " Lessons";

    // Academy complete
    if (
      completedCount >= TOTAL &&
      isCompleted(progress, TOTAL)
    ) {
      icon.textContent = "🏆";
      title.textContent = "Academy Complete!";
      message.textContent =
        "মাশাআল্লাহ! সবগুলো Lesson সম্পন্ন হয়েছে। এখন Revision চালিয়ে আপনার শেখা আরও শক্ত করুন।";
      status.textContent = "Completed";
      button.textContent = "Quran Academy Dashboard →";
      button.href = "/quran";
      return;
    }

    // Quiz passed but completion not yet reflected
    if (score !== null && score >= PASS_SCORE) {
      icon.textContent = "➡️";
      title.textContent =
        current >= TOTAL
          ? "Academy Complete করুন"
          : "Next Lesson চালিয়ে যান";
      message.textContent =
        "আপনার Quiz ভালো হয়েছে। এখন পরের Lesson-এ এগিয়ে যান।";
      status.textContent = "Next Lesson";
      button.textContent =
        current >= TOTAL
          ? "Dashboard দেখুন →"
          : "Lesson " + (current + 1) + " →";
      button.href = nextLessonURL(current);
      return;
    }

    // Failed quiz
    if (score !== null && score < PASS_SCORE) {
      icon.textContent = "🔄";
      title.textContent = "Revision করুন";
      message.textContent =
        "Quiz score 70%-এর নিচে। দুর্বল অংশগুলো আবার অনুশীলন করে Re-Test দিন।";
      status.textContent = "Revision";
      button.textContent = "Revision শুরু করুন →";
      button.href = lessonURL(current) + "#quranRevisionRetest";
      return;
    }

    // Practice complete
    if (practice) {
      icon.textContent = "📝";
      title.textContent = "Quiz দিন";
      message.textContent =
        "Practice শেষ হয়েছে। এখন Quiz দিয়ে নিজের শেখা যাচাই করুন।";
      status.textContent = "Ready for Quiz";
      button.textContent = "Quiz দিন →";
      button.href = lessonURL(current) + "#quranQuiz";
      return;
    }

    // Default
    icon.textContent = "📖";
    title.textContent =
      completedCount > 0
        ? "শেখা চালিয়ে যান"
        : "শেখা শুরু করুন";

    message.textContent =
      completedCount > 0
        ? "আপনার পরবর্তী Lesson-এর content দেখুন, শুনুন এবং Practice সম্পন্ন করুন।"
        : "Quran Academy journey শুরু করার জন্য প্রথম Lesson প্রস্তুত।";

    status.textContent =
      completedCount > 0
        ? "Continue"
        : "Not Started";

    button.textContent =
      "Lesson " + current + " শুরু করুন →";

    button.href = lessonURL(current);
  }

  function refresh() {
    document
      .querySelectorAll("[data-quran-dashboard-focus]")
      .forEach(updateFocus);
  }

  window.AIZoneRefreshQuranDashboardFocus = refresh;

  document.addEventListener("DOMContentLoaded", refresh);

  window.addEventListener("storage", function (event) {
    if (
      event.key === PROGRESS_KEY ||
      event.key === QUIZ_KEY ||
      (event.key && event.key.indexOf(PRACTICE_PREFIX) === 0)
    ) {
      refresh();
    }
  });
})();
/* AI-ZONE-QURAN-DASHBOARD-FOCUS-JS-END */
"""

if JS_START in js and JS_END in js:
    pattern = re.compile(
        re.escape(JS_START) + r".*?" + re.escape(JS_END),
        re.S
    )
    js = pattern.sub(focus_js.strip(), js, count=1)
    print("Dashboard Focus JS: REPLACED")
else:
    js += "\n\n" + focus_js.strip() + "\n"
    print("Dashboard Focus JS: INSTALLED")

JS.write_text(js, encoding="utf-8")

# ---------------------------------------------------------
# Verification
# ---------------------------------------------------------

dashboard_check = DASHBOARD.read_text(encoding="utf-8")
css_check = CSS.read_text(encoding="utf-8")
js_check = JS.read_text(encoding="utf-8")

checks = {
    "Dashboard Focus START": MARK_START in dashboard_check,
    "Dashboard Focus END": MARK_END in dashboard_check,
    "Dashboard data attribute": "data-quran-dashboard-focus" in dashboard_check,
    "Dashboard focus lesson": "data-focus-lesson" in dashboard_check,
    "Dashboard focus button": "data-focus-button" in dashboard_check,
    "CSS START": CSS_START in css_check,
    "CSS END": CSS_END in css_check,
    "CSS class": "quran-dashboard-focus" in css_check,
    "JS START": JS_START in js_check,
    "JS END": JS_END in js_check,
    "Refresh function": "AIZoneRefreshQuranDashboardFocus" in js_check,
    "Progress key": "ai_zone_quran_progress_v1" in js_check,
    "Quiz key": "ai_zone_quran_quiz_v1" in js_check,
    "PASS score": "PASS_SCORE = 70" in js_check,
}

print()
print("=== Verification ===")

failed = []

for name, ok in checks.items():
    print(f"{name}: {'PASS' if ok else 'FAIL'}")
    if not ok:
        failed.append(name)

if failed:
    print()
    print("FAILED CHECKS:")
    for item in failed:
        print("-", item)
    raise SystemExit(1)

print()
print("Dashboard Focus: PASS")
print("Existing Progress/Quiz/Revision Engine: PRESERVED")
print("GitHub push: NO")
print()
print("============================================================")
print(" SESSION 23 — STEP 23.6 INSTALL COMPLETE")
print("============================================================")
