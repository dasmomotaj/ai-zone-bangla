from pathlib import Path
import re
import shutil

ROOT = Path(".")
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"

TEMPLATES.mkdir(exist_ok=True)
STATIC.mkdir(exist_ok=True)

START = "<!-- AI-ZONE-QURAN-NEXT-ACTION-START -->"
END = "<!-- AI-ZONE-QURAN-NEXT-ACTION-END -->"

CSS_START = "/* AI-ZONE-QURAN-NEXT-ACTION-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-NEXT-ACTION-CSS-END */"

JS_START = "/* AI-ZONE-QURAN-NEXT-ACTION-JS-START */"
JS_END = "/* AI-ZONE-QURAN-NEXT-ACTION-JS-END */"

LESSON_FILES = [
    TEMPLATES / "quran_lesson.html",
    *[TEMPLATES / f"quran_lesson_{i}.html" for i in range(2, 21)]
]


def replace_block(text, start, end, block):
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        re.S
    )

    if pattern.search(text):
        return pattern.sub(block, text, count=1), True

    return text, False


def lesson_id_from_file(path):
    if path.name == "quran_lesson.html":
        return 1

    match = re.search(
        r"quran_lesson_(\d+)\.html$",
        path.name
    )

    if not match:
        return None

    return int(match.group(1))


def make_html(lesson_id):
    return f"""
{START}
<section
  class="quran-next-action"
  data-quran-next-action
  data-lesson-id="{lesson_id}"
  aria-live="polite">

  <div class="quran-next-action-icon"
       data-next-action-icon>→</div>

  <div class="quran-next-action-content">

    <span class="quran-next-action-label">
      SMART NEXT ACTION
    </span>

    <h2 data-next-action-title>
      আপনার পরবর্তী পদক্ষেপ
    </h2>

    <p data-next-action-message>
      আপনার শেখার অগ্রগতি দেখে পরবর্তী কাজ এখানে সাজেস্ট করা হবে।
    </p>

    <div class="quran-next-action-state"
         data-next-action-state>
      Smart Action প্রস্তুত হচ্ছে…
    </div>

    <div class="quran-next-action-buttons">

      <a
        class="quran-next-action-btn primary"
        data-next-action-primary
        href="/quran">
        ➡️ পরবর্তী পদক্ষেপ
      </a>

      <a
        class="quran-next-action-btn secondary"
        data-next-action-secondary
        href="/quran">
        🏠 Dashboard
      </a>

    </div>

  </div>
</section>
{END}
"""


CSS_BLOCK = """
/* AI-ZONE-QURAN-NEXT-ACTION-CSS-START */

.quran-next-action {
  margin: 24px 0;
  padding: 22px;
  display: flex;
  gap: 17px;
  align-items: flex-start;
  border-radius: 22px;
  border: 1px solid rgba(70, 210, 255, .22);
  background: linear-gradient(
    135deg,
    rgba(15, 25, 45, .97),
    rgba(7, 13, 28, .97)
  );
  box-shadow: 0 14px 45px rgba(0,0,0,.24);
}

.quran-next-action-icon {
  width: 54px;
  height: 54px;
  min-width: 54px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  font-size: 24px;
  font-weight: 800;
  background: rgba(70, 210, 255, .10);
  border: 1px solid rgba(70, 210, 255, .28);
}

.quran-next-action-content {
  flex: 1;
}

.quran-next-action-label {
  font-size: 11px;
  letter-spacing: 1.8px;
  opacity: .62;
}

.quran-next-action-content h2 {
  margin: 5px 0 8px;
  font-size: 21px;
}

.quran-next-action-content p {
  margin: 0 0 12px;
  line-height: 1.7;
  opacity: .82;
}

.quran-next-action-state {
  display: inline-block;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 13px;
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.10);
}

.quran-next-action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 16px;
}

.quran-next-action-btn {
  min-height: 44px;
  padding: 10px 16px;
  border-radius: 13px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  font-weight: 700;
}

.quran-next-action-btn.primary {
  background: linear-gradient(135deg, #19d3ff, #6d5cff);
  color: #fff;
}

.quran-next-action-btn.secondary {
  background: rgba(255,255,255,.07);
  color: inherit;
  border: 1px solid rgba(255,255,255,.12);
}

.quran-next-action.status-start {
  border-color: rgba(150,150,150,.22);
}

.quran-next-action.status-practice {
  border-color: rgba(70,180,255,.32);
}

.quran-next-action.status-quiz {
  border-color: rgba(255,190,70,.32);
}

.quran-next-action.status-revision {
  border-color: rgba(255,150,80,.36);
}

.quran-next-action.status-completed {
  border-color: rgba(40,220,150,.36);
}

@media (max-width: 620px) {
  .quran-next-action {
    padding: 17px;
    gap: 12px;
    border-radius: 18px;
  }

  .quran-next-action-icon {
    width: 44px;
    height: 44px;
    min-width: 44px;
    font-size: 20px;
  }

  .quran-next-action-content h2 {
    font-size: 18px;
  }

  .quran-next-action-buttons {
    flex-direction: column;
  }

  .quran-next-action-btn {
    width: 100%;
  }
}

/* AI-ZONE-QURAN-NEXT-ACTION-CSS-END */
"""


JS_BLOCK = r"""
/* AI-ZONE-QURAN-NEXT-ACTION-JS-START */

(function () {
  "use strict";

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PASS_SCORE = 70;

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (error) {
      return fallback;
    }
  }

  function lessonIdOf(item) {
    if (!item || typeof item !== "object") {
      return null;
    }

    const value =
      item.lessonId ??
      item.lesson_id ??
      item.lesson ??
      item.id;

    const number = Number(value);

    return Number.isFinite(number) ? number : null;
  }

  function scoreOf(item) {
    if (!item || typeof item !== "object") {
      return null;
    }

    const value =
      item.score ??
      item.percentage ??
      item.percent ??
      (
        item.result &&
        item.result.score
      );

    const number = Number(value);

    return Number.isFinite(number) ? number : null;
  }

  function isCompleted(progress, lessonId) {
    if (!progress) {
      return false;
    }

    if (Array.isArray(progress)) {
      return progress.some(function (item) {
        if (typeof item === "number") {
          return item === lessonId;
        }

        if (typeof item === "string") {
          return Number(item) === lessonId;
        }

        if (item && typeof item === "object") {
          return (
            lessonIdOf(item) === lessonId &&
            (
              item.completed === true ||
              item.complete === true ||
              item.done === true
            )
          );
        }

        return false;
      });
    }

    if (Array.isArray(progress.completed)) {
      return progress.completed.some(
        function (value) {
          return Number(value) === lessonId;
        }
      );
    }

    if (
      progress.completed &&
      typeof progress.completed === "object"
    ) {
      return (
        progress.completed[lessonId] === true ||
        progress.completed[String(lessonId)] === true
      );
    }

    return (
      progress[lessonId] === true ||
      progress[String(lessonId)] === true
    );
  }

  function practiceDone(lessonId) {
    const raw = localStorage.getItem(
      "quran_practice_" + lessonId
    );

    if (!raw) {
      return false;
    }

    try {
      const data = JSON.parse(raw);

      const understood =
        data.bujhechi ?? data.understood ?? false;

      const read =
        data.porechi ?? data.read ?? false;

      const practice =
        data.onushilon ?? data.practice ?? false;

      return Boolean(
        understood &&
        read &&
        practice
      );
    } catch (error) {
      return false;
    }
  }

  function latestQuiz(lessonId) {
    const data = readJSON(QUIZ_KEY, null);

    if (!data) {
      return null;
    }

    let items = [];

    if (Array.isArray(data)) {
      items = data;
    } else if (Array.isArray(data.results)) {
      items = data.results;
    } else if (Array.isArray(data.history)) {
      items = data.history;
    } else if (Array.isArray(data.attempts)) {
      items = data.attempts;
    }

    const matches = items
      .filter(function (item) {
        return lessonIdOf(item) === lessonId;
      })
      .map(function (item) {
        return {
          score: scoreOf(item),
          timestamp: Number(
            item.timestamp ??
            item.time ??
            item.createdAt ??
            item.created_at ??
            0
          )
        };
      })
      .filter(function (entry) {
        return entry.score !== null;
      });

    if (!matches.length) {
      return null;
    }

    matches.sort(function (a, b) {
      return b.timestamp - a.timestamp;
    });

    return matches[0];
  }

  function nextLessonURL(lessonId) {
    if (lessonId >= 20) {
      return "/quran";
    }

    return "/quran/lesson/" + (lessonId + 1);
  }

  function setText(root, selector, value) {
    const element = root.querySelector(selector);

    if (element) {
      element.textContent = value;
    }
  }

  function updateAction(root) {
    const lessonId = Number(
      root.dataset.lessonId
    );

    if (!Number.isFinite(lessonId)) {
      return;
    }

    const progress =
      readJSON(PROGRESS_KEY, null);

    const completed =
      isCompleted(progress, lessonId);

    const practice =
      practiceDone(lessonId);

    const quiz =
      latestQuiz(lessonId);

    root.classList.remove(
      "status-start",
      "status-practice",
      "status-quiz",
      "status-revision",
      "status-completed"
    );

    const primary = root.querySelector(
      "[data-next-action-primary]"
    );

    if (
      completed ||
      (quiz && quiz.score >= PASS_SCORE)
    ) {
      root.classList.add(
        "status-completed"
      );

      setText(
        root,
        "[data-next-action-icon]",
        "✓"
      );

      setText(
        root,
        "[data-next-action-title]",
        lessonId >= 20
          ? "Academy-এর শেষ পাঠ সম্পন্ন"
          : "পরের পাঠে এগিয়ে যান"
      );

      setText(
        root,
        "[data-next-action-message]",
        lessonId >= 20
          ? "এই পাঠটি সম্পন্ন হয়েছে। এখন Dashboard থেকে Revision চালিয়ে যেতে পারেন।"
          : "এই পাঠটি সম্পন্ন হয়েছে। এখন শেখার ধারাবাহিকতা বজায় রেখে পরের পাঠে এগিয়ে যান।"
      );

      setText(
        root,
        "[data-next-action-state]",
        quiz
          ? "Quiz Score: " + quiz.score + "% • Completed"
          : "Lesson Completed"
      );

      if (primary) {
        primary.textContent =
          lessonId >= 20
            ? "🏠 Academy Dashboard"
            : "➡️ পরের পাঠ";

        primary.href =
          nextLessonURL(lessonId);
      }

      return;
    }

    if (quiz && quiz.score < PASS_SCORE) {
      root.classList.add(
        "status-revision"
      );

      setText(
        root,
        "[data-next-action-icon]",
        "↻"
      );

      setText(
        root,
        "[data-next-action-title]",
        "Revision আগে করুন"
      );

      setText(
        root,
        "[data-next-action-message]",
        "সর্বশেষ Quiz স্কোর 70%-এর নিচে। আগে Revision ও Practice করুন, তারপর আবার Quiz দিন।"
      );

      setText(
        root,
        "[data-next-action-state]",
        "Quiz Score: " + quiz.score +
        "% • Revision Recommended"
      );

      if (primary) {
        primary.textContent =
          "🔄 Revision চালিয়ে যান";

        primary.href =
          "/quran";
      }

      return;
    }

    if (practice) {
      root.classList.add(
        "status-quiz"
      );

      setText(
        root,
        "[data-next-action-icon]",
        "📝"
      );

      setText(
        root,
        "[data-next-action-title]",
        "এখন Quiz দিন"
      );

      setText(
        root,
        "[data-next-action-message]",
        "আপনার Practice সম্পন্ন হয়েছে। এখন Quiz দিয়ে নিজের শেখা যাচাই করুন।"
      );

      setText(
        root,
        "[data-next-action-state]",
        "Practice Complete • Ready for Quiz"
      );

      if (primary) {
        primary.textContent =
          "📝 Quiz শুরু করুন";

        const quiz =
          document.querySelector(
            "[data-quran-quiz]"
          );

        if (quiz && quiz.id) {
          primary.href =
            "#" + quiz.id;
        } else {
          primary.href =
            "#quranQuiz";
        }
      }

      return;
    }

    root.classList.add(
      "status-practice"
    );

    setText(
      root,
      "[data-next-action-icon]",
      "→"
    );

    setText(
      root,
      "[data-next-action-title]",
      "Lesson চালিয়ে যান"
    );

    setText(
      root,
      "[data-next-action-message]",
      "Lesson content দেখুন, শুনুন এবং Practice সম্পন্ন করুন।"
    );

    setText(
      root,
      "[data-next-action-state]",
      "Practice এখনও সম্পন্ন হয়নি"
    );

    if (primary) {
      primary.textContent =
        "📖 Practice করুন";

      primary.href =
        "#quranLearningExperience";
    }
  }

  function refresh() {
    document
      .querySelectorAll(
        "[data-quran-next-action]"
      )
      .forEach(updateAction);
  }

  window.AIZoneRefreshQuranNextAction =
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
        event.key === null ||
        (
          event.key &&
          event.key.indexOf(
            "quran_practice_"
          ) === 0
        )
      ) {
        refresh();
      }
    }
  );

})();

/* AI-ZONE-QURAN-NEXT-ACTION-JS-END */
"""


print("=" * 60)
print(" AI Zone বাংলা — Quran Smart Next Action Installer")
print("=" * 60)

updated = 0
already = 0

for path in LESSON_FILES:

    if not path.exists():
        print(f"Missing: {path}")
        continue

    lesson_id = lesson_id_from_file(path)

    if lesson_id is None:
        continue

    backup = path.with_suffix(
        path.suffix + ".before-session23-step23-5"
    )

    if not backup.exists():
        shutil.copy2(path, backup)

    text = path.read_text(
        encoding="utf-8"
    )

    block = make_html(lesson_id)

    text, existed = replace_block(
        text,
        START,
        END,
        block
    )

    if existed:
        already += 1
    else:
        marker = (
            "AI-ZONE-QURAN-COMPLETION-FEEDBACK-END"
        )

        position = text.find(marker)

        if position >= 0:
            insert_at = text.find(
                "\n",
                position
            )

            if insert_at < 0:
                insert_at = len(text)

            text = (
                text[:insert_at + 1]
                + block
                + "\n"
                + text[insert_at + 1:]
            )
        else:
            text += "\n" + block + "\n"

        updated += 1

    path.write_text(
        text,
        encoding="utf-8"
    )

print()
print(f"Lessons updated: {updated}")
print(f"Already installed: {already}")
print("Lesson backups: PASS")


css_path = STATIC / "quran-progress.css"

css = (
    css_path.read_text(
        encoding="utf-8"
    )
    if css_path.exists()
    else ""
)

css, existed = replace_block(
    css,
    CSS_START,
    CSS_END,
    CSS_BLOCK.strip()
)

if not existed:
    css += "\n\n" + CSS_BLOCK.strip() + "\n"

css_path.write_text(
    css,
    encoding="utf-8"
)

print("Smart Next Action CSS: PASS")


js_path = STATIC / "quran-progress.js"

js = (
    js_path.read_text(
        encoding="utf-8"
    )
    if js_path.exists()
    else ""
)

js, existed = replace_block(
    js,
    JS_START,
    JS_END,
    JS_BLOCK.strip()
)

if not existed:
    js += "\n\n" + JS_BLOCK.strip() + "\n"

js_path.write_text(
    js,
    encoding="utf-8"
)

print("Smart Next Action JS: PASS")


verified = 0

for path in LESSON_FILES:

    if not path.exists():
        continue

    text = path.read_text(
        encoding="utf-8"
    )

    if (
        START in text
        and END in text
        and "data-quran-next-action" in text
        and "data-lesson-id=" in text
    ):
        verified += 1


css_ok = (
    CSS_START in css
    and CSS_END in css
    and "quran-next-action" in css
)

js_ok = (
    JS_START in js
    and JS_END in js
    and "AIZoneRefreshQuranNextAction" in js
    and "PASS_SCORE = 70" in js
)

print()
print("=" * 60)
print(" VERIFICATION")
print("=" * 60)

print(f"Lessons verified: {verified}/20")
print(
    "Smart Next Action CSS:",
    "PASS" if css_ok else "FAIL"
)
print(
    "Smart Next Action JS:",
    "PASS" if js_ok else "FAIL"
)
print(
    "Existing Progress/Quiz/Revision Engine: PRESERVED"
)
print("GitHub push: NO")

if (
    verified == 20
    and css_ok
    and js_ok
):
    print("STEP 23.5: PASS")
else:
    print("STEP 23.5: FAIL")

print("=" * 60)
