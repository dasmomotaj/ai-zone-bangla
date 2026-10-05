from pathlib import Path
import shutil
import re

ROOT = Path(".")
TEMPLATES = ROOT / "templates"

TOTAL = 20

START = "<!-- AI-ZONE-QURAN-LESSON-NAV-START -->"
END = "<!-- AI-ZONE-QURAN-LESSON-NAV-END -->"

def lesson_template(lesson_id):
    if lesson_id == 1:
        return TEMPLATES / "quran_lesson.html"
    return TEMPLATES / f"quran_lesson_{lesson_id}.html"

def build_nav(lesson_id):
    prev_id = lesson_id - 1
    next_id = lesson_id + 1

    prev_link = (
        f'<a class="quran-lesson-nav-btn secondary" '
        f'href="{{{{ url_for("quran_lesson_{prev_id}") }}}}">'
        f'← আগের পাঠ</a>'
        if prev_id >= 1
        else
        '<span class="quran-lesson-nav-btn disabled">← আগের পাঠ</span>'
    )

    next_link = (
        f'<a class="quran-lesson-nav-btn primary" '
        f'href="{{{{ url_for("quran_lesson_{next_id}") }}}}">'
        f'পরের পাঠ →</a>'
        if next_id <= TOTAL
        else
        '<a class="quran-lesson-nav-btn primary" '
        'href="{{ url_for("quran") }}">Academy Dashboard →</a>'
    )

    return f"""
{START}
<section class="quran-lesson-navigation" aria-label="Lesson navigation">
  <div class="quran-nav-inner">
    <div class="quran-nav-label">📖 Quran Academy</div>

    <div class="quran-nav-title">
      Lesson {lesson_id} / {TOTAL}
    </div>

    <div class="quran-nav-actions">
      {prev_link}

      <a class="quran-lesson-nav-btn dashboard"
         href="{{{{ url_for("quran") }}}}">
        🏠 Dashboard
      </a>

      {next_link}
    </div>
  </div>
</section>
{END}
"""

CSS_START = "/* AI-ZONE-QURAN-LESSON-NAV-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-LESSON-NAV-CSS-END */"

CSS = f"""
{CSS_START}

.quran-lesson-navigation {{
  width: min(100% - 24px, 980px);
  margin: 28px auto 40px;
}}

.quran-nav-inner {{
  padding: 18px;
  border: 1px solid rgba(90, 220, 255, .18);
  border-radius: 20px;
  background: rgba(10, 18, 32, .82);
  box-shadow: 0 12px 40px rgba(0, 0, 0, .22);
  backdrop-filter: blur(12px);
}}

.quran-nav-label {{
  font-size: .82rem;
  opacity: .7;
  margin-bottom: 5px;
}}

.quran-nav-title {{
  font-size: 1.05rem;
  font-weight: 800;
  margin-bottom: 15px;
}}

.quran-nav-actions {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}}

.quran-lesson-nav-btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 10px 15px;
  border-radius: 13px;
  text-decoration: none;
  font-weight: 700;
  font-size: .9rem;
  border: 1px solid rgba(255,255,255,.12);
  transition: transform .2s ease, box-shadow .2s ease;
}}

.quran-lesson-nav-btn:hover {{
  transform: translateY(-2px);
}}

.quran-lesson-nav-btn.primary {{
  background: linear-gradient(135deg, #00c6ff, #0072ff);
  color: #fff;
  box-shadow: 0 8px 24px rgba(0, 114, 255, .25);
}}

.quran-lesson-nav-btn.secondary,
.quran-lesson-nav-btn.dashboard {{
  color: inherit;
  background: rgba(255,255,255,.055);
}}

.quran-lesson-nav-btn.disabled {{
  opacity: .35;
  cursor: not-allowed;
}}

@media (max-width: 600px) {{
  .quran-nav-actions {{
    display: grid;
    grid-template-columns: 1fr;
  }}

  .quran-lesson-nav-btn {{
    width: 100%;
  }}
}}

{CSS_END}
"""

CSS_FILE = ROOT / "static" / "quran-progress.css"

print("=" * 60)
print(" AI Zone বাংলা — Quran Lesson Navigation Installer")
print(" Session 23 — Step 23.1")
print("=" * 60)

updated = 0

for lesson_id in range(1, TOTAL + 1):
    path = lesson_template(lesson_id)

    if not path.exists():
        print(f"Lesson {lesson_id}: FAIL — template missing")
        raise SystemExit(1)

    text = path.read_text(encoding="utf-8")

    if START in text and END in text:
        text = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            build_nav(lesson_id).strip(),
            text,
            flags=re.S
        )
        print(f"Lesson {lesson_id}: navigation already exists — refreshed")
    else:
        backup = path.with_name(path.name + ".before-session23-step23-1")
        if not backup.exists():
            shutil.copy2(path, backup)

        # Insert before the final body close when available.
        if "</body>" in text:
            text = text.replace(
                "</body>",
                build_nav(lesson_id).strip() + "\n</body>",
                1
            )
        else:
            text += "\n" + build_nav(lesson_id).strip() + "\n"

        print(f"Lesson {lesson_id}: navigation installed")

    path.write_text(text, encoding="utf-8")
    updated += 1

# ------------------------------------------------------------
# Shared CSS
# ------------------------------------------------------------

css_text = CSS_FILE.read_text(encoding="utf-8") if CSS_FILE.exists() else ""

if CSS_START in css_text and CSS_END in css_text:
    css_text = re.sub(
        re.escape(CSS_START) + r".*?" + re.escape(CSS_END),
        CSS.strip(),
        css_text,
        flags=re.S
    )
    print("Shared navigation CSS: refreshed")
else:
    if CSS_FILE.exists():
        backup = CSS_FILE.with_name(
            CSS_FILE.name + ".before-session23-step23-1"
        )
        if not backup.exists():
            shutil.copy2(CSS_FILE, backup)

    css_text += "\n\n" + CSS.strip() + "\n"
    print("Shared navigation CSS: installed")

CSS_FILE.write_text(css_text, encoding="utf-8")

# ------------------------------------------------------------
# Static verification
# ------------------------------------------------------------

print()
print("=== Verification ===")

if updated == TOTAL:
    print(f"Lessons updated: {updated}/{TOTAL} PASS")
else:
    print(f"Lessons updated: {updated}/{TOTAL} FAIL")
    raise SystemExit(1)

all_ok = True

for lesson_id in range(1, TOTAL + 1):
    path = lesson_template(lesson_id)
    text = path.read_text(encoding="utf-8")

    if START in text and END in text:
        print(f"Lesson {lesson_id} navigation: PASS")
    else:
        print(f"Lesson {lesson_id} navigation: FAIL")
        all_ok = False

if CSS_START in css_text and CSS_END in css_text:
    print("Navigation CSS: PASS")
else:
    print("Navigation CSS: FAIL")
    all_ok = False

if not all_ok:
    raise SystemExit(1)

print()
print("=" * 60)
print(" STEP 23.1 INSTALLATION: PASS")
print("=" * 60)
print(" Previous / Dashboard / Next navigation: installed")
print(" Lessons: 20/20")
print(" Responsive mobile layout: installed")
print(" Existing lesson content: preserved")
print(" GitHub push: NO")
print("=" * 60)
