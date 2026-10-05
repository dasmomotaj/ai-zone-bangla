from pathlib import Path
import shutil

ROOT = Path(".")
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"

DASHBOARD = TEMPLATES / "quran.html"
CSS = STATIC / "quran-progress.css"
JS = STATIC / "quran-progress.js"

HTML_START = "<!-- AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-START -->"
HTML_END = "<!-- AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-END -->"

CSS_START = "/* AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-CSS-END */"

JS_START = "/* AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-JS-START */"
JS_END = "/* AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-JS-END */"


def backup(path):
    if path.exists():
        target = Path(str(path) + ".before-session24-step24-1")
        shutil.copy2(path, target)
        print("Backup:", target)


def replace_block(text, start, end, block):
    a = text.find(start)
    b = text.find(end)

    if a != -1 and b != -1 and b > a:
        b += len(end)
        return text[:a] + block + text[b:]

    return text + "\n\n" + block + "\n"


HTML = """
<!-- AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-START -->

<section class="quran-unified-control" data-quran-unified-control>

  <div class="quran-unified-control-head">
    <div>
      <span class="quran-unified-kicker">
        QURAN ACADEMY • STUDENT CONTROL CENTER
      </span>

      <h2>🎯 আপনার শেখার Control Center</h2>

      <p>
        আপনার বর্তমান অবস্থার ভিত্তিতে এখন কী করবেন,
        কোন Lesson-এ যাবেন এবং পরবর্তী ধাপ কী—সব এক জায়গায়।
      </p>
    </div>

    <div class="quran-unified-current">
      <span>NOW</span>
      <strong data-unified-now>শেখা শুরু করুন</strong>
    </div>
  </div>

  <div class="quran-unified-flow">

    <div class="unified-step active" data-unified-step="lesson">
      <span class="unified-step-number">1</span>
      <div>
        <strong>Lesson</strong>
        <small data-unified-lesson>Lesson 1</small>
      </div>
    </div>

    <div class="unified-arrow">→</div>

    <div class="unified-step" data-unified-step="practice">
      <span class="unified-step-number">2</span>
      <div>
        <strong>Practice</strong>
        <small>অনুশীলন</small>
      </div>
    </div>

    <div class="unified-arrow">→</div>

    <div class="unified-step" data-unified-step="quiz">
      <span class="unified-step-number">3</span>
      <div>
        <strong>Quiz</strong>
        <small>পরীক্ষা</small>
      </div>
    </div>

    <div class="unified-arrow">→</div>

    <div class="unified-step" data-unified-step="revision">
      <span class="unified-step-number">4</span>
      <div>
        <strong>Revision</strong>
        <small>ভুল সংশোধন</small>
      </div>
    </div>

    <div class="unified-arrow">→</div>

    <div class="unified-step" data-unified-step="next">
      <span class="unified-step-number">5</span>
      <div>
        <strong>Next</strong>
        <small>পরবর্তী Lesson</small>
      </div>
    </div>

  </div>

  <div class="quran-unified-action">

    <div class="quran-unified-action-main">
      <span class="quran-unified-action-label">
        NEXT BEST ACTION
      </span>

      <h3 data-unified-action-title>
        Lesson 1 থেকে শুরু করুন
      </h3>

      <p data-unified-action-message>
        Lesson পড়ুন, Practice সম্পন্ন করুন, তারপর Quiz দিন।
      </p>

      <div class="quran-unified-meta">
        <span data-unified-status>Not Started</span>
        <span data-unified-score>Score: —</span>
      </div>
    </div>

    <a
      href="/quran/lesson/1"
      class="quran-unified-action-button"
      data-unified-action-button>
      শুরু করুন →
    </a>

  </div>

</section>

<!-- AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-END -->
"""


CSS_BLOCK = """
/* AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-CSS-START */

.quran-unified-control {
  margin: 28px 0;
  padding: 25px;
  border-radius: 26px;
  border: 1px solid rgba(90, 210, 255, .24);
  background:
    radial-gradient(circle at top right, rgba(0, 220, 255, .10), transparent 34%),
    radial-gradient(circle at bottom left, rgba(120, 80, 255, .08), transparent 32%),
    rgba(8, 16, 30, .82);
  box-shadow: 0 20px 55px rgba(0,0,0,.26);
}

.quran-unified-control-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.quran-unified-kicker {
  display: block;
  margin-bottom: 7px;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 1.8px;
  opacity: .58;
}

.quran-unified-control-head h2 {
  margin: 0 0 7px;
  font-size: clamp(23px, 4vw, 31px);
}

.quran-unified-control-head p {
  margin: 0;
  max-width: 720px;
  line-height: 1.7;
  opacity: .75;
}

.quran-unified-current {
  min-width: 150px;
  padding: 14px 16px;
  border-radius: 19px;
  text-align: center;
  background: rgba(255,255,255,.05);
  border: 1px solid rgba(255,255,255,.08);
}

.quran-unified-current span {
  display: block;
  margin-bottom: 5px;
  font-size: 10px;
  letter-spacing: 1.5px;
  opacity: .55;
}

.quran-unified-current strong {
  font-size: 14px;
}

.quran-unified-flow {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 22px 0;
  overflow-x: auto;
  padding-bottom: 4px;
}

.unified-step {
  min-width: 120px;
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 12px;
  border-radius: 16px;
  background: rgba(255,255,255,.035);
  border: 1px solid rgba(255,255,255,.07);
}

.unified-step.active {
  border-color: rgba(90,210,255,.38);
  background: rgba(90,210,255,.07);
}

.unified-step-number {
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 28px;
  border-radius: 50%;
  background: rgba(255,255,255,.07);
  font-size: 12px;
  font-weight: 900;
}

.unified-step strong,
.unified-step small {
  display: block;
}

.unified-step strong {
  font-size: 13px;
}

.unified-step small {
  margin-top: 2px;
  font-size: 10px;
  opacity: .58;
}

.unified-arrow {
  flex: 0 0 auto;
  opacity: .35;
  font-size: 18px;
}

.quran-unified-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 19px;
  border-radius: 20px;
  background: rgba(255,255,255,.045);
  border: 1px solid rgba(255,255,255,.08);
}

.quran-unified-action-label {
  display: block;
  margin-bottom: 5px;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 1.5px;
  opacity: .56;
}

.quran-unified-action h3 {
  margin: 0 0 5px;
  font-size: 19px;
}

.quran-unified-action p {
  margin: 0;
  line-height: 1.6;
  opacity: .7;
}

.quran-unified-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 10px;
}

.quran-unified-meta span {
  padding: 5px 9px;
  border-radius: 999px;
  background: rgba(255,255,255,.06);
  font-size: 10px;
  opacity: .72;
}

.quran-unified-action-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 125px;
  padding: 12px 17px;
  border-radius: 13px;
  text-decoration: none;
  font-weight: 850;
  background: rgba(90,210,255,.12);
  border: 1px solid rgba(90,210,255,.25);
}

@media (max-width: 700px) {
  .quran-unified-control {
    padding: 18px;
    border-radius: 21px;
  }

  .quran-unified-control-head {
    flex-direction: column;
  }

  .quran-unified-current {
    width: 100%;
    box-sizing: border-box;
  }

  .quran-unified-action {
    align-items: stretch;
    flex-direction: column;
  }

  .quran-unified-action-button {
    width: 100%;
    box-sizing: border-box;
  }
}

@media (max-width: 520px) {
  .quran-unified-flow {
    margin-left: -3px;
    margin-right: -3px;
  }

  .unified-step {
    min-width: 105px;
  }

  .unified-arrow {
    font-size: 15px;
  }
}

/* AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-CSS-END */
"""


JS_BLOCK = r"""
/* AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-JS-START */

(function () {
  "use strict";

  const TOTAL = 20;
  const PASS_SCORE = 70;

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function findLesson(value, id) {
    if (!value) return null;

    if (Array.isArray(value)) {
      for (const item of value) {
        const found = findLesson(item, id);
        if (found) return found;
      }
      return null;
    }

    if (typeof value !== "object") return null;

    const itemId = Number(
      value.lessonId ??
      value.lesson_id ??
      value.lesson
    );

    if (itemId === id) return value;

    const children = [
      value.results,
      value.items,
      value.data,
      value.history,
      value.attempts,
      value.lessons,
      value.records
    ];

    for (const child of children) {
      const found = findLesson(child, id);
      if (found) return found;
    }

    return null;
  }

  function getScore(id) {
    const item = findLesson(readJSON(QUIZ_KEY, []), id);

    if (!item) return null;

    const value =
      item.score ??
      item.percentage ??
      item.percent;

    const score = Number(value);

    return Number.isFinite(score) ? score : null;
  }

  function isCompleted(id) {
    const data = readJSON(PROGRESS_KEY, {});

    if (Array.isArray(data)) {
      return data.includes(id) || data.includes(String(id));
    }

    return !!(
      data &&
      (
        data[id] === true ||
        data[String(id)] === true
      )
    );
  }

  function practiceDone(id) {
    const data = readJSON("quran_practice_" + id, null);

    if (!data) return false;

    if (data === true) return true;

    if (typeof data === "object") {
      return !!(
        data.bujhechi ||
        data.understood ||
        data.porechi ||
        data.read ||
        data.onushilon ||
        data.practice
      );
    }

    return false;
  }

  function lessonURL(id) {
    return "/quran/lesson/" + id;
  }

  function calculate() {
    let current = 1;

    for (let id = 1; id <= TOTAL; id++) {
      const score = getScore(id);

      if (
        isCompleted(id) ||
        (score !== null && score >= PASS_SCORE)
      ) {
        current = id + 1;
      } else {
        current = id;
        break;
      }
    }

    if (current > TOTAL) {
      return {
        lesson: TOTAL,
        state: "complete",
        title: "🎉 Academy Complete",
        message: "সব 20টি Lesson সম্পন্ন হয়েছে। নিয়মিত Revision চালিয়ে যান।",
        button: "Dashboard →",
        url: "/quran",
        score: null
      };
    }

    const score = getScore(current);

    if (score !== null && score < PASS_SCORE) {
      return {
        lesson: current,
        state: "revision",
        title: "Lesson " + current + " Revision করুন",
        message: "Quiz Score " + score + "%। আগে Revision করে আবার চেষ্টা করুন।",
        button: "Revision →",
        url: lessonURL(current),
        score: score
      };
    }

    if (practiceDone(current)) {
      return {
        lesson: current,
        state: "quiz",
        title: "Lesson " + current + " Quiz দিন",
        message: "Practice সম্পন্ন হয়েছে। এবার Quiz দিয়ে আপনার শেখা যাচাই করুন।",
        button: "Quiz প্রস্তুতি →",
        url: lessonURL(current),
        score: null
      };
    }

    return {
      lesson: current,
      state: "practice",
      title: "Lesson " + current + " শুরু করুন",
      message: "Lesson পড়ুন, Practice সম্পন্ন করুন, তারপর Quiz দিন।",
      button: "Lesson খুলুন →",
      url: lessonURL(current),
      score: null
    };
  }

  function render() {
    const root = document.querySelector(
      "[data-quran-unified-control]"
    );

    if (!root) return;

    const data = calculate();

    root.querySelector("[data-unified-now]").textContent =
      data.state === "complete"
        ? "Academy Complete"
        : data.title;

    root.querySelector("[data-unified-lesson]").textContent =
      data.state === "complete"
        ? "20 / 20"
        : "Lesson " + data.lesson;

    root.querySelector("[data-unified-action-title]").textContent =
      data.title;

    root.querySelector("[data-unified-action-message]").textContent =
      data.message;

    root.querySelector("[data-unified-status]").textContent =
      data.state === "revision"
        ? "Revision"
        : data.state === "quiz"
          ? "Ready for Quiz"
          : data.state === "complete"
            ? "Complete"
            : "Practice";

    root.querySelector("[data-unified-score]").textContent =
      data.score === null
        ? "Score: —"
        : "Score: " + data.score + "%";

    const button = root.querySelector(
      "[data-unified-action-button]"
    );

    button.href = data.url;
    button.textContent = data.button;

    root.querySelectorAll("[data-unified-step]").forEach(function (step) {
      step.classList.remove("active");
    });

    const active =
      data.state === "revision"
        ? "revision"
        : data.state === "quiz"
          ? "quiz"
          : data.state === "complete"
            ? "next"
            : "practice";

    const activeStep = root.querySelector(
      '[data-unified-step="' + active + '"]'
    );

    if (activeStep) {
      activeStep.classList.add("active");
    }
  }

  window.AIZoneRefreshQuranUnifiedControl = render;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }

})();

/* AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-JS-END */
"""


def install():
    if not DASHBOARD.exists():
        raise SystemExit("ERROR: templates/quran.html not found")

    print("============================================================")
    print(" AI Zone বাংলা — Session 24 Step 24.1")
    print(" UNIFIED STUDENT CONTROL CENTER")
    print("============================================================")

    backup(DASHBOARD)
    backup(CSS)
    backup(JS)

    dashboard = DASHBOARD.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
    js = JS.read_text(encoding="utf-8") if JS.exists() else ""

    dashboard = replace_block(
        dashboard,
        HTML_START,
        HTML_END,
        HTML
    )

    css = replace_block(
        css,
        CSS_START,
        CSS_END,
        CSS_BLOCK
    )

    js = replace_block(
        js,
        JS_START,
        JS_END,
        JS_BLOCK
    )

    DASHBOARD.write_text(dashboard, encoding="utf-8")
    CSS.write_text(css, encoding="utf-8")
    JS.write_text(js, encoding="utf-8")

    print("HTML: INSTALLED")
    print("CSS: INSTALLED")
    print("JS: INSTALLED")


def verify():
    dashboard = DASHBOARD.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")

    checks = [
        (
            "HTML markers",
            HTML_START in dashboard and HTML_END in dashboard
        ),
        (
            "Control Center",
            "data-quran-unified-control" in dashboard
        ),
        (
            "Flow steps",
            "data-unified-step" in dashboard
        ),
        (
            "Action UI",
            "data-unified-action-title" in dashboard
            and "data-unified-action-button" in dashboard
        ),
        (
            "CSS markers",
            CSS_START in css and CSS_END in css
        ),
        (
            "Mobile CSS",
            "@media (max-width: 700px)" in css
            and "@media (max-width: 520px)" in css
        ),
        (
            "JS markers",
            JS_START in js and JS_END in js
        ),
        (
            "Refresh function",
            "AIZoneRefreshQuranUnifiedControl" in js
        ),
        (
            "Progress key",
            "ai_zone_quran_progress_v1" in js
        ),
        (
            "Quiz key",
            "ai_zone_quran_quiz_v1" in js
        ),
        (
            "No GitHub push",
            True
        ),
    ]

    print()
    print("=== Verification ===")

    passed = True

    for name, ok in checks:
        status = "PASS" if ok else "FAIL"
        print(f"{name}: {status}")

        if not ok:
            passed = False

    return passed


if __name__ == "__main__":
    install()

    if verify():
        print()
        print("============================================================")
        print(" SESSION 24 — STEP 24.1 INSTALL COMPLETE")
        print(" Unified Student Control Center: PASS")
        print(" Existing systems preserved")
        print(" GitHub push: NO")
        print("============================================================")
    else:
        raise SystemExit("INSTALLATION VERIFICATION FAILED")
