from pathlib import Path
import shutil
import re
import subprocess
import sys

ROOT = Path(".")
STATIC = ROOT / "static"
JS = STATIC / "quran-progress.js"
CSS = STATIC / "quran-progress.css"
DASHBOARD = ROOT / "templates" / "quran.html"

print("=" * 64)
print(" AI Zone বাংলা — Quran Revision Re-Test Engine")
print(" Session 22 — Step 22.12")
print("=" * 64)

TOTAL = 20
RETEST_KEY = "ai_zone_quran_retest_v1"

# --------------------------------------------------
# 1. BACKUP
# --------------------------------------------------

for path in [JS, CSS, DASHBOARD]:
    if path.exists():
        backup = path.with_name(
            path.name + ".before-session22-step22-12"
        )
        if not backup.exists():
            shutil.copy2(path, backup)
            print(f"Backup created: {backup}")

# --------------------------------------------------
# 2. REVISION RE-TEST JS
# --------------------------------------------------

REVISION_JS_START = "// AI-ZONE-QURAN-REVISION-RETEST-JS-START"
REVISION_JS_END = "// AI-ZONE-QURAN-REVISION-RETEST-JS-END"

revision_js = f"""
{REVISION_JS_START}
(function () {{
    "use strict";

    const QUIZ_KEY = "ai_zone_quran_quiz_v1";
    const MISTAKE_KEY = "ai_zone_quran_mistakes_v1";
    const RETEST_KEY = "ai_zone_quran_retest_v1";
    const PASS_SCORE = 70;

    function safeJSON(key, fallback) {{
        try {{
            const raw = localStorage.getItem(key);
            if (!raw) return fallback;
            const parsed = JSON.parse(raw);
            return parsed == null ? fallback : parsed;
        }} catch (e) {{
            return fallback;
        }}
    }}

    function saveJSON(key, value) {{
        try {{
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        }} catch (e) {{
            return false;
        }}
    }}

    function lessonIdOf(item) {{
        if (!item || typeof item !== "object") return null;

        const raw =
            item.lessonId ??
            item.lesson_id ??
            item.lesson ??
            item.id;

        const id = Number(raw);

        if (!Number.isInteger(id) || id < 1 || id > {TOTAL}) {{
            return null;
        }}

        return id;
    }}

    function scoreOf(item) {{
        if (!item || typeof item !== "object") return null;

        const raw =
            item.score ??
            item.percent ??
            item.percentage ??
            item.result;

        const score = Number(raw);

        if (!Number.isFinite(score)) return null;

        return Math.max(0, Math.min(100, score));
    }}

    function timestampOf(item) {{
        if (!item || typeof item !== "object") return 0;

        const raw =
            item.timestamp ??
            item.time ??
            item.createdAt ??
            item.updatedAt ??
            item.attemptedAt;

        const value = Date.parse(raw);

        return Number.isFinite(value) ? value : 0;
    }}

    function extractQuizResults(data) {{
        if (Array.isArray(data)) return data;

        if (!data || typeof data !== "object") return [];

        if (Array.isArray(data.results)) return data.results;
        if (Array.isArray(data.attempts)) return data.attempts;
        if (Array.isArray(data.quizzes)) return data.quizzes;

        return [];
    }}

    function getLatestScores() {{
        const data = safeJSON(QUIZ_KEY, []);
        const results = extractQuizResults(data);

        const latest = {{}};

        results.forEach(item => {{
            const lessonId = lessonIdOf(item);
            const score = scoreOf(item);

            if (lessonId === null || score === null) return;

            const old = latest[lessonId];

            if (!old || timestampOf(item) >= timestampOf(old)) {{
                latest[lessonId] = item;
            }}
        }});

        return latest;
    }}

    function getMistakes() {{
        const data = safeJSON(MISTAKE_KEY, {{}});

        if (Array.isArray(data)) {{
            return data;
        }}

        if (data && Array.isArray(data.mistakes)) {{
            return data.mistakes;
        }}

        return [];
    }}

    function normalizeMistakes() {{
        const mistakes = getMistakes();

        return mistakes
            .map(item => {{
                const lessonId = lessonIdOf(item);
                if (lessonId === null) return null;

                return {{
                    ...item,
                    lessonId
                }};
            }})
            .filter(Boolean);
    }}

    function buildRetestData() {{
        const latestScores = getLatestScores();
        const mistakes = normalizeMistakes();

        const previous = safeJSON(RETEST_KEY, {{}});
        const history = previous.history && typeof previous.history === "object"
            ? previous.history
            : {{}};

        const queue = [];
        const improved = [];
        const stillWeak = [];

        mistakes.forEach(item => {{
            const lessonId = item.lessonId;

            const latest = latestScores[lessonId];
            const currentScore = latest ? scoreOf(latest) : null;

            const previousAttempt =
                history[String(lessonId)] || null;

            const previousScore =
                previousAttempt &&
                Number.isFinite(Number(previousAttempt.score))
                    ? Number(previousAttempt.score)
                    : null;

            let status = "needs-retest";

            if (currentScore !== null && currentScore >= PASS_SCORE) {{
                status = "improved";
                improved.push({{
                    lessonId,
                    score: currentScore,
                    previousScore
                }});
            }} else {{
                status = "still-weak";
                stillWeak.push({{
                    lessonId,
                    score: currentScore,
                    previousScore
                }});

                queue.push({{
                    lessonId,
                    score: currentScore,
                    previousScore,
                    status
                }});
            }}

            history[String(lessonId)] = {{
                lessonId,
                score: currentScore,
                previousScore,
                status,
                checkedAt: new Date().toISOString()
            }};
        }});

        queue.sort((a, b) => {{
            const as = a.score === null ? 0 : a.score;
            const bs = b.score === null ? 0 : b.score;
            return as - bs;
        }});

        const data = {{
            version: 1,
            updatedAt: new Date().toISOString(),
            passScore: PASS_SCORE,
            queue,
            improved,
            stillWeak,
            history
        }};

        saveJSON(RETEST_KEY, data);

        return data;
    }}

    function refresh() {{
        const data = buildRetestData();

        const panel = document.getElementById("quranRevisionRetest");
        const status = document.getElementById("quranRetestStatus");
        const list = document.getElementById("quranRetestList");
        const count = document.getElementById("quranRetestCount");
        const improvedCount = document.getElementById("quranRetestImproved");
        const weakCount = document.getElementById("quranRetestStillWeak");

        if (panel) panel.hidden = false;

        if (count) {{
            count.textContent = String(data.queue.length);
        }}

        if (improvedCount) {{
            improvedCount.textContent = String(data.improved.length);
        }}

        if (weakCount) {{
            weakCount.textContent = String(data.stillWeak.length);
        }}

        if (status) {{
            if (!data.queue.length && data.improved.length) {{
                status.textContent =
                    "🎉 দারুণ! সব ট্র্যাক করা ভুলে পাস স্কোর অর্জিত হয়েছে।";
            }} else if (data.queue.length) {{
                status.textContent =
                    "🔁 কিছু lesson আবার Revision + Re-Test করা দরকার।";
            }} else {{
                status.textContent =
                    "📚 Re-Test queue তৈরি হলে এখানে দেখা যাবে।";
            }}
        }}

        if (list) {{
            list.innerHTML = "";

            if (!data.queue.length) {{
                const empty = document.createElement("div");
                empty.className = "quran-retest-empty";
                empty.textContent =
                    data.improved.length
                        ? "✅ বর্তমানে কোনো weak re-test নেই।"
                        : "📖 Quiz ও mistake data তৈরি হলে queue দেখা যাবে।";
                list.appendChild(empty);
                return;
            }}

            data.queue.forEach(item => {{
                const row = document.createElement("div");
                row.className = "quran-retest-item";

                const scoreText =
                    item.score === null
                        ? "Score: —"
                        : "Score: " + item.score + "%";

                const previousText =
                    item.previousScore === null
                        ? ""
                        : " · আগের: " + item.previousScore + "%";

                row.innerHTML =
                    '<div class="quran-retest-item-main">' +
                    '<strong>Lesson ' + item.lessonId + '</strong>' +
                    '<span>' + scoreText + previousText + '</span>' +
                    '</div>' +
                    '<a class="quran-retest-link" href="/quran/lesson/' +
                    item.lessonId +
                    '">Revision করুন →</a>';

                list.appendChild(row);
            }});
        }}

        return data;
    }}

    function recordRetest(lessonId, score) {{
        lessonId = Number(lessonId);
        score = Number(score);

        if (
            !Number.isInteger(lessonId) ||
            lessonId < 1 ||
            lessonId > {TOTAL} ||
            !Number.isFinite(score)
        ) {{
            return false;
        }}

        const data = safeJSON(RETEST_KEY, {{
            version: 1,
            history: {{}}
        }});

        if (!data.history || typeof data.history !== "object") {{
            data.history = {{}};
        }}

        const old = data.history[String(lessonId)] || {{}};

        data.history[String(lessonId)] = {{
            lessonId,
            score: Math.max(0, Math.min(100, score)),
            previousScore:
                Number.isFinite(Number(old.score))
                    ? Number(old.score)
                    : null,
            status:
                score >= PASS_SCORE
                    ? "improved"
                    : "still-weak",
            checkedAt: new Date().toISOString()
        }};

        data.updatedAt = new Date().toISOString();

        saveJSON(RETEST_KEY, data);
        refresh();

        return true;
    }}

    window.AIZoneQuranRevisionRetest = {{
        refresh,
        rebuild: buildRetestData,
        getRetest: () => safeJSON(RETEST_KEY, {{}}),
        recordRetest,
        getLatestScores
    }};

    document.addEventListener("DOMContentLoaded", refresh);

    window.addEventListener("storage", function (event) {{
        if (
            event.key === QUIZ_KEY ||
            event.key === MISTAKE_KEY ||
            event.key === RETEST_KEY
        ) {{
            refresh();
        }}
    }});
}})();
{REVISION_JS_END}
"""

def install_marked_block(path, start, end, block):
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

    text = path.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        re.S
    )

    if pattern.search(text):
        text = pattern.sub(block.strip(), text)
    else:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"

    path.write_text(text, encoding="utf-8")

install_marked_block(
    JS,
    REVISION_JS_START,
    REVISION_JS_END,
    revision_js
)

print("Revision Re-Test JS: INSTALLED")

# --------------------------------------------------
# 3. CSS
# --------------------------------------------------

CSS_START = "/* AI-ZONE-QURAN-REVISION-RETEST-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-REVISION-RETEST-CSS-END */"

css_block = f"""
{CSS_START}
.quran-revision-retest {{
    margin: 18px 0;
    padding: 18px;
    border: 1px solid rgba(0, 220, 255, 0.22);
    border-radius: 18px;
    background: rgba(8, 18, 32, 0.72);
}}

.quran-retest-summary {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    margin: 14px 0;
}}

.quran-retest-stat {{
    padding: 12px;
    border-radius: 14px;
    background: rgba(255,255,255,0.045);
    text-align: center;
}}

.quran-retest-stat strong {{
    display: block;
    font-size: 1.35rem;
}}

.quran-retest-stat span {{
    display: block;
    margin-top: 4px;
    opacity: 0.72;
    font-size: 0.82rem;
}}

.quran-retest-status {{
    margin: 12px 0;
    padding: 11px 13px;
    border-radius: 12px;
    background: rgba(0, 220, 255, 0.07);
}}

.quran-retest-item {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 12px;
    margin-top: 9px;
    border-radius: 13px;
    background: rgba(255,255,255,0.035);
}}

.quran-retest-item-main {{
    display: flex;
    flex-direction: column;
    gap: 4px;
}}

.quran-retest-item-main span {{
    opacity: 0.72;
    font-size: 0.82rem;
}}

.quran-retest-link {{
    text-decoration: none;
    white-space: nowrap;
}}

.quran-retest-empty {{
    padding: 14px;
    border-radius: 13px;
    background: rgba(255,255,255,0.035);
    opacity: 0.78;
}}

@media (max-width: 640px) {{
    .quran-retest-summary {{
        grid-template-columns: 1fr;
    }}

    .quran-retest-item {{
        align-items: flex-start;
        flex-direction: column;
    }}
}}
{CSS_END}
"""

install_marked_block(
    CSS,
    CSS_START,
    CSS_END,
    css_block
)

print("Revision Re-Test CSS: INSTALLED")

# --------------------------------------------------
# 4. DASHBOARD PANEL
# --------------------------------------------------

PANEL_START = "<!-- AI-ZONE-QURAN-REVISION-RETEST-START -->"
PANEL_END = "<!-- AI-ZONE-QURAN-REVISION-RETEST-END -->"

panel = f"""
{PANEL_START}
<section
    id="quranRevisionRetest"
    class="quran-revision-retest"
    aria-label="Quran Revision Re-Test"
>
    <div>
        <h2>🔁 Revision Re-Test</h2>
        <p>
            ভুল হওয়া lesson আবার অনুশীলন করুন,
            তারপর Re-Test করে উন্নতি যাচাই করুন।
        </p>
    </div>

    <div class="quran-retest-summary">
        <div class="quran-retest-stat">
            <strong id="quranRetestCount">0</strong>
            <span>Re-Test Queue</span>
        </div>

        <div class="quran-retest-stat">
            <strong id="quranRetestImproved">0</strong>
            <span>Improved</span>
        </div>

        <div class="quran-retest-stat">
            <strong id="quranRetestStillWeak">0</strong>
            <span>Still Weak</span>
        </div>
    </div>

    <div id="quranRetestStatus" class="quran-retest-status">
        📚 Re-Test queue তৈরি হলে এখানে দেখা যাবে।
    </div>

    <div id="quranRetestList">
        <div class="quran-retest-empty">
            📖 Quiz ও mistake data তৈরি হলে queue দেখা যাবে।
        </div>
    </div>
</section>
{PANEL_END}
"""

if not DASHBOARD.exists():
    raise SystemExit("Missing dashboard template: templates/quran.html")

dashboard = DASHBOARD.read_text(encoding="utf-8")

panel_pattern = re.compile(
    re.escape(PANEL_START) + r".*?" + re.escape(PANEL_END),
    re.S
)

if panel_pattern.search(dashboard):
    dashboard = panel_pattern.sub(panel.strip(), dashboard)
else:
    # Insert after mistake tracker if available.
    mistake_end = "<!-- AI-ZONE-QURAN-MISTAKE-TRACKER-END -->"

    if mistake_end in dashboard:
        dashboard = dashboard.replace(
            mistake_end,
            mistake_end + "\n\n" + panel.strip(),
            1
        )
    else:
        dashboard = dashboard.rstrip() + "\n\n" + panel.strip() + "\n"

DASHBOARD.write_text(dashboard, encoding="utf-8")

print("Dashboard Revision Re-Test Panel: INSTALLED")

# --------------------------------------------------
# 5. PYTHON SYNTAX
# --------------------------------------------------

targets = [
    ROOT / "app.py",
    ROOT / "quran_quiz_bank.py",
    ROOT / "quran_audio_sources.py",
]

for target in targets:
    if target.exists():
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(target)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{target}: PASS")
        else:
            print(f"{target}: FAIL")
            print(result.stderr)
            raise SystemExit(1)

# --------------------------------------------------
# 6. MARKER VERIFICATION
# --------------------------------------------------

checks = [
    (JS, REVISION_JS_START, "Revision Re-Test JS"),
    (JS, "AIZoneQuranRevisionRetest", "Re-Test Engine"),
    (JS, RETEST_KEY, "Re-Test Storage"),
    (CSS, CSS_START, "Re-Test CSS"),
    (CSS, ".quran-revision-retest", "Re-Test Styling"),
    (DASHBOARD, PANEL_START, "Dashboard Re-Test Panel"),
    (DASHBOARD, "quranRetestCount", "Re-Test Count"),
    (DASHBOARD, "quranRetestImproved", "Improved Counter"),
    (DASHBOARD, "quranRetestStillWeak", "Still Weak Counter"),
    (DASHBOARD, "quranRetestList", "Re-Test Queue"),
]

for path, marker, label in checks:
    content = path.read_text(encoding="utf-8")

    if marker in content:
        print(f"{label}: PASS")
    else:
        print(f"{label}: FAIL")
        raise SystemExit(1)

print()
print("=" * 64)
print(" STEP 22.12 INSTALL FINISHED")
print("=" * 64)
print(" Revision Re-Test Engine: READY")
print(" Re-Test Queue: READY")
print(" Improved Counter: READY")
print(" Still Weak Counter: READY")
print(" Quiz Data Preserved")
print(" Mistake Tracker Preserved")
print(" Existing Lesson Content Preserved")
print(" NO GITHUB PUSH")
print("=" * 64)
