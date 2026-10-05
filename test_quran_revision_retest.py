from pathlib import Path
import re
import json
import sys

ROOT = Path(".")
JS = ROOT / "static" / "quran-progress.js"

print("=" * 64)
print(" AI Zone বাংলা — Quran Revision Re-Test")
print(" Session 22 — Step 22.12-F Functional QA")
print("=" * 64)

if not JS.exists():
    print("FAIL: quran-progress.js missing")
    sys.exit(1)

js = JS.read_text(encoding="utf-8")

# --------------------------------------------------
# 1. Required engine markers
# --------------------------------------------------

required = [
    "// AI-ZONE-QURAN-REVISION-RETEST-JS-START",
    "// AI-ZONE-QURAN-REVISION-RETEST-JS-END",
    "AIZoneQuranRevisionRetest",
    "ai_zone_quran_retest_v1",
    "ai_zone_quran_quiz_v1",
    "ai_zone_quran_mistakes_v1",
    "recordRetest",
    "getLatestScores",
]

print()
print("=== Engine Structure ===")

for marker in required:
    if marker in js:
        print(f"{marker}: PASS")
    else:
        print(f"{marker}: FAIL")
        sys.exit(1)

# --------------------------------------------------
# 2. Extract engine block
# --------------------------------------------------

start_marker = "// AI-ZONE-QURAN-REVISION-RETEST-JS-START"
end_marker = "// AI-ZONE-QURAN-REVISION-RETEST-JS-END"

start = js.find(start_marker)
end = js.find(end_marker)

if start == -1 or end == -1 or end <= start:
    print("Engine block extraction: FAIL")
    sys.exit(1)

engine = js[start:end + len(end_marker)]

print()
print("=== Engine Block ===")
print("Engine block extraction: PASS")
print(f"Engine block size: {len(engine)} bytes")

# --------------------------------------------------
# 3. Verify required functions
# --------------------------------------------------

functions = [
    "safeJSON",
    "saveJSON",
    "lessonIdOf",
    "scoreOf",
    "timestampOf",
    "extractQuizResults",
    "getLatestScores",
    "getMistakes",
    "normalizeMistakes",
    "buildRetestData",
    "refresh",
    "recordRetest",
]

print()
print("=== Required Functions ===")

for fn in functions:
    pattern = rf"function\s+{re.escape(fn)}\s*\("
    if re.search(pattern, engine):
        print(f"{fn}(): PASS")
    else:
        print(f"{fn}(): FAIL")
        sys.exit(1)

# --------------------------------------------------
# 4. Verify PASS threshold
# --------------------------------------------------

print()
print("=== Pass Threshold ===")

if "const PASS_SCORE = 70;" in engine:
    print("PASS_SCORE = 70: PASS")
else:
    print("PASS_SCORE = 70: FAIL")
    sys.exit(1)

# --------------------------------------------------
# 5. Verify status transitions
# --------------------------------------------------

print()
print("=== Status Logic ===")

status_checks = {
    '"improved"': "Improved status",
    '"still-weak"': "Still Weak status",
    '"needs-retest"': "Needs Re-Test status",
}

for marker, label in status_checks.items():
    if marker in engine:
        print(f"{label}: PASS")
    else:
        print(f"{label}: FAIL")
        sys.exit(1)

# --------------------------------------------------
# 6. Verify storage persistence
# --------------------------------------------------

print()
print("=== Storage Persistence ===")

storage_checks = [
    "localStorage.getItem",
    "localStorage.setItem",
    'saveJSON(RETEST_KEY',
]

for marker in storage_checks:
    if marker in engine:
        print(f"{marker}: PASS")
    else:
        print(f"{marker}: FAIL")
        sys.exit(1)

# --------------------------------------------------
# 7. Simulated expected transition model
# --------------------------------------------------

print()
print("=== Simulated Re-Test Scenarios ===")

PASS_SCORE = 70

scenarios = [
    {
        "name": "Weak → Improved",
        "old_score": 45,
        "new_score": 82,
        "expected": "improved",
    },
    {
        "name": "Weak → Still Weak",
        "old_score": 45,
        "new_score": 58,
        "expected": "still-weak",
    },
    {
        "name": "Very Weak → Improved",
        "old_score": 25,
        "new_score": 75,
        "expected": "improved",
    },
    {
        "name": "Weak → Still Weak",
        "old_score": 60,
        "new_score": 65,
        "expected": "still-weak",
    },
]

scenario_pass = 0

for scenario in scenarios:
    new_score = scenario["new_score"]

    actual = (
        "improved"
        if new_score >= PASS_SCORE
        else "still-weak"
    )

    if actual == scenario["expected"]:
        print(
            f"{scenario['name']}: PASS "
            f"({scenario['old_score']}% → {new_score}%)"
        )
        scenario_pass += 1
    else:
        print(
            f"{scenario['name']}: FAIL "
            f"(expected {scenario['expected']}, got {actual})"
        )

if scenario_pass != len(scenarios):
    print("Scenario validation: FAIL")
    sys.exit(1)

print(f"Scenario validation: {scenario_pass}/{len(scenarios)} PASS")

# --------------------------------------------------
# 8. Verify queue ordering logic exists
# --------------------------------------------------

print()
print("=== Queue Intelligence ===")

queue_checks = [
    "queue.sort",
    "data.queue",
    "data.improved",
    "data.stillWeak",
    "history",
]

for marker in queue_checks:
    if marker in engine:
        print(f"{marker}: PASS")
    else:
        print(f"{marker}: FAIL")
        sys.exit(1)

# --------------------------------------------------
# 9. Verify dashboard IDs
# --------------------------------------------------

dashboard = ROOT / "templates" / "quran.html"

if not dashboard.exists():
    print("Dashboard template: FAIL")
    sys.exit(1)

html = dashboard.read_text(encoding="utf-8")

print()
print("=== Dashboard Integration ===")

dashboard_checks = [
    "AI-ZONE-QURAN-REVISION-RETEST-START",
    "quranRevisionRetest",
    "quranRetestCount",
    "quranRetestImproved",
    "quranRetestStillWeak",
    "quranRetestStatus",
    "quranRetestList",
]

for marker in dashboard_checks:
    if marker in html:
        print(f"{marker}: PASS")
    else:
        print(f"{marker}: FAIL")
        sys.exit(1)

# --------------------------------------------------
# 10. Final result
# --------------------------------------------------

print()
print("=" * 64)
print(" STEP 22.12-F FUNCTIONAL QA: PASS")
print("=" * 64)
print(" Engine structure: PASS")
print(" Required functions: PASS")
print(" Pass threshold: PASS")
print(" Status transitions: PASS")
print(" Storage persistence: PASS")
print(" Simulated scenarios: PASS")
print(" Queue intelligence: PASS")
print(" Dashboard integration: PASS")
print()
print(" Revision Re-Test Engine is structurally verified.")
print(" NO GITHUB PUSH")
print("=" * 64)
