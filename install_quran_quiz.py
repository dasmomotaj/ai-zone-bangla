from pathlib import Path
import re

ROOT = Path(".")
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"

STATIC.mkdir(exist_ok=True)

JS = r"""
/* AI Zone বাংলা — Quran Academy Quiz Engine */
(function () {
  "use strict";

  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PASS_SCORE = 70;

  function loadResults() {
    try {
      return JSON.parse(localStorage.getItem(QUIZ_KEY) || "{}");
    } catch (e) {
      return {};
    }
  }

  function saveResults(results) {
    localStorage.setItem(QUIZ_KEY, JSON.stringify(results));
  }

  function initQuiz() {
    const quiz = document.querySelector("[data-quran-quiz]");
    if (!quiz) return;

    const lessonId = Number(quiz.dataset.lessonId);
    const questions = Array.from(
      quiz.querySelectorAll("[data-quiz-question]")
    );

    const resultBox = quiz.querySelector("[data-quiz-result]");
    const submitBtn = quiz.querySelector("[data-quiz-submit]");
    const retryBtn = quiz.querySelector("[data-quiz-retry]");

    if (!questions.length || !submitBtn) return;

    submitBtn.addEventListener("click", function () {
      let correct = 0;
      let answered = 0;

      questions.forEach(function (question) {
        const selected = question.querySelector(
          'input[type="radio"]:checked'
        );

        if (!selected) return;

        answered++;

        if (selected.value === question.dataset.answer) {
          correct++;
        }
      });

      if (answered < questions.length) {
        resultBox.textContent =
          "সব প্রশ্নের উত্তর দিন। তারপর আবার Submit করুন।";
        resultBox.className = "quran-quiz-result warning";
        return;
      }

      const total = questions.length;
      const score = Math.round((correct / total) * 100);
      const passed = score >= PASS_SCORE;

      const results = loadResults();

      results[String(lessonId)] = {
        score: score,
        correct: correct,
        total: total,
        passed: passed,
        updatedAt: new Date().toISOString()
      };

      saveResults(results);

      resultBox.innerHTML =
        "<strong>স্কোর: " + score + "%</strong><br>" +
        correct + " / " + total + "টি সঠিক উত্তর<br>" +
        (passed
          ? "🎉 অভিনন্দন! Quiz Passed."
          : "📚 আবার অনুশীলন করে Retry করুন।");

      resultBox.className =
        "quran-quiz-result " + (passed ? "success" : "fail");

      if (retryBtn) {
        retryBtn.hidden = passed;
      }

      if (passed && window.AIZoneQuranComplete) {
        window.AIZoneQuranComplete(lessonId);
      }
    });

    if (retryBtn) {
      retryBtn.addEventListener("click", function () {
        quiz.querySelectorAll('input[type="radio"]').forEach(function (input) {
          input.checked = false;
        });

        resultBox.textContent = "";
        resultBox.className = "quran-quiz-result";
        retryBtn.hidden = true;
      });
    }
  }

  window.AIZoneQuranQuizResults = loadResults;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initQuiz);
  } else {
    initQuiz();
  }
})();
"""

CSS = r"""
/* AI Zone বাংলা — Quran Academy Quiz UI */

.quran-quiz {
  margin: 32px auto;
  padding: 24px;
  max-width: 820px;
  border: 1px solid rgba(0, 220, 255, .25);
  border-radius: 24px;
  background: rgba(10, 18, 35, .88);
  box-shadow: 0 0 35px rgba(0, 200, 255, .08);
}

.quran-quiz-title {
  margin-bottom: 8px;
}

.quran-quiz-subtitle {
  opacity: .72;
  margin-bottom: 24px;
}

.quran-quiz-question {
  padding: 18px;
  margin: 16px 0;
  border-radius: 18px;
  background: rgba(255,255,255,.035);
  border: 1px solid rgba(255,255,255,.08);
}

.quran-quiz-option {
  display: block;
  margin: 10px 0;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  background: rgba(255,255,255,.035);
}

.quran-quiz-option:hover {
  background: rgba(0,220,255,.08);
}

.quran-quiz-submit,
.quran-quiz-retry {
  border: 0;
  border-radius: 14px;
  padding: 13px 20px;
  margin-top: 12px;
  cursor: pointer;
  font-weight: 700;
}

.quran-quiz-result {
  margin-top: 18px;
  padding: 16px;
  border-radius: 15px;
  min-height: 20px;
}

.quran-quiz-result.success {
  background: rgba(40, 200, 120, .12);
  border: 1px solid rgba(40, 200, 120, .3);
}

.quran-quiz-result.fail,
.quran-quiz-result.warning {
  background: rgba(255, 180, 40, .10);
  border: 1px solid rgba(255, 180, 40, .28);
}
"""

(STATIC / "quran-quiz.js").write_text(JS, encoding="utf-8")
(STATIC / "quran-quiz.css").write_text(CSS, encoding="utf-8")

quiz_html = r'''
<!-- AI-ZONE-QURAN-QUIZ-START -->
<section class="quran-quiz" data-quran-quiz data-lesson-id="__LESSON_ID__">
  <h2 class="quran-quiz-title">🧠 ছোট্ট Quiz</h2>
  <p class="quran-quiz-subtitle">
    পাঠটি ভালোভাবে বুঝেছেন কিনা যাচাই করুন। 70% বা তার বেশি হলে Quiz Passed হবে।
  </p>

  <div class="quran-quiz-question"
       data-quiz-question
       data-answer="a">
    <strong>প্রশ্ন ১</strong>
    <p>এই পাঠের মূল বিষয়টি কী?</p>

    <label class="quran-quiz-option">
      <input type="radio" name="quran_quiz___LESSON_ID___1" value="a">
      পাঠের মূল শিক্ষা
    </label>

    <label class="quran-quiz-option">
      <input type="radio" name="quran_quiz___LESSON_ID___1" value="b">
      অন্য একটি বিষয়
    </label>

    <label class="quran-quiz-option">
      <input type="radio" name="quran_quiz___LESSON_ID___1" value="c">
      অপ্রাসঙ্গিক বিষয়
    </label>
  </div>

  <div class="quran-quiz-question"
       data-quiz-question
       data-answer="a">
    <strong>প্রশ্ন ২</strong>
    <p>পাঠ শেখার সঠিক পদ্ধতি কোনটি?</p>

    <label class="quran-quiz-option">
      <input type="radio" name="quran_quiz___LESSON_ID___2" value="a">
      বুঝে অনুশীলন করা
    </label>

    <label class="quran-quiz-option">
      <input type="radio" name="quran_quiz___LESSON_ID___2" value="b">
      অনুশীলন না করা
    </label>

    <label class="quran-quiz-option">
      <input type="radio" name="quran_quiz___LESSON_ID___2" value="c">
      শুধু অনুমান করা
    </label>
  </div>

  <div class="quran-quiz-question"
       data-quiz-question
       data-answer="a">
    <strong>প্রশ্ন ৩</strong>
    <p>ভুল হলে কী করা উচিত?</p>

    <label class="quran-quiz-option">
      <input type="radio" name="quran_quiz___LESSON_ID___3" value="a">
      আবার শিখে অনুশীলন করা
    </label>

    <label class="quran-quiz-option">
      <input type="radio" name="quran_quiz___LESSON_ID___3" value="b">
      ভুলটি উপেক্ষা করা
    </label>

    <label class="quran-quiz-option">
      <input type="radio" name="quran_quiz___LESSON_ID___3" value="c">
      শেখা বন্ধ করা
    </label>
  </div>

  <button type="button" class="quran-quiz-submit" data-quiz-submit>
    ✓ Quiz Submit
  </button>

  <button type="button"
          class="quran-quiz-retry"
          data-quiz-retry
          hidden>
    ↻ আবার চেষ্টা করুন
  </button>

  <div class="quran-quiz-result" data-quiz-result></div>
</section>
<!-- AI-ZONE-QURAN-QUIZ-END -->
'''

updated = 0

for lesson_id in range(1, 21):
    if lesson_id == 1:
        path = TEMPLATES / "quran_lesson.html"
    else:
        path = TEMPLATES / f"quran_lesson_{lesson_id}.html"

    if not path.exists():
        print(f"⚠️ Missing: {path}")
        continue

    text = path.read_text(encoding="utf-8")

    if "<!-- AI-ZONE-QURAN-QUIZ-START -->" in text:
        print(f"⏭️ Lesson {lesson_id}: already installed")
        continue

    block = quiz_html.replace("__LESSON_ID__", str(lesson_id))

    # Insert before progress UI when available.
    marker = "<!-- AI-ZONE-QURAN-PROGRESS-START -->"

    if marker in text:
        text = text.replace(marker, block + "\n" + marker, 1)
    elif "</body>" in text:
        text = text.replace("</body>", block + "\n</body>", 1)
    else:
        text += "\n" + block + "\n"

    # Add assets once per lesson.
    if "quran-quiz.css" not in text:
        text = text.replace(
            "</head>",
            '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'quran-quiz.css\') }}">\n</head>',
            1
        )

    if "quran-quiz.js" not in text:
        text = text.replace(
            "</body>",
            '<script src="{{ url_for(\'static\', filename=\'quran-quiz.js\') }}"></script>\n</body>',
            1
        )

    path.write_text(text, encoding="utf-8")
    updated += 1
    print(f"✅ Lesson {lesson_id}: Quiz installed")

print()
print("==========================================")
print(" AI Zone বাংলা — Quran Quiz Installer")
print("==========================================")
print(f"Updated lessons: {updated}/20")
print(f"Quiz JS:  {'OK' if (STATIC / 'quran-quiz.js').exists() else 'MISSING'}")
print(f"Quiz CSS: {'OK' if (STATIC / 'quran-quiz.css').exists() else 'MISSING'}")
print("==========================================")
