from pathlib import Path
import re
import shutil

ROOT = Path(".")
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
BASE = TEMPLATES / "base.html"
INDEX = TEMPLATES / "index.html"

STATIC.mkdir(exist_ok=True)

print("==========================================")
print(" AI Zone বাংলা — Premium UI Installer")
print(" Demo 4 + 7 + 9 + 12")
print("==========================================")

# -------------------------------------------------
# 1. BACKUPS
# -------------------------------------------------

for p in [BASE, INDEX]:
    if p.exists():
        backup = p.with_name(p.name + ".before-premium")
        if not backup.exists():
            shutil.copy2(p, backup)
            print(f"✅ Backup: {backup}")

# -------------------------------------------------
# 2. PREMIUM CSS
# -------------------------------------------------

css = r"""
/* =================================================
   AI ZONE বাংলা — PREMIUM UI
   Neon Dark + Micro Interactions
   ================================================= */

:root {
    --az-bg: #030b1c;
    --az-bg2: #07152d;
    --az-card: rgba(9, 25, 52, .78);
    --az-border: rgba(0, 229, 255, .35);
    --az-cyan: #00e5ff;
    --az-blue: #2979ff;
    --az-purple: #8b5cf6;
    --az-text: #f5fbff;
    --az-muted: #a9bfd8;
    --az-glow: 0 0 25px rgba(0,229,255,.28);
}

/* Page background */
body {
    background:
        radial-gradient(circle at 15% 10%, rgba(0,229,255,.10), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(91,76,255,.10), transparent 30%),
        linear-gradient(135deg, var(--az-bg), var(--az-bg2)) !important;
    color: var(--az-text);
}

/* Navbar */
nav {
    position: sticky !important;
    top: 10px;
    z-index: 1000;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    background: rgba(3,11,28,.78) !important;
    border: 1px solid rgba(0,229,255,.16);
    border-radius: 18px;
    box-shadow: 0 8px 35px rgba(0,0,0,.25);
}

/* Navigation links */
nav a {
    position: relative;
    transition:
        transform .22s ease,
        color .22s ease,
        background .22s ease,
        box-shadow .22s ease;
}

nav a:hover,
nav a:focus-visible {
    transform: translateY(-2px);
    color: #fff !important;
}

/* =================================================
   DEMO 2 — Highlight Quran Button
   ================================================= */

nav a[href="/quran"] {
    display: inline-flex !important;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 9px 15px !important;
    margin: 2px 4px;
    color: #eaffff !important;
    font-weight: 700;
    border: 1px solid var(--az-cyan);
    border-radius: 999px;
    background:
        linear-gradient(
            135deg,
            rgba(0,229,255,.16),
            rgba(41,121,255,.22)
        ) !important;
    box-shadow:
        0 0 10px rgba(0,229,255,.22),
        inset 0 0 12px rgba(0,229,255,.06);
    animation: quranGlow 2.8s ease-in-out infinite;
}

nav a[href="/quran"]:hover,
nav a[href="/quran"]:focus-visible {
    transform: translateY(-3px) scale(1.02);
    box-shadow:
        0 0 12px rgba(0,229,255,.55),
        0 0 30px rgba(0,229,255,.28),
        inset 0 0 15px rgba(0,229,255,.12);
}

@keyframes quranGlow {
    0%,100% {
        box-shadow:
            0 0 8px rgba(0,229,255,.20),
            inset 0 0 8px rgba(0,229,255,.04);
    }
    50% {
        box-shadow:
            0 0 18px rgba(0,229,255,.42),
            0 0 35px rgba(41,121,255,.18),
            inset 0 0 12px rgba(0,229,255,.08);
    }
}

/* =================================================
   Cards — Demo 9 Micro Interactions
   ================================================= */

article,
.card,
.tool-card,
.lesson-card {
    transition:
        transform .25s ease,
        box-shadow .25s ease,
        border-color .25s ease;
}

article:hover,
.card:hover,
.tool-card:hover,
.lesson-card:hover {
    transform: translateY(-5px);
    border-color: rgba(0,229,255,.55);
    box-shadow:
        0 12px 35px rgba(0,0,0,.28),
        0 0 18px rgba(0,229,255,.10);
}

/* Buttons */
button,
.btn,
a.button,
input[type="submit"] {
    transition:
        transform .2s ease,
        box-shadow .2s ease,
        filter .2s ease;
}

button:hover,
.btn:hover,
a.button:hover,
input[type="submit"]:hover {
    transform: translateY(-2px);
    filter: brightness(1.08);
    box-shadow: 0 8px 22px rgba(0,229,255,.18);
}

button:active,
.btn:active,
a.button:active,
input[type="submit"]:active {
    transform: scale(.97);
}

/* =================================================
   Demo 7 — Animated nav indicator
   ================================================= */

nav a::after {
    content: "";
    position: absolute;
    left: 50%;
    bottom: 2px;
    width: 0;
    height: 2px;
    border-radius: 99px;
    background: var(--az-cyan);
    box-shadow: 0 0 8px var(--az-cyan);
    transform: translateX(-50%);
    transition: width .25s ease;
}

nav a:hover::after,
nav a:focus-visible::after {
    width: 55%;
}

nav a[href="/quran"]::after {
    display: none;
}

/* =================================================
   Demo 12 — AI Design Assistant
   ================================================= */

.az-ai-assistant {
    position: relative;
    margin: 35px auto;
    padding: 25px;
    max-width: 900px;
    border: 1px solid rgba(0,229,255,.28);
    border-radius: 24px;
    background:
        linear-gradient(
            145deg,
            rgba(8,27,58,.92),
            rgba(5,15,35,.88)
        );
    box-shadow:
        0 15px 45px rgba(0,0,0,.28),
        0 0 30px rgba(0,229,255,.07);
    overflow: hidden;
}

.az-ai-assistant::before {
    content: "";
    position: absolute;
    inset: -80px;
    background: conic-gradient(
        from 90deg,
        transparent,
        rgba(0,229,255,.10),
        transparent,
        rgba(139,92,246,.08),
        transparent
    );
    animation: azSpin 12s linear infinite;
    pointer-events: none;
}

.az-ai-content {
    position: relative;
    z-index: 1;
}

.az-ai-title {
    margin: 0 0 8px;
    font-size: clamp(22px, 4vw, 34px);
}

.az-ai-subtitle {
    color: var(--az-muted);
    line-height: 1.7;
}

.az-ai-form {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 18px;
}

.az-ai-input {
    flex: 1 1 240px;
    min-width: 0;
    padding: 13px 15px;
    border-radius: 14px;
    border: 1px solid rgba(0,229,255,.25);
    outline: none;
    background: rgba(0,0,0,.22);
    color: white;
    font: inherit;
}

.az-ai-input:focus {
    border-color: var(--az-cyan);
    box-shadow: 0 0 0 3px rgba(0,229,255,.10);
}

.az-ai-generate {
    border: 0;
    border-radius: 14px;
    padding: 13px 20px;
    cursor: pointer;
    color: white;
    font-weight: 700;
    background: linear-gradient(135deg, #147eff, #00bcd4);
}

.az-ai-result {
    display: none;
    margin-top: 18px;
    padding: 16px;
    border-radius: 15px;
    background: rgba(0,229,255,.07);
    border: 1px solid rgba(0,229,255,.18);
    line-height: 1.7;
}

.az-ai-result.show {
    display: block;
    animation: azReveal .35s ease;
}

@keyframes azReveal {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes azSpin {
    to {
        transform: rotate(360deg);
    }
}

/* Mobile */
@media (max-width: 700px) {
    nav {
        top: 5px;
        border-radius: 14px;
    }

    nav a[href="/quran"] {
        padding: 8px 11px !important;
        font-size: .92rem;
    }

    .az-ai-assistant {
        margin: 25px 10px;
        padding: 20px;
        border-radius: 20px;
    }

    .az-ai-form {
        flex-direction: column;
    }

    .az-ai-generate {
        width: 100%;
    }
}

/* Accessibility — reduced motion */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
        transition-duration: .01ms !important;
    }
}
"""

(STATIC / "ai-zone-premium.css").write_text(css, encoding="utf-8")
print("✅ Premium CSS installed")

# -------------------------------------------------
# 3. PREMIUM JS
# -------------------------------------------------

js = r"""
document.addEventListener("DOMContentLoaded", () => {

    /* Demo 7 — active navigation */
    const currentPath = window.location.pathname;

    document.querySelectorAll("nav a").forEach(link => {
        try {
            const url = new URL(link.href, window.location.origin);

            if (url.pathname === currentPath) {
                link.classList.add("az-active");
                link.setAttribute("aria-current", "page");
            }
        } catch (_) {}
    });

    /* Demo 9 — click feedback */
    document.querySelectorAll("button, .btn, nav a").forEach(el => {
        el.addEventListener("click", () => {
            el.classList.add("az-clicked");

            setTimeout(() => {
                el.classList.remove("az-clicked");
            }, 220);
        });
    });

    /* Demo 12 — AI-assisted design demo */
    const generate = document.querySelector(".az-ai-generate");
    const input = document.querySelector(".az-ai-input");
    const result = document.querySelector(".az-ai-result");

    if (generate && input && result) {
        generate.addEventListener("click", () => {
            const value = input.value.trim();

            if (!value) {
                result.textContent =
                    "💡 আগে আপনার ডিজাইনের ধারণা লিখুন।";
                result.classList.add("show");
                return;
            }

            result.innerHTML =
                "✨ আপনার ইনপুট অনুযায়ী একটি ডিজাইন ধারণা প্রস্তুত হয়েছে।" +
                "<br><br>" +
                "🎨 Dark + Cyan theme<br>" +
                "📱 Responsive mobile layout<br>" +
                "✨ Subtle micro-interactions<br>" +
                "📖 Highlighted Quran learning section";

            result.classList.add("show");
        });
    }
});
"""

(STATIC / "ai-zone-premium.js").write_text(js, encoding="utf-8")
print("✅ Premium JS installed")

# -------------------------------------------------
# 4. BASE.HTML
# -------------------------------------------------

if BASE.exists():
    s = BASE.read_text(encoding="utf-8")

    # Add CSS only once
    css_tag = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'ai-zone-premium.css\') }}">'

    if "ai-zone-premium.css" not in s:
        if "</head>" in s:
            s = s.replace("</head>", f"    {css_tag}\n</head>", 1)
        else:
            s += "\n" + css_tag + "\n"
        print("✅ Premium CSS linked")

    # Make Quran button identifiable
    pattern = r'<a([^>]*href=["\']\/quran["\'][^>]*)>(.*?)</a>'

    def quran_replace(m):
        attrs = m.group(1)
        content = m.group(2)

        if "aria-label=" not in attrs:
            attrs += ' aria-label="কুরআন শিক্ষা"'

        return f'<a{attrs}>{content}</a>'

    s = re.sub(pattern, quran_replace, s, count=1, flags=re.S)

    # Add JS only once
    js_tag = '<script src="{{ url_for(\'static\', filename=\'ai-zone-premium.js\') }}" defer></script>'

    if "ai-zone-premium.js" not in s:
        if "</body>" in s:
            s = s.replace("</body>", f"    {js_tag}\n</body>", 1)
        else:
            s += "\n" + js_tag + "\n"
        print("✅ Premium JS linked")

    BASE.write_text(s, encoding="utf-8")
    print("✅ base.html updated")

# -------------------------------------------------
# 5. AI DESIGN ASSISTANT ON HOMEPAGE
# -------------------------------------------------

if INDEX.exists():
    s = INDEX.read_text(encoding="utf-8")

    if "az-ai-assistant" not in s:

        assistant = r'''
<section class="az-ai-assistant" aria-labelledby="az-ai-title">
    <div class="az-ai-content">

        <h2 id="az-ai-title" class="az-ai-title">
            ✨ AI Design Assistant
        </h2>

        <p class="az-ai-subtitle">
            আপনার ওয়েবসাইটের জন্য কী ধরনের ডিজাইন চান?
            নিচে লিখুন—একটি premium design concept দেখুন।
        </p>

        <div class="az-ai-form">
            <input
                class="az-ai-input"
                type="text"
                placeholder="যেমন: আমার ওয়েবসাইটের জন্য neon dark design চাই"
                aria-label="Design idea"
            >

            <button class="az-ai-generate" type="button">
                Generate Design ✨
            </button>
        </div>

        <div class="az-ai-result" aria-live="polite"></div>

    </div>
</section>
'''

        if "</body>" in s:
            s = s.replace("</body>", assistant + "\n</body>", 1)
        else:
            s += "\n" + assistant

        INDEX.write_text(s, encoding="utf-8")
        print("✅ AI Design Assistant added to homepage")
    else:
        print("ℹ️ AI Design Assistant already exists")

# -------------------------------------------------
# 6. CHECKS
# -------------------------------------------------

print()
print("=== Checking files ===")

required = [
    STATIC / "ai-zone-premium.css",
    STATIC / "ai-zone-premium.js",
]

for p in required:
    if p.exists():
        print(f"✅ {p}")
    else:
        print(f"❌ Missing: {p}")

print()
print("==========================================")
print("✅ PREMIUM UI INSTALLATION COMPLETE")
print("==========================================")
print()
print("Demo 4 → Neon Dark UI")
print("Demo 7 → Animated Navigation")
print("Demo 9 → Micro-interactions")
print("Demo 12 → AI Design Assistant")
print()
print("Quran lessons were NOT modified.")
