from pathlib import Path
import re
import shutil

ROOT = Path(".")
DASHBOARD = ROOT / "templates" / "quran.html"
CSS = ROOT / "static" / "quran-progress.css"
JS = ROOT / "static" / "quran-progress.js"

MARK_START = "<!-- AI-ZONE-QURAN-PRIORITY-SYNC-START -->"
MARK_END = "<!-- AI-ZONE-QURAN-PRIORITY-SYNC-END -->"

CSS_START = "/* AI-ZONE-QURAN-PRIORITY-SYNC-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-PRIORITY-SYNC-CSS-END */"

JS_START = "/* AI-ZONE-QURAN-PRIORITY-SYNC-JS-START */"
JS_END = "/* AI-ZONE-QURAN-PRIORITY-SYNC-JS-END */"

BACKUP_SUFFIX = ".before-session23-step23-7"

assert DASHBOARD.exists(), "templates/quran.html not found"
assert CSS.exists(), "static/quran-progress.css not found"
assert JS.exists(), "static/quran-progress.js not found"

dashboard = DASHBOARD.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
js = JS.read_text(encoding="utf-8")

print("=" * 60)
print(" AI Zone বাংলা — Session 23 Step 23.7")
print(" SMART FOCUS + REVISION PRIORITY SYNC")
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
# HTML
# ---------------------------------------------------------

priority_html = f"""
{MARK_START}
<div
  class="quran-focus-priority"
  data-quran-focus-priority>

  <div class="quran-focus-priority-icon" data-priority-icon>✓</div>

  <div class="quran-focus-priority-content">
    <span class="quran-focus-priority-label">WHY THIS ACTION?</span>

    <strong data-priority-title>আপনার শেখার অগ্রগতি ভালোভাবে চালিয়ে যান</strong>

    <p data-priority-message>
      আপনার বর্তমান learning status অনুযায়ী পরবর্তী কাজ নির্বাচন করা হয়েছে।
    </p>

    <div class="quran-focus-priority-meta">
      <span data-priority-badge>Normal</span>
      <span data-priority-score>Score: —</span>
    </div>
  </div>

</div>
{MARK_END}
"""

if MARK_START in dashboard and MARK_END in dashboard:
    pattern = re.compile(
        re.escape(MARK_START) + r".*?" + re.escape(MARK_END),
        re.S
    )
    dashboard = pattern.sub(priority_html.strip(), dashboard, count=1)
    print("Priority Sync HTML: REPLACED")
else:
    # Insert inside the Smart Dashboard Focus block.
    focus_end = "<!-- AI-ZONE-QURAN-DASHBOARD-FOCUS-END -->"

    if focus_end in dashboard:
        dashboard = dashboard.replace(
            focus_end,
            priority_html.strip() + "\n" + focus_end,
            1
        )
    else:
        dashboard = dashboard.replace(
            "</body>",
            priority_html.strip() + "\n</body>",
            1
        )

    print("Priority Sync HTML: ADDED")

DASHBOARD.write_text(dashboard, encoding="utf-8")

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

priority_css = f"""
{CSS_START}

.quran-focus-priority {{
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 13px;
  margin-top: 16px;
  padding: 14px 16px;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,.08);
  background: rgba(255,255,255,.035);
}}

.quran-focus-priority-icon {{
  flex: 0 0 38px;
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  font-size: 1rem;
  background: rgba(255,255,255,.07);
}}

.quran-focus-priority-content {{
  min-width: 0;
  flex: 1;
}}

.quran-focus-priority-label {{
  display: block;
  margin-bottom: 3px;
  font-size: .64rem;
  font-weight: 800;
  letter-spacing: .12em;
  opacity: .55;
}}

.quran-focus-priority-content strong {{
  display: block;
  font-size: .92rem;
  line-height: 1.45;
}}

.quran-focus-priority-content p {{
  margin: 4px 0 0;
  font-size: .78rem;
  line-height: 1.55;
  opacity: .70;
}}

.quran-focus-priority-meta {{
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 8px;
}}

.quran-focus-priority-meta span {{
  padding: 4px 8px;
  border-radius: 999px;
  font-size: .66rem;
  font-weight: 800;
  border: 1px solid rgba(255,255,255,.08);
  background: rgba(255,255,255,.04);
}}

.quran-focus-priority.priority-high {{
  border-color: rgba(255, 120, 120, .28);
}}

.quran-focus-priority.priority-medium {{
  border-color: rgba(255, 190, 80, .25);
}}

.quran-focus-priority.priority-low {{
  border-color: rgba(80, 220, 255, .22);
}}

.quran-focus-priority.priority-complete {{
  border-color: rgba(100, 220, 150, .25);
}}

@media (max-width: 620px) {{
  .quran-focus-priority {{
    padding: 12px;
  }}

  .quran-focus-priority-icon {{
    flex-basis: 34px;
    width: 34px;
    height: 34px;
  }}
}}

{CSS_END}
"""

if CSS_START in css and CSS_END in css:
    pattern = re.compile(
        re.escape(CSS_START) + r".*?" + re.escape(CSS_END),
        re.S
    )
    css = pattern.sub(priority_css.strip(), css, count=1)
    print("Priority Sync CSS: REPLACED")
else:
    css += "\n\n" + priority_css.strip() + "\n"
    print("Priority Sync CSS: INSTALLED")

CSS.write_text(css, encoding="utf-8")

# ---------------------------------------------------------
# JS
# ---------------------------------------------------------

priority_js = r"""
/* AI-ZONE-QURAN-PRIORITY-SYNC-JS-START */
(function () {
  "use strict";

  const TOTAL = 20;
  const PASS_SCORE = 70;

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PRIORITY_KEY = "ai_zone_quran_revision_priority_v1";
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

  function isCompleted(progress, lessonId) {
    if (!progress) return false;

    if (Array.isArray(progress)) {
      return progress.some(x => Number(x) === lessonId);
    }

    if (Array.isArray(progress.completed)) {
      return progress.completed.some(x => Number(x) === lessonId);
    }

    if (progress.completed && typeof progress.completed === "object") {
      return Boolean(
        progress.completed[lessonId] ||
        progress.completed[String(lessonId)]
      );
    }

    return progress[String(lessonId)] === true;
  }

  function practiceDone(lessonId) {
    const data = readJSON(
      PRACTICE_PREFIX + lessonId,
      null
    );

    if (!data) return false;
    if (data === true) return true;

    if (typeof data === "object") {
      return Boolean(
        (data.bujhechi || data.understood) &&
        (data.porechi || data.read) &&
        (data.onushilon || data.practice)
      );
    }

    return false;
  }

  function quizEntries(data) {
    if (Array.isArray(data)) return data;

    if (!data || typeof data !== "object") return [];

    for (const key of [
      "results",
      "history",
      "attempts",
      "quizzes"
    ]) {
      if (Array.isArray(data[key])) {
        return data[key];
      }
    }

    return [];
  }

  function latestQuiz(data, lessonId) {
    const entries = quizEntries(data).filter(item => {
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

    entries.sort((a, b) => {
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

  function scoreOf(result) {
    if (!result || typeof result !== "object") {
      return null;
    }

    const score = Number(
      result.score ??
      result.percent ??
      result.percentage ??
      result.result
    );

    return Number.isFinite(score) ? score : null;
  }

  function priorityForLesson(priorityData, lessonId) {
    if (!priorityData) return null;

    const candidates = [];

    if (Array.isArray(priorityData)) {
      candidates.push(...priorityData);
    }

    if (Array.isArray(priorityData.items)) {
      candidates.push(...priorityData.items);
    }

    if (Array.isArray(priorityData.results)) {
      candidates.push(...priorityData.results);
    }

    if (typeof priorityData === "object") {
      const direct =
        priorityData[lessonId] ??
        priorityData[String(lessonId)];

      if (direct && typeof direct === "object") {
        return direct;
      }
    }

    return candidates.find(item => {
      if (!item || typeof item !== "object") return false;

      const id = Number(
        item.lessonId ??
        item.lesson_id ??
        item.lesson ??
        item.id
      );

      return id === lessonId;
    }) || null;
  }

  function setPriority(
    root,
    icon,
    title,
    message,
    badge,
    score,
    className
  ) {
    root.classList.remove(
      "priority-high",
      "priority-medium",
      "priority-low",
      "priority-complete"
    );

    if (className) {
      root.classList.add(className);
    }

    root.querySelector("[data-priority-icon]").textContent = icon;
    root.querySelector("[data-priority-title]").textContent = title;
    root.querySelector("[data-priority-message]").textContent = message;
    root.querySelector("[data-priority-badge]").textContent = badge;
    root.querySelector("[data-priority-score]").textContent =
      score === null || score === undefined
        ? "Score: —"
        : "Score: " + score + "%";
  }

  function updatePriority(root) {
    const progress = readJSON(PROGRESS_KEY, null);
    const quiz = readJSON(QUIZ_KEY, null);
    const priorityData = readJSON(PRIORITY_KEY, null);

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
      (_, i) => isCompleted(progress, i + 1)
    ).filter(Boolean).length;

    const completed = isCompleted(progress, current);
    const practice = practiceDone(current);
    const quizResult = latestQuiz(quiz, current);
    const score = scoreOf(quizResult);
    const savedPriority = priorityForLesson(
      priorityData,
      current
    );

    // Full academy complete
    if (
      completedCount >= TOTAL &&
      isCompleted(progress, TOTAL)
    ) {
      setPriority(
        root,
        "🏆",
        "সব Lesson সম্পন্ন হয়েছে",
        "এখন Revision চালিয়ে শেখা আরও শক্ত করুন এবং প্রয়োজন হলে শিক্ষক/ক্বারির সহায়তা নিন।",
        "Complete",
        null,
        "priority-complete"
      );
      return;
    }

    // Failed quiz — strongest priority
    if (score !== null && score < PASS_SCORE) {
      let priority = "HIGH";

      if (score >= 55) {
        priority = "MEDIUM";
      } else if (score >= 40) {
        priority = "HIGH";
      }

      const className =
        priority === "HIGH"
          ? "priority-high"
          : "priority-medium";

      setPriority(
        root,
        "🔄",
        "Revision এখন সবচেয়ে গুরুত্বপূর্ণ",
        "Lesson " + current +
        " Quiz-এ " + score +
        "% পাওয়া গেছে। দুর্বল অংশগুলো আবার অনুশীলন করে Re-Test দিন।",
        priority,
        score,
        className
      );
      return;
    }

    // Saved Revision Priority Engine data
    if (
      savedPriority &&
      typeof savedPriority === "object"
    ) {
      const saved = String(
        savedPriority.priority ??
        savedPriority.level ??
        ""
      ).toUpperCase();

      if (saved === "HIGH") {
        setPriority(
          root,
          "⚠️",
          "এই Lesson-এ বেশি মনোযোগ দিন",
          "Revision Priority Engine এই Lesson-কে High Priority হিসেবে চিহ্নিত করেছে।",
          "HIGH",
          score,
          "priority-high"
        );
        return;
      }

      if (saved === "MEDIUM") {
        setPriority(
          root,
          "🟡",
          "এই Lesson আবার ঝালিয়ে নিন",
          "Revision Priority Engine অনুযায়ী এই Lesson-এ আরও কিছু অনুশীলন উপকারী হবে।",
          "MEDIUM",
          score,
          "priority-medium"
        );
        return;
      }
    }

    // Practice completed
    if (practice) {
      setPriority(
        root,
        "📝",
        "Quiz-এর আগে Practice শেষ করুন",
        "আপনি Practice সম্পন্ন করেছেন। এখন Quiz দিয়ে শেখা যাচাই করুন।",
        "READY",
        score,
        "priority-low"
      );
      return;
    }

    // Normal learning
    setPriority(
      root,
      "📖",
      "Lesson content দিয়ে শুরু করুন",
      "দেখুন → শুনুন → পড়ুন → অনুশীলন করুন। তারপর Quiz দিন।",
      "NORMAL",
      score,
      "priority-low"
    );
  }

  function refresh() {
    document
      .querySelectorAll("[data-quran-focus-priority]")
      .forEach(updatePriority);
  }

  window.AIZoneRefreshQuranDashboardPriority =
    refresh;

  document.addEventListener(
    "DOMContentLoaded",
    refresh
  );

  window.addEventListener(
    "storage",
    function (event) {
      if (
        event.key === PROGRESS_KEY ||
        event.key === QUIZ_KEY ||
        event.key === PRIORITY_KEY ||
        (event.key &&
          event.key.indexOf(PRACTICE_PREFIX) === 0)
      ) {
        refresh();
      }
    }
  );
})();
/* AI-ZONE-QURAN-PRIORITY-SYNC-JS-END */
"""

if JS_START in js and JS_END in js:
    pattern = re.compile(
        re.escape(JS_START) + r".*?" + re.escape(JS_END),
        re.S
    )
    js = pattern.sub(priority_js.strip(), js, count=1)
    print("Priority Sync JS: REPLACED")
else:
    js += "\n\n" + priority_js.strip() + "\n"
    print("Priority Sync JS: INSTALLED")

JS.write_text(js, encoding="utf-8")

# ---------------------------------------------------------
# Verification
# ---------------------------------------------------------

dashboard_check = DASHBOARD.read_text(encoding="utf-8")
css_check = CSS.read_text(encoding="utf-8")
js_check = JS.read_text(encoding="utf-8")

checks = {
    "HTML START": MARK_START in dashboard_check,
    "HTML END": MARK_END in dashboard_check,
    "Priority container": "data-quran-focus-priority" in dashboard_check,
    "Priority title": "data-priority-title" in dashboard_check,
    "Priority message": "data-priority-message" in dashboard_check,
    "Priority badge": "data-priority-badge" in dashboard_check,
    "CSS START": CSS_START in css_check,
    "CSS END": CSS_END in css_check,
    "CSS class": "quran-focus-priority" in css_check,
    "Mobile CSS": "@media (max-width: 620px)" in css_check,
    "JS START": JS_START in js_check,
    "JS END": JS_END in js_check,
    "Refresh function": "AIZoneRefreshQuranDashboardPriority" in js_check,
    "Revision priority key": "ai_zone_quran_revision_priority_v1" in js_check,
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
print("Priority Sync: PASS")
print("Existing Progress/Quiz/Revision Engine: PRESERVED")
print("GitHub push: NO")

print()
print("=" * 60)
print(" SESSION 23 — STEP 23.7 INSTALL COMPLETE")
print("=" * 60)
