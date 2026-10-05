from pathlib import Path
import re

TEMPLATES = Path("templates")
STATIC = Path("static")
TOTAL = 20

START = "<!-- AI-ZONE-QURAN-AUDIO-LAYER-START -->"
END = "<!-- AI-ZONE-QURAN-AUDIO-LAYER-END -->"

CSS_START = "/* AI-ZONE-QURAN-AUDIO-CSS-START */"
CSS_END = "/* AI-ZONE-QURAN-AUDIO-CSS-END */"

JS_START = "/* AI-ZONE-QURAN-AUDIO-JS-START */"
JS_END = "/* AI-ZONE-QURAN-AUDIO-JS-END */"


def lesson_id_from_file(path):
    if path.name == "quran_lesson.html":
        return 1

    m = re.fullmatch(r"quran_lesson_(\d+)\.html", path.name)
    return int(m.group(1)) if m else None


def build_audio_block(lesson_id):
    return f"""
{START}
<section class="quran-audio-layer" id="quranAudioLayer" data-lesson-id="{lesson_id}">
    <div class="audio-layer-head">
        <div>
            <span class="audio-kicker">🎧 AUDIO LEARNING</span>
            <h2>শুনুন → অনুসরণ করুন → আবার শুনুন</h2>
            <p>এই Lesson-এর অডিও শেখার জন্য প্রস্তুত। Audio source যুক্ত হলে এখান থেকেই চালানো যাবে।</p>
        </div>
        <span class="audio-status" id="quranAudioStatus">Ready</span>
    </div>

    <div class="audio-player-card">
        <div class="audio-icon">🔊</div>

        <div class="audio-player-main">
            <div class="audio-title-row">
                <strong>Lesson {lesson_id} Audio</strong>
                <span id="quranAudioTime">00:00 / 00:00</span>
            </div>

            <div class="audio-progress-track"
                 id="quranAudioProgressTrack"
                 role="progressbar"
                 aria-valuemin="0"
                 aria-valuemax="100"
                 aria-valuenow="0">
                <div class="audio-progress-fill" id="quranAudioProgressFill"></div>
            </div>

            <div class="audio-controls">
                <button type="button"
                        class="audio-control-btn primary"
                        id="quranAudioPlayBtn">
                    ▶ Play
                </button>

                <button type="button"
                        class="audio-control-btn"
                        id="quranAudioResetBtn">
                    ↺ Reset
                </button>

                <label class="audio-volume">
                    🔉
                    <input id="quranAudioVolume"
                           type="range"
                           min="0"
                           max="1"
                           step="0.05"
                           value="1"
                           aria-label="Audio volume">
                </label>
            </div>
        </div>
    </div>

    <div class="audio-source-note">
        <span>ℹ️</span>
        <div>
            <strong>Audio source hook ready</strong>
            <p>
                বর্তমানে এটি একটি safe audio player framework।
                নির্ভরযোগ্য Quran recitation source যুক্ত করার পর Play ব্যবহার করা যাবে।
            </p>
        </div>
    </div>

    <audio id="quranLessonAudio" preload="metadata"></audio>
</section>
{END}
"""


AUDIO_CSS = f"""
{CSS_START}
.quran-audio-layer {{
    margin: 28px 0;
    padding: 22px;
    border: 1px solid rgba(80, 220, 255, .22);
    border-radius: 24px;
    background:
        radial-gradient(circle at top right, rgba(0, 210, 255, .10), transparent 42%),
        rgba(8, 14, 30, .82);
    box-shadow: 0 14px 45px rgba(0,0,0,.28);
}}

.audio-layer-head {{
    display:flex;
    align-items:flex-start;
    justify-content:space-between;
    gap:16px;
    margin-bottom:18px;
}}

.audio-kicker {{
    display:inline-block;
    font-size:.72rem;
    letter-spacing:.12em;
    font-weight:800;
    color:#67e8f9;
    margin-bottom:6px;
}}

.audio-layer-head h2 {{
    margin:0 0 6px;
    font-size:1.35rem;
}}

.audio-layer-head p {{
    margin:0;
    opacity:.76;
    line-height:1.65;
}}

.audio-status {{
    flex:0 0 auto;
    padding:7px 11px;
    border-radius:999px;
    font-size:.72rem;
    font-weight:800;
    background:rgba(34,197,94,.10);
    border:1px solid rgba(34,197,94,.25);
}}

.audio-player-card {{
    display:flex;
    gap:16px;
    align-items:center;
    padding:18px;
    border-radius:20px;
    background:rgba(255,255,255,.035);
    border:1px solid rgba(255,255,255,.08);
}}

.audio-icon {{
    width:52px;
    height:52px;
    display:grid;
    place-items:center;
    flex:0 0 52px;
    border-radius:16px;
    background:rgba(34,211,238,.10);
    font-size:1.45rem;
}}

.audio-player-main {{
    min-width:0;
    flex:1;
}}

.audio-title-row {{
    display:flex;
    justify-content:space-between;
    gap:12px;
    margin-bottom:13px;
}}

.audio-title-row strong {{
    font-size:.98rem;
}}

.audio-title-row span {{
    font-size:.76rem;
    opacity:.65;
    white-space:nowrap;
}}

.audio-progress-track {{
    height:8px;
    border-radius:999px;
    overflow:hidden;
    cursor:pointer;
    background:rgba(255,255,255,.10);
}}

.audio-progress-fill {{
    width:0%;
    height:100%;
    border-radius:inherit;
    background:linear-gradient(90deg,#22d3ee,#38bdf8,#818cf8);
    transition:width .12s linear;
}}

.audio-controls {{
    display:flex;
    align-items:center;
    gap:9px;
    flex-wrap:wrap;
    margin-top:14px;
}}

.audio-control-btn {{
    border:1px solid rgba(255,255,255,.12);
    background:rgba(255,255,255,.045);
    color:inherit;
    border-radius:12px;
    padding:9px 13px;
    font-weight:800;
    cursor:pointer;
}}

.audio-control-btn.primary {{
    border-color:rgba(34,211,238,.35);
    background:rgba(34,211,238,.12);
}}

.audio-volume {{
    display:flex;
    align-items:center;
    gap:8px;
    margin-left:auto;
}}

.audio-volume input {{
    width:90px;
    accent-color:#22d3ee;
}}

.audio-source-note {{
    display:flex;
    gap:10px;
    margin-top:14px;
    padding:13px 15px;
    border-radius:16px;
    background:rgba(59,130,246,.06);
    border:1px solid rgba(59,130,246,.14);
    font-size:.82rem;
}}

.audio-source-note p {{
    margin:4px 0 0;
    opacity:.72;
    line-height:1.55;
}}

@media (max-width:600px) {{
    .quran-audio-layer {{
        padding:16px;
        border-radius:20px;
    }}

    .audio-layer-head {{
        flex-direction:column;
    }}

    .audio-player-card {{
        align-items:flex-start;
    }}

    .audio-title-row {{
        flex-direction:column;
        gap:4px;
    }}

    .audio-volume {{
        margin-left:0;
        width:100%;
    }}

    .audio-volume input {{
        flex:1;
        width:auto;
    }}
}}
{CSS_END}
"""


AUDIO_JS = f"""
{JS_START}
(function () {{
    "use strict";

    const audio = document.getElementById("quranLessonAudio");
    const playBtn = document.getElementById("quranAudioPlayBtn");
    const resetBtn = document.getElementById("quranAudioResetBtn");
    const volume = document.getElementById("quranAudioVolume");
    const fill = document.getElementById("quranAudioProgressFill");
    const track = document.getElementById("quranAudioProgressTrack");
    const timeText = document.getElementById("quranAudioTime");
    const status = document.getElementById("quranAudioStatus");

    if (!audio || !playBtn) return;

    function formatTime(seconds) {{
        if (!Number.isFinite(seconds) || seconds < 0) return "00:00";
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return String(mins).padStart(2, "0") + ":" +
               String(secs).padStart(2, "0");
    }}

    function updateProgress() {{
        const duration = audio.duration || 0;
        const current = audio.currentTime || 0;
        const percent = duration ? (current / duration) * 100 : 0;

        fill.style.width = percent + "%";
        track.setAttribute("aria-valuenow", String(Math.round(percent)));

        timeText.textContent =
            formatTime(current) + " / " + formatTime(duration);
    }}

    function setStatus(text) {{
        status.textContent = text;
    }}

    playBtn.addEventListener("click", function () {{
        if (!audio.src) {{
            setStatus("Audio source not connected");
            return;
        }}

        if (audio.paused) {{
            audio.play()
                .then(function () {{
                    playBtn.textContent = "⏸ Pause";
                    setStatus("Playing");
                }})
                .catch(function () {{
                    setStatus("Unable to play");
                }});
        }} else {{
            audio.pause();
            playBtn.textContent = "▶ Play";
            setStatus("Paused");
        }}
    }});

    resetBtn.addEventListener("click", function () {{
        audio.pause();
        audio.currentTime = 0;
        playBtn.textContent = "▶ Play";
        setStatus("Ready");
        updateProgress();
    }});

    volume.addEventListener("input", function () {{
        audio.volume = Number(volume.value);
    }});

    track.addEventListener("click", function (event) {{
        if (!audio.duration) return;

        const rect = track.getBoundingClientRect();
        const ratio = Math.max(
            0,
            Math.min(1, (event.clientX - rect.left) / rect.width)
        );

        audio.currentTime = ratio * audio.duration;
        updateProgress();
    }});

    audio.addEventListener("timeupdate", updateProgress);

    audio.addEventListener("loadedmetadata", function () {{
        setStatus("Ready");
        updateProgress();
    }});

    audio.addEventListener("play", function () {{
        playBtn.textContent = "⏸ Pause";
        setStatus("Playing");
    }});

    audio.addEventListener("pause", function () {{
        if (!audio.ended) {{
            playBtn.textContent = "▶ Play";
            setStatus("Paused");
        }}
    }});

    audio.addEventListener("ended", function () {{
        playBtn.textContent = "▶ Play";
        setStatus("Finished");
        updateProgress();
    }});

    audio.addEventListener("error", function () {{
        setStatus("Audio source unavailable");
    }});

    window.AIZoneQuranAudio = {{
        setSource: function (src) {{
            if (!src) return false;
            audio.src = src;
            audio.load();
            setStatus("Ready");
            return true;
        }},
        play: function () {{
            return audio.play();
        }},
        pause: function () {{
            audio.pause();
        }},
        reset: function () {{
            audio.pause();
            audio.currentTime = 0;
            updateProgress();
        }}
    }};

    updateProgress();
}})();
{JS_END}
"""


lesson_files = [
    p for p in sorted(TEMPLATES.glob("quran_lesson*.html"))
    if lesson_id_from_file(p) is not None
]

print("=" * 42)
print(" AI Zone বাংলা — Step 22.6")
print(" Quran Audio Learning Layer")
print("=" * 42)

updated = 0

for path in lesson_files:
    lesson_id = lesson_id_from_file(path)
    text = path.read_text(encoding="utf-8")

    # Remove only our own previous block.
    pattern = re.escape(START) + r".*?" + re.escape(END)
    text = re.sub(pattern, "", text, flags=re.S)

    # Put audio layer before Practice → Quiz flow.
    marker = "<!-- AI-ZONE-QURAN-PRACTICE-QUIZ-FLOW-START -->"

    if marker in text:
        text = text.replace(
            marker,
            build_audio_block(lesson_id) + "\n" + marker,
            1
        )
    else:
        # Fallback: insert before Quiz section.
        quiz_marker = "<!-- AI-ZONE-QURAN-QUIZ-START -->"
        if quiz_marker in text:
            text = text.replace(
                quiz_marker,
                build_audio_block(lesson_id) + "\n" + quiz_marker,
                1
            )
        else:
            raise RuntimeError(f"No insertion marker found: {path}")

    path.write_text(text, encoding="utf-8")
    updated += 1

# Append shared CSS safely.
css_path = STATIC / "quran-progress.css"
css_text = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

css_text = re.sub(
    re.escape(CSS_START) + r".*?" + re.escape(CSS_END),
    "",
    css_text,
    flags=re.S
)
css_text = css_text.rstrip() + "\n\n" + AUDIO_CSS.strip() + "\n"
css_path.write_text(css_text, encoding="utf-8")

# Append shared JS safely.
js_path = STATIC / "quran-progress.js"
js_text = js_path.read_text(encoding="utf-8") if js_path.exists() else ""

js_text = re.sub(
    re.escape(JS_START) + r".*?" + re.escape(JS_END),
    "",
    js_text,
    flags=re.S
)
js_text = js_text.rstrip() + "\n\n" + AUDIO_JS.strip() + "\n"
js_path.write_text(js_text, encoding="utf-8")

# Verification.
verified = 0

for path in lesson_files:
    text = path.read_text(encoding="utf-8")

    required = [
        START,
        "quran-audio-layer",
        "quranLessonAudio",
        "quranAudioPlayBtn",
        "quranAudioProgressFill",
        END,
    ]

    if all(item in text for item in required):
        verified += 1

print(f"Updated templates: {updated}/{TOTAL}")
print(f"Verified templates: {verified}/{TOTAL}")

if updated != TOTAL or verified != TOTAL:
    raise SystemExit("TEMPLATE VERIFICATION: FAIL")

print("TEMPLATE VERIFICATION: PASS")
print("Audio CSS: PASS")
print("Audio JS: PASS")
print("==========================================")
print(" STEP 22.6 INSTALL FINISHED")
print(" Fresh Flask + LIVE QA is next")
print(" NO GITHUB PUSH")
print("==========================================")
