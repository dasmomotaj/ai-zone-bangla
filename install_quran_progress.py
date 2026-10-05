from pathlib import Path

TEMPLATES = Path("templates")

START = "<!-- AI-ZONE-QURAN-PROGRESS-START -->"
END = "<!-- AI-ZONE-QURAN-PROGRESS-END -->"

def progress_block(lesson_id):
    if lesson_id < 20:
        next_link = f"""
        <a class="quran-next-button"
           href="/quran/lesson/{lesson_id + 1}">
            পরের পাঠে যান →
        </a>
"""
    else:
        next_link = """
        <a class="quran-next-button"
           href="/quran">
            🏆 Academy Dashboard
        </a>
"""

    return f"""
{START}
<section class="quran-progress-panel"
         data-quran-progress
         data-lesson-id="{lesson_id}">

    <div class="quran-progress-top">
        <span class="quran-progress-title">
            📈 আপনার Quran Academy Progress
        </span>
        <span class="quran-progress-value">0%</span>
    </div>

    <div class="quran-progress-track">
        <div class="quran-progress-fill"></div>
    </div>

    <p class="quran-progress-info">
        0 / 20টি পাঠ সম্পন্ন
    </p>

    <button
        type="button"
        class="quran-complete-button"
        onclick="AIZoneQuranComplete({lesson_id})">
        ✓ পাঠটি সম্পন্ন করুন
    </button>
{next_link}
</section>
{END}
"""

def add_assets(content):
    css_tag = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'quran-progress.css\') }}">'
    js_tag = '<script src="{{ url_for(\'static\', filename=\'quran-progress.js\') }}"></script>'

    if "quran-progress.css" not in content:
        if "</head>" in content:
            content = content.replace(
                "</head>",
                f"    {css_tag}\n</head>",
                1
            )
        else:
            content = css_tag + "\n" + content

    if "quran-progress.js" not in content:
        if "</body>" in content:
            content = content.replace(
                "</body>",
                f"    {js_tag}\n</body>",
                1
            )
        else:
            content += "\n" + js_tag + "\n"

    return content

def inject_progress(content, lesson_id):
    if START in content and END in content:
        print(f"Lesson {lesson_id}: progress UI already exists")
        return content

    block = progress_block(lesson_id)

    # Prefer inserting before an existing Quran navigation section.
    markers = [
        '<div class="quran-nav"',
        '<div class="lesson-nav"',
        '<nav class="quran-nav"',
        '<nav class="lesson-nav"',
    ]

    for marker in markers:
        pos = content.find(marker)
        if pos != -1:
            return content[:pos] + block + "\n" + content[pos:]

    # Fallback: insert before </body>
    if "</body>" in content:
        return content.replace(
            "</body>",
            block + "\n</body>",
            1
        )

    # Final fallback
    return content + "\n" + block + "\n"

updated = 0

for lesson_id in range(1, 21):
    if lesson_id == 1:
        path = TEMPLATES / "quran_lesson.html"
    else:
        path = TEMPLATES / f"quran_lesson_{lesson_id}.html"

    if not path.exists():
        print(f"Lesson {lesson_id}: SKIPPED — file not found")
        continue

    original = path.read_text(encoding="utf-8")
    content = add_assets(original)
    content = inject_progress(content, lesson_id)

    if content != original:
        path.write_text(content, encoding="utf-8")
        updated += 1
        print(f"Lesson {lesson_id}: ✅ progress UI installed")
    else:
        print(f"Lesson {lesson_id}: no changes needed")

print()
print("==========================================")
print(" Progress installation finished")
print(f" Updated lesson templates: {updated}/20")
print("==========================================")
