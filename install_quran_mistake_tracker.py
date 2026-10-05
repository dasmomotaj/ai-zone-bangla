from pathlib import Path
import shutil
import re
import subprocess
import sys

ROOT = Path(".")
STATIC = ROOT / "static"
JS = STATIC / "quran-progress.js"
CSS = STATIC / "quran-progress.css"

print("=" * 60)
print(" AI Zone বাংলা — Quran Per-Question Mistake Tracker")
print(" Session 22 — Step 22.11")
print("=" * 60)

# --------------------------------------------------
# 1. BACKUP
# --------------------------------------------------

for path in [JS, CSS]:
    if path.exists():
        backup = path.with_name(
            path.name + ".before-session22-step22-11"
        )
        if not backup.exists():
            shutil.copy2(path, backup)
            print(f"Backup created: {backup}")

# --------------------------------------------------
# 2. JAVASCRIPT
# --------------------------------------------------

JS_START = "// AI-ZONE-QURAN-MISTAKE-TRACKER-JS-START"
JS_END = "// AI-ZONE-QURAN-MISTAKE-TRACKER-JS-END"

tracker_js = r'''
// AI-ZONE-QURAN-MISTAKE-TRACKER-JS-START
(function () {
    "use strict";

    const TOTAL = 20;

    const QUIZ_KEY =
        "ai_zone_quran_quiz_v1";

    const MISTAKE_KEY =
        "ai_zone_quran_mistakes_v1";

    function readJSON(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            return raw ? JSON.parse(raw) : fallback;
        } catch (e) {
            return fallback;
        }
    }

    function writeJSON(key, value) {
        try {
            localStorage.setItem(
                key,
                JSON.stringify(value)
            );
            return true;
        } catch (e) {
            return false;
        }
    }

    function lessonIdOf(item) {
        if (!item || typeof item !== "object") {
            return null;
        }

        const value =
            item.lessonId ??
            item.lesson ??
            item.lesson_id;

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

    function questionIdOf(item, index) {
        if (!item || typeof item !== "object") {
            return "q-" + String(index + 1);
        }

        const value =
            item.questionId ??
            item.question_id ??
            item.qid ??
            item.id;

        if (
            value !== undefined &&
            value !== null &&
            String(value).trim()
        ) {
            return String(value);
        }

        return "q-" + String(index + 1);
    }

    function isWrong(item) {
        if (!item || typeof item !== "object") {
            return false;
        }

        if (
            item.correct === false ||
            item.isCorrect === false ||
            item.is_correct === false ||
            item.correctAnswer === false
        ) {
            return true;
        }

        if (
            item.correct === true ||
            item.isCorrect === true ||
            item.is_correct === true
        ) {
            return false;
        }

        if (
            item.selectedAnswer !== undefined &&
            item.correctAnswer !== undefined
        ) {
            return String(item.selectedAnswer) !==
                   String(item.correctAnswer);
        }

        if (
            item.selected !== undefined &&
            item.correct !== undefined &&
            typeof item.correct !== "boolean"
        ) {
            return String(item.selected) !==
                   String(item.correct);
        }

        return false;
    }

    function extractQuestionResults(data) {
        const output = [];

        function inspectCollection(
            collection,
            lessonFallback
        ) {
            if (!Array.isArray(collection)) {
                return;
            }

            collection.forEach(function (item, index) {
                if (!item || typeof item !== "object") {
                    return;
                }

                const lessonId =
                    lessonIdOf(item) ||
                    lessonFallback;

                if (!lessonId) {
                    return;
                }

                output.push({
                    lessonId: lessonId,
                    questionId:
                        questionIdOf(item, index),
                    wrong: isWrong(item),
                    question:
                        String(
                            item.question ??
                            item.text ??
                            item.prompt ??
                            ""
                        ).trim(),
                    timestamp:
                        Number(
                            item.timestamp ??
                            item.completedAt ??
                            item.createdAt ??
                            Date.now()
                        ) || Date.now()
                });
            });
        }

        if (Array.isArray(data)) {
            data.forEach(function (item) {
                if (!item || typeof item !== "object") {
                    return;
                }

                const lessonId = lessonIdOf(item);

                if (
                    Array.isArray(item.questions)
                ) {
                    inspectCollection(
                        item.questions,
                        lessonId
                    );
                }

                if (
                    Array.isArray(item.answers)
                ) {
                    inspectCollection(
                        item.answers,
                        lessonId
                    );
                }

                if (
                    Array.isArray(item.results)
                ) {
                    inspectCollection(
                        item.results,
                        lessonId
                    );
                }
            });
        }

        if (
            data &&
            typeof data === "object" &&
            Array.isArray(data.results)
        ) {
            data.results.forEach(function (item) {
                if (!item || typeof item !== "object") {
                    return;
                }

                const lessonId = lessonIdOf(item);

                if (Array.isArray(item.questions)) {
                    inspectCollection(
                        item.questions,
                        lessonId
                    );
                }

                if (Array.isArray(item.answers)) {
                    inspectCollection(
                        item.answers,
                        lessonId
                    );
            });
        }

        return output;
    }

    function buildMistakes() {
        const quizData =
            readJSON(QUIZ_KEY, {});

        const previous =
            readJSON(MISTAKE_KEY, {});

        const mistakes =
            previous &&
            typeof previous === "object" &&
            previous.questions
                ? previous.questions
                : {};

        const results =
            extractQuestionResults(quizData);

        results.forEach(function (item) {
            const key =
                String(item.lessonId) +
                ":" +
                String(item.questionId);

            if (!mistakes[key]) {
                mistakes[key] = {
                    lessonId: item.lessonId,
                    questionId: item.questionId,
                    question: item.question,
                    wrongCount: 0,
                    correctCount: 0,
                    lastResult: null,
                    lastAttempt: 0
                };
            }

            if (item.question) {
                mistakes[key].question =
                    item.question;
            }

            if (item.wrong) {
                mistakes[key].wrongCount += 1;
                mistakes[key].lastResult = "wrong";
            } else {
                mistakes[key].correctCount += 1;
                mistakes[key].lastResult = "correct";
            }

            mistakes[key].lastAttempt =
                item.timestamp;
        });

        const weak = Object.values(mistakes)
            .filter(function (item) {
                return (
                    item.wrongCount > 0 &&
                    item.lastResult === "wrong"
                );
            })
            .sort(function (a, b) {
                if (
                    a.wrongCount !==
                    b.wrongCount
                ) {
                    return (
                        b.wrongCount -
                        a.wrongCount
                    );
                }

                return (
                    a.lessonId -
                    b.lessonId
                );
            });

        const data = {
            updatedAt: Date.now(),
            totalTracked:
                Object.keys(mistakes).length,
            weakQuestions: weak.length,
            questions: mistakes,
            queue: weak
        };

        writeJSON(MISTAKE_KEY, data);

        return data;
    }

    function render() {
        const panel =
            document.getElementById(
                "quranMistakeTracker"
            );

        if (!panel) {
            return;
        }

        const data = buildMistakes();

        const count =
            document.getElementById(
                "quranMistakeCount"
            );

        const list =
            document.getElementById(
                "quranMistakeList"
            );

        const status =
            document.getElementById(
                "quranMistakeStatus"
            );

        if (count) {
            count.textContent =
                String(data.weakQuestions);
        }

        if (status) {
            status.textContent =
                data.weakQuestions === 0
                    ? "এখনও কোনো প্রশ্নের ভুল Revision দরকার নেই।"
                    : "যে প্রশ্নগুলোতে ভুল হচ্ছে সেগুলো Revision-এর জন্য রাখা হয়েছে।";
        }

        if (!list) {
            return;
        }

        if (data.queue.length === 0) {
            list.innerHTML =
                '<div class="quran-mistake-empty">' +
                '🎉 এখনো কোনো tracked mistake নেই।' +
                '</div>';
            return;
        }

        list.innerHTML =
            data.queue.slice(0, 10).map(
                function (item) {

                    const questionText =
                        item.question
                            ? item.question
                            : "Question " +
                              item.questionId;

                    return (
                        '<div class="quran-mistake-item">' +

                            '<div>' +
                                '<div class="quran-mistake-title">' +
                                    'Lesson ' +
                                    item.lessonId +
                                '</div>' +

                                '<div class="quran-mistake-question">' +
                                    questionText +
                                '</div>' +

                                '<div class="quran-mistake-count">' +
                                    'ভুল: ' +
                                    item.wrongCount +
                                    ' বার' +
                                '</div>' +
                            '</div>' +

                            '<a ' +
                              'class="quran-mistake-btn" ' +
                              'href="/quran/lesson/' +
                              item.lessonId +
                            '">' +
                                'Practice →' +
                            '</a>' +

                        '</div>'
                    );
                }
            ).join("");
    }

    window.AIZoneQuranMistakeTracker = {
        refresh: render,
        rebuild: buildMistakes,
        getData: buildMistakes
    };

    document.addEventListener(
        "DOMContentLoaded",
        render
    );

    window.addEventListener(
        "storage",
        function (event) {
            if (
                event.key === QUIZ_KEY ||
                event.key === MISTAKE_KEY
            ) {
                render();
            }
        }
    );

})();
// AI-ZONE-QURAN-MISTAKE-TRACKER-JS-END
'''

if not JS.exists():
    print("ERROR: quran-progress.js not found")
    sys.exit(1)

js = JS.read_text(encoding="utf-8")

pattern = re.compile(
    re.escape(JS_START) +
    r".*?" +
    re.escape(JS_END),
    re.DOTALL
)

js = pattern.sub("", js).rstrip()

JS.write_text(
    js + "\n\n" + tracker_js,
    encoding="utf-8"
)

print("Mistake Tracker JS: INSTALLED")

# --------------------------------------------------
# 3. CSS
# --------------------------------------------------

CSS_START = "/* AI-ZONE-QURAN-MISTAKE-TRACKER-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-MISTAKE-TRACKER-CSS-END */"

tracker_css = r'''
/* AI-ZONE-QURAN-MISTAKE-TRACKER-CSS-START */

.quran-mistake-tracker {
    margin-top: 18px;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(255, 100, 100, 0.20);
    background: rgba(255, 255, 255, 0.025);
}

.quran-mistake-summary {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 14px 0;
}

.quran-mistake-number {
    font-size: 1.7rem;
    font-weight: 900;
}

.quran-mistake-label {
    opacity: 0.70;
    font-size: 0.82rem;
}

.quran-mistake-list {
    display: grid;
    gap: 10px;
}

.quran-mistake-item {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    gap: 12px;
    padding: 14px;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.quran-mistake-title {
    font-weight: 850;
}

.quran-mistake-question {
    margin-top: 5px;
    font-size: 0.88rem;
    opacity: 0.82;
}

.quran-mistake-count {
    margin-top: 6px;
    font-size: 0.76rem;
    opacity: 0.62;
}

.quran-mistake-btn {
    padding: 9px 12px;
    border-radius: 11px;
    text-decoration: none;
    font-weight: 750;
    border: 1px solid rgba(255, 100, 100, 0.22);
    background: rgba(255, 100, 100, 0.08);
}

.quran-mistake-empty {
    padding: 15px;
    border-radius: 14px;
    text-align: center;
    opacity: 0.75;
}

@media (max-width: 620px) {
    .quran-mistake-item {
        grid-template-columns: 1fr;
    }

    .quran-mistake-btn {
        width: 100%;
        text-align: center;
    }
}

/* AI-ZONE-QURAN-MISTAKE-TRACKER-CSS-END */
'''

css = CSS.read_text(encoding="utf-8")

pattern = re.compile(
    re.escape(CSS_START) +
    r".*?" +
    re.escape(CSS_END),
    re.DOTALL
)

css = pattern.sub("", css).rstrip()

CSS.write_text(
    css + "\n\n" + tracker_css,
    encoding="utf-8"
)

print("Mistake Tracker CSS: INSTALLED")

# --------------------------------------------------
# 4. DASHBOARD PANEL
# --------------------------------------------------

DASH = ROOT / "templates" / "quran.html"

DASH_START = "<!-- AI-ZONE-QURAN-MISTAKE-TRACKER-START -->"
DASH_END = "<!-- AI-ZONE-QURAN-MISTAKE-TRACKER-END -->"

panel = r'''
<!-- AI-ZONE-QURAN-MISTAKE-TRACKER-START -->

<section
    class="quran-mistake-tracker"
    id="quranMistakeTracker"
>

    <h2 class="revision-title">
        🧠 Mistake Tracker
    </h2>

    <div class="quran-mistake-summary">

        <div
            class="quran-mistake-number"
            id="quranMistakeCount"
        >0</div>

        <div class="quran-mistake-label">
            Weak Questions
        </div>

    </div>

    <p
        class="revision-status"
        id="quranMistakeStatus"
    >
        Mistake Tracker প্রস্তুত হচ্ছে…
    </p>

    <div
        class="quran-mistake-list"
        id="quranMistakeList"
    >
        <div class="quran-mistake-empty">
            Mistake data প্রস্তুত হচ্ছে…
        </div>
    </div>

</section>

<script>
document.addEventListener("DOMContentLoaded", function () {
    if (window.AIZoneQuranMistakeTracker) {
        window.AIZoneQuranMistakeTracker.refresh();
    }
});
</script>

<!-- AI-ZONE-QURAN-MISTAKE-TRACKER-END -->
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

pos = html.lower().rfind("</body>")

if pos != -1:
    html = (
        html[:pos]
        + "\n"
        + panel
        + "\n"
        + html[pos:]
    )
else:
    html += "\n" + panel

DASH.write_text(html, encoding="utf-8")

print("Dashboard Mistake Tracker Panel: INSTALLED")

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
# 6. FINAL VERIFICATION
# --------------------------------------------------

js_final = JS.read_text(encoding="utf-8")
css_final = CSS.read_text(encoding="utf-8")
dash_final = DASH.read_text(encoding="utf-8")

checks = [
    (
        "Mistake Tracker JS",
        JS_START in js_final
        and JS_END in js_final
        and "AIZoneQuranMistakeTracker"
            in js_final
        and "ai_zone_quran_mistakes_v1"
            in js_final
    ),
    (
        "Mistake Tracker CSS",
        CSS_START in css_final
        and CSS_END in css_final
        and ".quran-mistake-tracker"
            in css_final
    ),
    (
        "Dashboard Panel",
        DASH_START in dash_final
        and DASH_END in dash_final
        and 'id="quranMistakeTracker"'
            in dash_final
    ),
]

for name, ok in checks:
    print(
        f"{name}: "
        f"{'PASS' if ok else 'FAIL'}"
    )

    if not ok:
        sys.exit(1)

print()
print("=" * 60)
print(" STEP 22.11 INSTALL FINISHED")
print("=" * 60)
print(" Per-Question Mistake Tracker: READY")
print(" Weak Question Queue: READY")
print(" Mistake Count Tracking: READY")
print(" Existing Quiz Data Preserved")
print(" Existing Lesson Content Preserved")
print(" NO GITHUB PUSH")
print("=" * 60)
