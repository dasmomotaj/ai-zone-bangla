(function () {

    "use strict";

    const STORAGE_KEY = "ai_zone_quran_progress_v1";
    const TOTAL_LESSONS = 20;

    function getProgress() {
        try {
            const saved = JSON.parse(
                localStorage.getItem(STORAGE_KEY) || "[]"
            );

            if (!Array.isArray(saved)) {
                return [];
            }

            return [...new Set(
                saved
                    .map(Number)
                    .filter(
                        n => n >= 1 && n <= TOTAL_LESSONS
                    )
            )].sort((a, b) => a - b);

        } catch (error) {
            return [];
        }
    }

    function saveProgress(list) {
        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify(
                [...new Set(list)]
                    .sort((a, b) => a - b)
            )
        );
    }

    function markComplete(lessonId) {

        const id = Number(lessonId);

        if (
            !Number.isInteger(id) ||
            id < 1 ||
            id > TOTAL_LESSONS
        ) {
            return;
        }

        const progress = getProgress();

        if (!progress.includes(id)) {
            progress.push(id);
        }

        saveProgress(progress);

        render();
    }

    function isComplete(lessonId) {
        return getProgress().includes(
            Number(lessonId)
        );
    }

    function render() {

        const panel = document.querySelector(
            "[data-quran-progress]"
        );

        if (!panel) {
            return;
        }

        const lessonId = Number(
            panel.dataset.lessonId
        );

        if (
            !Number.isInteger(lessonId) ||
            lessonId < 1 ||
            lessonId > TOTAL_LESSONS
        ) {
            return;
        }

        const progress = getProgress();

        const completedCount = progress.length;

        const percent = Math.round(
            (completedCount / TOTAL_LESSONS) * 100
        );

        const fill = panel.querySelector(
            ".quran-progress-fill"
        );

        const value = panel.querySelector(
            ".quran-progress-value"
        );

        const info = panel.querySelector(
            ".quran-progress-info"
        );

        const button = panel.querySelector(
            ".quran-complete-button"
        );

        if (fill) {
            fill.style.width = percent + "%";
        }

        if (value) {
            value.textContent = percent + "%";
        }

        if (info) {
            info.textContent =
                completedCount +
                " / " +
                TOTAL_LESSONS +
                "টি পাঠ সম্পন্ন";
        }

        if (button && isComplete(lessonId)) {

            button.textContent =
                "✓ এই পাঠ সম্পন্ন হয়েছে";

            button.classList.add("completed");

        } else if (button) {

            button.textContent =
                "✓ পাঠটি সম্পন্ন করুন";

            button.classList.remove("completed");
        }
    }

    window.AIZoneQuranComplete = markComplete;

    document.addEventListener(
        "DOMContentLoaded",
        render
    );

})();

/* AI Zone বাংলা — Quran Academy Dashboard Progress Summary */

(function () {
  "use strict";

  const STORAGE_KEY = "ai_zone_quran_progress_v1";
  const TOTAL = 20;

  function getCompleted() {
    try {
      const data = JSON.parse(
        localStorage.getItem(STORAGE_KEY) || "{}"
      );

      return Object.keys(data)
        .map(Number)
        .filter(
          id => Number.isInteger(id) &&
                id >= 1 &&
                id <= TOTAL &&
                data[id]
        )
        .sort((a, b) => a - b);
    } catch (error) {
      return [];
    }
  }

  function updateDashboard() {
    const completed = getCompleted();
    const count = completed.length;
    const remaining = Math.max(TOTAL - count, 0);
    const percent = Math.round((count / TOTAL) * 100);

    const next = Array.from(
      { length: TOTAL },
      (_, i) => i + 1
    ).find(id => !completed.includes(id)) || TOTAL;

    const completedEl =
      document.getElementById("quranCompletedCount");

    const remainingEl =
      document.getElementById("quranRemainingCount");

    const percentEl =
      document.getElementById("quranProgressPercent");

    const nextEl =
      document.getElementById("quranNextLesson");

    const fillEl =
      document.getElementById("quranAcademyProgressFill");

    const textEl =
      document.getElementById("quranProgressText");

    const buttonEl =
      document.getElementById("quranContinueButton");

    if (completedEl) completedEl.textContent = count;
    if (remainingEl) remainingEl.textContent = remaining;
    if (percentEl) percentEl.textContent = percent + "%";
    if (nextEl) nextEl.textContent = next;

    if (fillEl) {
      fillEl.style.width = percent + "%";
    }

    if (textEl) {
      textEl.textContent =
        count + " / " + TOTAL + "টি পাঠ সম্পন্ন";
    }

    if (buttonEl) {
      buttonEl.href =
        "/quran/lesson/" + next;

      buttonEl.textContent =
        count === TOTAL
          ? "✓ সব পাঠ সম্পন্ন"
          : "▶ Lesson " + next + " চালিয়ে যান";
    }
  }

  document.addEventListener(
    "DOMContentLoaded",
    updateDashboard
  );

  window.addEventListener(
    "storage",
    updateDashboard
  );

  window.AIZoneRefreshQuranDashboard =
    updateDashboard;

})();

/* =========================================================
   AI ZONE QURAN ACADEMY — UNIFIED STATUS SYNC
   Session 21.3
   ========================================================= */

(function () {
    const PROGRESS_KEY = "ai_zone_quran_progress_v1";
    const QUIZ_KEY = "ai_zone_quran_quiz_v1";
    const TOTAL = 20;

    function readJSON(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            return raw ? JSON.parse(raw) : fallback;
        } catch (e) {
            return fallback;
        }
    }

    function getCompletedLessons() {
        const data = readJSON(PROGRESS_KEY, {});
        const completed = [];

        for (let i = 1; i <= TOTAL; i++) {
            if (data[String(i)] === true || data[i] === true) {
                completed.push(i);
            }
        }

        return completed;
    }

    function getQuizResults() {
        return readJSON(QUIZ_KEY, {});
    }

    function syncAcademyStatus() {
        const completed = getCompletedLessons();
        const quizzes = getQuizResults();

        document.querySelectorAll("[data-quran-lesson-card]").forEach(card => {
            const lessonId = Number(card.dataset.quranLessonCard);
            const status = card.querySelector("[data-quran-card-status]");
            const quizStatus = card.querySelector("[data-quran-card-quiz]");

            const isCompleted = completed.includes(lessonId);
            const quiz = quizzes[String(lessonId)] || quizzes[lessonId];

            if (status) {
                if (isCompleted) {
                    status.textContent = "✓ সম্পন্ন";
                    status.classList.add("is-complete");
                } else {
                    status.textContent = "শুরু করুন";
                    status.classList.remove("is-complete");
                }
            }

            if (quizStatus && quiz) {
                if (quiz.passed) {
                    quizStatus.textContent = "Quiz ✓";
                    quizStatus.classList.add("is-passed");
                } else if (typeof quiz.score === "number") {
                    quizStatus.textContent = "Quiz " + quiz.score + "%";
                    quizStatus.classList.remove("is-passed");
                }
            }
        });

        document.documentElement.dataset.quranCompleted =
            String(completed.length);

        document.documentElement.dataset.quranTotal =
            String(TOTAL);
    }

    window.AIZoneSyncQuranAcademyStatus = syncAcademyStatus;

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", syncAcademyStatus);
    } else {
        syncAcademyStatus();
    }

    window.addEventListener("storage", function (event) {
        if (
            event.key === PROGRESS_KEY ||
            event.key === QUIZ_KEY
        ) {
            syncAcademyStatus();
        }
    });
})();

/* =========================================================
   AI ZONE QURAN ACADEMY — SMART CONTINUE
   Session 21.5
   ========================================================= */

(function () {
    const PROGRESS_KEY = "ai_zone_quran_progress_v1";
    const TOTAL = 20;

    function readProgress() {
        try {
            return JSON.parse(
                localStorage.getItem(PROGRESS_KEY) || "{}"
            );
        } catch (e) {
            return {};
        }
    }

    function isCompleted(progress, lessonId) {
        return (
            progress[String(lessonId)] === true ||
            progress[lessonId] === true
        );
    }

    function getNextLesson() {
        const progress = readProgress();

        for (let i = 1; i <= TOTAL; i++) {
            if (!isCompleted(progress, i)) {
                return i;
            }
        }

        return null;
    }

    function updateContinueButton() {
        const button =
            document.getElementById("quranContinueButton");

        if (!button) {
            return;
        }

        const nextLesson = getNextLesson();

        if (nextLesson === null) {
            button.textContent = "✓ Academy Complete";
            button.removeAttribute("href");
            button.classList.add("academy-complete");
            button.setAttribute("aria-disabled", "true");
            return;
        }

        button.textContent =
            "▶ Continue Lesson " + nextLesson;

        button.href =
            nextLesson === 1
                ? "/quran/lesson/1"
                : "/quran/lesson/" + nextLesson;

        button.classList.remove("academy-complete");
        button.removeAttribute("aria-disabled");
    }

    window.AIZoneSmartContinue = updateContinueButton;

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            updateContinueButton
        );
    } else {
        updateContinueButton();
    }

    window.addEventListener("storage", function (event) {
        if (event.key === PROGRESS_KEY) {
            updateContinueButton();
        }
    });
})();
