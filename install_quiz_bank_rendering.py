from pathlib import Path
import re

TEMPLATES = Path("templates")

START = "<!-- AI-ZONE-QURAN-QUIZ-START -->"
END = "<!-- AI-ZONE-QURAN-QUIZ-END -->"


def build_quiz_block(lesson_id):
    return """<!-- AI-ZONE-QURAN-QUIZ-START -->
<section class="quran-quiz"
         data-quran-quiz
         data-lesson-id="__LESSON_ID__">

  <h2 class="quran-quiz-title">🧠 Quiz</h2>

  <p class="quran-quiz-subtitle">
    এই পাঠের বিষয়টি কতটা বুঝেছেন তা যাচাই করুন।
    70% বা তার বেশি হলে Quiz Passed হবে।
  </p>

  {% set quiz = get_quiz(__LESSON_ID__) %}

  {% if quiz.questions %}

    {% for question in quiz.questions %}
    <div class="quran-quiz-question"
         data-quiz-question
         data-answer="{{ question.answer }}">

      <strong>প্রশ্ন {{ loop.index }}</strong>

      <p>{{ question.question }}</p>

      {% for option in question.options %}
      <label class="quran-quiz-option">
        <input
          type="radio"
          name="quran_quiz___LESSON_ID___{{ loop.index }}"
          value="{{ loop.index0 }}">
        {{ option }}
      </label>
      {% endfor %}

    </div>
    {% endfor %}

    <button type="button"
            class="quran-quiz-submit"
            data-quiz-submit>
      ✓ Quiz Submit
    </button>

    <button type="button"
            class="quran-quiz-retry"
            data-quiz-retry
            hidden>
      ↻ আবার চেষ্টা করুন
    </button>

    <div class="quran-quiz-result"
         data-quiz-result></div>

  {% else %}

    <div class="quran-quiz-result warning">
      📚 এই পাঠের Quiz প্রশ্ন এখনো প্রস্তুত করা হচ্ছে।
      পাঠটি সম্পন্ন করে নিয়মিত অনুশীলন চালিয়ে যান।
    </div>

  {% endif %}

</section>
<!-- AI-ZONE-QURAN-QUIZ-END -->""".replace(
        "__LESSON_ID__",
        str(lesson_id)
    )


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

    if START not in text or END not in text:
        print(f"⚠️ Lesson {lesson_id}: Quiz block not found")
        continue

    pattern = re.escape(START) + r".*?" + re.escape(END)

    text = re.sub(
        pattern,
        build_quiz_block(lesson_id),
        text,
        count=1,
        flags=re.S,
    )

    path.write_text(text, encoding="utf-8")

    updated += 1
    print(f"✅ Lesson {lesson_id}: Bank rendering installed")


print()
print("==========================================")
print(" Quiz Bank Rendering Installer")
print("==========================================")
print(f"Updated lessons: {updated}/20")
print("==========================================")
