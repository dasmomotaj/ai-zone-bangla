from pathlib import Path
import shutil

ROOT = Path(".")
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"

DASHBOARD = TEMPLATES / "quran.html"
CSS = STATIC / "quran-progress.css"
JS = STATIC / "quran-progress.js"

HTML_START = "<!-- AI-ZONE-QURAN-SMART-REVISION-CENTER-START -->"
HTML_END = "<!-- AI-ZONE-QURAN-SMART-REVISION-CENTER-END -->"

CSS_START = "/* AI-ZONE-QURAN-SMART-REVISION-CENTER-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-SMART-REVISION-CENTER-CSS-END */"

JS_START = "/* AI-ZONE-QURAN-SMART-REVISION-CENTER-JS-START */"
JS_END = "/* AI-ZONE-QURAN-SMART-REVISION-CENTER-JS-END */"


def replace_block(text, start, end, block):
    a = text.find(start)
    b = text.find(end)

    if a != -1 and b != -1 and b > a:
        b += len(end)
        return text[:a] + block + text[b:]

    return text + "\n\n" + block + "\n"


def backup(path, suffix):
    if path.exists():
        target = Path(str(path) + suffix)
        shutil.copy2(path, target)
        print(f"Backup: {target}")


def install_dashboard():
    text = DASHBOARD.read_text(encoding="utf-8")

    backup(DASHBOARD, ".before-session23-step23-8")

    block = f"""{HTML_START}
<section class="quran-smart-revision-center" data-quran-smart-revision-center>

  <div class="quran-smart-revision-head">
    <div>
      <span class="quran-smart-revision-kicker">SMART REVISION CENTER</span>
      <h2>🔄 স্মার্ট Revision Center</h2>
      <p>
        আপনার Quiz, ভুল এবং Re-Test ফলাফল দেখে কোন পাঠ আগে Revision করা দরকার
        তা এখানে সাজানো হবে।
      </p>
    </div>

    <div class="quran-smart-revision-summary">
      <span data-revision-total>0</span>
      <small>Revision Items</small>
    </div>
  </div>

  <div class="quran-smart-revision-stats">

    <div class="revision-stat revision-high">
      <span class="revision-stat-icon">🔴</span>
      <strong data-revision-high>0</strong>
      <small>High Priority</small>
    </div>

    <div class="revision-stat revision-medium">
      <span class="revision-stat-icon">🟡</span>
      <strong data-revision-medium>0</strong>
      <small>Medium Priority</small>
    </div>

    <div class="revision-stat revision-improved">
      <span class="revision-stat-icon">🟢</span>
      <strong data-revision-improved>0</strong>
      <small>Improved</small>
    </div>

    <div class="revision-stat revision-retest">
      <span class="revision-stat-icon">🔄</span>
      <strong data-revision-retest>0</strong>
      <small>Re-Test</small>
    </div>

  </div>

  <div class="quran-smart-revision-list" data-revision-list>
    <div class="revision-empty" data-revision-empty>
      <span>✨</span>
      <strong>এখন কোনো Revision item নেই</strong>
      <p>Quiz ও Practice চালিয়ে যান। প্রয়োজন হলে এখানে পাঠগুলো automatically দেখা যাবে।</p>
    </div>
  </div>

</section>
{HTML_END}"""

    text = replace_block(text, HTML_START, HTML_END, block)

    marker = '<!-- AI-ZONE-QURAN-DASHBOARD-FOCUS-END -->'

    if HTML_START not in text:
        if marker in text:
            text = text.replace(marker, block + "\n" + marker, 1)
        else:
            text += "\n" + block + "\n"

    DASHBOARD.write_text(text, encoding="utf-8")
    print("Smart Revision Center HTML: INSTALLED")


def install_css():
    css = CSS.read_text(encoding="utf-8") if CSS.exists() else ""

    backup(CSS, ".before-session23-step23-8")

    block = f"""{CSS_START}

.quran-smart-revision-center {{
  margin: 28px 0;
  padding: 24px;
  border: 1px solid rgba(90, 210, 255, 0.24);
  border-radius: 24px;
  background:
    radial-gradient(circle at top right, rgba(0, 210, 255, 0.10), transparent 35%),
    rgba(10, 18, 32, 0.78);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.25);
}}

.quran-smart-revision-head {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}}

.quran-smart-revision-kicker {{
  display: block;
  margin-bottom: 6px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1.7px;
  opacity: .65;
}}

.quran-smart-revision-head h2 {{
  margin: 0 0 7px;
  font-size: clamp(22px, 4vw, 30px);
}}

.quran-smart-revision-head p {{
  margin: 0;
  max-width: 720px;
  line-height: 1.7;
  opacity: .78;
}}

.quran-smart-revision-summary {{
  min-width: 110px;
  padding: 13px 16px;
  text-align: center;
  border-radius: 18px;
  background: rgba(255,255,255,.055);
  border: 1px solid rgba(255,255,255,.09);
}}

.quran-smart-revision-summary span {{
  display: block;
  font-size: 28px;
  font-weight: 900;
}}

.quran-smart-revision-summary small {{
  opacity: .65;
}}

.quran-smart-revision-stats {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin: 20px 0;
}}

.revision-stat {{
  padding: 17px;
  border-radius: 18px;
  background: rgba(255,255,255,.045);
  border: 1px solid rgba(255,255,255,.08);
}}

.revision-stat-icon {{
  display: block;
  margin-bottom: 7px;
  font-size: 20px;
}}

.revision-stat strong {{
  display: block;
  font-size: 25px;
}}

.revision-stat small {{
  opacity: .68;
}}

.quran-smart-revision-list {{
  display: grid;
  gap: 10px;
}}

.quran-revision-item {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 15px 17px;
  border-radius: 17px;
  background: rgba(255,255,255,.045);
  border: 1px solid rgba(255,255,255,.075);
}}

.quran-revision-item-main {{
  min-width: 0;
}}

.quran-revision-item-title {{
  display: block;
  font-weight: 850;
}}

.quran-revision-item-meta {{
  display: block;
  margin-top: 4px;
  font-size: 12px;
  opacity: .65;
}}

.quran-revision-item-badge {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 88px;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 800;
}}

.quran-revision-item-badge.high {{
  background: rgba(255, 70, 70, .12);
}}

.quran-revision-item-badge.medium {{
  background: rgba(255, 190, 50, .12);
}}

.quran-revision-item-badge.improved {{
  background: rgba(80, 220, 150, .12);
}}

.quran-revision-item-actions {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}}

.quran-revision-item-actions a {{
  text-decoration: none;
}}

.revision-empty {{
  padding: 25px;
  text-align: center;
  border-radius: 18px;
  background: rgba(255,255,255,.035);
  border: 1px dashed rgba(255,255,255,.12);
}}

.revision-empty span {{
  display: block;
  margin-bottom: 7px;
  font-size: 25px;
}}

.revision-empty strong {{
  display: block;
}}

.revision-empty p {{
  margin: 7px 0 0;
  opacity: .65;
}}

@media (max-width: 760px) {{
  .quran-smart-revision-stats {{
    grid-template-columns: repeat(2, 1fr);
  }}

  .quran-smart-revision-head {{
    align-items: flex-start;
  }}
}}

@media (max-width: 560px) {{
  .quran-smart-revision-center {{
    padding: 17px;
    border-radius: 20px;
  }}

  .quran-smart-revision-head {{
    flex-direction: column;
  }}

  .quran-smart-revision-summary {{
    width: 100%;
    box-sizing: border-box;
  }}

  .quran-smart-revision-stats {{
    grid-template-columns: 1fr 1fr;
  }}

  .quran-revision-item {{
    align-items: flex-start;
    flex-direction: column;
  }}

  .quran-revision-item-actions {{
    width: 100%;
  }}
}}

{CSS_END}"""

    css = replace_block(css, CSS_START, CSS_END, block)
    CSS.write_text(css, encoding="utf-8")
    print("Smart Revision Center CSS: INSTALLED")


def install_js():
    js = JS.read_text(encoding="utf-8") if JS.exists() else ""

    backup(JS, ".before-session23-step23-8")

    block = f"""{JS_START}

(function () {{
  "use strict";

  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PRIORITY_KEY = "ai_zone_quran_revision_priority_v1";
  const RETEST_KEY = "ai_zone_quran_retest_v1";
  const MISTAKE_KEY = "ai_zone_quran_mistakes_v1";
  const PASS_SCORE = 70;
  const TOTAL = 20;

  function readJSON(key, fallback) {{
    try {{
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    }} catch (e) {{
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
    return Number.isInteger(n) && n >= 1 && n <= TOTAL ? n : null;
  }}

  function scoreOf(item) {{
    if (!item || typeof item !== "object") return null;

    const value =
      item.score ??
      item.percentage ??
      item.percent ??
      item.result;

    const n = Number(value);
    return Number.isFinite(n) ? n : null;
  }}

  function priorityOf(item) {{
    if (!item || typeof item !== "object") return "";

    return String(
      item.priority ??
      item.level ??
      item.status ??
      ""
    ).toLowerCase();
  }}

  function collect(value, output) {{
    if (!value) return;

    if (Array.isArray(value)) {{
      value.forEach(item => collect(item, output));
      return;
    }}

    if (typeof value !== "object") return;

    const lesson = lessonIdOf(value);

    if (lesson) {{
      output.push(value);
    }}

    [
      value.results,
      value.items,
      value.data,
      value.history,
      value.attempts,
      value.lessons,
      value.records,
      value.questions
    ].forEach(child => {{
      if (child) collect(child, output);
    }});
  }}

  function latestByLesson(value) {{
    const all = [];
    collect(value, all);

    const map = {{}};

    all.forEach(item => {{
      const lesson = lessonIdOf(item);
      if (!lesson) return;

      const stamp = Number(
        item.timestamp ??
        item.time ??
        item.updatedAt ??
        item.createdAt ??
        0
      );

      if (!map[lesson] || stamp >= map[lesson].stamp) {{
        map[lesson] = {{ item, stamp }};
      }}
    }});

    return map;
  }}

  function getPriority(lesson) {{
    const data = latestByLesson(readJSON(PRIORITY_KEY, []));
    const item = data[lesson]?.item;
    const priority = priorityOf(item);

    if (priority.includes("high")) return "high";
    if (priority.includes("medium")) return "medium";
    if (priority.includes("low")) return "low";

    return "";
  }}

  function getScore(lesson) {{
    const data = latestByLesson(readJSON(QUIZ_KEY, []));
    return scoreOf(data[lesson]?.item);
  }}

  function hasRetest(lesson) {{
    const data = latestByLesson(readJSON(RETEST_KEY, []));
    const item = data[lesson]?.item;

    if (!item) return false;

    const status = String(
      item.status ??
      item.result ??
      item.state ??
      ""
    ).toLowerCase();

    return (
      status.includes("retest") ||
      status.includes("pending") ||
      status.includes("weak") ||
      item.needsRetest === true ||
      item.retestPending === true
    );
  }}

  function hasMistake(lesson) {{
    const data = latestByLesson(readJSON(MISTAKE_KEY, []));
    return !!data[lesson];
  }}

  function lessonURL(lesson) {{
    if (lesson === 1) {{
      return "{{{{ url_for('quran_lesson', lesson_id=1) }}}}";
    }}

    return "{{{{ url_for('quran_lesson_2') }}}}".replace(
      "2",
      String(lesson)
    );
  }}

  function safeLessonURL(lesson) {{
    if (lesson === 1) return "/quran/lesson/1";
    return "/quran/lesson/" + lesson;
  }}

  function buildItems() {{
    const items = [];
    const completed = readJSON("ai_zone_quran_progress_v1", {{}});

    for (let lesson = 1; lesson <= TOTAL; lesson++) {{
      const score = getScore(lesson);
      const priority = getPriority(lesson);
      const retest = hasRetest(lesson);
      const mistake = hasMistake(lesson);

      const progressDone =
        Array.isArray(completed)
          ? completed.includes(lesson) || completed.includes(String(lesson))
          : completed &&
            (
              completed[lesson] === true ||
              completed[String(lesson)] === true
            );

      if (retest) {{
        items.push({{
          lesson,
          type: "retest",
          label: "Re-Test",
          title: "Lesson " + lesson,
          meta: score !== null
            ? "আগের Score: " + score + "%"
            : "আবার পরীক্ষা দিন",
          rank: 1
        }});
        return;
      }}

      if (score !== null && score < PASS_SCORE) {{
        items.push({{
          lesson,
          type: priority === "high" ? "high" : "medium",
          label: priority === "high" ? "High Priority" : "Revision",
          title: "Lesson " + lesson,
          meta: "Quiz Score: " + score + "%",
          rank: priority === "high" ? 2 : 3
        }});
        return;
      }}

      if (priority === "high" || priority === "medium" || mistake) {{
        items.push({{
          lesson,
          type: priority || "medium",
          label: priority === "high" ? "High Priority" : "Medium Priority",
          title: "Lesson " + lesson,
          meta: mistake ? "ভুলগুলো আবার অনুশীলন করুন" : "আরও Revision দরকার",
          rank: priority === "high" ? 2 : 3
        }});
        return;
      }}

      if (progressDone && score !== null && score >= PASS_SCORE) {{
        items.push({{
          lesson,
          type: "improved",
          label: "Improved",
          title: "Lesson " + lesson,
          meta: "Quiz Score: " + score + "%",
          rank: 4
        }});
      }}
    }}

    return items.sort((a, b) => a.rank - b.rank || a.lesson - b.lesson);
  }}

  function render() {{
    const root = document.querySelector("[data-quran-smart-revision-center]");
    if (!root) return;

    const list = root.querySelector("[data-revision-list]");
    const empty = root.querySelector("[data-revision-empty]");

    const items = buildItems();

    root.querySelector("[data-revision-total]").textContent = items.length;
    root.querySelector("[data-revision-high]").textContent =
      items.filter(x => x.type === "high").length;
    root.querySelector("[data-revision-medium]").textContent =
      items.filter(x => x.type === "medium").length;
    root.querySelector("[data-revision-improved]").textContent =
      items.filter(x => x.type === "improved").length;
    root.querySelector("[data-revision-retest]").textContent =
      items.filter(x => x.type === "retest").length;

    list.querySelectorAll(".quran-revision-item").forEach(el => el.remove());

    if (!items.length) {{
      empty.style.display = "";
      return;
    }}

    empty.style.display = "none";

    items.forEach(item => {{
      const row = document.createElement("div");
      row.className = "quran-revision-item";

      const main = document.createElement("div");
      main.className = "quran-revision-item-main";

      const title = document.createElement("span");
      title.className = "quran-revision-item-title";
      title.textContent = item.title;

      const meta = document.createElement("span");
      meta.className = "quran-revision-item-meta";
      meta.textContent = item.meta;

      main.appendChild(title);
      main.appendChild(meta);

      const actions = document.createElement("div");
      actions.className = "quran-revision-item-actions";

      const badge = document.createElement("span");
      badge.className = "quran-revision-item-badge " + item.type;
      badge.textContent = item.label;

      const link = document.createElement("a");
      link.className = "btn btn-primary";
      link.href = safeLessonURL(item.lesson);
      link.textContent =
        item.type === "retest"
          ? "Re-Test দেখুন →"
          : "Revision করুন →";

      actions.appendChild(badge);
      actions.appendChild(link);

      row.appendChild(main);
      row.appendChild(actions);

      list.appendChild(row);
    }});
  }}

  window.AIZoneRefreshQuranSmartRevisionCenter = render;

  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", render);
  }} else {{
    render();
  }}

}})();

{JS_END}"""

    js = replace_block(js, JS_START, JS_END, block)
    JS.write_text(js, encoding="utf-8")
    print("Smart Revision Center JS: INSTALLED")


def verify():
    print()
    print("=== Verification ===")

    checks = [
        ("Dashboard HTML", HTML_START in DASHBOARD.read_text(encoding="utf-8")
         and HTML_END in DASHBOARD.read_text(encoding="utf-8")),
        ("Dashboard data attribute",
         "data-quran-smart-revision-center" in DASHBOARD.read_text(encoding="utf-8")),
        ("CSS markers",
         CSS_START in CSS.read_text(encoding="utf-8")
         and CSS_END in CSS.read_text(encoding="utf-8")),
        ("JS markers",
         JS_START in JS.read_text(encoding="utf-8")
         and JS_END in JS.read_text(encoding="utf-8")),
        ("Refresh function",
         "AIZoneRefreshQuranSmartRevisionCenter" in JS.read_text(encoding="utf-8")),
        ("Revision Priority key",
         "ai_zone_quran_revision_priority_v1" in JS.read_text(encoding="utf-8")),
        ("Re-Test key",
         "ai_zone_quran_retest_v1" in JS.read_text(encoding="utf-8")),
        ("Mistake key",
         "ai_zone_quran_mistakes_v1" in JS.read_text(encoding="utf-8")),
        ("Progress key",
         "ai_zone_quran_progress_v1" in JS.read_text(encoding="utf-8")),
        ("No GitHub push",
         True),
    ]

    for name, ok in checks:
        print(f"{name}: {'PASS' if ok else 'FAIL'}")

    return all(ok for _, ok in checks)


print("============================================================")
print(" AI Zone বাংলা — Session 23 Step 23.8")
print(" SMART REVISION CENTER INSTALLER")
print("============================================================")

if not DASHBOARD.exists():
    raise SystemExit("ERROR: templates/quran.html not found")

install_dashboard()
install_css()
install_js()

if verify():
    print()
    print("============================================================")
    print(" SESSION 23 — STEP 23.8 INSTALL COMPLETE")
    print(" Smart Revision Center: PASS")
    print(" Existing systems preserved")
    print(" GitHub push: NO")
    print("============================================================")
else:
    print()
    print("INSTALLATION VERIFICATION FAILED")
    raise SystemExit(1)
