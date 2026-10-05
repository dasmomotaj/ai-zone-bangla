from pathlib import Path

p = Path("templates/quran.html")
s = p.read_text()

START = "<!-- AI-ZONE-QURAN-PROGRESS-SUMMARY-START -->"
END = "<!-- AI-ZONE-QURAN-PROGRESS-SUMMARY-END -->"

if START in s and END in s:
    print("Progress Summary already installed.")
    raise SystemExit(0)

block = f"""
{START}
<section class="academy-progress-summary" id="academyProgressSummary">
  <div class="progress-summary-head">
    <div>
      <span class="progress-summary-kicker">YOUR LEARNING JOURNEY</span>
      <h2>📊 আপনার Quran Learning Progress</h2>
      <p>প্রতিদিন অল্প অল্প করে এগিয়ে যান। নিয়মিত অনুশীলনই সবচেয়ে গুরুত্বপূর্ণ।</p>
    </div>
  </div>

  <div class="progress-summary-grid">
    <div class="progress-summary-card">
      <span class="progress-summary-icon">✅</span>
      <strong id="quranCompletedCount">0</strong>
      <span>সম্পন্ন পাঠ</span>
    </div>

    <div class="progress-summary-card">
      <span class="progress-summary-icon">📖</span>
      <strong id="quranRemainingCount">20</strong>
      <span>বাকি পাঠ</span>
    </div>

    <div class="progress-summary-card">
      <span class="progress-summary-icon">🎯</span>
      <strong id="quranProgressPercent">0%</strong>
      <span>মোট অগ্রগতি</span>
    </div>

    <div class="progress-summary-card">
      <span class="progress-summary-icon">🚀</span>
      <strong id="quranNextLesson">1</strong>
      <span>পরবর্তী পাঠ</span>
    </div>
  </div>

  <div class="academy-progress-track">
    <div
      class="academy-progress-fill"
      id="quranAcademyProgressFill"
      style="width:0%">
    </div>
  </div>

  <div class="academy-progress-footer">
    <span id="quranProgressText">0 / 20টি পাঠ সম্পন্ন</span>
    <a href="/quran/lesson/1" id="quranContinueButton">
      ▶ শেখা শুরু করুন
    </a>
  </div>
</section>
{END}
"""

# Insert before the first major lesson grid/cards section.
markers = [
    '<main',
    '<section class="lesson',
    '<section class="academy',
]

inserted = False

for marker in markers:
    pos = s.find(marker)

    if pos != -1:
        s = s[:pos] + block + "\n" + s[pos:]
        inserted = True
        break

if not inserted:
    # Safe fallback: insert immediately after </header> or before </body>
    marker = "</header>"
    pos = s.find(marker)

    if pos != -1:
        pos += len(marker)
        s = s[:pos] + "\n" + block + "\n" + s[pos:]
        inserted = True

if not inserted:
    marker = "</body>"
    pos = s.rfind(marker)

    if pos != -1:
        s = s[:pos] + block + "\n" + s[pos:]
        inserted = True

if not inserted:
    raise SystemExit("Could not find a safe insertion point.")

p.write_text(s)

print("Progress Summary installed: OK")
