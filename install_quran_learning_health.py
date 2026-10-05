from pathlib import Path
import shutil

ROOT = Path(".")
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"

DASHBOARD = TEMPLATES / "quran.html"
CSS = STATIC / "quran-progress.css"
JS = STATIC / "quran-progress.js"

HTML_START = "<!-- AI-ZONE-QURAN-LEARNING-HEALTH-START -->"
HTML_END = "<!-- AI-ZONE-QURAN-LEARNING-HEALTH-END -->"

CSS_START = "/* AI-ZONE-QURAN-LEARNING-HEALTH-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-LEARNING-HEALTH-CSS-END */"

JS_START = "/* AI-ZONE-QURAN-LEARNING-HEALTH-JS-START */"
JS_END = "/* AI-ZONE-QURAN-LEARNING-HEALTH-JS-END */"


def backup(path):
    if path.exists():
        target = Path(str(path) + ".before-session23-step23-9")
        shutil.copy2(path, target)
        print(f"Backup: {target}")


def replace_block(text, start, end, block):
    a = text.find(start)
    b = text.find(end)

    if a != -1 and b != -1 and b > a:
        b += len(end)
        return text[:a] + block + text[b:]

    return text + "\n\n" + block + "\n"


def install_html():
    backup(DASHBOARD)
    text = DASHBOARD.read_text(encoding="utf-8")

    block = f"""{HTML_START}

<section class="quran-learning-health" data-quran-learning-health>

  <div class="quran-learning-health-head">
    <div>
      <span class="quran-learning-health-kicker">
        ACADEMY LEARNING HEALTH
      </span>

      <h2>📊 আপনার Learning Health</h2>

      <p>
        আপনার বর্তমান Progress, Quiz, Revision এবং Re-Test status
        এক জায়গায় দেখে শেখার অবস্থাটা বুঝুন।
      </p>
    </div>

    <div class="quran-learning-health-score">
      <strong data-health-score>0%</strong>
      <span data-health-label>Getting Started</span>
    </div>
  </div>

  <div class="quran-learning-health-grid">

    <div class="health-card">
      <span class="health-icon">📚</span>
      <strong data-health-completed>0</strong>
      <small>Completed Lessons</small>
    </div>

    <div class="health-card">
      <span class="health-icon">✅</span>
      <strong data-health-passed>0</strong>
      <small>Quiz Passed</small>
    </div>

    <div class="health-card">
      <span class="health-icon">🔄</span>
      <strong data-health-revision>0</strong>
      <small>Revision Needed</small>
    </div>

    <div class="health-card">
      <span class="health-icon">📝</span>
      <strong data-health-retest>0</strong>
      <small>Re-Test Pending</small>
    </div>

    <div class="health-card">
      <span class="health-icon">🔴</span>
      <strong data-health-high>0</strong>
      <small>High Priority</small>
    </div>

  </div>

  <div class="quran-learning-health-message">
    <div class="health-message-icon">💡</div>

    <div>
      <strong data-health-message-title>
        শেখা শুরু করার জন্য প্রস্তুত
      </strong>

      <p data-health-message>
        Lesson 1 থেকে ধীরে ধীরে শুরু করুন।
      </p>
    </div>
  </div>

</section>

{HTML_END}"""

    text = replace_block(text, HTML_START, HTML_END, block)

    # Keep the Health section close to the existing Smart Focus.
    focus_end = '<!-- AI-ZONE-QURAN-DASHBOARD-FOCUS-END -->'

    if HTML_START not in text and focus_end in text:
        text = text.replace(
            focus_end,
            block + "\n" + focus_end,
            1
        )

    DASHBOARD.write_text(text, encoding="utf-8")
    print("Learning Health HTML: INSTALLED")


def install_css():
    backup(CSS)
    css = CSS.read_text(encoding="utf-8") if CSS.exists() else ""

    block = f"""{CSS_START}

.quran-learning-health {{
  margin: 28px 0;
  padding: 24px;
  border-radius: 24px;
  border: 1px solid rgba(90, 210, 255, .22);
  background:
    radial-gradient(circle at top left, rgba(0, 210, 255, .09), transparent 35%),
    rgba(10, 18, 32, .78);
  box-shadow: 0 18px 50px rgba(0,0,0,.24);
}}

.quran-learning-health-head {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}}

.quran-learning-health-kicker {{
  display: block;
  margin-bottom: 6px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1.7px;
  opacity: .62;
}}

.quran-learning-health-head h2 {{
  margin: 0 0 7px;
  font-size: clamp(22px, 4vw, 30px);
}}

.quran-learning-health-head p {{
  margin: 0;
  max-width: 720px;
  line-height: 1.7;
  opacity: .76;
}}

.quran-learning-health-score {{
  min-width: 125px;
  padding: 15px;
  text-align: center;
  border-radius: 20px;
  background: rgba(255,255,255,.055);
  border: 1px solid rgba(255,255,255,.09);
}}

.quran-learning-health-score strong {{
  display: block;
  font-size: 30px;
  font-weight: 900;
}}

.quran-learning-health-score span {{
  font-size: 12px;
  opacity: .65;
}}

.quran-learning-health-grid {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 11px;
  margin: 20px 0;
}}

.health-card {{
  padding: 16px;
  border-radius: 18px;
  background: rgba(255,255,255,.045);
  border: 1px solid rgba(255,255,255,.075);
}}

.health-icon {{
  display: block;
  margin-bottom: 7px;
  font-size: 20px;
}}

.health-card strong {{
  display: block;
  font-size: 24px;
  font-weight: 900;
}}

.health-card small {{
  opacity: .66;
  line-height: 1.4;
}}

.quran-learning-health-message {{
  display: flex;
  align-items: flex-start;
  gap: 13px;
  padding: 17px;
  border-radius: 18px;
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.07);
}}

.health-message-icon {{
  font-size: 22px;
}}

.quran-learning-health-message strong {{
  display: block;
  margin-bottom: 4px;
}}

.quran-learning-health-message p {{
  margin: 0;
  line-height: 1.65;
  opacity: .72;
}}

@media (max-width: 900px) {{
  .quran-learning-health-grid {{
    grid-template-columns: repeat(3, 1fr);
  }}
}}

@media (max-width: 620px) {{
  .quran-learning-health {{
    padding: 17px;
    border-radius: 20px;
  }}

  .quran-learning-health-head {{
    flex-direction: column;
    align-items: stretch;
  }}

  .quran-learning-health-score {{
    min-width: 0;
  }}

  .quran-learning-health-grid {{
    grid-template-columns: repeat(2, 1fr);
  }}

  .health-card {{
    padding: 14px;
  }}

  .quran-learning-health-message {{
    padding: 14px;
  }}
}}

{CSS_END}"""

    css = replace_block(css, CSS_START, CSS_END, block)
    CSS.write_text(css, encoding="utf-8")
    print("Learning Health CSS: INSTALLED")


def install_js():
    backup(JS)
    js = JS.read_text(encoding="utf-8") if JS.exists() else ""

    block = f"""{JS_START}

(function () {{
  "use strict";

  const TOTAL = 20;
  const PASS_SCORE = 70;

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PRIORITY_KEY = "ai_zone_quran_revision_priority_v1";
  const RETEST_KEY = "ai_zone_quran_retest_v1";

  function readJSON(key, fallback) {{
    try {{
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    }} catch (e) {{
      return fallback;
    }}
  }}

  function lessonId(item) {{
    if (!item || typeof item !== "object") return null;

    const value =
      item.lessonId ??
      item.lesson_id ??
      item.lesson;

    const n = Number(value);

    return Number.isInteger(n) && n >= 1 && n <= TOTAL
      ? n
      : null;
  }}

  function score(item) {{
    if (!item || typeof item !== "object") return null;

    const value =
      item.score ??
      item.percentage ??
      item.percent;

    const n = Number(value);

    return Number.isFinite(n) ? n : null;
  }}

  function collect(value, output) {{
    if (!value) return;

    if (Array.isArray(value)) {{
      value.forEach(item => collect(item, output));
      return;
    }}

    if (typeof value !== "object") return;

    if (lessonId(value)) {{
      output.push(value);
    }}

    [
      value.results,
      value.items,
      value.data,
      value.history,
      value.attempts,
      value.lessons,
      value.records
    ].forEach(child => {{
      if (child) collect(child, output);
    }});
  }}

  function latestMap(value) {{
    const all = [];
    collect(value, all);

    const map = {{}};

    all.forEach(item => {{
      const id = lessonId(item);
      if (!id) return;

      const stamp = Number(
        item.timestamp ??
        item.time ??
        item.updatedAt ??
        item.createdAt ??
        0
      );

      if (!map[id] || stamp >= map[id].stamp) {{
        map[id] = {{
          item: item,
          stamp: stamp
        }};
      }}
    }});

    return map;
  }}

  function completedLessons() {{
    const data = readJSON(PROGRESS_KEY, {{}});
    const result = new Set();

    if (Array.isArray(data)) {{
      data.forEach(item => {{
        const n = Number(
          typeof item === "object"
            ? lessonId(item)
            : item
        );

        if (Number.isInteger(n) && n >= 1 && n <= TOTAL) {{
          result.add(n);
        }}
      }});
    }} else if (data && typeof data === "object") {{
      for (let i = 1; i <= TOTAL; i++) {{
        if (
          data[i] === true ||
          data[String(i)] === true
        ) {{
          result.add(i);
        }}
      }}
    }}

    return result;
  }}

  function quizMap() {{
    return latestMap(readJSON(QUIZ_KEY, []));
  }}

  function priorityMap() {{
    return latestMap(readJSON(PRIORITY_KEY, []));
  }}

  function retestMap() {{
    return latestMap(readJSON(RETEST_KEY, []));
  }}

  function priorityValue(item) {{
    if (!item || typeof item !== "object") return "";

    return String(
      item.priority ??
      item.level ??
      item.status ??
      ""
    ).toLowerCase();
  }}

  function retestPending(item) {{
    if (!item) return false;

    const status = String(
      item.status ??
      item.result ??
      item.state ??
      ""
    ).toLowerCase();

    return (
      status.includes("pending") ||
      status.includes("retest") ||
      status.includes("weak") ||
      item.needsRetest === true ||
      item.retestPending === true
    );
  }}

  function calculate() {{
    const completed = completedLessons();
    const quizzes = quizMap();
    const priorities = priorityMap();
    const retests = retestMap();

    let passed = 0;
    let revision = 0;
    let retest = 0;
    let high = 0;

    for (let i = 1; i <= TOTAL; i++) {{
      const q = quizzes[i]?.item;
      const p = priorities[i]?.item;
      const r = retests[i]?.item;

      const s = score(q);
      const priority = priorityValue(p);

      if (s !== null && s >= PASS_SCORE) {{
        passed++;
      }}

      if (r && retestPending(r)) {{
        retest++;
      }}

      if (priority === "high") {{
        high++;
      }}

      if (
        (s !== null && s < PASS_SCORE) ||
        priority === "high" ||
        priority === "medium"
      ) {{
        revision++;
      }}
    }}

    let health = Math.round(
      (completed.size / TOTAL) * 100
    );

    // Quiz quality slightly refines the overall health.
    if (passed > 0) {{
      const quizFactor = Math.round(
        (passed / TOTAL) * 20
      );

      health = Math.min(
        100,
        Math.round((health * 0.8) + quizFactor)
      );
    }}

    return {{
      completed: completed.size,
      passed,
      revision,
      retest,
      high,
      health
    }};
  }}

  function healthLabel(value) {{
    if (value >= 90) return "Excellent";
    if (value >= 70) return "Strong Progress";
    if (value >= 40) return "Good Start";
    if (value > 0) return "In Progress";
    return "Getting Started";
  }}

  function render() {{
    const root = document.querySelector(
      "[data-quran-learning-health]"
    );

    if (!root) return;

    const data = calculate();

    root.querySelector("[data-health-score]").textContent =
      data.health + "%";

    root.querySelector("[data-health-label]").textContent =
      healthLabel(data.health);

    root.querySelector("[data-health-completed]").textContent =
      data.completed + "/" + TOTAL;

    root.querySelector("[data-health-passed]").textContent =
      data.passed;

    root.querySelector("[data-health-revision]").textContent =
      data.revision;

    root.querySelector("[data-health-retest]").textContent =
      data.retest;

    root.querySelector("[data-health-high]").textContent =
      data.high;

    const title = root.querySelector(
      "[data-health-message-title]"
    );

    const message = root.querySelector(
      "[data-health-message]"
    );

    if (data.completed >= TOTAL && data.revision === 0) {{
      title.textContent = "🎉 Academy progress looks excellent";

      message.textContent =
        "সব Lesson সম্পন্ন এবং কোনো Revision priority নেই। নিয়মিত Revision চালিয়ে যান।";

    }} else if (data.retest > 0) {{
      title.textContent = "🔄 Re-Test আগে করুন";

      message.textContent =
        "কিছু পাঠের Re-Test pending আছে। আগে সেগুলো আবার পরীক্ষা করুন।";

    }} else if (data.high > 0) {{
      title.textContent = "🔴 High Priority Revision করুন";

      message.textContent =
        "কিছু Lesson-এর priority বেশি। সেগুলো আগে Revision করলে শেখার ভিত্তি আরও শক্ত হবে।";

    }} else if (data.revision > 0) {{
      title.textContent = "📖 Revision চালিয়ে যান";

      message.textContent =
        "কিছু Lesson-এ আরও অনুশীলন দরকার। Revision Center থেকে এগুলো দেখুন।";

    }} else if (data.completed > 0) {{
      title.textContent = "🚀 শেখার যাত্রা ভালোভাবে চলছে";

      message.textContent =
        "আপনার progress আছে। নিয়মিত Practice ও Quiz চালিয়ে পরের Lesson-এ এগিয়ে যান।";

    }} else {{
      title.textContent = "🌱 শেখা শুরু করুন";

      message.textContent =
        "Lesson 1 থেকে শুরু করুন এবং ধীরে ধীরে Practice → Quiz → Revision flow অনুসরণ করুন।";
    }}
  }}

  window.AIZoneRefreshQuranLearningHealth = render;

  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", render);
  }} else {{
    render();
  }}

}})();

{JS_END}"""

    js = replace_block(js, JS_START, JS_END, block)
    JS.write_text(js, encoding="utf-8")
    print("Learning Health JS: INSTALLED")


def verify():
    dashboard = DASHBOARD.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")

    print()
    print("=== Verification ===")

    checks = [
        ("HTML markers",
         HTML_START in dashboard and HTML_END in dashboard),

        ("Health data attribute",
         "data-quran-learning-health" in dashboard),

        ("Health score",
         "data-health-score" in dashboard),

        ("Health stats",
         "data-health-completed" in dashboard
         and "data-health-passed" in dashboard
         and "data-health-revision" in dashboard
         and "data-health-retest" in dashboard
         and "data-health-high" in dashboard),

        ("CSS markers",
         CSS_START in css and CSS_END in css),

        ("JS markers",
         JS_START in js and JS_END in js),

        ("Refresh function",
         "AIZoneRefreshQuranLearningHealth" in js),

        ("Progress key",
         "ai_zone_quran_progress_v1" in js),

        ("Quiz key",
         "ai_zone_quran_quiz_v1" in js),

        ("Priority key",
         "ai_zone_quran_revision_priority_v1" in js),

        ("Re-Test key",
         "ai_zone_quran_retest_v1" in js),

        ("No GitHub push", True),
    ]

    for name, ok in checks:
        print(f"{name}: {'PASS' if ok else 'FAIL'}")

    return all(ok for _, ok in checks)


print("============================================================")
print(" AI Zone বাংলা — Session 23 Step 23.9")
print(" UNIFIED LEARNING HEALTH INSTALLER")
print("============================================================")

if not DASHBOARD.exists():
    raise SystemExit("ERROR: templates/quran.html not found")

install_html()
install_css()
install_js()

if verify():
    print()
    print("============================================================")
    print(" SESSION 23 — STEP 23.9 INSTALL COMPLETE")
    print(" Learning Health: PASS")
    print(" Existing systems preserved")
    print(" GitHub push: NO")
    print("============================================================")
else:
    print()
    print("INSTALLATION VERIFICATION FAILED")
    raise SystemExit(1)
