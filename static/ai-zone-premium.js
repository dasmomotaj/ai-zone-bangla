
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
