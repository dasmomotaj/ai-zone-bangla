from pathlib import Path
import re
import shutil

ROOT = Path(".")
TEMPLATES = ROOT / "templates"

TOTAL = 20

MARKER_START = "<!-- AI-ZONE-QURAN-CONTENT-UPGRADE-START -->"
MARKER_END = "<!-- AI-ZONE-QURAN-CONTENT-UPGRADE-END -->"

CONTENT = {
    1: {
        "title": "আরবি হরফ",
        "goal": "কুরআন পড়ার জন্য ২৮টি মৌলিক আরবি হরফ চিনতে শেখা।",
        "rule": "প্রতিটি হরফের নিজস্ব আকৃতি ও উচ্চারণ আছে। প্রথমে হরফ চিনুন, তারপর সঠিক উচ্চারণ অনুশীলন করুন।",
        "examples": "ا — ب — ت — ث — ج — ح — خ",
        "mistakes": [
            "একটি হরফকে অন্য হরফ মনে করা",
            "শুধু দেখে মুখস্থ করা কিন্তু উচ্চারণ না শোনা",
            "হরফের মাখরাজ না জেনে দ্রুত পড়া",
        ],
        "practice": "আজ অন্তত ৩ বার হরফগুলো দেখে চিনুন এবং ধীরে ধীরে পড়ুন।",
    },
    2: {
        "title": "হরফের সংযোগ ও আকৃতি",
        "goal": "আরবি শব্দে হরফ কীভাবে যুক্ত হয়ে বিভিন্ন আকৃতি নেয় তা বোঝা।",
        "rule": "একই হরফ শব্দের শুরু, মাঝ বা শেষে অবস্থান করলে তার লিখিত আকৃতি পরিবর্তিত হতে পারে।",
        "examples": "بـ — ـبـ — ـب | مـ — ـمـ — ـم",
        "mistakes": [
            "আলাদা ও যুক্ত হরফকে ভিন্ন হরফ মনে করা",
            "শব্দের মধ্যে হরফ শনাক্ত না করা",
        ],
        "practice": "একটি হরফ নিয়ে তার আলাদা, শুরু, মাঝ ও শেষের আকৃতি শনাক্ত করুন।",
    },
    3: {
        "title": "হারাকাত",
        "goal": "ফাতহা, কাসরা ও দাম্মাহ চিনে স্বল্প স্বরের পাঠ শেখা।",
        "rule": "হারাকাত হরফের উচ্চারণে স্বল্প স্বর নির্দেশ করে।",
        "examples": "بَ — بِ — بُ",
        "mistakes": [
            "ফাতহা, কাসরা ও দাম্মাহ গুলিয়ে ফেলা",
            "হারাকাত বাদ দিয়ে পড়া",
        ],
        "practice": "একই হরফে তিনটি হারাকাত দেখে আলাদা করে পড়ার অনুশীলন করুন।",
    },
    4: {
        "title": "তানভীন",
        "goal": "দুই ফাতহা, দুই কাসরা ও দুই দাম্মাহ চিনতে শেখা।",
        "rule": "তানভীন সাধারণত শব্দের শেষে নুন-সাকিনের মতো একটি অতিরিক্ত নাসিক্য ধ্বনি নির্দেশ করে।",
        "examples": "ـً — ـٍ — ـٌ",
        "mistakes": [
            "একক হারাকাতের সঙ্গে তানভীন গুলিয়ে ফেলা",
            "তানভীনের ধ্বনি ভুলভাবে দীর্ঘ করা",
        ],
        "practice": "তিন ধরনের তানভীন আলাদা করে শনাক্ত করুন।",
    },
    5: {
        "title": "সুকুন ও শাদ্দাহ",
        "goal": "সুকুন ও শাদ্দাহর চিহ্ন দেখে সঠিকভাবে পড়া শেখা।",
        "rule": "সুকুন হরফে স্বরধ্বনি না থাকার নির্দেশ দেয়; শাদ্দাহ হরফের দ্বিত্ব নির্দেশ করে।",
        "examples": "بْ — بَّ",
        "mistakes": [
            "সুকুনকে হারাকাতের মতো পড়া",
            "শাদ্দাহযুক্ত হরফকে একবারের মতো পড়া",
        ],
        "practice": "সুকুন ও শাদ্দাহর উদাহরণ আলাদা করে পড়ুন।",
    },
    6: {
        "title": "মাদ্দ",
        "goal": "দীর্ঘ স্বর বা মাদের মৌলিক ধারণা বোঝা।",
        "rule": "মাদের অক্ষর ও সংশ্লিষ্ট নিয়ম অনুযায়ী স্বরধ্বনি দীর্ঘ হতে পারে।",
        "examples": "قَالَ — يَقُولُ — قِيلَ",
        "mistakes": [
            "সব জায়গায় একই দৈর্ঘ্য প্রয়োগ করা",
            "মাদ্দের অক্ষর চিনতে না পারা",
        ],
        "practice": "মাদের জায়গা চিহ্নিত করে ধীরে পাঠ করুন।",
    },
    7: {
        "title": "মাখরাজ",
        "goal": "আরবি হরফ কোন উচ্চারণস্থল থেকে বের হয় তার মৌলিক ধারণা নেওয়া।",
        "rule": "সঠিক মাখরাজ ছাড়া কাছাকাছি উচ্চারণের কিছু আরবি হরফের পার্থক্য নষ্ট হতে পারে।",
        "examples": "ح — ه | ص — س | ط — ت",
        "mistakes": [
            "বাংলা উচ্চারণ দিয়ে আরবি ধ্বনি পুরোপুরি প্রতিস্থাপন করা",
            "কাছাকাছি হরফের পার্থক্য না করা",
        ],
        "practice": "শিক্ষক/কারির কাছ থেকে শুনে প্রতিটি কঠিন হরফের উচ্চারণ মিলিয়ে নিন।",
    },
    8: {
        "title": "নূন সাকিনাহ ও তানভীন",
        "goal": "নূন সাকিনাহ ও তানভীনের পরবর্তী হরফ অনুযায়ী মৌলিক নিয়ম বোঝা।",
        "rule": "পরবর্তী হরফের ভিত্তিতে নূন সাকিনাহ ও তানভীনের পাঠের ধরন পরিবর্তিত হয়।",
        "examples": "مِنْ هَادٍ — عَلِيمٌ خَبِيرٌ",
        "mistakes": [
            "পরবর্তী হরফ না দেখে একইভাবে পড়া",
            "নিয়মের নাম মুখস্থ করে প্রয়োগ না শেখা",
        ],
        "practice": "পরবর্তী হরফ দেখে কোন নিয়ম প্রযোজ্য তা শনাক্ত করুন।",
    },
    9: {
        "title": "ইযহার",
        "goal": "ইযহারের মৌলিক ধারণা ও প্রয়োগ বোঝা।",
        "rule": "নূন সাকিনাহ বা তানভীনের পরে হালকির নির্দিষ্ট হরফ এলে ইযহার হয়।",
        "examples": "مِنْهُمْ — عَلِيمٌ حَكِيمٌ",
        "mistakes": [
            "নূন ধ্বনি অতিরিক্ত লুকিয়ে ফেলা",
            "পরবর্তী হরফ শনাক্ত না করা",
        ],
        "practice": "ইযহারের উদাহরণে নূন সাকিনাহ/তানভীন স্পষ্টভাবে লক্ষ্য করুন।",
    },
    10: {
        "title": "ইদগাম",
        "goal": "নূন সাকিনাহ ও তানভীনের ক্ষেত্রে ইদগামের মৌলিক ধারণা শেখা।",
        "rule": "নির্দিষ্ট হরফের আগে নূন সাকিনাহ বা তানভীন এলে ইদগামের নিয়ম প্রযোজ্য হতে পারে।",
        "examples": "مَنْ يَقُولُ — غَفُورٌ رَحِيمٌ",
        "mistakes": [
            "সব ইদগামকে একইভাবে পড়া",
            "ইদগাম হরফগুলো না জানা",
        ],
        "practice": "উদাহরণ দেখে নূন সাকিনাহ/তানভীনের পরের হরফ শনাক্ত করুন।",
    },
    11: {
        "title": "ইকলাব",
        "goal": "ইকলাবের মৌলিক নিয়ম শনাক্ত করা।",
        "rule": "নূন সাকিনাহ বা তানভীনের পরে ب এলে ইকলাবের নিয়ম প্রযোজ্য হয়।",
        "examples": "مِنْ بَعْدِ",
        "mistakes": [
            "ب দেখেও ইকলাব শনাক্ত না করা",
            "নাসিক্য ধ্বনির বৈশিষ্ট্য ঠিকভাবে না বোঝা",
        ],
        "practice": "ب-এর আগে নূন সাকিনাহ বা তানভীন আছে কি না দেখুন।",
    },
    12: {
        "title": "ইখফা",
        "goal": "ইখফার মৌলিক ধারণা ও শনাক্তকরণ শেখা।",
        "rule": "ইযহার, ইদগাম ও ইকলাবের বাইরে নির্দিষ্ট হরফগুলোর আগে নূন সাকিনাহ/তানভীনে ইখফা হয়।",
        "examples": "مِنْ شَرِّ — أَنْفُسَكُمْ",
        "mistakes": [
            "ইখফাকে সম্পূর্ণ ইযহার বা সম্পূর্ণ ইদগামের মতো পড়া",
            "গুন্নাহর মাত্রা ভুল করা",
        ],
        "practice": "উদাহরণে ইখফার জায়গা চিহ্নিত করে কারির পাঠ শুনে অনুশীলন করুন।",
    },
    13: {
        "title": "মীম সাকিনাহ",
        "goal": "মীম সাকিনাহর প্রধান নিয়মগুলো শনাক্ত করা।",
        "rule": "মীম সাকিনাহর পরে কোন হরফ এসেছে তার ওপর পাঠের নিয়ম নির্ভর করে।",
        "examples": "تَرْمِيهِمْ بِحِجَارَةٍ",
        "mistakes": [
            "মীম সাকিনাহর পরের হরফ না দেখা",
            "মীমের গুন্নাহর স্থান ভুল করা",
        ],
        "practice": "মীম সাকিনাহ দেখে পরবর্তী হরফের সঙ্গে সম্পর্ক নির্ণয় করুন।",
    },
    14: {
        "title": "গুন্নাহ",
        "goal": "গুন্নাহর মৌলিক ধারণা ও নাসিক্য ধ্বনি সম্পর্কে ধারণা নেওয়া।",
        "rule": "গুন্নাহ একটি নাসিক্য ধ্বনি; এর প্রয়োগ নির্দিষ্ট তাজবিদ নিয়মে আসে।",
        "examples": "إِنَّ — ثُمَّ",
        "mistakes": [
            "গুন্নাহকে সাধারণ মুখের ধ্বনি হিসেবে পড়া",
            "অতিরিক্ত দীর্ঘ করা",
        ],
        "practice": "শিক্ষকের/কারির পাঠ শুনে গুন্নাহর সময় ও ধ্বনি অনুসরণ করুন।",
    },
    15: {
        "title": "কলকলাহ",
        "goal": "কলকলাহর অক্ষর ও মৌলিক উচ্চারণ বুঝতে শেখা।",
        "rule": "কলকলাহর নির্দিষ্ট অক্ষর সাকিন অবস্থায় বিশেষ প্রতিধ্বনির বৈশিষ্ট্য পায়।",
        "examples": "قَدْ — يَجْعَلْ",
        "mistakes": [
            "কলকলাহকে অতিরিক্ত জোরে বলা",
            "হরফের মূল মাখরাজ পরিবর্তন করা",
        ],
        "practice": "ق ط ب ج د অক্ষরগুলো সাকিন অবস্থায় শুনে অনুশীলন করুন।",
    },
    16: {
        "title": "তাফখীম ও তারকীক",
        "goal": "কিছু আরবি হরফ ভারী ও হালকা উচ্চারণের মৌলিক পার্থক্য বোঝা।",
        "rule": "তাফখীমে ধ্বনির ভারী বৈশিষ্ট্য এবং তারকীকে হালকা বৈশিষ্ট্য প্রকাশ পায়; নিয়মভেদে প্রয়োগ আলাদা।",
        "examples": "ص — س | ط — ت",
        "mistakes": [
            "ভারী হরফকে অতিরিক্ত ভারী করা",
            "হালকা হরফে অপ্রয়োজনীয় ভার দেওয়া",
        ],
        "practice": "কাছাকাছি হরফের কারির পাঠ শুনে পার্থক্য ধরুন।",
    },
    17: {
        "title": "ওয়াকফ ও ইবতিদা",
        "goal": "কোথায় থামা এবং কোথা থেকে পুনরায় শুরু করা যায় তার মৌলিক ধারণা শেখা।",
        "rule": "আয়াতের অর্থ ও তিলাওয়াতের চিহ্ন বিবেচনা করে থামা/শুরু করার নিয়ম শেখা হয়।",
        "examples": "وقف — ابتداء",
        "mistakes": [
            "শুধু শ্বাসের সুবিধার জন্য যেকোনো জায়গায় থামা",
            "থামার পর অর্থের অসঙ্গতি তৈরি করা",
        ],
        "practice": "মুশহাফের ওয়াকফ চিহ্ন দেখে শিক্ষক/কারির ব্যাখ্যার সঙ্গে মিলিয়ে অনুশীলন করুন।",
    },
    18: {
        "title": "শব্দ থেকে আয়াত পাঠ",
        "goal": "শেখা মৌলিক নিয়মগুলো ব্যবহার করে ছোট শব্দ ও আয়াত পড়ার অভ্যাস তৈরি করা।",
        "rule": "হরফ, হারাকাত, মাদ্দ ও তাজবিদ নিয়ম একসঙ্গে দেখে ধীরে পাঠ করতে হবে।",
        "examples": "প্রথমে শব্দ → তারপর ছোট বাক্যাংশ → তারপর পূর্ণ আয়াত",
        "mistakes": [
            "দ্রুত পড়ার চেষ্টা করা",
            "নিয়ম দেখেও প্রয়োগ না করা",
        ],
        "practice": "একটি ছোট আয়াত ধীরে পড়ুন, কঠিন অংশ চিহ্নিত করুন, তারপর আবার পড়ুন।",
    },
    19: {
        "title": "কুরআনিক শব্দভাণ্ডার",
        "goal": "কুরআনে বারবার আসা পরিচিত শব্দের অর্থ শেখার অভ্যাস তৈরি করা।",
        "rule": "শব্দের অর্থ প্রসঙ্গ অনুযায়ী বুঝতে হবে; শুধু একটি বাংলা অর্থকে সব জায়গায় চূড়ান্ত ধরে নেওয়া ঠিক নয়।",
        "examples": "رَبّ — كِتَاب — نُور",
        "mistakes": [
            "একটি শব্দের একটি অর্থ সব প্রসঙ্গে প্রয়োগ করা",
            "বিশ্বস্ত অনুবাদ/তাফসিরের প্রয়োজন উপেক্ষা করা",
        ],
        "practice": "একটি শব্দের অর্থ, ব্যবহার ও আয়াতের প্রসঙ্গ একসঙ্গে দেখুন।",
    },
    20: {
        "title": "Revision ও Final Assessment",
        "goal": "আগের ১৯টি lesson-এর গুরুত্বপূর্ণ বিষয় পুনরাবৃত্তি ও মূল্যায়ন করা।",
        "rule": "যে বিষয়ে ভুল বেশি হয়েছে সেটি আবার অনুশীলন করে তারপর assessment দেওয়া সবচেয়ে কার্যকর।",
        "examples": "হরফ → হারাকাত → মাদ্দ → মাখরাজ → তাজবিদ → পাঠ",
        "mistakes": [
            "শুধু quiz score দেখে শেখা সম্পূর্ণ মনে করা",
            "দুর্বল lesson পুনরায় না দেখা",
        ],
        "practice": "Progress ও Quiz result দেখে দুর্বল lessonগুলো পুনরায় সম্পন্ন করুন।",
    },
}


def lesson_file(lesson_id):
    if lesson_id == 1:
        return TEMPLATES / "quran_lesson.html"
    return TEMPLATES / f"quran_lesson_{lesson_id}.html"


def build_block(lesson_id):
    data = CONTENT[lesson_id]

    mistakes = "".join(
        f"<li>{item}</li>" for item in data["mistakes"]
    )

    return f"""
{MARKER_START}
<section class="quran-content-upgrade" aria-label="Structured Quran Lesson Content">
  <div class="quran-content-header">
    <span class="quran-content-badge">📚 STRUCTURED LESSON</span>
    <h2>Lesson {lesson_id}: {data["title"]}</h2>
    <p>লক্ষ্য → নিয়ম → উদাহরণ → ভুল সংশোধন → অনুশীলন</p>
  </div>

  <div class="quran-content-grid">

    <article class="quran-content-card">
      <span class="quran-content-icon">🎯</span>
      <h3>আজকের লক্ষ্য</h3>
      <p>{data["goal"]}</p>
    </article>

    <article class="quran-content-card">
      <span class="quran-content-icon">📖</span>
      <h3>মূল নিয়ম</h3>
      <p>{data["rule"]}</p>
    </article>

    <article class="quran-content-card">
      <span class="quran-content-icon">🔎</span>
      <h3>উদাহরণ</h3>
      <div class="quran-example-box" dir="rtl">{data["examples"]}</div>
    </article>

    <article class="quran-content-card">
      <span class="quran-content-icon">⚠️</span>
      <h3>সাধারণ ভুল</h3>
      <ul class="quran-mistake-list">
        {mistakes}
      </ul>
    </article>

  </div>

  <div class="quran-content-practice">
    <div>
      <span class="quran-content-badge">🧠 PRACTICE TASK</span>
      <h3>এখন অনুশীলন করুন</h3>
      <p>{data["practice"]}</p>
    </div>
    <button type="button"
            class="quran-content-practice-btn"
            onclick="this.classList.toggle('is-done'); this.textContent=this.classList.contains('is-done') ? '✓ অনুশীলন সম্পন্ন' : '🧠 অনুশীলন সম্পন্ন করুন';">
      🧠 অনুশীলন সম্পন্ন করুন
    </button>
  </div>

  <div class="quran-content-note">
    <strong>📌 গুরুত্বপূর্ণ:</strong>
    কুরআন তিলাওয়াতের সঠিক উচ্চারণ শেখার জন্য যোগ্য শিক্ষক/কারি বা নির্ভরযোগ্য তিলাওয়াত শুনে যাচাই করা সবচেয়ে নিরাপদ।
    AI Zone বাংলা শেখার সহায়ক; এটি আলেম/কারির বিকল্প নয়।
  </div>
</section>
{MARKER_END}
"""


def remove_old_block(text):
    pattern = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        re.S,
    )
    return pattern.sub("", text)


def main():
    print("=" * 42)
    print(" AI Zone বাংলা — Quran Content Upgrade")
    print("=" * 42)

    updated = 0
    missing = 0

    for lesson_id in range(1, TOTAL + 1):
        path = lesson_file(lesson_id)

        if not path.exists():
            print(f"Lesson {lesson_id}: MISSING")
            missing += 1
            continue

        backup = path.with_suffix(path.suffix + ".before-session22-step22-8")
        if not backup.exists():
            shutil.copy2(path, backup)

        text = path.read_text(encoding="utf-8")
        text = remove_old_block(text)

        marker = '<!-- AI-ZONE-QURAN-EXPERIENCE-START -->'

        if marker in text:
            text = text.replace(
                marker,
                build_block(lesson_id) + "\n" + marker,
                1,
            )
        else:
            quiz_marker = '<!-- AI-ZONE-QURAN-QUIZ-START -->'

            if quiz_marker in text:
                text = text.replace(
                    quiz_marker,
                    build_block(lesson_id) + "\n" + quiz_marker,
                    1,
                )
            else:
                text = text.replace(
                    "</main>",
                    build_block(lesson_id) + "\n</main>",
                    1,
                )

        path.write_text(text, encoding="utf-8")
        updated += 1
        print(f"Lesson {lesson_id}: UPDATED")

    print()
    print(f"Updated: {updated}/{TOTAL}")
    print(f"Missing: {missing}")

    if updated == TOTAL and missing == 0:
        print("Content upgrade: PASS")
    else:
        print("Content upgrade: CHECK")

    print()
    print("No GitHub push.")
    print("Next: syntax + template verification + fresh Flask QA.")


if __name__ == "__main__":
    main()
