from pathlib import Path
import shutil
import re
import subprocess
import sys

ROOT = Path(".")
STATIC = ROOT / "static"
JS = STATIC / "quran-progress.js"
CSS = STATIC / "quran-progress.css"

print("=" * 58)
print(" AI Zone বাংলা — Quran Revision Priority Engine")
print(" Session 22 — Step 22.10")
print("=" * 58)

# --------------------------------------------------
# 1. BACKUP
# --------------------------------------------------

for path in [JS, CSS]:
    if path.exists():
        backup = path.with_name(
            path.name + ".before-session22-step22-10"
        )
        if not backup.exists():
            shutil.copy2(path, backup)
            print(f"Backup created: {backup}")

# --------------------------------------------------
# 2. JAVASCRIPT
# --------------------------------------------------

JS_START = "// AI-ZONE-QURAN-REVISION-PRIORITY-JS-START"
JS_END = "// AI-ZONE-QURAN-REVISION-PRIORITY-JS-END"

priority_js = r'''
// AI-ZONE-QURAN-REVISION-PRIORITY-JS-START
(function () {
    "use strict";

    const TOTAL = 20;
    const QUIZ_KEY = "ai_zone_quran_quiz_v1";
    const REVISION_KEY = "ai_zone_quran_revision_v1";
    const PRIORITY_KEY = "ai_zone_quran_revision_priority_v1";

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

        if (Array.isArray(data)) {
            return data;
        }

        if (data && Array.isArray(data.results)) {
            return data.results;
        }

        return [];
    }

    function getLessonId(item) {
        const value =
            item.lessonId ??
            item.lesson ??
            item.lesson_id ??
            item.id;

        const id = Number(value);

        if (
            Number.isInteger(id) &&
            id >= 1 &&
            id <= TOTAL
        ) {
            return id;
        }

        return null;
    }

    function getScore(item) {
        const value =
            item.score ??
            item.percent ??
            item.percentage ??
            item.result;

        const score = Number(value);

        return Number.isFinite(score)
            ? Math.max(0, Math.min(100, score))
            : null;
    }

    function buildPriorityQueue() {
        const results = getQuizData();
        const latest = {};

        for (const item of results) {
            if (!item || typeof item !== "object") {
                continue;
            }

            const lessonId = getLessonId(item);
            const score = getScore(item);

            if (lessonId === null || score === null) {
                continue;
            }

            const timestamp =
                Number(
                    item.updatedAt ??
                    item.completedAt ??
                    item.timestamp ??
                    item.createdAt ??
                    0
                ) || 0;

            if (
                !latest[lessonId] ||
                timestamp >= latest[lessonId].timestamp
            ) {
                latest[lessonId] = {
                    lessonId: lessonId,
                    score: score,
                    timestamp: timestamp
                };
            }
        }

        const queue = Object.values(latest)
            .filter(item => item.score < 70)
            .map(item => {
                let priority = "LOW";
                let label = "সাধারণ Revision";

                if (item.score < 40) {
                    priority = "HIGH";
                    label = "জরুরি Revision";
                } else if (item.score < 55) {
                    priority = "MEDIUM";
                    label = "গুরুত্বপূর্ণ Revision";
                }

                return {
                    lessonId: item.lessonId,
                    score: item.score,
                    priority: priority,
                    label: label,
                    timestamp: item.timestamp
                };
            })
            .sort(function (a, b) {
                if (a.score !== b.score) {
                    return a.score - b.score;
                }

                return a.lessonId - b.lessonId;
            });

        const data = {
            updatedAt: Date.now(),
            totalWeak: queue.length,
            high: queue.filter(
                item => item.priority === "HIGH"
            ).length,
            medium: queue.filter(
                item => item.priority === "MEDIUM"
            ).length,
            low: queue.filter(
                item => item.priority === "LOW"
            ).length,
            queue: queue
        };

        try {
            localStorage.setItem(
                PRIORITY_KEY,
                JSON.stringify(data)
            );
        } catch (e) {
            // Safe fallback when storage is unavailable.
        }

        return data;
    }

    function renderPriority() {
        const panel = document.getElementById(
            "quranRevisionPriority"
        );

        if (!panel) {
            return;
        }

        const data = buildPriorityQueue();

        const high = document.getElementById(
            "quranRevisionHigh"
        );

        const medium = document.getElementById(
            "quranRevisionMedium"
        );

        const low = document.getElementById(
            "quranRevisionLow"
        );

        const list = document.getElementById(
            "quranRevisionPriorityList"
        );

        const status = document.getElementById(
            "quranRevisionPriorityStatus"
        );

        if (high) {
            high.textContent = String(data.high);
        }

        if (medium) {
            medium.textContent = String(data.medium);
        }

        if (low) {
            low.textContent = String(data.low);
        }

        if (status) {
            if (data.totalWeak === 0) {
                status.textContent =
                    "এখনও কোনো Priority Revision প্রয়োজন নেই।";
            } else {
                status.textContent =
                    "কম score-এর Lesson আগে Revision করার জন্য সাজানো হয়েছে।";
            }
        }

        if (list) {
            if (data.queue.length === 0) {
                list.innerHTML =
                    '<div class="revision-priority-empty">' +
                    '🎉 সব tracked Lesson আপাতত ভালো অবস্থায় আছে।' +
                    '</div>';
                return;
            }

            list.innerHTML = data.queue.map(function (item) {
                const badgeClass =
                    item.priority.toLowerCase();

                return (
                    '<div class="revision-priority-item">' +

                        '<div class="revision-priority-main">' +
                            '<div class="revision-priority-title">' +
                                'Lesson ' +
                                item.lessonId +
                            '</div>' +

                            '<div class="revision-priority-score">' +
                                'Quiz Score: ' +
                                item.score +
                                '%' +
                            '</div>' +
                        '</div>' +

                        '<span class="revision-priority-badge ' +
                            badgeClass +
                        '">' +
                            item.label +
                        '</span>' +

                        '<a class="revision-priority-btn" ' +
                           'href="/quran/lesson/' +
                           item.lessonId +
                        '">' +
                            'Revision →' +
                        '</a>' +

                    '</div>'
                );
            }).join("");
        }
    }

    window.AIZoneQuranRevisionPriority = {
        refresh: renderPriority,
        rebuild: buildPriorityQueue,
        getQueue: buildPriorityQueue
    };

    document.addEventListener(
        "DOMContentLoaded",
        renderPriority
    );

    window.addEventListener(
        "storage",
        function (event) {
            if (
                event.key === QUIZ_KEY ||
                event.key === REVISION_KEY
            ) {
                renderPriority();
            }
        }
    );

})();
// AI-ZONE-QURAN-REVISION-PRIORITY-JS-END
'''

if not JS.exists():
    print("ERROR: quran-progress.js not found")
    sys.exit(1)

js_text = JS.read_text(encoding="utf-8")

pattern = re.compile(
    re.escape(JS_START) +
    r".*?" +
    re.escape(JS_END),
    re.DOTALL
)

js_text = pattern.sub("", js_text).rstrip() + "\n"

JS.write_text(
    js_text + "\n" + priority_js + "\n",
    encoding="utf-8"
)

print("Revision Priority JS: INSTALLED")

# --------------------------------------------------
# 3. CSS
# --------------------------------------------------

CSS_START = "/* AI-ZONE-QURAN-REVISION-PRIORITY-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-REVISION-PRIORITY-CSS-END */"

priority_css = r'''
/* AI-ZONE-QURAN-REVISION-PRIORITY-CSS-START */

.quran-revision-priority {
    margin: 20px 0 0;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(255, 205, 90, 0.22);
    background: rgba(255, 255, 255, 0.025);
}

.revision-priority-summary {
    display: grid;
    grid-template-columns:
        repeat(3, minmax(0, 1fr));
    gap: 10px;
    margin: 16px 0;
}

.revision-priority-stat {
    padding: 13px;
    border-radius: 15px;
    text-align: center;
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.revision-priority-stat strong {
    display: block;
    font-size: 1.25rem;
}

.revision-priority-stat span {
    display: block;
    margin-top: 4px;
    font-size: 0.78rem;
    opacity: 0.70;
}

.revision-priority-list {
    display: grid;
    gap: 10px;
}

.revision-priority-item {
    display: grid;
    grid-template-columns:
        1fr auto auto;
    align-items: center;
    gap: 12px;
    padding: 14px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.revision-priority-title {
    font-weight: 800;
}

.revision-priority-score {
    margin-top: 4px;
    font-size: 0.84rem;
    opacity: 0.70;
}

.revision-priority-badge {
    padding: 7px 10px;
    border-radius: 10px;
    font-size: 0.75rem;
    font-weight: 800;
    white-space: nowrap;
    border: 1px solid rgba(255, 255, 255, 0.10);
}

.revision-priority-badge.high {
    background: rgba(255, 90, 90, 0.13);
}

.revision-priority-badge.medium {
    background: rgba(255, 185, 70, 0.13);
}

.revision-priority-badge.low {
    background: rgba(90, 220, 255, 0.10);
}

.revision-priority-btn {
    padding: 9px 12px;
    border-radius: 11px;
    text-decoration: none;
    font-weight: 700;
    border: 1px solid rgba(90, 220, 255, 0.24);
    background: rgba(90, 220, 255, 0.08);
}

.revision-priority-empty {
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    opacity: 0.78;
}

@media (max-width: 620px) {
    .revision-priority-summary {
        grid-template-columns: 1fr 1fr 1fr;
    }

    .revision-priority-item {
        grid-template-columns: 1fr;
    }

    .revision-priority-badge,
    .revision-priority-btn {
        width: 100%;
        text-align: center;
    }
}

/* AI-ZONE-QURAN-REVISION-PRIORITY-CSS-END */
'''

css_text = CSS.read_text(encoding="utf-8")

pattern = re.compile(
    re.escape(CSS_START) +
    r".*?" +
    re.escape(CSS_END),
    re.DOTALL
)

css_text = pattern.sub("", css_text).rstrip() + "\n"

CSS.write_text(
    css_text + "\n" + priority_css + "\n",
    encoding="utf-8"
)

print("Revision Priority CSS: INSTALLED")

# --------------------------------------------------
# 4. DASHBOARD PANEL
# --------------------------------------------------

DASH = ROOT / "templates" / "quran.html"

DASH_START = "<!-- AI-ZONE-QURAN-REVISION-PRIORITY-START -->"
DASH_END = "<!-- AI-ZONE-QURAN-REVISION-PRIORITY-END -->"

panel = r'''
<!-- AI-ZONE-QURAN-REVISION-PRIORITY-START -->

<section
    class="quran-revision-priority"
    id="quranRevisionPriority"
>

    <div class="revision-header">
        <h2 class="revision-title">
            🎯 Revision Priority
        </h2>
    </div>

    <p
        class="revision-status"
        id="quranRevisionPriorityStatus"
    >
        Revision priority প্রস্তুত হচ্ছে…
    </p>

    <div class="revision-priority-summary">

        <div class="revision-priority-stat">
            <strong id="quranRevisionHigh">0</strong>
            <span>High</span>
        </div>

        <div class="revision-priority-stat">
            <strong id="quranRevisionMedium">0</strong>
            <span>Medium</span>
        </div>

        <div class="revision-priority-stat">
            <strong id="quranRevisionLow">0</strong>
            <span>Low</span>
        </div>

    </div>

    <div
        class="revision-priority-list"
        id="quranRevisionPriorityList"
    >
        <div class="revision-priority-empty">
            Revision queue প্রস্তুত হচ্ছে…
        </div>
    </div>

</section>

<script>
document.addEventListener("DOMContentLoaded", function () {
    if (window.AIZoneQuranRevisionPriority) {
        window.AIZoneQuranRevisionPriority.refresh();
    }
});
</script>

<!-- AI-ZONE-QURAN-REVISION-PRIORITY-END -->
'''

if not DASH.exists():
    print("ERROR: templates/quran.html not found")
    sys.exit(1)

html = DASH.read_text(encoding="utf-8")

pattern = re.compile(
    re.escape(DASH_START) +
    r".*?" +
    re.escape(DASH_END),
    re.DOTALL
)

html = pattern.sub("", html).rstrip()

body_pos = html.lower().rfind("</body>")

if body_pos != -1:
    html = (
        html[:body_pos]
        + "\n"
        + panel
        + "\n"
        + html[body_pos:]
    )
else:
    html += "\n" + panel

DASH.write_text(html, encoding="utf-8")

print("Dashboard Priority Panel: INSTALLED")

# --------------------------------------------------
# 5. PYTHON SYNTAX
# --------------------------------------------------

result = subprocess.run(
    ["python", "-m", "py_compile", "app.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

if result.returncode != 0:
    print("App syntax: FAIL")
    print(result.stdout)
    sys.exit(1)

print("App syntax: PASS")

# --------------------------------------------------
# 6. VERIFY
# --------------------------------------------------

js_final = JS.read_text(encoding="utf-8")
css_final = CSS.read_text(encoding="utf-8")
dash_final = DASH.read_text(encoding="utf-8")

checks = [
    (
        "Priority JS",
        JS_START in js_final
        and JS_END in js_final
        and "AIZoneQuranRevisionPriority" in js_final
    ),
    (
        "Priority CSS",
        CSS_START in css_final
        and CSS_END in css_final
        and ".quran-revision-priority" in css_final
    ),
    (
        "Dashboard Panel",
        DASH_START in dash_final
        and DASH_END in dash_final
        and 'id="quranRevisionPriority"' in dash_final
    ),
]

for name, ok in checks:
    print(f"{name}: {'PASS' if ok else 'FAIL'}")

    if not ok:
        sys.exit(1)

print()
print("=" * 58)
print(" STEP 22.10 INSTALL FINISHED")
print("=" * 58)
print(" Priority Engine: READY")
print(" High / Medium / Low: READY")
print(" Weak Lessons sorted by score: READY")
print(" Existing content preserved")
print(" NO GITHUB PUSH")
print("=" * 58)
