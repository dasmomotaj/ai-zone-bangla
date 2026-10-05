from pathlib import Path
import re

TEMPLATES = Path("templates")
TOTAL = 20

START = "<!-- AI-ZONE-QURAN-PRACTICE-QUIZ-FLOW-START -->"
END = "<!-- AI-ZONE-QURAN-PRACTICE-QUIZ-FLOW-END -->"


def lesson_id_from_file(path):
    if path.name == "quran_lesson.html":
        return 1

    match = re.fullmatch(r"quran_lesson_(\d+)\.html", path.name)
    return int(match.group(1)) if match else None


def build_flow(lesson_id):
    if lesson_id < TOTAL:
        next_url = "{{ url_for('quran_lesson_" + str(lesson_id + 1) + "') }}"
        next_text = "➜ Next Lesson"
    else:
        next_url = "{{ url_for('quran') }}"
        next_text = "🏠 Quran Academy Dashboard"

    return f"""
{START}
<section class="quran-practice-quiz-flow"
         id="practiceQuizFlow"
         data-lesson-id="{lesson_id}">

  <div class="flow-header">
    <span class="flow-icon">🎯</span>
    <div>
      <h2>Practice → Quiz</h2>
      <p>অনুশীলন শেষ করে তারপর Quiz দিন</p>
    </div>
  </div>

  <div class="flow-status" id="practiceQuizStatus">
    🔒 Practice সম্পূর্ণ করুন
  </div>

  <div class="flow-steps">

    <div class="flow-step" id="flowPracticeStep">
      <span>1</span>
      <strong>Practice</strong>
      <small id="flowPracticeText">0/3 সম্পন্ন</small>
    </div>

    <div class="flow-arrow">→</div>

    <div class="flow-step locked" id="flowQuizStep">
      <span>2</span>
      <strong>Quiz</strong>
      <small id="flowQuizText">Locked</small>
    </div>

  </div>

  <div class="flow-actions">

    <button type="button"
            class="practice-flow-quiz-btn"
            id="practiceFlowQuizBtn"
            disabled>
      🔒 আগে Practice Complete করুন
    </button>

    <a class="practice-flow-next"
       href="{next_url}">
       {next_text}
    </a>

  </div>

  <div class="flow-note" id="practiceFlowNote">
    💡 “বুঝেছি”, “পড়েছি” এবং “অনুশীলন করেছি”—
    তিনটি ধাপ সম্পন্ন করলে Quiz unlock হবে।
  </div>

</section>

<style>
.quran-practice-quiz-flow {{
  margin:28px 0;
  padding:22px;
  border:1px solid rgba(34,211,238,.25);
  border-radius:22px;
  background:linear-gradient(145deg,rgba(8,18,35,.96),rgba(10,27,48,.92));
  box-shadow:0 12px 35px rgba(0,0,0,.28);
}}

.flow-header {{
  display:flex;
  align-items:center;
  gap:12px;
  margin-bottom:16px;
}}

.flow-icon {{
  font-size:28px;
}}

.flow-header h2 {{
  margin:0;
  font-size:22px;
}}

.flow-header p {{
  margin:4px 0 0;
  opacity:.72;
  font-size:14px;
}}

.flow-status {{
  padding:12px 14px;
  border-radius:14px;
  background:rgba(245,158,11,.09);
  border:1px solid rgba(245,158,11,.20);
  margin-bottom:18px;
  font-weight:700;
}}

.flow-status.ready {{
  background:rgba(34,197,94,.09);
  border-color:rgba(34,197,94,.28);
}}

.flow-steps {{
  display:flex;
  align-items:center;
  gap:10px;
  margin-bottom:18px;
}}

.flow-step {{
  flex:1;
  padding:14px;
  border-radius:16px;
  border:1px solid rgba(34,211,238,.20);
  background:rgba(255,255,255,.035);
}}

.flow-step span {{
  display:inline-flex;
  width:30px;
  height:30px;
  align-items:center;
  justify-content:center;
  border-radius:50%;
  background:rgba(34,211,238,.12);
}}

.flow-step strong {{
  display:block;
  margin-top:8px;
}}

.flow-step small {{
  display:block;
  margin-top:4px;
  opacity:.65;
}}

.flow-step.complete {{
  border-color:rgba(34,197,94,.35);
}}

.flow-step.unlocked {{
  border-color:rgba(34,211,238,.45);
  box-shadow:0 0 18px rgba(34,211,238,.08);
}}

.flow-step.locked {{
  opacity:.55;
}}

.flow-arrow {{
  opacity:.5;
}}

.practice-flow-quiz-btn {{
  width:100%;
  min-height:52px;
  border:0;
  border-radius:15px;
  font-size:16px;
  font-weight:800;
  cursor:pointer;
  background:rgba(148,163,184,.12);
  color:inherit;
}}

.practice-flow-quiz-btn.ready {{
  background:linear-gradient(135deg,#0891b2,#2563eb);
  box-shadow:0 8px 25px rgba(37,99,235,.25);
}}

.practice-flow-next {{
  display:block;
  text-align:center;
  margin-top:12px;
  padding:12px;
  border-radius:14px;
  text-decoration:none;
  border:1px solid rgba(34,211,238,.20);
}}

.flow-note {{
  margin-top:14px;
  font-size:13px;
  opacity:.68;
  line-height:1.6;
}}

@media (max-width:600px) {{
  .quran-practice-quiz-flow {{
    padding:17px;
    border-radius:18px;
  }}

  .flow-arrow {{
    display:none;
  }}

  .flow-step {{
    padding:11px;
  }}
}}
</style>

<script>
(function() {{
  const lessonId = {lesson_id};
  const practiceKey = "ai_zone_quran_practice_" + lessonId;

  function getPracticeState() {{
    try {{
      const raw = localStorage.getItem(practiceKey);
      return raw ? (JSON.parse(raw) || {{}}) : {{}};
    }} catch (error) {{
      return {{}};
    }}
  }}

  function isComplete() {{
    const state = getPracticeState();

    return !!(state.bujhechi || state.understood)
        && !!(state.porechi || state.read)
        && !!(state.onushilon || state.practice);
  }}

  function completedCount() {{
    const state = getPracticeState();
    let count = 0;

    if (state.bujhechi || state.understood) count++;
    if (state.porechi || state.read) count++;
    if (state.onushilon || state.practice) count++;

    return count;
  }}

  function updateFlow() {{
    const complete = isComplete();
    const count = completedCount();

    const status = document.getElementById("practiceQuizStatus");
    const practiceStep = document.getElementById("flowPracticeStep");
    const quizStep = document.getElementById("flowQuizStep");
    const practiceText = document.getElementById("flowPracticeText");
    const quizText = document.getElementById("flowQuizText");
    const button = document.getElementById("practiceFlowQuizBtn");
    const note = document.getElementById("practiceFlowNote");

    if (!status || !button) return;

    practiceText.textContent = count + "/3 সম্পন্ন";

    if (complete) {{
      status.textContent = "✅ Practice Complete — Quiz Unlocked!";
      status.classList.add("ready");

      practiceStep.classList.add("complete");

      quizStep.classList.remove("locked");
      quizStep.classList.add("unlocked");

      quizText.textContent = "Unlocked";

      button.disabled = false;
      button.classList.add("ready");
      button.textContent = "📝 Quiz দিন →";

      note.textContent =
        "🎉 Practice সম্পূর্ণ হয়েছে। এবার Quiz দিয়ে শেখা যাচাই করুন।";
    }} else {{
      status.textContent = "🔒 Practice সম্পূর্ণ করুন";
      status.classList.remove("ready");

      quizStep.classList.add("locked");
      quizStep.classList.remove("unlocked");

      quizText.textContent = "Locked";

      button.disabled = true;
      button.classList.remove("ready");
      button.textContent = "🔒 আগে Practice Complete করুন";

      note.textContent =
        "💡 তিনটি Practice ধাপ সম্পন্ন করলে Quiz automatically unlock হবে।";
    }}
  }}

  function scrollToQuiz() {{
    const selectors = [
      ".quran-quiz",
      "[data-quran-quiz]",
      "#quranQuiz"
    ];

    for (const selector of selectors) {{
      const target = document.querySelector(selector);

      if (target) {{
        target.scrollIntoView({{
          behavior:"smooth",
          block:"start"
        }});
        return;
      }}
    }}

    const headings = document.querySelectorAll("h2,h3");

    for (const heading of headings) {{
      const text = heading.textContent || "";

      if (/quiz/i.test(text) || /কুইজ/.test(text)) {{
        heading.scrollIntoView({{
          behavior:"smooth",
          block:"start"
        }});
        return;
      }}
    }}
  }}

  document.addEventListener("DOMContentLoaded", function() {{
    updateFlow();

    const button = document.getElementById("practiceFlowQuizBtn");

    if (button) {{
      button.addEventListener("click", function() {{
        if (isComplete()) {{
          scrollToQuiz();
        }}
      }});
    }}

    window.addEventListener("storage", updateFlow);

    setInterval(updateFlow, 700);
  }});

}})();
</script>
{END}
"""


updated = 0
verified = 0

for path in sorted(TEMPLATES.glob("quran_lesson*.html")):
    lesson_id = lesson_id_from_file(path)

    if lesson_id is None or not (1 <= lesson_id <= TOTAL):
        continue

    text = path.read_text(encoding="utf-8")

    # Remove only an existing Step 22.5 block.
    pattern = re.escape(START) + r".*?" + re.escape(END)
    text = re.sub(pattern, "", text, flags=re.S)

    block = build_flow(lesson_id)

    quiz_marker = "<!-- AI-ZONE-QURAN-QUIZ-START -->"

    if quiz_marker in text:
        text = text.replace(
            quiz_marker,
            block + "\n" + quiz_marker,
            1
        )
    else:
        raise RuntimeError(
            f"Quiz marker missing in {path}"
        )

    path.write_text(text, encoding="utf-8")
    updated += 1

    required = [
        START,
        "quran-practice-quiz-flow",
        "practiceQuizStatus",
        "practiceFlowQuizBtn",
        "flowPracticeStep",
        "flowQuizStep",
        END,
    ]

    if all(item in text for item in required):
        verified += 1
    else:
        print(f"VERIFY FAIL: Lesson {lesson_id}")

print("==========================================")
print(" AI Zone বাংলা — Step 22.5")
print(" Practice → Quiz Smart Flow")
print("==========================================")
print(f"Updated templates: {updated}/{TOTAL}")
print(f"Verified templates: {verified}/{TOTAL}")

if updated == TOTAL and verified == TOTAL:
    print("TEMPLATE VERIFICATION: PASS")
else:
    print("TEMPLATE VERIFICATION: FAIL")
