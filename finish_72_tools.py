import sqlite3

DB = "aizonabangla.db"

extra_tools = [
    (
        "DeepAI",
        "AI Image",
        "https://deepai.org",
        "AI-powered image generation and creative tools with free usage options."
    ),
    (
        "Tensor.Art",
        "AI Image",
        "https://tensor.art",
        "AI image generation platform with free usage options and community models."
    ),
    (
        "FlexClip",
        "AI Video",
        "https://www.flexclip.com",
        "AI-assisted online video creation and editing with a free plan."
    ),
    (
        "Suno",
        "AI Design",
        "https://suno.com",
        "AI-powered creative music generation platform with a free usage tier."
    ),
    (
        "Leonardo AI",
        "AI Design",
        "https://leonardo.ai",
        "AI-powered creative design and generation platform with free usage options."
    ),
]

conn = sqlite3.connect(DB)
cur = conn.cursor()

existing_names = {
    row[0].strip().lower()
    for row in cur.execute("SELECT name FROM tools")
}

existing_urls = {
    row[0].strip().lower()
    for row in cur.execute("SELECT url FROM tools")
}

added = 0

for name, category, url, description in extra_tools:
    if name.lower() in existing_names:
        print(f"SKIP NAME: {name}")
        continue

    if url.lower() in existing_urls:
        print(f"SKIP URL: {name}")
        continue

    cur.execute(
        """
        INSERT INTO tools (name, description, category, url)
        VALUES (?, ?, ?, ?)
        """,
        (name, description, category, url)
    )

    print(f"ADD: {name} [{category}]")
    added += 1

conn.commit()

total = cur.execute("SELECT COUNT(*) FROM tools").fetchone()[0]

print()
print("=" * 55)
print("AI ZONE বাংলা — FINAL TOOL COUNT")
print("=" * 55)
print(f"Added this step : {added}")
print(f"Total tools     : {total}")

print()
print("Category counts:")

for category in [
    "AI Chat",
    "AI Writing",
    "AI Image",
    "AI Video",
    "AI Design",
]:
    count = cur.execute(
        "SELECT COUNT(*) FROM tools WHERE category=?",
        (category,)
    ).fetchone()[0]

    print(f"{category:12}: {count}")

conn.close()

if total == 72:
    print()
    print("PASS: Exactly 72 AI tools are now available.")
else:
    print()
    print(f"WARNING: Expected 72, found {total}.")
