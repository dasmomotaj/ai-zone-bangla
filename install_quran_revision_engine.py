from pathlib import Path
import shutil
import re

ROOT = Path(".")
STATIC = ROOT / "static"
TEMPLATES = ROOT / "templates"

JS = STATIC / "quran-progress.js"
CSS = STATIC / "quran-progress.css"

TOTAL = 20

print("=" * 54)
print(" AI Zone বাংলা — Quran Smart Revision Engine")
print(" Session 22 — Step 22.9")
print("=" * 54)

# --------------------------------------------------
# 1. BACKUPS
# --------------------------------------------------

for path in [JS, CSS]:
    if path.exists():
        backup = path.with_name(path.name + ".before-session22-step22-9")
        if not backup.exists():
            shutil.copy2(path, backup)
            print(f"Backup created: {backup}")

# --------------------------------------------------
# 2. REVISION JAVASCRIPT
# --------------------------------------------------

JS_START = "// AI-ZONE-QURAN-REVISION-JS-START"
JS_END = "// AI-ZONE-QURAN-REVISION-JS-END"

revision_js = r'''
// AI-ZONE-QURAN-REVISION-JS-START
(function () {
    "use strict";

    const TOTAL = 20;
    const QUIZ_KEY = "ai_zone_quran_quiz_v1";
    const REVISION_KEY = "ai_zone_quran_revision_v1";

    function readJSON(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            return raw ? JSON.parse(raw) : fallback;
        } catch (e) {
            return fallback;
        }
    }

    function getQuizData() {
        const data = readJSON(QUIZ_KEY, {});
        return data && typeof data === "object" ? data : {};
    }

    function getResults() {
        const data = getQuizData();

        if (Array.isArray(data)) {
            return data;
        }

        if (Array.isArray(data.results)) {
            return data.results;
        }

        return [];
    }

    function normalizeLessonId(item) {
        const value =
            item.lessonId ??
            item.lesson ??
            item.lesson_id ??
            item.id;

        const id = Number(value);

        return Number.isInteger(id) && id >= 1 && id <= TOTAL
            ? id
            : null;
    }

    function normalizeScore(item) {
        const value =
            item.score ??
            item.percent ??
            item.percentage ??
            item.result;

        const score = Number(value);

        return Number.isFinite(score) ? score : null;
    }

    function buildRevision() {
        const results = getResults();
        const lessonMap = {};

        for (const item of results) {
            if (!item || typeof item !== "object") {
                continue;
            }

            const lessonId = normalizeLessonId(item);
            const score = normalizeScore(item);

            if (lessonId === null || score === null) {
                continue;
            }

            lessonMap[lessonId] = {
                lessonId: lessonId,
                score: Math.max(0, Math.min(100, score)),
                weak: score < 70,
                updatedAt: Date.now()
            };
        }

        const weakLessons = Object.values(lessonMap)
            .filter(item => item.weak)
            .sort((a, b) => a.score - b.score);

        const revision = {
            updatedAt: Date.now(),
            weakLessons: weakLessons,
            allLessons: Object.values(lessonMap),
            weakCount: weakLessons.length,
            totalTracked: Object.keys(lessonMap).length
        };

        try {
            localStorage.setItem(
                REVISION_KEY,
                JSON.stringify(revision)
            );
        } catch (e) {
            // localStorage may be unavailable.
        }

        return revision;
    }

    function getRevision() {
        const saved = readJSON(REVISION_KEY, null);

        if (
            saved &&
            typeof saved === "object" &&
            Array.isArray(saved.weakLessons)
        ) {
            return saved;
        }

        return buildRevision();
    }

    function render() {
        const panel = document.getElementById(
            "quranSmartRevision"
        );

        if (!panel) {
            return;
        }

        const revision = buildRevision();

        const count = document.getElementById(
            "quranRevisionWeakCount"
        );

        const status = document.getElementById(
            "quranRevisionStatus"
        );

        const list = document.getElementById(
            "quranRevisionList"
        );

        if (count) {
            count.textContent = String(revision.weakCount);
        }

        if (status) {
            if (revision.totalTracked === 0) {
                status.textContent =
                    "এখনও কোনো Quiz result পাওয়া যায়নি। আগে Quiz দিন।";
            } else if (revision.weakCount === 0) {
                status.textContent =
                    "দারুণ! এখন পর্যন্ত কোনো দুর্বল Lesson শনাক্ত হয়নি।";
            } else {
                status.textContent =
                    revision.weakCount +
                    "টি Lesson Revision করার পরামর্শ দেওয়া হচ্ছে।";
            }
        }

        if (list) {
            if (revision.weakLessons.length === 0) {
                list.innerHTML =
                    '<div class="revision-empty">🎉 Revision queue খালি।</div>';
                return;
            }

            list.innerHTML = revision.weakLessons.map(function (item) {
                return (
                    '<div class="revision-item">' +
                        '<div class="revision-item-info">' +
                            '<strong>Lesson ' +
                            item.lessonId +
                            '</strong>' +
                            '<span>Quiz Score: ' +
                            item.score +
                            '%</span>' +
                        '</div>' +
                        '<a class="revision-study-btn" href="/quran/lesson/' +
                            item.lessonId +
                        '">Revision করুন →</a>' +
                    '</div>'
                );
            }).join("");
        }
    }

    window.AIZoneQuranRevision = {
        refresh: render,
        rebuild: buildRevision,
        getRevision: getRevision
    };

    document.addEventListener("DOMContentLoaded", render);

    window.addEventListener("storage", function (event) {
        if (event.key === QUIZ_KEY) {
            render();
        }
    });

})();
// AI-ZONE-QURAN-REVISION-JS-END
'''

# Remove old revision block if present
if JS.exists():
    js_text = JS.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(JS_START) + r".*?" +
        re.escape(JS_END),
        re.DOTALL
    )

    js_text = pattern.sub("", js_text).rstrip() + "\n"

    JS.write_text(
        js_text + "\n" + revision_js + "\n",
        encoding="utf-8"
    )
else:
    JS.write_text(revision_js, encoding="utf-8")

print("Revision JS: INSTALLED")

# --------------------------------------------------
# 3. REVISION CSS
# --------------------------------------------------

CSS_START = "/* AI-ZONE-QURAN-REVISION-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-REVISION-CSS-END */"

revision_css = r'''
/* AI-ZONE-QURAN-REVISION-CSS-START */

.quran-smart-revision {
    margin: 28px 0;
    padding: 22px;
    border-radius: 22px;
    border: 1px solid rgba(90, 220, 255, 0.22);
    background:
        linear-gradient(
            145deg,
            rgba(12, 28, 48, 0.96),
            rgba(8, 16, 30, 0.98)
        );
    box-shadow: 0 18px 55px rgba(0, 0, 0, 0.24);
}

.revision-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    flex-wrap: wrap;
}

.revision-title {
    margin: 0;
    font-size: 1.25rem;
}

.revision-badge {
    min-width: 42px;
    height: 42px;
    padding: 0 12px;
    border-radius: 14px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    background: rgba(255, 185, 80, 0.14);
    border: 1px solid rgba(255, 185, 80, 0.30);
}

.revision-status {
    margin: 12px 0 18px;
    opacity: 0.82;
    line-height: 1.7;
}

.revision-list {
    display: grid;
    gap: 12px;
}

.revision-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
    padding: 15px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.revision-item-info {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.revision-item-info span {
    font-size: 0.88rem;
    opacity: 0.72;
}

.revision-study-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 10px 14px;
    border-radius: 12px;
    text-decoration: none;
    font-weight: 700;
    background: rgba(90, 220, 255, 0.12);
    border: 1px solid rgba(90, 220, 255, 0.28);
}

.revision-study-btn:hover {
    transform: translateY(-1px);
}

.revision-empty {
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    background: rgba(90, 220, 255, 0.06);
}

/* AI-ZONE-QURAN-REVISION-CSS-END */
'''

if CSS.exists():
    css_text = CSS.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(CSS_START) + r".*?" +
        re.escape(CSS_END),
        re.DOTALL
    )

    css_text = pattern.sub("", css_text).rstrip() + "\n"

    CSS.write_text(
        css_text + "\n" + revision_css + "\n",
        encoding="utf-8"
    )
else:
    CSS.write_text(revision_css, encoding="utf-8")

print("Revision CSS: INSTALLED")

# --------------------------------------------------
# 4. ADD REVISION PANEL TO DASHBOARD
# --------------------------------------------------

dashboard = TEMPLATES / "quran.html"

DASH_START = "<!-- AI-ZONE-QURAN-SMART-REVISION-START -->"
DASH_END = "<!-- AI-ZONE-QURAN-SMART-REVISION-END -->"

dashboard_block = r'''
<!-- AI-ZONE-QURAN-SMART-REVISION-START -->
<section class="quran-smart-revision" id="quranSmartRevision">

    <div class="revision-header">
        <h2 class="revision-title">
            🧠 Smart Revision
        </h2>

        <span class="revision-badge"
              id="quranRevisionWeakCount">0</span>
    </div>

    <p class="revision-status" id="quranRevisionStatus">
        Quiz result বিশ্লেষণ করা হচ্ছে…
    </p>

    <div class="revision-list" id="quranRevisionList">
        <div class="revision-empty">
            Revision queue প্রস্তুত হচ্ছে…
        </div>
    </div>

</section>

<script>
document.addEventListener("DOMContentLoaded", function () {
    if (window.AIZoneQuranRevision) {
        window.AIZoneQuranRevision.refresh();
    }
});
</script>
<!-- AI-ZONE-QURAN-SMART-REVISION-END -->
'''

if dashboard.exists():
    html = dashboard.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(DASH_START) + r".*?" +
        re.escape(DASH_END),
        re.DOTALL
    )

    html = pattern.sub("", html).rstrip()

    # Insert before the first closing body if possible.
    lower = html.lower()
    body_pos = lower.rfind("</body>")

    if body_pos != -1:
        html = (
            html[:body_pos]
            + "\n"
            + dashboard_block
            + "\n"
            + html[body_pos:]
        )
    else:
        html += "\n" + dashboard_block

    dashboard.write_text(html, encoding="utf-8")

    print("Dashboard Smart Revision panel: INSTALLED")
else:
    print("Dashboard quran.html: NOT FOUND")

# --------------------------------------------------
# 5. SYNTAX CHECK
# --------------------------------------------------

import subprocess
import sys

checks = [
    ["python", "-m", "py_compile", "app.py"],
]

for command in checks:
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    if result.returncode == 0:
        print("App syntax: PASS")
    else:
        print("App syntax: FAIL")
        print(result.stdout)
        sys.exit(1)

# --------------------------------------------------
# 6. TEMPLATE CHECK
# --------------------------------------------------

if dashboard.exists():
    final_html = dashboard.read_text(encoding="utf-8")

    required = [
        DASH_START,
        DASH_END,
        'id="quranSmartRevision"',
        'id="quranRevisionWeakCount"',
        'id="quranRevisionStatus"',
        'id="quranRevisionList"',
    ]

    missing = [
        item for item in required
        if item not in final_html
    ]

    if missing:
        print("Dashboard verification: FAIL")
        for item in missing:
            print("Missing:", item)
        sys.exit(1)

    print("Dashboard Smart Revision: PASS")

# --------------------------------------------------
# 7. ASSET CHECK
# --------------------------------------------------

js_final = JS.read_text(encoding="utf-8")
css_final = CSS.read_text(encoding="utf-8")

if JS_START in js_final and \
   JS_END in js_final and \
   "AIZoneQuranRevision" in js_final:
    print("Revision JS verification: PASS")
else:
    print("Revision JS verification: FAIL")
    sys.exit(1)

if CSS_START in css_final and \
   CSS_END in css_final and \
   ".quran-smart-revision" in css_final:
    print("Revision CSS verification: PASS")
else:
    print("Revision CSS verification: FAIL")
    sys.exit(1)

print()
print("=" * 54)
print(" STEP 22.9 INSTALL FINISHED")
print("=" * 54)
print(" Smart Revision Engine: READY")
print(" Dashboard Revision Panel: READY")
print(" Quiz results → Weak Lessons: READY")
print(" No lesson content overwritten")
print(" NO GITHUB PUSH")
print("=" * 54)
