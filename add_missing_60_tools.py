import sqlite3
import shutil
from pathlib import Path
from datetime import datetime

DB = Path("aizonabangla.db")

if not DB.exists():
    raise SystemExit("ERROR: aizonabangla.db পাওয়া যায়নি।")

# --------------------------------------------------
# 1. BACKUP
# --------------------------------------------------
backup = Path(
    f"aizonabangla.db.before-72-tools-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
)
shutil.copy2(DB, backup)
print(f"Backup created: {backup}")

# --------------------------------------------------
# 2. 60 ADDITIONAL TOOLS
# --------------------------------------------------
tools = [
    # AI CHAT
    ("Microsoft Copilot", "AI Chat", "https://copilot.microsoft.com"),
    ("Perplexity", "AI Chat", "https://www.perplexity.ai"),
    ("DeepSeek", "AI Chat", "https://chat.deepseek.com"),
    ("Grok", "AI Chat", "https://grok.com"),
    ("Mistral Le Chat", "AI Chat", "https://chat.mistral.ai"),
    ("Poe", "AI Chat", "https://poe.com"),
    ("You.com", "AI Chat", "https://you.com"),
    ("HuggingChat", "AI Chat", "https://huggingface.co/chat"),
    ("Meta AI", "AI Chat", "https://www.meta.ai"),
    ("Pi", "AI Chat", "https://pi.ai"),
    ("Character.AI", "AI Chat", "https://character.ai"),
    ("Qwen", "AI Chat", "https://chat.qwen.ai"),

    # AI WRITING
    ("Grammarly", "AI Writing", "https://www.grammarly.com"),
    ("QuillBot", "AI Writing", "https://quillbot.com"),
    ("Wordtune", "AI Writing", "https://www.wordtune.com"),
    ("Rytr", "AI Writing", "https://rytr.me"),
    ("Writesonic", "AI Writing", "https://writesonic.com"),
    ("Simplified", "AI Writing", "https://simplified.com"),
    ("HyperWrite", "AI Writing", "https://www.hyperwriteai.com"),
    ("Sudowrite", "AI Writing", "https://sudowrite.com"),
    ("Anyword", "AI Writing", "https://www.anyword.com"),
    ("Frase", "AI Writing", "https://www.frase.io"),
    ("Jasper", "AI Writing", "https://www.jasper.ai"),
    ("Copy.ai", "AI Writing", "https://www.copy.ai"),

    # AI IMAGE
    ("Ideogram", "AI Image", "https://ideogram.ai"),
    ("Adobe Firefly", "AI Image", "https://firefly.adobe.com"),
    ("Microsoft Designer", "AI Image", "https://designer.microsoft.com"),
    ("Bing Image Creator", "AI Image", "https://www.bing.com/images/create"),
    ("Playground AI", "AI Image", "https://playground.com"),
    ("Mage Space", "AI Image", "https://www.mage.space"),
    ("NightCafe", "AI Image", "https://creator.nightcafe.studio"),
    ("Craiyon", "AI Image", "https://www.craiyon.com"),
    ("Pixlr AI", "AI Image", "https://pixlr.com"),
    ("Photoroom", "AI Image", "https://www.photoroom.com"),
    ("Picsart AI", "AI Image", "https://picsart.com"),
    ("Freepik AI", "AI Image", "https://www.freepik.com/ai"),

    # AI VIDEO
    ("Pika", "AI Video", "https://pika.art"),
    ("Kling AI", "AI Video", "https://klingai.com"),
    ("Hailuo AI", "AI Video", "https://hailuoai.video"),
    ("Luma Dream Machine", "AI Video", "https://lumalabs.ai/dream-machine"),
    ("HeyGen", "AI Video", "https://www.heygen.com"),
    ("VEED AI", "AI Video", "https://www.veed.io"),
    ("CapCut", "AI Video", "https://www.capcut.com"),
    ("InVideo AI", "AI Video", "https://invideo.io"),
    ("Descript", "AI Video", "https://www.descript.com"),
    ("OpusClip", "AI Video", "https://www.opus.pro"),
    ("Canva Video", "AI Video", "https://www.canva.com/video-editor"),
    ("Adobe Express", "AI Video", "https://www.adobe.com/express"),

    # AI DESIGN
    ("Gamma", "AI Design", "https://gamma.app"),
    ("Microsoft Designer", "AI Design", "https://designer.microsoft.com"),
    ("Looka", "AI Design", "https://looka.com"),
    ("Kittl", "AI Design", "https://www.kittl.com"),
    ("Uizard", "AI Design", "https://uizard.io"),
    ("Figma", "AI Design", "https://www.figma.com"),
    ("Visme", "AI Design", "https://www.visme.co"),
    ("Beautiful.ai", "AI Design", "https://www.beautiful.ai"),
    ("Tome", "AI Design", "https://tome.app"),
    ("Remove.bg", "AI Design", "https://www.remove.bg"),
    ("Clipdrop", "AI Design", "https://clipdrop.co"),
    ("PhotoRoom", "AI Design", "https://www.photoroom.com"),
]

# Remove duplicate names/URLs inside this new list
seen_names = set()
seen_urls = set()
clean_tools = []

for name, category, url in tools:
    if name.lower() in seen_names:
        continue
    if url.lower() in seen_urls:
        continue

    seen_names.add(name.lower())
    seen_urls.add(url.lower())
    clean_tools.append((name, category, url))

# --------------------------------------------------
# 3. DATABASE
# --------------------------------------------------
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

columns = {
    row["name"]
    for row in cur.execute("PRAGMA table_info(tools)")
}

required = {"name", "description", "category", "url"}

if not required.issubset(columns):
    conn.close()
    raise SystemExit(
        f"ERROR: tools table missing columns: {required - columns}"
    )

existing = cur.execute(
    "SELECT name, url FROM tools"
).fetchall()

existing_names = {r["name"].strip().lower() for r in existing}
existing_urls = {r["url"].strip().lower() for r in existing}

added = 0
skipped = 0

for name, category, url in clean_tools:

    if name.lower() in existing_names:
        print(f"SKIP NAME: {name}")
        skipped += 1
        continue

    if url.lower() in existing_urls:
        print(f"SKIP URL: {name}")
        skipped += 1
        continue

    description = (
        f"{name} — AI-powered {category.replace('AI ', '').lower()} tool "
        f"with a free or free-tier option. Check the official website "
        f"for current limits and features."
    )

    cur.execute(
        """
        INSERT INTO tools (name, description, category, url)
        VALUES (?, ?, ?, ?)
        """,
        (name, description, category, url)
    )

    existing_names.add(name.lower())
    existing_urls.add(url.lower())
    added += 1
    print(f"ADD: {name} [{category}]")

conn.commit()

# --------------------------------------------------
# 4. FINAL VERIFICATION
# --------------------------------------------------
total = cur.execute(
    "SELECT COUNT(*) FROM tools"
).fetchone()[0]

print()
print("=" * 60)
print("AI ZONE বাংলা — 72 TOOL RESTORE CHECK")
print("=" * 60)
print(f"New tools prepared : {len(clean_tools)}")
print(f"Added              : {added}")
print(f"Skipped            : {skipped}")
print(f"Total tools        : {total}")

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

    print(f"  {category:12} : {count}")

conn.close()

if total == 72:
    print()
    print("PASS: Exactly 72 tools are now in the database.")
else:
    print()
    print(f"WARNING: Expected 72 tools, but database has {total}.")
