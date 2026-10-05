from pathlib import Path
import shutil
import re

ROOT = Path(".")
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"

START = "<!-- AI-ZONE-QURAN-JOURNEY-HEADER-START -->"
END = "<!-- AI-ZONE-QURAN-JOURNEY-HEADER-END -->"

CSS_START = "/* AI-ZONE-QURAN-JOURNEY-HEADER-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-JOURNEY-HEADER-CSS-END */"

TOTAL = 20


def lesson_number(path):
    name = path.name

    if name == "quran_lesson.html":
        return 1

    m = re.fullmatch(r"quran_lesson_(\d+)\.html", name)
    if not m:
        return None

    n = int(m.group(1))
    if 2 <= n <= TOTAL:
        return n

    return None


def build_block(n):
    percent = round((n / TOTAL) * 100)

    return f'''
{START}
<section class="quran-journey-header" aria-label="Quran learning journey">

  <div class="quran-journey-top">

    <div class="quran-journey-title">
      <span class="quran-journey-kicker">QURAN ACADEMY</span>
      <h2>আপনার শেখার যাত্রা</h2>
      <p>Lesson {n} / {TOTAL}</p>
    </div>

    <div class="quran-journey-percent">
      <strong>{percent}%</strong>
      <span>Academy Journey</span>
    </div>

  </div>

  <div class="quran-journey-progress">
    <div
      class="quran-journey-progress-fill"
      style="width: {percent}%"
      aria-valuenow="{percent}"
      aria-valuemin="0"
      aria-valuemax="100"
      role="progressbar">
    </div>
  </div>

  <div class="quran-journey-steps">

    <div class="quran-journey-step completed">
      <span>✓</span>
      <small>Dashboard</small>
    </div>

    <div class="quran-journey-line"></div>

    <div class="quran-journey-step active">
      <span>{n}</span>
      <small>বর্তমান Lesson</small>
    </div>

    <div class="quran-journey-line"></div>

    <div class="quran-journey-step">
      <span>3</span>
      <small>Practice</small>
    </div>

    <div class="quran-journey-line"></div>

    <div class="quran-journey-step">
      <span>4</span>
      <small>Quiz</small>
    </div>

    <div class="quran-journey-line"></div>

    <div class="quran-journey-step">
      <span>5</span>
      <small>Revision</small>
    </div>

  </div>

</section>
{END}
'''


def install_template(path, n):
    text = path.read_text(encoding="utf-8")

    if START in text and END in text:
        print(f"Lesson {n}: journey header already exists")
        return False

    backup = path.with_name(path.name + ".before-session23-step23-2")
    if not backup.exists():
        shutil.copy2(path, backup)

    block = build_block(n)

    # Prefer inserting after the first main opening heading.
    patterns = [
        r'(<main[^>]*>)',
        r'(<div[^>]*class=["\'][^"\']*quran[^"\']*lesson[^"\']*["\'][^>]*>)',
        r'(<body[^>]*>)',
    ]

    inserted = False

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            pos = match.end()
            text = text[:pos] + "\n" + block + "\n" + text[pos:]
            inserted = True
            break

    if not inserted:
        # Safe fallback: append before closing body.
        body_match = re.search(r"</body>", text, flags=re.I)

        if body_match:
            pos = body_match.start()
            text = text[:pos] + "\n" + block + "\n" + text[pos:]
            inserted = True

    if not inserted:
        print(f"Lesson {n}: could not find safe insertion point")
        return False

    path.write_text(text, encoding="utf-8")
    print(f"Lesson {n}: UPDATED")
    return True


def install_css():
    css_path = STATIC / "quran-progress.css"
    STATIC.mkdir(exist_ok=True)

    css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

    if CSS_START in css and CSS_END in css:
        print("Journey header CSS: already installed")
        return

    css_block = f'''
{CSS_START}

.quran-journey-header {{
  margin: 0 auto 28px;
  padding: 22px;
  border: 1px solid rgba(34, 211, 238, 0.22);
  border-radius: 24px;
  background:
    linear-gradient(
      135deg,
      rgba(8, 18, 38, 0.96),
      rgba(11, 28, 48, 0.92)
    );
  box-shadow:
    0 18px 50px rgba(0, 0, 0, 0.25),
    0 0 30px rgba(34, 211, 238, 0.06);
  overflow: hidden;
}}

.quran-journey-top {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}}

.quran-journey-kicker {{
  display: inline-block;
  margin-bottom: 5px;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.16em;
  opacity: 0.72;
}}

.quran-journey-title h2 {{
  margin: 0;
  font-size: clamp(1.05rem, 3vw, 1.45rem);
}}

.quran-journey-title p {{
  margin: 6px 0 0;
  opacity: 0.68;
  font-size: 0.88rem;
}}

.quran-journey-percent {{
  min-width: 105px;
  text-align: right;
}}

.quran-journey-percent strong {{
  display: block;
  font-size: 1.35rem;
}}

.quran-journey-percent span {{
  display: block;
  margin-top: 3px;
  font-size: 0.7rem;
  opacity: 0.62;
}}

.quran-journey-progress {{
  height: 7px;
  margin: 20px 0;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  overflow: hidden;
}}

.quran-journey-progress-fill {{
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(
    90deg,
    #22d3ee,
    #60a5fa
  );
  box-shadow: 0 0 16px rgba(34, 211, 238, 0.45);
}}

.quran-journey-steps {{
  display: flex;
  align-items: center;
  width: 100%;
}}

.quran-journey-step {{
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 55px;
  text-align: center;
  opacity: 0.48;
}}

.quran-journey-step span {{
  width: 30px;
  height: 30px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.16);
  font-size: 0.78rem;
  font-weight: 800;
}}

.quran-journey-step small {{
  font-size: 0.67rem;
  line-height: 1.2;
  white-space: nowrap;
}}

.quran-journey-step.completed {{
  opacity: 0.82;
}}

.quran-journey-step.completed span {{
  border-color: rgba(34, 211, 238, 0.42);
}}

.quran-journey-step.active {{
  opacity: 1;
}}

.quran-journey-step.active span {{
  border-color: rgba(34, 211, 238, 0.8);
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.24);
}}

.quran-journey-line {{
  flex: 1;
  height: 1px;
  margin: 0 4px 21px;
  background: rgba(255,255,255,0.12);
}}

@media (max-width: 620px) {{
  .quran-journey-header {{
    padding: 17px;
    border-radius: 20px;
  }}

  .quran-journey-top {{
    align-items: flex-start;
  }}

  .quran-journey-percent {{
    min-width: 80px;
  }}

  .quran-journey-steps {{
    overflow-x: auto;
    padding-bottom: 4px;
    scrollbar-width: thin;
  }}

  .quran-journey-step {{
    min-width: 58px;
  }}

  .quran-journey-line {{
    min-width: 22px;
  }}
}}

{CSS_END}
'''

    css_path.write_text(css.rstrip() + "\n\n" + css_block.strip() + "\n",
                        encoding="utf-8")

    print("Journey header CSS: INSTALLED")


def main():
    print("=" * 60)
    print(" AI Zone বাংলা — Quran Academy")
    print(" Session 23 — Step 23.2")
    print(" Lesson Progress Header")
    print("=" * 60)

    if not TEMPLATES.exists():
        print("ERROR: templates directory not found")
        raise SystemExit(1)

    updated = 0
    skipped = 0

    lesson_files = []

    for path in TEMPLATES.glob("quran_lesson*.html"):
        n = lesson_number(path)
        if n is not None:
            lesson_files.append((n, path))

    lesson_files.sort()

    print()
    print("=== Updating Lessons ===")

    for n, path in lesson_files:
        before = START in path.read_text(encoding="utf-8")

        changed = install_template(path, n)

        if changed:
            updated += 1
        elif before:
            skipped += 1

    print()
    print("=== Installing Shared CSS ===")
    install_css()

    print()
    print("=== Verification ===")

    pass_count = 0

    for n, path in lesson_files:
        text = path.read_text(encoding="utf-8")

        if (
            START in text
            and END in text
            and f"Lesson {n} / {TOTAL}" in text
            and "quran-journey-header" in text
            and "quran-journey-progress-fill" in text
        ):
            print(f"Lesson {n}: PASS")
            pass_count += 1
        else:
            print(f"Lesson {n}: FAIL")

    css_text = (STATIC / "quran-progress.css").read_text(encoding="utf-8")

    css_ok = (
        CSS_START in css_text
        and CSS_END in css_text
        and "quran-journey-header" in css_text
        and "quran-journey-progress-fill" in css_text
    )

    print()
    print("============================================================")
    print(" SESSION 23 — STEP 23.2 RESULT")
    print("============================================================")
    print(f"Lessons verified: {pass_count}/{len(lesson_files)}")
    print(f"Updated this run: {updated}")
    print(f"Already installed: {skipped}")
    print(f"Journey CSS: {'PASS' if css_ok else 'FAIL'}")
    print("Existing lesson content: PRESERVED")
    print("GitHub push: NO")
    print("============================================================")

    if pass_count != 20 or not css_ok:
        raise SystemExit(1)

    print("STEP 23.2: PASS")


if __name__ == "__main__":
    main()
