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

/* AI-ZONE-QURAN-AUDIO-JS-START */
(function () {
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

    function formatTime(seconds) {
        if (!Number.isFinite(seconds) || seconds < 0) return "00:00";
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return String(mins).padStart(2, "0") + ":" +
               String(secs).padStart(2, "0");
    }

    function updateProgress() {
        const duration = audio.duration || 0;
        const current = audio.currentTime || 0;
        const percent = duration ? (current / duration) * 100 : 0;

        fill.style.width = percent + "%";
        track.setAttribute("aria-valuenow", String(Math.round(percent)));

        timeText.textContent =
            formatTime(current) + " / " + formatTime(duration);
    }

    function setStatus(text) {
        status.textContent = text;
    }

    playBtn.addEventListener("click", function () {
        if (!audio.src) {
            setStatus("Audio source not connected");
            return;
        }

        if (audio.paused) {
            audio.play()
                .then(function () {
                    playBtn.textContent = "⏸ Pause";
                    setStatus("Playing");
                })
                .catch(function () {
                    setStatus("Unable to play");
                });
        } else {
            audio.pause();
            playBtn.textContent = "▶ Play";
            setStatus("Paused");
        }
    });

    resetBtn.addEventListener("click", function () {
        audio.pause();
        audio.currentTime = 0;
        playBtn.textContent = "▶ Play";
        setStatus("Ready");
        updateProgress();
    });

    volume.addEventListener("input", function () {
        audio.volume = Number(volume.value);
    });

    track.addEventListener("click", function (event) {
        if (!audio.duration) return;

        const rect = track.getBoundingClientRect();
        const ratio = Math.max(
            0,
            Math.min(1, (event.clientX - rect.left) / rect.width)
        );

        audio.currentTime = ratio * audio.duration;
        updateProgress();
    });

    audio.addEventListener("timeupdate", updateProgress);

    audio.addEventListener("loadedmetadata", function () {
        setStatus("Ready");
        updateProgress();
    });

    audio.addEventListener("play", function () {
        playBtn.textContent = "⏸ Pause";
        setStatus("Playing");
    });

    audio.addEventListener("pause", function () {
        if (!audio.ended) {
            playBtn.textContent = "▶ Play";
            setStatus("Paused");
        }
    });

    audio.addEventListener("ended", function () {
        playBtn.textContent = "▶ Play";
        setStatus("Finished");
        updateProgress();
    });

    audio.addEventListener("error", function () {
        setStatus("Audio source unavailable");
    });

    window.AIZoneQuranAudio = {
        setSource: function (src) {
            if (!src) return false;
            audio.src = src;
            audio.load();
            setStatus("Ready");
            return true;
        },
        play: function () {
            return audio.play();
        },
        pause: function () {
            audio.pause();
        },
        reset: function () {
            audio.pause();
            audio.currentTime = 0;
            updateProgress();
        }
    };

    updateProgress();
})();
/* AI-ZONE-QURAN-AUDIO-JS-END */


// AI-ZONE-QURAN-REVISION-JS-START
(function () {
    "use strict";

    const TOTAL = 20;
    const QUIZ_KEY = "ai_zone_quran_quiz_v1";
    const REVISION_KEY = "ai_zone_quran_revision_v1";

    function readJSON(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            return raw ? JSON.parse(raw) : fallback;
        } catch (e) {
            return fallback;
        }
    }

    function getQuizData() {
        const data = readJSON(QUIZ_KEY, {});
        return data && typeof data === "object" ? data : {};
    }

    function getResults() {
        const data = getQuizData();

        if (Array.isArray(data)) {
            return data;
        }

        if (Array.isArray(data.results)) {
            return data.results;
        }

        return [];
    }

    function normalizeLessonId(item) {
        const value =
            item.lessonId ??
            item.lesson ??
            item.lesson_id ??
            item.id;

        const id = Number(value);

        return Number.isInteger(id) && id >= 1 && id <= TOTAL
            ? id
            : null;
    }

    function normalizeScore(item) {
        const value =
            item.score ??
            item.percent ??
            item.percentage ??
            item.result;

        const score = Number(value);

        return Number.isFinite(score) ? score : null;
    }

    function buildRevision() {
        const results = getResults();
        const lessonMap = {};

        for (const item of results) {
            if (!item || typeof item !== "object") {
                continue;
            }

            const lessonId = normalizeLessonId(item);
            const score = normalizeScore(item);

            if (lessonId === null || score === null) {
                continue;
            }

            lessonMap[lessonId] = {
                lessonId: lessonId,
                score: Math.max(0, Math.min(100, score)),
                weak: score < 70,
                updatedAt: Date.now()
            };
        }

        const weakLessons = Object.values(lessonMap)
            .filter(item => item.weak)
            .sort((a, b) => a.score - b.score);

        const revision = {
            updatedAt: Date.now(),
            weakLessons: weakLessons,
            allLessons: Object.values(lessonMap),
            weakCount: weakLessons.length,
            totalTracked: Object.keys(lessonMap).length
        };

        try {
            localStorage.setItem(
                REVISION_KEY,
                JSON.stringify(revision)
            );
        } catch (e) {
            // localStorage may be unavailable.
        }

        return revision;
    }

    function getRevision() {
        const saved = readJSON(REVISION_KEY, null);

        if (
            saved &&
            typeof saved === "object" &&
            Array.isArray(saved.weakLessons)
        ) {
            return saved;
        }

        return buildRevision();
    }

    function render() {
        const panel = document.getElementById(
            "quranSmartRevision"
        );

        if (!panel) {
            return;
        }

        const revision = buildRevision();

        const count = document.getElementById(
            "quranRevisionWeakCount"
        );

        const status = document.getElementById(
            "quranRevisionStatus"
        );

        const list = document.getElementById(
            "quranRevisionList"
        );

        if (count) {
            count.textContent = String(revision.weakCount);
        }

        if (status) {
            if (revision.totalTracked === 0) {
                status.textContent =
                    "এখনও কোনো Quiz result পাওয়া যায়নি। আগে Quiz দিন।";
            } else if (revision.weakCount === 0) {
                status.textContent =
                    "দারুণ! এখন পর্যন্ত কোনো দুর্বল Lesson শনাক্ত হয়নি।";
            } else {
                status.textContent =
                    revision.weakCount +
                    "টি Lesson Revision করার পরামর্শ দেওয়া হচ্ছে।";
            }
        }

        if (list) {
            if (revision.weakLessons.length === 0) {
                list.innerHTML =
                    '<div class="revision-empty">🎉 Revision queue খালি।</div>';
                return;
            }

            list.innerHTML = revision.weakLessons.map(function (item) {
                return (
                    '<div class="revision-item">' +
                        '<div class="revision-item-info">' +
                            '<strong>Lesson ' +
                            item.lessonId +
                            '</strong>' +
                            '<span>Quiz Score: ' +
                            item.score +
                            '%</span>' +
                        '</div>' +
                        '<a class="revision-study-btn" href="/quran/lesson/' +
                            item.lessonId +
                        '">Revision করুন →</a>' +
                    '</div>'
                );
            }).join("");
        }
    }

    window.AIZoneQuranRevision = {
        refresh: render,
        rebuild: buildRevision,
        getRevision: getRevision
    };

    document.addEventListener("DOMContentLoaded", render);

    window.addEventListener("storage", function (event) {
        if (event.key === QUIZ_KEY) {
            render();
        }
    });

})();
// AI-ZONE-QURAN-REVISION-JS-END


// AI-ZONE-QURAN-REVISION-PRIORITY-JS-START
(function () {
    "use strict";

    const TOTAL = 20;
    const QUIZ_KEY = "ai_zone_quran_quiz_v1";
    const REVISION_KEY = "ai_zone_quran_revision_v1";
    const PRIORITY_KEY = "ai_zone_quran_revision_priority_v1";

    function readJSON(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            return raw ? JSON.parse(raw) : fallback;
        } catch (e) {
            return fallback;
        }
    }

    function getQuizData() {
        const data = readJSON(QUIZ_KEY, {});

        if (Array.isArray(data)) {
            return data;
        }

        if (data && Array.isArray(data.results)) {
            return data.results;
        }

        return [];
    }

    function getLessonId(item) {
        const value =
            item.lessonId ??
            item.lesson ??
            item.lesson_id ??
            item.id;

        const id = Number(value);

        if (
            Number.isInteger(id) &&
            id >= 1 &&
            id <= TOTAL
        ) {
            return id;
        }

        return null;
    }

    function getScore(item) {
        const value =
            item.score ??
            item.percent ??
            item.percentage ??
            item.result;

        const score = Number(value);

        return Number.isFinite(score)
            ? Math.max(0, Math.min(100, score))
            : null;
    }

    function buildPriorityQueue() {
        const results = getQuizData();
        const latest = {};

        for (const item of results) {
            if (!item || typeof item !== "object") {
                continue;
            }

            const lessonId = getLessonId(item);
            const score = getScore(item);

            if (lessonId === null || score === null) {
                continue;
            }

            const timestamp =
                Number(
                    item.updatedAt ??
                    item.completedAt ??
                    item.timestamp ??
                    item.createdAt ??
                    0
                ) || 0;

            if (
                !latest[lessonId] ||
                timestamp >= latest[lessonId].timestamp
            ) {
                latest[lessonId] = {
                    lessonId: lessonId,
                    score: score,
                    timestamp: timestamp
                };
            }
        }

        const queue = Object.values(latest)
            .filter(item => item.score < 70)
            .map(item => {
                let priority = "LOW";
                let label = "সাধারণ Revision";

                if (item.score < 40) {
                    priority = "HIGH";
                    label = "জরুরি Revision";
                } else if (item.score < 55) {
                    priority = "MEDIUM";
                    label = "গুরুত্বপূর্ণ Revision";
                }

                return {
                    lessonId: item.lessonId,
                    score: item.score,
                    priority: priority,
                    label: label,
                    timestamp: item.timestamp
                };
            })
            .sort(function (a, b) {
                if (a.score !== b.score) {
                    return a.score - b.score;
                }

                return a.lessonId - b.lessonId;
            });

        const data = {
            updatedAt: Date.now(),
            totalWeak: queue.length,
            high: queue.filter(
                item => item.priority === "HIGH"
            ).length,
            medium: queue.filter(
                item => item.priority === "MEDIUM"
            ).length,
            low: queue.filter(
                item => item.priority === "LOW"
            ).length,
            queue: queue
        };

        try {
            localStorage.setItem(
                PRIORITY_KEY,
                JSON.stringify(data)
            );
        } catch (e) {
            // Safe fallback when storage is unavailable.
        }

        return data;
    }

    function renderPriority() {
        const panel = document.getElementById(
            "quranRevisionPriority"
        );

        if (!panel) {
            return;
        }

        const data = buildPriorityQueue();

        const high = document.getElementById(
            "quranRevisionHigh"
        );

        const medium = document.getElementById(
            "quranRevisionMedium"
        );

        const low = document.getElementById(
            "quranRevisionLow"
        );

        const list = document.getElementById(
            "quranRevisionPriorityList"
        );

        const status = document.getElementById(
            "quranRevisionPriorityStatus"
        );

        if (high) {
            high.textContent = String(data.high);
        }

        if (medium) {
            medium.textContent = String(data.medium);
        }

        if (low) {
            low.textContent = String(data.low);
        }

        if (status) {
            if (data.totalWeak === 0) {
                status.textContent =
                    "এখনও কোনো Priority Revision প্রয়োজন নেই।";
            } else {
                status.textContent =
                    "কম score-এর Lesson আগে Revision করার জন্য সাজানো হয়েছে।";
            }
        }

        if (list) {
            if (data.queue.length === 0) {
                list.innerHTML =
                    '<div class="revision-priority-empty">' +
                    '🎉 সব tracked Lesson আপাতত ভালো অবস্থায় আছে।' +
                    '</div>';
                return;
            }

            list.innerHTML = data.queue.map(function (item) {
                const badgeClass =
                    item.priority.toLowerCase();

                return (
                    '<div class="revision-priority-item">' +

                        '<div class="revision-priority-main">' +
                            '<div class="revision-priority-title">' +
                                'Lesson ' +
                                item.lessonId +
                            '</div>' +

                            '<div class="revision-priority-score">' +
                                'Quiz Score: ' +
                                item.score +
                                '%' +
                            '</div>' +
                        '</div>' +

                        '<span class="revision-priority-badge ' +
                            badgeClass +
                        '">' +
                            item.label +
                        '</span>' +

                        '<a class="revision-priority-btn" ' +
                           'href="/quran/lesson/' +
                           item.lessonId +
                        '">' +
                            'Revision →' +
                        '</a>' +

                    '</div>'
                );
            }).join("");
        }
    }

    window.AIZoneQuranRevisionPriority = {
        refresh: renderPriority,
        rebuild: buildPriorityQueue,
        getQueue: buildPriorityQueue
    };

    document.addEventListener(
        "DOMContentLoaded",
        renderPriority
    );

    window.addEventListener(
        "storage",
        function (event) {
            if (
                event.key === QUIZ_KEY ||
                event.key === REVISION_KEY
            ) {
                renderPriority();
            }
        }
    );

})();
// AI-ZONE-QURAN-REVISION-PRIORITY-JS-END


// AI-ZONE-QURAN-MISTAKE-TRACKER-JS-START
(function () {
    "use strict";

    const TOTAL = 20;

    const QUIZ_KEY =
        "ai_zone_quran_quiz_v1";

    const MISTAKE_KEY =
        "ai_zone_quran_mistakes_v1";

    function readJSON(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            return raw ? JSON.parse(raw) : fallback;
        } catch (e) {
            return fallback;
        }
    }

    function writeJSON(key, value) {
        try {
            localStorage.setItem(
                key,
                JSON.stringify(value)
            );
            return true;
        } catch (e) {
            return false;
        }
    }

    function lessonIdOf(item) {
        if (!item || typeof item !== "object") {
            return null;
        }

        const value =
            item.lessonId ??
            item.lesson ??
            item.lesson_id;

        const id = Number(value);

        if (
            Number.isInteger(id) &&
            id >= 1 &&
            id <= TOTAL
        ) {
            return id;
        }

        return null;
    }

    function questionIdOf(item, index) {
        if (!item || typeof item !== "object") {
            return "q-" + String(index + 1);
        }

        const value =
            item.questionId ??
            item.question_id ??
            item.qid ??
            item.id;

        if (
            value !== undefined &&
            value !== null &&
            String(value).trim()
        ) {
            return String(value);
        }

        return "q-" + String(index + 1);
    }

    function isWrong(item) {
        if (!item || typeof item !== "object") {
            return false;
        }

        if (
            item.correct === false ||
            item.isCorrect === false ||
            item.is_correct === false ||
            item.correctAnswer === false
        ) {
            return true;
        }

        if (
            item.correct === true ||
            item.isCorrect === true ||
            item.is_correct === true
        ) {
            return false;
        }

        if (
            item.selectedAnswer !== undefined &&
            item.correctAnswer !== undefined
        ) {
            return String(item.selectedAnswer) !==
                   String(item.correctAnswer);
        }

        if (
            item.selected !== undefined &&
            item.correct !== undefined &&
            typeof item.correct !== "boolean"
        ) {
            return String(item.selected) !==
                   String(item.correct);
        }

        return false;
    }

    function extractQuestionResults(data) {
        const output = [];

        function inspectCollection(
            collection,
            lessonFallback
        ) {
            if (!Array.isArray(collection)) {
                return;
            }

            collection.forEach(function (item, index) {
                if (!item || typeof item !== "object") {
                    return;
                }

                const lessonId =
                    lessonIdOf(item) ||
                    lessonFallback;

                if (!lessonId) {
                    return;
                }

                output.push({
                    lessonId: lessonId,
                    questionId:
                        questionIdOf(item, index),
                    wrong: isWrong(item),
                    question:
                        String(
                            item.question ??
                            item.text ??
                            item.prompt ??
                            ""
                        ).trim(),
                    timestamp:
                        Number(
                            item.timestamp ??
                            item.completedAt ??
                            item.createdAt ??
                            Date.now()
                        ) || Date.now()
                });
            });
        }

        if (Array.isArray(data)) {
            data.forEach(function (item) {
                if (!item || typeof item !== "object") {
                    return;
                }

                const lessonId = lessonIdOf(item);

                if (
                    Array.isArray(item.questions)
                ) {
                    inspectCollection(
                        item.questions,
                        lessonId
                    );
                }

                if (
                    Array.isArray(item.answers)
                ) {
                    inspectCollection(
                        item.answers,
                        lessonId
                    );
                }

                if (
                    Array.isArray(item.results)
                ) {
                    inspectCollection(
                        item.results,
                        lessonId
                    );
                }
            });
        }

        if (
            data &&
            typeof data === "object" &&
            Array.isArray(data.results)
        ) {
            data.results.forEach(function (item) {
                if (!item || typeof item !== "object") {
                    return;
                }

                const lessonId = lessonIdOf(item);

                if (Array.isArray(item.questions)) {
                    inspectCollection(
                        item.questions,
                        lessonId
                    );
                }

                if (Array.isArray(item.answers)) {
                    inspectCollection(
                        item.answers,
                        lessonId
                    );
            });
        }

        return output;
    }

    function buildMistakes() {
        const quizData =
            readJSON(QUIZ_KEY, {});

        const previous =
            readJSON(MISTAKE_KEY, {});

        const mistakes =
            previous &&
            typeof previous === "object" &&
            previous.questions
                ? previous.questions
                : {};

        const results =
            extractQuestionResults(quizData);

        results.forEach(function (item) {
            const key =
                String(item.lessonId) +
                ":" +
                String(item.questionId);

            if (!mistakes[key]) {
                mistakes[key] = {
                    lessonId: item.lessonId,
                    questionId: item.questionId,
                    question: item.question,
                    wrongCount: 0,
                    correctCount: 0,
                    lastResult: null,
                    lastAttempt: 0
                };
            }

            if (item.question) {
                mistakes[key].question =
                    item.question;
            }

            if (item.wrong) {
                mistakes[key].wrongCount += 1;
                mistakes[key].lastResult = "wrong";
            } else {
                mistakes[key].correctCount += 1;
                mistakes[key].lastResult = "correct";
            }

            mistakes[key].lastAttempt =
                item.timestamp;
        });

        const weak = Object.values(mistakes)
            .filter(function (item) {
                return (
                    item.wrongCount > 0 &&
                    item.lastResult === "wrong"
                );
            })
            .sort(function (a, b) {
                if (
                    a.wrongCount !==
                    b.wrongCount
                ) {
                    return (
                        b.wrongCount -
                        a.wrongCount
                    );
                }

                return (
                    a.lessonId -
                    b.lessonId
                );
            });

        const data = {
            updatedAt: Date.now(),
            totalTracked:
                Object.keys(mistakes).length,
            weakQuestions: weak.length,
            questions: mistakes,
            queue: weak
        };

        writeJSON(MISTAKE_KEY, data);

        return data;
    }

    function render() {
        const panel =
            document.getElementById(
                "quranMistakeTracker"
            );

        if (!panel) {
            return;
        }

        const data = buildMistakes();

        const count =
            document.getElementById(
                "quranMistakeCount"
            );

        const list =
            document.getElementById(
                "quranMistakeList"
            );

        const status =
            document.getElementById(
                "quranMistakeStatus"
            );

        if (count) {
            count.textContent =
                String(data.weakQuestions);
        }

        if (status) {
            status.textContent =
                data.weakQuestions === 0
                    ? "এখনও কোনো প্রশ্নের ভুল Revision দরকার নেই।"
                    : "যে প্রশ্নগুলোতে ভুল হচ্ছে সেগুলো Revision-এর জন্য রাখা হয়েছে।";
        }

        if (!list) {
            return;
        }

        if (data.queue.length === 0) {
            list.innerHTML =
                '<div class="quran-mistake-empty">' +
                '🎉 এখনো কোনো tracked mistake নেই।' +
                '</div>';
            return;
        }

        list.innerHTML =
            data.queue.slice(0, 10).map(
                function (item) {

                    const questionText =
                        item.question
                            ? item.question
                            : "Question " +
                              item.questionId;

                    return (
                        '<div class="quran-mistake-item">' +

                            '<div>' +
                                '<div class="quran-mistake-title">' +
                                    'Lesson ' +
                                    item.lessonId +
                                '</div>' +

                                '<div class="quran-mistake-question">' +
                                    questionText +
                                '</div>' +

                                '<div class="quran-mistake-count">' +
                                    'ভুল: ' +
                                    item.wrongCount +
                                    ' বার' +
                                '</div>' +
                            '</div>' +

                            '<a ' +
                              'class="quran-mistake-btn" ' +
                              'href="/quran/lesson/' +
                              item.lessonId +
                            '">' +
                                'Practice →' +
                            '</a>' +

                        '</div>'
                    );
                }
            ).join("");
    }

    window.AIZoneQuranMistakeTracker = {
        refresh: render,
        rebuild: buildMistakes,
        getData: buildMistakes
    };

    document.addEventListener(
        "DOMContentLoaded",
        render
    );

    window.addEventListener(
        "storage",
        function (event) {
            if (
                event.key === QUIZ_KEY ||
                event.key === MISTAKE_KEY
            ) {
                render();
            }
        }
    );

})();
// AI-ZONE-QURAN-MISTAKE-TRACKER-JS-END

// AI-ZONE-QURAN-REVISION-RETEST-JS-START
(function () {
    "use strict";

    const QUIZ_KEY = "ai_zone_quran_quiz_v1";
    const MISTAKE_KEY = "ai_zone_quran_mistakes_v1";
    const RETEST_KEY = "ai_zone_quran_retest_v1";
    const PASS_SCORE = 70;

    function safeJSON(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            if (!raw) return fallback;
            const parsed = JSON.parse(raw);
            return parsed == null ? fallback : parsed;
        } catch (e) {
            return fallback;
        }
    }

    function saveJSON(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            return false;
        }
    }

    function lessonIdOf(item) {
        if (!item || typeof item !== "object") return null;

        const raw =
            item.lessonId ??
            item.lesson_id ??
            item.lesson ??
            item.id;

        const id = Number(raw);

        if (!Number.isInteger(id) || id < 1 || id > 20) {
            return null;
        }

        return id;
    }

    function scoreOf(item) {
        if (!item || typeof item !== "object") return null;

        const raw =
            item.score ??
            item.percent ??
            item.percentage ??
            item.result;

        const score = Number(raw);

        if (!Number.isFinite(score)) return null;

        return Math.max(0, Math.min(100, score));
    }

    function timestampOf(item) {
        if (!item || typeof item !== "object") return 0;

        const raw =
            item.timestamp ??
            item.time ??
            item.createdAt ??
            item.updatedAt ??
            item.attemptedAt;

        const value = Date.parse(raw);

        return Number.isFinite(value) ? value : 0;
    }

    function extractQuizResults(data) {
        if (Array.isArray(data)) return data;

        if (!data || typeof data !== "object") return [];

        if (Array.isArray(data.results)) return data.results;
        if (Array.isArray(data.attempts)) return data.attempts;
        if (Array.isArray(data.quizzes)) return data.quizzes;

        return [];
    }

    function getLatestScores() {
        const data = safeJSON(QUIZ_KEY, []);
        const results = extractQuizResults(data);

        const latest = {};

        results.forEach(item => {
            const lessonId = lessonIdOf(item);
            const score = scoreOf(item);

            if (lessonId === null || score === null) return;

            const old = latest[lessonId];

            if (!old || timestampOf(item) >= timestampOf(old)) {
                latest[lessonId] = item;
            }
        });

        return latest;
    }

    function getMistakes() {
        const data = safeJSON(MISTAKE_KEY, {});

        if (Array.isArray(data)) {
            return data;
        }

        if (data && Array.isArray(data.mistakes)) {
            return data.mistakes;
        }

        return [];
    }

    function normalizeMistakes() {
        const mistakes = getMistakes();

        return mistakes
            .map(item => {
                const lessonId = lessonIdOf(item);
                if (lessonId === null) return null;

                return {
                    ...item,
                    lessonId
                };
            })
            .filter(Boolean);
    }

    function buildRetestData() {
        const latestScores = getLatestScores();
        const mistakes = normalizeMistakes();

        const previous = safeJSON(RETEST_KEY, {});
        const history = previous.history && typeof previous.history === "object"
            ? previous.history
            : {};

        const queue = [];
        const improved = [];
        const stillWeak = [];

        mistakes.forEach(item => {
            const lessonId = item.lessonId;

            const latest = latestScores[lessonId];
            const currentScore = latest ? scoreOf(latest) : null;

            const previousAttempt =
                history[String(lessonId)] || null;

            const previousScore =
                previousAttempt &&
                Number.isFinite(Number(previousAttempt.score))
                    ? Number(previousAttempt.score)
                    : null;

            let status = "needs-retest";

            if (currentScore !== null && currentScore >= PASS_SCORE) {
                status = "improved";
                improved.push({
                    lessonId,
                    score: currentScore,
                    previousScore
                });
            } else {
                status = "still-weak";
                stillWeak.push({
                    lessonId,
                    score: currentScore,
                    previousScore
                });

                queue.push({
                    lessonId,
                    score: currentScore,
                    previousScore,
                    status
                });
            }

            history[String(lessonId)] = {
                lessonId,
                score: currentScore,
                previousScore,
                status,
                checkedAt: new Date().toISOString()
            };
        });

        queue.sort((a, b) => {
            const as = a.score === null ? 0 : a.score;
            const bs = b.score === null ? 0 : b.score;
            return as - bs;
        });

        const data = {
            version: 1,
            updatedAt: new Date().toISOString(),
            passScore: PASS_SCORE,
            queue,
            improved,
            stillWeak,
            history
        };

        saveJSON(RETEST_KEY, data);

        return data;
    }

    function refresh() {
        const data = buildRetestData();

        const panel = document.getElementById("quranRevisionRetest");
        const status = document.getElementById("quranRetestStatus");
        const list = document.getElementById("quranRetestList");
        const count = document.getElementById("quranRetestCount");
        const improvedCount = document.getElementById("quranRetestImproved");
        const weakCount = document.getElementById("quranRetestStillWeak");

        if (panel) panel.hidden = false;

        if (count) {
            count.textContent = String(data.queue.length);
        }

        if (improvedCount) {
            improvedCount.textContent = String(data.improved.length);
        }

        if (weakCount) {
            weakCount.textContent = String(data.stillWeak.length);
        }

        if (status) {
            if (!data.queue.length && data.improved.length) {
                status.textContent =
                    "🎉 দারুণ! সব ট্র্যাক করা ভুলে পাস স্কোর অর্জিত হয়েছে।";
            } else if (data.queue.length) {
                status.textContent =
                    "🔁 কিছু lesson আবার Revision + Re-Test করা দরকার।";
            } else {
                status.textContent =
                    "📚 Re-Test queue তৈরি হলে এখানে দেখা যাবে।";
            }
        }

        if (list) {
            list.innerHTML = "";

            if (!data.queue.length) {
                const empty = document.createElement("div");
                empty.className = "quran-retest-empty";
                empty.textContent =
                    data.improved.length
                        ? "✅ বর্তমানে কোনো weak re-test নেই।"
                        : "📖 Quiz ও mistake data তৈরি হলে queue দেখা যাবে।";
                list.appendChild(empty);
                return;
            }

            data.queue.forEach(item => {
                const row = document.createElement("div");
                row.className = "quran-retest-item";

                const scoreText =
                    item.score === null
                        ? "Score: —"
                        : "Score: " + item.score + "%";

                const previousText =
                    item.previousScore === null
                        ? ""
                        : " · আগের: " + item.previousScore + "%";

                row.innerHTML =
                    '<div class="quran-retest-item-main">' +
                    '<strong>Lesson ' + item.lessonId + '</strong>' +
                    '<span>' + scoreText + previousText + '</span>' +
                    '</div>' +
                    '<a class="quran-retest-link" href="/quran/lesson/' +
                    item.lessonId +
                    '">Revision করুন →</a>';

                list.appendChild(row);
            });
        }

        return data;
    }

    function recordRetest(lessonId, score) {
        lessonId = Number(lessonId);
        score = Number(score);

        if (
            !Number.isInteger(lessonId) ||
            lessonId < 1 ||
            lessonId > 20 ||
            !Number.isFinite(score)
        ) {
            return false;
        }

        const data = safeJSON(RETEST_KEY, {
            version: 1,
            history: {}
        });

        if (!data.history || typeof data.history !== "object") {
            data.history = {};
        }

        const old = data.history[String(lessonId)] || {};

        data.history[String(lessonId)] = {
            lessonId,
            score: Math.max(0, Math.min(100, score)),
            previousScore:
                Number.isFinite(Number(old.score))
                    ? Number(old.score)
                    : null,
            status:
                score >= PASS_SCORE
                    ? "improved"
                    : "still-weak",
            checkedAt: new Date().toISOString()
        };

        data.updatedAt = new Date().toISOString();

        saveJSON(RETEST_KEY, data);
        refresh();

        return true;
    }

    window.AIZoneQuranRevisionRetest = {
        refresh,
        rebuild: buildRetestData,
        getRetest: () => safeJSON(RETEST_KEY, {}),
        recordRetest,
        getLatestScores
    };

    document.addEventListener("DOMContentLoaded", refresh);

    window.addEventListener("storage", function (event) {
        if (
            event.key === QUIZ_KEY ||
            event.key === MISTAKE_KEY ||
            event.key === RETEST_KEY
        ) {
            refresh();
        }
    });
})();
// AI-ZONE-QURAN-REVISION-RETEST-JS-END

/* AI-ZONE-QURAN-SMART-STATUS-JS-START */

(function () {
  "use strict";

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PRACTICE_PREFIX = "quran_practice_";

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      if (!raw) return fallback;
      return JSON.parse(raw);
    } catch (error) {
      return fallback;
    }
  }

  function isCompleted(progress, lessonId) {
    if (!progress) return false;

    if (Array.isArray(progress)) {
      return progress.map(Number).includes(lessonId);
    }

    if (progress.completed) {
      if (Array.isArray(progress.completed)) {
        return progress.completed.map(Number).includes(lessonId);
      }

      if (typeof progress.completed === "object") {
        return Boolean(
          progress.completed[lessonId] ||
          progress.completed[String(lessonId)]
        );
      }
    }

    if (typeof progress === "object") {
      const value =
        progress[lessonId] ??
        progress[String(lessonId)];

      if (typeof value === "boolean") {
        return value;
      }
    }

    return false;
  }

  function practiceDone(lessonId) {
    const data = readJSON(
      PRACTICE_PREFIX + lessonId,
      null
    );

    if (!data || typeof data !== "object") {
      return false;
    }

    return Boolean(
      (data.bujhechi || data.understood) &&
      (data.porechi || data.read) &&
      (data.onushilon || data.practice)
    );
  }

  function hasPassedQuiz(quiz, lessonId) {
    if (!quiz) return false;

    const source = Array.isArray(quiz)
      ? quiz
      : Array.isArray(quiz.results)
        ? quiz.results
        : [];

    const matching = source.filter(item => {
      if (!item || typeof item !== "object") return false;

      const id =
        item.lessonId ??
        item.lesson_id ??
        item.lesson;

      return Number(id) === lessonId;
    });

    if (!matching.length) return false;

    const latest = matching[matching.length - 1];

    const score = Number(
      latest.score ??
      latest.percentage ??
      latest.percent ??
      -1
    );

    return score >= 70;
  }

  function updateStatus(root) {
    const lessonId = Number(
      root.getAttribute("data-lesson-id")
    );

    if (!lessonId) return;

    const progress = readJSON(
      PROGRESS_KEY,
      null
    );

    const quiz = readJSON(
      QUIZ_KEY,
      null
    );

    const completed = isCompleted(
      progress,
      lessonId
    );

    const practiced = practiceDone(
      lessonId
    );

    const quizPassed = hasPassedQuiz(
      quiz,
      lessonId
    );

    let status = "not-started";

    if (completed || quizPassed) {
      status = "completed";
    } else if (practiced) {
      status = "quiz";
    } else {
      status = "practice";
    }

    const icon =
      root.querySelector("[data-status-icon]");

    const title =
      root.querySelector("[data-status-title]");

    const message =
      root.querySelector("[data-status-message]");

    const badge =
      root.querySelector("[data-status-badge]");

    root.classList.remove(
      "status-not-started",
      "status-practice",
      "status-quiz",
      "status-completed"
    );

    root.classList.add(
      "status-" + status
    );

    if (status === "completed") {
      if (icon) icon.textContent = "✓";
      if (title) title.textContent = "পাঠ সম্পন্ন";
      if (message) {
        message.textContent =
          "এই পাঠটি সম্পন্ন হয়েছে। পরের পাঠ বা Revision চালিয়ে যান।";
      }
      if (badge) badge.textContent = "Completed";

    } else if (status === "quiz") {
      if (icon) icon.textContent = "3";
      if (title) title.textContent = "Quiz-এর জন্য প্রস্তুত";
      if (message) {
        message.textContent =
          "Practice শেষ হয়েছে। এখন Quiz দিয়ে নিজের শেখা যাচাই করুন।";
      }
      if (badge) badge.textContent = "Ready for Quiz";

    } else if (status === "practice") {
      if (icon) icon.textContent = "→";
      if (title) title.textContent = "শেখা চালিয়ে যান";
      if (message) {
        message.textContent =
          "Lesson content দেখুন, শুনুন এবং Practice সম্পন্ন করুন।";
      }
      if (badge) badge.textContent = "Continue";

    } else {
      if (icon) icon.textContent = "○";
      if (title) title.textContent = "শেখা শুরু করুন";
      if (message) {
        message.textContent =
          "এই পাঠটি শুরু করার জন্য প্রস্তুত।";
      }
      if (badge) badge.textContent = "Not Started";
    }
  }

  function refresh() {
    document
      .querySelectorAll("[data-quran-smart-status]")
      .forEach(updateStatus);
  }

  window.AIZoneRefreshQuranSmartStatus = refresh;

  if (
    document.readyState === "loading"
  ) {
    document.addEventListener(
      "DOMContentLoaded",
      refresh
    );
  } else {
    refresh();
  }

  window.addEventListener(
    "storage",
    function (event) {
      if (
        event.key === PROGRESS_KEY ||
        event.key === QUIZ_KEY ||
        (
          event.key &&
          event.key.startsWith(PRACTICE_PREFIX)
        )
      ) {
        refresh();
      }
    }
  );

})();

/* AI-ZONE-QURAN-SMART-STATUS-JS-END */


/* AI-ZONE-QURAN-COMPLETION-FEEDBACK-JS-START */

(function () {
  "use strict";

  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PASS_SCORE = 70;

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (error) {
      return fallback;
    }
  }

  function lessonIdOf(item) {
    const value =
      item?.lessonId ??
      item?.lesson_id ??
      item?.lesson ??
      item?.id;

    const number = Number(value);
    return Number.isFinite(number) ? number : null;
  }

  function scoreOf(item) {
    const value =
      item?.score ??
      item?.percentage ??
      item?.percent ??
      item?.result?.score;

    const number = Number(value);
    return Number.isFinite(number) ? number : null;
  }

  function latestQuizResult(lessonId) {
    const data = readJSON(QUIZ_KEY, null);

    if (!data) return null;

    let items = [];

    if (Array.isArray(data)) {
      items = data;
    } else if (Array.isArray(data.results)) {
      items = data.results;
    } else if (Array.isArray(data.history)) {
      items = data.history;
    } else if (Array.isArray(data.attempts)) {
      items = data.attempts;
    }

    const matches = items
      .filter(item => lessonIdOf(item) === lessonId)
      .map(item => ({
        item,
        score: scoreOf(item),
        timestamp: Number(
          item?.timestamp ??
          item?.time ??
          item?.createdAt ??
          item?.created_at ??
          0
        )
      }))
      .filter(entry => entry.score !== null);

    if (!matches.length) return null;

    matches.sort((a, b) => b.timestamp - a.timestamp);

    return matches[0];
  }

  function setText(root, selector, value) {
    const element = root.querySelector(selector);
    if (element) element.textContent = value;
  }

  function updateCompletion(root) {
    const lessonId = Number(root.dataset.lessonId);
    if (!Number.isFinite(lessonId)) return;

    const result = latestQuizResult(lessonId);

    root.classList.remove(
      "status-completed",
      "status-revision",
      "status-ready"
    );

    if (!result) {
      setText(
        root,
        "[data-completion-title]",
        "আপনার শেখার অগ্রগতি"
      );

      setText(
        root,
        "[data-completion-message]",
        "Practice ও Quiz সম্পন্ন করার পর আপনার ফলাফল অনুযায়ী পরবর্তী পদক্ষেপ এখানে দেখা যাবে।"
      );

      setText(
        root,
        "[data-completion-state]",
        "Quiz এখনও সম্পন্ন হয়নি"
      );

      return;
    }

    const score = result.score;

    if (score >= PASS_SCORE) {
      root.classList.add("status-completed");

      setText(
        root,
        "[data-completion-icon]",
        "✓"
      );

      setText(
        root,
        "[data-completion-title]",
        "মাশাআল্লাহ! পাঠটি সম্পন্ন হয়েছে"
      );

      setText(
        root,
        "[data-completion-message]",
        "আপনি এই পাঠের Quiz-এ পাস করেছেন। এখন পরের পাঠে এগিয়ে যেতে পারেন অথবা Revision করতে পারেন।"
      );

      setText(
        root,
        "[data-completion-state]",
        "Quiz Score: " + score + "% • Completed"
      );

    } else {
      root.classList.add("status-revision");

      setText(
        root,
        "[data-completion-icon]",
        "↻"
      );

      setText(
        root,
        "[data-completion-title]",
        "আরও একটু অনুশীলন করুন"
      );

      setText(
        root,
        "[data-completion-message]",
        "এই Quiz-এ আপনার স্কোর 70%-এর নিচে। আগে Revision ও Practice করুন, তারপর আবার Quiz দিন।"
      );

      setText(
        root,
        "[data-completion-state]",
        "Quiz Score: " + score + "% • Revision Recommended"
      );
    }
  }

  function refreshCompletionFeedback() {
    document
      .querySelectorAll("[data-quran-completion-feedback]")
      .forEach(updateCompletion);
  }

  window.AIZoneRefreshQuranCompletionFeedback =
    refreshCompletionFeedback;

  document.addEventListener(
    "DOMContentLoaded",
    refreshCompletionFeedback
  );

  window.addEventListener(
    "storage",
    function (event) {
      if (event.key === QUIZ_KEY || event.key === null) {
        refreshCompletionFeedback();
      }
    }
  );
})();

/* AI-ZONE-QURAN-COMPLETION-FEEDBACK-JS-END */


/* AI-ZONE-QURAN-NEXT-ACTION-JS-START */

(function () {
  "use strict";

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PASS_SCORE = 70;

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (error) {
      return fallback;
    }
  }

  function lessonIdOf(item) {
    if (!item || typeof item !== "object") {
      return null;
    }

    const value =
      item.lessonId ??
      item.lesson_id ??
      item.lesson ??
      item.id;

    const number = Number(value);

    return Number.isFinite(number) ? number : null;
  }

  function scoreOf(item) {
    if (!item || typeof item !== "object") {
      return null;
    }

    const value =
      item.score ??
      item.percentage ??
      item.percent ??
      (
        item.result &&
        item.result.score
      );

    const number = Number(value);

    return Number.isFinite(number) ? number : null;
  }

  function isCompleted(progress, lessonId) {
    if (!progress) {
      return false;
    }

    if (Array.isArray(progress)) {
      return progress.some(function (item) {
        if (typeof item === "number") {
          return item === lessonId;
        }

        if (typeof item === "string") {
          return Number(item) === lessonId;
        }

        if (item && typeof item === "object") {
          return (
            lessonIdOf(item) === lessonId &&
            (
              item.completed === true ||
              item.complete === true ||
              item.done === true
            )
          );
        }

        return false;
      });
    }

    if (Array.isArray(progress.completed)) {
      return progress.completed.some(
        function (value) {
          return Number(value) === lessonId;
        }
      );
    }

    if (
      progress.completed &&
      typeof progress.completed === "object"
    ) {
      return (
        progress.completed[lessonId] === true ||
        progress.completed[String(lessonId)] === true
      );
    }

    return (
      progress[lessonId] === true ||
      progress[String(lessonId)] === true
    );
  }

  function practiceDone(lessonId) {
    const raw = localStorage.getItem(
      "quran_practice_" + lessonId
    );

    if (!raw) {
      return false;
    }

    try {
      const data = JSON.parse(raw);

      const understood =
        data.bujhechi ?? data.understood ?? false;

      const read =
        data.porechi ?? data.read ?? false;

      const practice =
        data.onushilon ?? data.practice ?? false;

      return Boolean(
        understood &&
        read &&
        practice
      );
    } catch (error) {
      return false;
    }
  }

  function latestQuiz(lessonId) {
    const data = readJSON(QUIZ_KEY, null);

    if (!data) {
      return null;
    }

    let items = [];

    if (Array.isArray(data)) {
      items = data;
    } else if (Array.isArray(data.results)) {
      items = data.results;
    } else if (Array.isArray(data.history)) {
      items = data.history;
    } else if (Array.isArray(data.attempts)) {
      items = data.attempts;
    }

    const matches = items
      .filter(function (item) {
        return lessonIdOf(item) === lessonId;
      })
      .map(function (item) {
        return {
          score: scoreOf(item),
          timestamp: Number(
            item.timestamp ??
            item.time ??
            item.createdAt ??
            item.created_at ??
            0
          )
        };
      })
      .filter(function (entry) {
        return entry.score !== null;
      });

    if (!matches.length) {
      return null;
    }

    matches.sort(function (a, b) {
      return b.timestamp - a.timestamp;
    });

    return matches[0];
  }

  function nextLessonURL(lessonId) {
    if (lessonId >= 20) {
      return "/quran";
    }

    return "/quran/lesson/" + (lessonId + 1);
  }

  function setText(root, selector, value) {
    const element = root.querySelector(selector);

    if (element) {
      element.textContent = value;
    }
  }

  function updateAction(root) {
    const lessonId = Number(
      root.dataset.lessonId
    );

    if (!Number.isFinite(lessonId)) {
      return;
    }

    const progress =
      readJSON(PROGRESS_KEY, null);

    const completed =
      isCompleted(progress, lessonId);

    const practice =
      practiceDone(lessonId);

    const quiz =
      latestQuiz(lessonId);

    root.classList.remove(
      "status-start",
      "status-practice",
      "status-quiz",
      "status-revision",
      "status-completed"
    );

    const primary = root.querySelector(
      "[data-next-action-primary]"
    );

    if (
      completed ||
      (quiz && quiz.score >= PASS_SCORE)
    ) {
      root.classList.add(
        "status-completed"
      );

      setText(
        root,
        "[data-next-action-icon]",
        "✓"
      );

      setText(
        root,
        "[data-next-action-title]",
        lessonId >= 20
          ? "Academy-এর শেষ পাঠ সম্পন্ন"
          : "পরের পাঠে এগিয়ে যান"
      );

      setText(
        root,
        "[data-next-action-message]",
        lessonId >= 20
          ? "এই পাঠটি সম্পন্ন হয়েছে। এখন Dashboard থেকে Revision চালিয়ে যেতে পারেন।"
          : "এই পাঠটি সম্পন্ন হয়েছে। এখন শেখার ধারাবাহিকতা বজায় রেখে পরের পাঠে এগিয়ে যান।"
      );

      setText(
        root,
        "[data-next-action-state]",
        quiz
          ? "Quiz Score: " + quiz.score + "% • Completed"
          : "Lesson Completed"
      );

      if (primary) {
        primary.textContent =
          lessonId >= 20
            ? "🏠 Academy Dashboard"
            : "➡️ পরের পাঠ";

        primary.href =
          nextLessonURL(lessonId);
      }

      return;
    }

    if (quiz && quiz.score < PASS_SCORE) {
      root.classList.add(
        "status-revision"
      );

      setText(
        root,
        "[data-next-action-icon]",
        "↻"
      );

      setText(
        root,
        "[data-next-action-title]",
        "Revision আগে করুন"
      );

      setText(
        root,
        "[data-next-action-message]",
        "সর্বশেষ Quiz স্কোর 70%-এর নিচে। আগে Revision ও Practice করুন, তারপর আবার Quiz দিন।"
      );

      setText(
        root,
        "[data-next-action-state]",
        "Quiz Score: " + quiz.score +
        "% • Revision Recommended"
      );

      if (primary) {
        primary.textContent =
          "🔄 Revision চালিয়ে যান";

        primary.href =
          "/quran";
      }

      return;
    }

    if (practice) {
      root.classList.add(
        "status-quiz"
      );

      setText(
        root,
        "[data-next-action-icon]",
        "📝"
      );

      setText(
        root,
        "[data-next-action-title]",
        "এখন Quiz দিন"
      );

      setText(
        root,
        "[data-next-action-message]",
        "আপনার Practice সম্পন্ন হয়েছে। এখন Quiz দিয়ে নিজের শেখা যাচাই করুন।"
      );

      setText(
        root,
        "[data-next-action-state]",
        "Practice Complete • Ready for Quiz"
      );

      if (primary) {
        primary.textContent =
          "📝 Quiz শুরু করুন";

        const quiz =
          document.querySelector(
            "[data-quran-quiz]"
          );

        if (quiz && quiz.id) {
          primary.href =
            "#" + quiz.id;
        } else {
          primary.href =
            "#quranQuiz";
        }
      }

      return;
    }

    root.classList.add(
      "status-practice"
    );

    setText(
      root,
      "[data-next-action-icon]",
      "→"
    );

    setText(
      root,
      "[data-next-action-title]",
      "Lesson চালিয়ে যান"
    );

    setText(
      root,
      "[data-next-action-message]",
      "Lesson content দেখুন, শুনুন এবং Practice সম্পন্ন করুন।"
    );

    setText(
      root,
      "[data-next-action-state]",
      "Practice এখনও সম্পন্ন হয়নি"
    );

    if (primary) {
      primary.textContent =
        "📖 Practice করুন";

      primary.href =
        "#quranLearningExperience";
    }
  }

  function refresh() {
    document
      .querySelectorAll(
        "[data-quran-next-action]"
      )
      .forEach(updateAction);
  }

  window.AIZoneRefreshQuranNextAction =
    refresh;

  document.addEventListener(
    "DOMContentLoaded",
    refresh
  );

  window.addEventListener(
    "storage",
    function (event) {
      if (
        event.key === PROGRESS_KEY ||
        event.key === QUIZ_KEY ||
        event.key === null ||
        (
          event.key &&
          event.key.indexOf(
            "quran_practice_"
          ) === 0
        )
      ) {
        refresh();
      }
    }
  );

})();

/* AI-ZONE-QURAN-NEXT-ACTION-JS-END */


/* AI-ZONE-QURAN-DASHBOARD-FOCUS-JS-START */
(function () {
  "use strict";

  const TOTAL = 20;
  const PASS_SCORE = 70;

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PRACTICE_PREFIX = "quran_practice_";

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      if (!raw) return fallback;
      return JSON.parse(raw);
    } catch (e) {
      return fallback;
    }
  }

  function normalizeLessonId(value) {
    const n = Number(value);
    return Number.isInteger(n) && n >= 1 && n <= TOTAL ? n : null;
  }

  function isCompleted(progress, lessonId) {
    if (!progress) return false;

    if (Array.isArray(progress)) {
      return progress.some(function (x) {
        return Number(x) === lessonId;
      });
    }

    if (Array.isArray(progress.completed)) {
      return progress.completed.some(function (x) {
        return Number(x) === lessonId;
      });
    }

    if (progress.completed && typeof progress.completed === "object") {
      return Boolean(
        progress.completed[lessonId] ||
        progress.completed[String(lessonId)]
      );
    }

    if (progress[String(lessonId)] === true) return true;

    return false;
  }

  function practiceDone(lessonId) {
    const data = readJSON(
      PRACTICE_PREFIX + lessonId,
      null
    );

    if (!data) return false;

    if (data === true) return true;

    if (typeof data === "object") {
      const a = Boolean(data.bujhechi || data.understood);
      const b = Boolean(data.porechi || data.read);
      const c = Boolean(data.onushilon || data.practice);

      return a && b && c;
    }

    return false;
  }

  function quizEntries(quiz) {
    if (Array.isArray(quiz)) return quiz;

    if (!quiz || typeof quiz !== "object") return [];

    const keys = ["results", "history", "attempts", "quizzes"];

    for (const key of keys) {
      if (Array.isArray(quiz[key])) {
        return quiz[key];
      }
    }

    return [];
  }

  function latestQuiz(quiz, lessonId) {
    const entries = quizEntries(quiz)
      .filter(function (item) {
        if (!item || typeof item !== "object") return false;

        const id = Number(
          item.lessonId ??
          item.lesson_id ??
          item.lesson ??
          item.id
        );

        return id === lessonId;
      });

    if (!entries.length) return null;

    entries.sort(function (a, b) {
      const ta = Number(
        a.timestamp ??
        a.time ??
        a.createdAt ??
        a.date ??
        0
      );

      const tb = Number(
        b.timestamp ??
        b.time ??
        b.createdAt ??
        b.date ??
        0
      );

      return tb - ta;
    });

    return entries[0];
  }

  function quizScore(item) {
    if (!item || typeof item !== "object") return null;

    const raw =
      item.score ??
      item.percent ??
      item.percentage ??
      item.result;

    const score = Number(raw);

    return Number.isFinite(score) ? score : null;
  }

  function nextLessonURL(lessonId) {
    if (lessonId >= TOTAL) return "/quran";
    return "/quran/lesson/" + (lessonId + 1);
  }

  function lessonURL(lessonId) {
    return "/quran/lesson/" + lessonId;
  }

  function updateFocus(root) {
    const progress = readJSON(PROGRESS_KEY, null);
    const quiz = readJSON(QUIZ_KEY, null);

    let current = 1;

    for (let i = 1; i <= TOTAL; i++) {
      if (!isCompleted(progress, i)) {
        current = i;
        break;
      }

      if (i === TOTAL) {
        current = TOTAL;
      }
    }

    const completedCount = Array.from(
      { length: TOTAL },
      function (_, index) {
        return isCompleted(progress, index + 1);
      }
    ).filter(Boolean).length;

    const title = root.querySelector("[data-focus-title]");
    const message = root.querySelector("[data-focus-message]");
    const button = root.querySelector("[data-focus-button]");
    const icon = root.querySelector("[data-focus-icon]");
    const status = root.querySelector("[data-focus-status]");
    const lesson = root.querySelector("[data-focus-lesson]");
    const progressText = root.querySelector("[data-focus-progress]");

    if (!title || !message || !button || !icon) return;

    const completed = isCompleted(progress, current);
    const practice = practiceDone(current);
    const quizResult = latestQuiz(quiz, current);
    const score = quizScore(quizResult);

    lesson.textContent =
      "Lesson " + current + " / " + TOTAL;

    progressText.textContent =
      completedCount + " / " + TOTAL + " Lessons";

    // Academy complete
    if (
      completedCount >= TOTAL &&
      isCompleted(progress, TOTAL)
    ) {
      icon.textContent = "🏆";
      title.textContent = "Academy Complete!";
      message.textContent =
        "মাশাআল্লাহ! সবগুলো Lesson সম্পন্ন হয়েছে। এখন Revision চালিয়ে আপনার শেখা আরও শক্ত করুন।";
      status.textContent = "Completed";
      button.textContent = "Quran Academy Dashboard →";
      button.href = "/quran";
      return;
    }

    // Quiz passed but completion not yet reflected
    if (score !== null && score >= PASS_SCORE) {
      icon.textContent = "➡️";
      title.textContent =
        current >= TOTAL
          ? "Academy Complete করুন"
          : "Next Lesson চালিয়ে যান";
      message.textContent =
        "আপনার Quiz ভালো হয়েছে। এখন পরের Lesson-এ এগিয়ে যান।";
      status.textContent = "Next Lesson";
      button.textContent =
        current >= TOTAL
          ? "Dashboard দেখুন →"
          : "Lesson " + (current + 1) + " →";
      button.href = nextLessonURL(current);
      return;
    }

    // Failed quiz
    if (score !== null && score < PASS_SCORE) {
      icon.textContent = "🔄";
      title.textContent = "Revision করুন";
      message.textContent =
        "Quiz score 70%-এর নিচে। দুর্বল অংশগুলো আবার অনুশীলন করে Re-Test দিন।";
      status.textContent = "Revision";
      button.textContent = "Revision শুরু করুন →";
      button.href = lessonURL(current) + "#quranRevisionRetest";
      return;
    }

    // Practice complete
    if (practice) {
      icon.textContent = "📝";
      title.textContent = "Quiz দিন";
      message.textContent =
        "Practice শেষ হয়েছে। এখন Quiz দিয়ে নিজের শেখা যাচাই করুন।";
      status.textContent = "Ready for Quiz";
      button.textContent = "Quiz দিন →";
      button.href = lessonURL(current) + "#quranQuiz";
      return;
    }

    // Default
    icon.textContent = "📖";
    title.textContent =
      completedCount > 0
        ? "শেখা চালিয়ে যান"
        : "শেখা শুরু করুন";

    message.textContent =
      completedCount > 0
        ? "আপনার পরবর্তী Lesson-এর content দেখুন, শুনুন এবং Practice সম্পন্ন করুন।"
        : "Quran Academy journey শুরু করার জন্য প্রথম Lesson প্রস্তুত।";

    status.textContent =
      completedCount > 0
        ? "Continue"
        : "Not Started";

    button.textContent =
      "Lesson " + current + " শুরু করুন →";

    button.href = lessonURL(current);
  }

  function refresh() {
    document
      .querySelectorAll("[data-quran-dashboard-focus]")
      .forEach(updateFocus);
  }

  window.AIZoneRefreshQuranDashboardFocus = refresh;

  document.addEventListener("DOMContentLoaded", refresh);

  window.addEventListener("storage", function (event) {
    if (
      event.key === PROGRESS_KEY ||
      event.key === QUIZ_KEY ||
      (event.key && event.key.indexOf(PRACTICE_PREFIX) === 0)
    ) {
      refresh();
    }
  });
})();
/* AI-ZONE-QURAN-DASHBOARD-FOCUS-JS-END */


/* AI-ZONE-QURAN-PRIORITY-SYNC-JS-START */
(function () {
  "use strict";

  const TOTAL = 20;
  const PASS_SCORE = 70;

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PRIORITY_KEY = "ai_zone_quran_revision_priority_v1";
  const PRACTICE_PREFIX = "quran_practice_";

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      if (!raw) return fallback;
      return JSON.parse(raw);
    } catch (e) {
      return fallback;
    }
  }

  function isCompleted(progress, lessonId) {
    if (!progress) return false;

    if (Array.isArray(progress)) {
      return progress.some(x => Number(x) === lessonId);
    }

    if (Array.isArray(progress.completed)) {
      return progress.completed.some(x => Number(x) === lessonId);
    }

    if (progress.completed && typeof progress.completed === "object") {
      return Boolean(
        progress.completed[lessonId] ||
        progress.completed[String(lessonId)]
      );
    }

    return progress[String(lessonId)] === true;
  }

  function practiceDone(lessonId) {
    const data = readJSON(
      PRACTICE_PREFIX + lessonId,
      null
    );

    if (!data) return false;
    if (data === true) return true;

    if (typeof data === "object") {
      return Boolean(
        (data.bujhechi || data.understood) &&
        (data.porechi || data.read) &&
        (data.onushilon || data.practice)
      );
    }

    return false;
  }

  function quizEntries(data) {
    if (Array.isArray(data)) return data;

    if (!data || typeof data !== "object") return [];

    for (const key of [
      "results",
      "history",
      "attempts",
      "quizzes"
    ]) {
      if (Array.isArray(data[key])) {
        return data[key];
      }
    }

    return [];
  }

  function latestQuiz(data, lessonId) {
    const entries = quizEntries(data).filter(item => {
      if (!item || typeof item !== "object") return false;

      const id = Number(
        item.lessonId ??
        item.lesson_id ??
        item.lesson ??
        item.id
      );

      return id === lessonId;
    });

    if (!entries.length) return null;

    entries.sort((a, b) => {
      const ta = Number(
        a.timestamp ??
        a.time ??
        a.createdAt ??
        a.date ??
        0
      );

      const tb = Number(
        b.timestamp ??
        b.time ??
        b.createdAt ??
        b.date ??
        0
      );

      return tb - ta;
    });

    return entries[0];
  }

  function scoreOf(result) {
    if (!result || typeof result !== "object") {
      return null;
    }

    const score = Number(
      result.score ??
      result.percent ??
      result.percentage ??
      result.result
    );

    return Number.isFinite(score) ? score : null;
  }

  function priorityForLesson(priorityData, lessonId) {
    if (!priorityData) return null;

    const candidates = [];

    if (Array.isArray(priorityData)) {
      candidates.push(...priorityData);
    }

    if (Array.isArray(priorityData.items)) {
      candidates.push(...priorityData.items);
    }

    if (Array.isArray(priorityData.results)) {
      candidates.push(...priorityData.results);
    }

    if (typeof priorityData === "object") {
      const direct =
        priorityData[lessonId] ??
        priorityData[String(lessonId)];

      if (direct && typeof direct === "object") {
        return direct;
      }
    }

    return candidates.find(item => {
      if (!item || typeof item !== "object") return false;

      const id = Number(
        item.lessonId ??
        item.lesson_id ??
        item.lesson ??
        item.id
      );

      return id === lessonId;
    }) || null;
  }

  function setPriority(
    root,
    icon,
    title,
    message,
    badge,
    score,
    className
  ) {
    root.classList.remove(
      "priority-high",
      "priority-medium",
      "priority-low",
      "priority-complete"
    );

    if (className) {
      root.classList.add(className);
    }

    root.querySelector("[data-priority-icon]").textContent = icon;
    root.querySelector("[data-priority-title]").textContent = title;
    root.querySelector("[data-priority-message]").textContent = message;
    root.querySelector("[data-priority-badge]").textContent = badge;
    root.querySelector("[data-priority-score]").textContent =
      score === null || score === undefined
        ? "Score: —"
        : "Score: " + score + "%";
  }

  function updatePriority(root) {
    const progress = readJSON(PROGRESS_KEY, null);
    const quiz = readJSON(QUIZ_KEY, null);
    const priorityData = readJSON(PRIORITY_KEY, null);

    let current = 1;

    for (let i = 1; i <= TOTAL; i++) {
      if (!isCompleted(progress, i)) {
        current = i;
        break;
      }

      if (i === TOTAL) {
        current = TOTAL;
      }
    }

    const completedCount = Array.from(
      { length: TOTAL },
      (_, i) => isCompleted(progress, i + 1)
    ).filter(Boolean).length;

    const completed = isCompleted(progress, current);
    const practice = practiceDone(current);
    const quizResult = latestQuiz(quiz, current);
    const score = scoreOf(quizResult);
    const savedPriority = priorityForLesson(
      priorityData,
      current
    );

    // Full academy complete
    if (
      completedCount >= TOTAL &&
      isCompleted(progress, TOTAL)
    ) {
      setPriority(
        root,
        "🏆",
        "সব Lesson সম্পন্ন হয়েছে",
        "এখন Revision চালিয়ে শেখা আরও শক্ত করুন এবং প্রয়োজন হলে শিক্ষক/ক্বারির সহায়তা নিন।",
        "Complete",
        null,
        "priority-complete"
      );
      return;
    }

    // Failed quiz — strongest priority
    if (score !== null && score < PASS_SCORE) {
      let priority = "HIGH";

      if (score >= 55) {
        priority = "MEDIUM";
      } else if (score >= 40) {
        priority = "HIGH";
      }

      const className =
        priority === "HIGH"
          ? "priority-high"
          : "priority-medium";

      setPriority(
        root,
        "🔄",
        "Revision এখন সবচেয়ে গুরুত্বপূর্ণ",
        "Lesson " + current +
        " Quiz-এ " + score +
        "% পাওয়া গেছে। দুর্বল অংশগুলো আবার অনুশীলন করে Re-Test দিন।",
        priority,
        score,
        className
      );
      return;
    }

    // Saved Revision Priority Engine data
    if (
      savedPriority &&
      typeof savedPriority === "object"
    ) {
      const saved = String(
        savedPriority.priority ??
        savedPriority.level ??
        ""
      ).toUpperCase();

      if (saved === "HIGH") {
        setPriority(
          root,
          "⚠️",
          "এই Lesson-এ বেশি মনোযোগ দিন",
          "Revision Priority Engine এই Lesson-কে High Priority হিসেবে চিহ্নিত করেছে।",
          "HIGH",
          score,
          "priority-high"
        );
        return;
      }

      if (saved === "MEDIUM") {
        setPriority(
          root,
          "🟡",
          "এই Lesson আবার ঝালিয়ে নিন",
          "Revision Priority Engine অনুযায়ী এই Lesson-এ আরও কিছু অনুশীলন উপকারী হবে।",
          "MEDIUM",
          score,
          "priority-medium"
        );
        return;
      }
    }

    // Practice completed
    if (practice) {
      setPriority(
        root,
        "📝",
        "Quiz-এর আগে Practice শেষ করুন",
        "আপনি Practice সম্পন্ন করেছেন। এখন Quiz দিয়ে শেখা যাচাই করুন।",
        "READY",
        score,
        "priority-low"
      );
      return;
    }

    // Normal learning
    setPriority(
      root,
      "📖",
      "Lesson content দিয়ে শুরু করুন",
      "দেখুন → শুনুন → পড়ুন → অনুশীলন করুন। তারপর Quiz দিন।",
      "NORMAL",
      score,
      "priority-low"
    );
  }

  function refresh() {
    document
      .querySelectorAll("[data-quran-focus-priority]")
      .forEach(updatePriority);
  }

  window.AIZoneRefreshQuranDashboardPriority =
    refresh;

  document.addEventListener(
    "DOMContentLoaded",
    refresh
  );

  window.addEventListener(
    "storage",
    function (event) {
      if (
        event.key === PROGRESS_KEY ||
        event.key === QUIZ_KEY ||
        event.key === PRIORITY_KEY ||
        (event.key &&
          event.key.indexOf(PRACTICE_PREFIX) === 0)
      ) {
        refresh();
      }
    }
  );
})();
/* AI-ZONE-QURAN-PRIORITY-SYNC-JS-END */


/* AI-ZONE-QURAN-SMART-REVISION-CENTER-JS-START */

(function () {
  "use strict";

  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PRIORITY_KEY = "ai_zone_quran_revision_priority_v1";
  const RETEST_KEY = "ai_zone_quran_retest_v1";
  const MISTAKE_KEY = "ai_zone_quran_mistakes_v1";
  const PASS_SCORE = 70;
  const TOTAL = 20;

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function lessonIdOf(item) {
    if (!item || typeof item !== "object") return null;

    const value =
      item.lessonId ??
      item.lesson_id ??
      item.lesson ??
      item.id;

    const n = Number(value);
    return Number.isInteger(n) && n >= 1 && n <= TOTAL ? n : null;
  }

  function scoreOf(item) {
    if (!item || typeof item !== "object") return null;

    const value =
      item.score ??
      item.percentage ??
      item.percent ??
      item.result;

    const n = Number(value);
    return Number.isFinite(n) ? n : null;
  }

  function priorityOf(item) {
    if (!item || typeof item !== "object") return "";

    return String(
      item.priority ??
      item.level ??
      item.status ??
      ""
    ).toLowerCase();
  }

  function collect(value, output) {
    if (!value) return;

    if (Array.isArray(value)) {
      value.forEach(item => collect(item, output));
      return;
    }

    if (typeof value !== "object") return;

    const lesson = lessonIdOf(value);

    if (lesson) {
      output.push(value);
    }

    [
      value.results,
      value.items,
      value.data,
      value.history,
      value.attempts,
      value.lessons,
      value.records,
      value.questions
    ].forEach(child => {
      if (child) collect(child, output);
    });
  }

  function latestByLesson(value) {
    const all = [];
    collect(value, all);

    const map = {};

    all.forEach(item => {
      const lesson = lessonIdOf(item);
      if (!lesson) return;

      const stamp = Number(
        item.timestamp ??
        item.time ??
        item.updatedAt ??
        item.createdAt ??
        0
      );

      if (!map[lesson] || stamp >= map[lesson].stamp) {
        map[lesson] = { item, stamp };
      }
    });

    return map;
  }

  function getPriority(lesson) {
    const data = latestByLesson(readJSON(PRIORITY_KEY, []));
    const item = data[lesson]?.item;
    const priority = priorityOf(item);

    if (priority.includes("high")) return "high";
    if (priority.includes("medium")) return "medium";
    if (priority.includes("low")) return "low";

    return "";
  }

  function getScore(lesson) {
    const data = latestByLesson(readJSON(QUIZ_KEY, []));
    return scoreOf(data[lesson]?.item);
  }

  function hasRetest(lesson) {
    const data = latestByLesson(readJSON(RETEST_KEY, []));
    const item = data[lesson]?.item;

    if (!item) return false;

    const status = String(
      item.status ??
      item.result ??
      item.state ??
      ""
    ).toLowerCase();

    return (
      status.includes("retest") ||
      status.includes("pending") ||
      status.includes("weak") ||
      item.needsRetest === true ||
      item.retestPending === true
    );
  }

  function hasMistake(lesson) {
    const data = latestByLesson(readJSON(MISTAKE_KEY, []));
    return !!data[lesson];
  }

  function lessonURL(lesson) {
    if (lesson === 1) {
      return "{{ url_for('quran_lesson', lesson_id=1) }}";
    }

    return "{{ url_for('quran_lesson_2') }}".replace(
      "2",
      String(lesson)
    );
  }

  function safeLessonURL(lesson) {
    if (lesson === 1) return "/quran/lesson/1";
    return "/quran/lesson/" + lesson;
  }

  function buildItems() {
    const items = [];
    const completed = readJSON("ai_zone_quran_progress_v1", {});

    for (let lesson = 1; lesson <= TOTAL; lesson++) {
      const score = getScore(lesson);
      const priority = getPriority(lesson);
      const retest = hasRetest(lesson);
      const mistake = hasMistake(lesson);

      const progressDone =
        Array.isArray(completed)
          ? completed.includes(lesson) || completed.includes(String(lesson))
          : completed &&
            (
              completed[lesson] === true ||
              completed[String(lesson)] === true
            );

      if (retest) {
        items.push({
          lesson,
          type: "retest",
          label: "Re-Test",
          title: "Lesson " + lesson,
          meta: score !== null
            ? "আগের Score: " + score + "%"
            : "আবার পরীক্ষা দিন",
          rank: 1
        });
        return;
      }

      if (score !== null && score < PASS_SCORE) {
        items.push({
          lesson,
          type: priority === "high" ? "high" : "medium",
          label: priority === "high" ? "High Priority" : "Revision",
          title: "Lesson " + lesson,
          meta: "Quiz Score: " + score + "%",
          rank: priority === "high" ? 2 : 3
        });
        return;
      }

      if (priority === "high" || priority === "medium" || mistake) {
        items.push({
          lesson,
          type: priority || "medium",
          label: priority === "high" ? "High Priority" : "Medium Priority",
          title: "Lesson " + lesson,
          meta: mistake ? "ভুলগুলো আবার অনুশীলন করুন" : "আরও Revision দরকার",
          rank: priority === "high" ? 2 : 3
        });
        return;
      }

      if (progressDone && score !== null && score >= PASS_SCORE) {
        items.push({
          lesson,
          type: "improved",
          label: "Improved",
          title: "Lesson " + lesson,
          meta: "Quiz Score: " + score + "%",
          rank: 4
        });
      }
    }

    return items.sort((a, b) => a.rank - b.rank || a.lesson - b.lesson);
  }

  function render() {
    const root = document.querySelector("[data-quran-smart-revision-center]");
    if (!root) return;

    const list = root.querySelector("[data-revision-list]");
    const empty = root.querySelector("[data-revision-empty]");

    const items = buildItems();

    root.querySelector("[data-revision-total]").textContent = items.length;
    root.querySelector("[data-revision-high]").textContent =
      items.filter(x => x.type === "high").length;
    root.querySelector("[data-revision-medium]").textContent =
      items.filter(x => x.type === "medium").length;
    root.querySelector("[data-revision-improved]").textContent =
      items.filter(x => x.type === "improved").length;
    root.querySelector("[data-revision-retest]").textContent =
      items.filter(x => x.type === "retest").length;

    list.querySelectorAll(".quran-revision-item").forEach(el => el.remove());

    if (!items.length) {
      empty.style.display = "";
      return;
    }

    empty.style.display = "none";

    items.forEach(item => {
      const row = document.createElement("div");
      row.className = "quran-revision-item";

      const main = document.createElement("div");
      main.className = "quran-revision-item-main";

      const title = document.createElement("span");
      title.className = "quran-revision-item-title";
      title.textContent = item.title;

      const meta = document.createElement("span");
      meta.className = "quran-revision-item-meta";
      meta.textContent = item.meta;

      main.appendChild(title);
      main.appendChild(meta);

      const actions = document.createElement("div");
      actions.className = "quran-revision-item-actions";

      const badge = document.createElement("span");
      badge.className = "quran-revision-item-badge " + item.type;
      badge.textContent = item.label;

      const link = document.createElement("a");
      link.className = "btn btn-primary";
      link.href = safeLessonURL(item.lesson);
      link.textContent =
        item.type === "retest"
          ? "Re-Test দেখুন →"
          : "Revision করুন →";

      actions.appendChild(badge);
      actions.appendChild(link);

      row.appendChild(main);
      row.appendChild(actions);

      list.appendChild(row);
    });
  }

  window.AIZoneRefreshQuranSmartRevisionCenter = render;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }

})();

/* AI-ZONE-QURAN-SMART-REVISION-CENTER-JS-END */


/* AI-ZONE-QURAN-LEARNING-HEALTH-JS-START */

(function () {
  "use strict";

  const TOTAL = 20;
  const PASS_SCORE = 70;

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";
  const PRIORITY_KEY = "ai_zone_quran_revision_priority_v1";
  const RETEST_KEY = "ai_zone_quran_retest_v1";

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function lessonId(item) {
    if (!item || typeof item !== "object") return null;

    const value =
      item.lessonId ??
      item.lesson_id ??
      item.lesson;

    const n = Number(value);

    return Number.isInteger(n) && n >= 1 && n <= TOTAL
      ? n
      : null;
  }

  function score(item) {
    if (!item || typeof item !== "object") return null;

    const value =
      item.score ??
      item.percentage ??
      item.percent;

    const n = Number(value);

    return Number.isFinite(n) ? n : null;
  }

  function collect(value, output) {
    if (!value) return;

    if (Array.isArray(value)) {
      value.forEach(item => collect(item, output));
      return;
    }

    if (typeof value !== "object") return;

    if (lessonId(value)) {
      output.push(value);
    }

    [
      value.results,
      value.items,
      value.data,
      value.history,
      value.attempts,
      value.lessons,
      value.records
    ].forEach(child => {
      if (child) collect(child, output);
    });
  }

  function latestMap(value) {
    const all = [];
    collect(value, all);

    const map = {};

    all.forEach(item => {
      const id = lessonId(item);
      if (!id) return;

      const stamp = Number(
        item.timestamp ??
        item.time ??
        item.updatedAt ??
        item.createdAt ??
        0
      );

      if (!map[id] || stamp >= map[id].stamp) {
        map[id] = {
          item: item,
          stamp: stamp
        };
      }
    });

    return map;
  }

  function completedLessons() {
    const data = readJSON(PROGRESS_KEY, {});
    const result = new Set();

    if (Array.isArray(data)) {
      data.forEach(item => {
        const n = Number(
          typeof item === "object"
            ? lessonId(item)
            : item
        );

        if (Number.isInteger(n) && n >= 1 && n <= TOTAL) {
          result.add(n);
        }
      });
    } else if (data && typeof data === "object") {
      for (let i = 1; i <= TOTAL; i++) {
        if (
          data[i] === true ||
          data[String(i)] === true
        ) {
          result.add(i);
        }
      }
    }

    return result;
  }

  function quizMap() {
    return latestMap(readJSON(QUIZ_KEY, []));
  }

  function priorityMap() {
    return latestMap(readJSON(PRIORITY_KEY, []));
  }

  function retestMap() {
    return latestMap(readJSON(RETEST_KEY, []));
  }

  function priorityValue(item) {
    if (!item || typeof item !== "object") return "";

    return String(
      item.priority ??
      item.level ??
      item.status ??
      ""
    ).toLowerCase();
  }

  function retestPending(item) {
    if (!item) return false;

    const status = String(
      item.status ??
      item.result ??
      item.state ??
      ""
    ).toLowerCase();

    return (
      status.includes("pending") ||
      status.includes("retest") ||
      status.includes("weak") ||
      item.needsRetest === true ||
      item.retestPending === true
    );
  }

  function calculate() {
    const completed = completedLessons();
    const quizzes = quizMap();
    const priorities = priorityMap();
    const retests = retestMap();

    let passed = 0;
    let revision = 0;
    let retest = 0;
    let high = 0;

    for (let i = 1; i <= TOTAL; i++) {
      const q = quizzes[i]?.item;
      const p = priorities[i]?.item;
      const r = retests[i]?.item;

      const s = score(q);
      const priority = priorityValue(p);

      if (s !== null && s >= PASS_SCORE) {
        passed++;
      }

      if (r && retestPending(r)) {
        retest++;
      }

      if (priority === "high") {
        high++;
      }

      if (
        (s !== null && s < PASS_SCORE) ||
        priority === "high" ||
        priority === "medium"
      ) {
        revision++;
      }
    }

    let health = Math.round(
      (completed.size / TOTAL) * 100
    );

    // Quiz quality slightly refines the overall health.
    if (passed > 0) {
      const quizFactor = Math.round(
        (passed / TOTAL) * 20
      );

      health = Math.min(
        100,
        Math.round((health * 0.8) + quizFactor)
      );
    }

    return {
      completed: completed.size,
      passed,
      revision,
      retest,
      high,
      health
    };
  }

  function healthLabel(value) {
    if (value >= 90) return "Excellent";
    if (value >= 70) return "Strong Progress";
    if (value >= 40) return "Good Start";
    if (value > 0) return "In Progress";
    return "Getting Started";
  }

  function render() {
    const root = document.querySelector(
      "[data-quran-learning-health]"
    );

    if (!root) return;

    const data = calculate();

    root.querySelector("[data-health-score]").textContent =
      data.health + "%";

    root.querySelector("[data-health-label]").textContent =
      healthLabel(data.health);

    root.querySelector("[data-health-completed]").textContent =
      data.completed + "/" + TOTAL;

    root.querySelector("[data-health-passed]").textContent =
      data.passed;

    root.querySelector("[data-health-revision]").textContent =
      data.revision;

    root.querySelector("[data-health-retest]").textContent =
      data.retest;

    root.querySelector("[data-health-high]").textContent =
      data.high;

    const title = root.querySelector(
      "[data-health-message-title]"
    );

    const message = root.querySelector(
      "[data-health-message]"
    );

    if (data.completed >= TOTAL && data.revision === 0) {
      title.textContent = "🎉 Academy progress looks excellent";

      message.textContent =
        "সব Lesson সম্পন্ন এবং কোনো Revision priority নেই। নিয়মিত Revision চালিয়ে যান।";

    } else if (data.retest > 0) {
      title.textContent = "🔄 Re-Test আগে করুন";

      message.textContent =
        "কিছু পাঠের Re-Test pending আছে। আগে সেগুলো আবার পরীক্ষা করুন।";

    } else if (data.high > 0) {
      title.textContent = "🔴 High Priority Revision করুন";

      message.textContent =
        "কিছু Lesson-এর priority বেশি। সেগুলো আগে Revision করলে শেখার ভিত্তি আরও শক্ত হবে।";

    } else if (data.revision > 0) {
      title.textContent = "📖 Revision চালিয়ে যান";

      message.textContent =
        "কিছু Lesson-এ আরও অনুশীলন দরকার। Revision Center থেকে এগুলো দেখুন।";

    } else if (data.completed > 0) {
      title.textContent = "🚀 শেখার যাত্রা ভালোভাবে চলছে";

      message.textContent =
        "আপনার progress আছে। নিয়মিত Practice ও Quiz চালিয়ে পরের Lesson-এ এগিয়ে যান।";

    } else {
      title.textContent = "🌱 শেখা শুরু করুন";

      message.textContent =
        "Lesson 1 থেকে শুরু করুন এবং ধীরে ধীরে Practice → Quiz → Revision flow অনুসরণ করুন।";
    }
  }

  window.AIZoneRefreshQuranLearningHealth = render;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }

})();

/* AI-ZONE-QURAN-LEARNING-HEALTH-JS-END */





/* AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-JS-START */

(function () {
  "use strict";

  const TOTAL = 20;
  const PASS_SCORE = 70;

  const PROGRESS_KEY = "ai_zone_quran_progress_v1";
  const QUIZ_KEY = "ai_zone_quran_quiz_v1";

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function findLesson(value, id) {
    if (!value) return null;

    if (Array.isArray(value)) {
      for (const item of value) {
        const found = findLesson(item, id);
        if (found) return found;
      }
      return null;
    }

    if (typeof value !== "object") return null;

    const itemId = Number(
      value.lessonId ??
      value.lesson_id ??
      value.lesson
    );

    if (itemId === id) return value;

    const children = [
      value.results,
      value.items,
      value.data,
      value.history,
      value.attempts,
      value.lessons,
      value.records
    ];

    for (const child of children) {
      const found = findLesson(child, id);
      if (found) return found;
    }

    return null;
  }

  function getScore(id) {
    const item = findLesson(readJSON(QUIZ_KEY, []), id);

    if (!item) return null;

    const value =
      item.score ??
      item.percentage ??
      item.percent;

    const score = Number(value);

    return Number.isFinite(score) ? score : null;
  }

  function isCompleted(id) {
    const data = readJSON(PROGRESS_KEY, {});

    if (Array.isArray(data)) {
      return data.includes(id) || data.includes(String(id));
    }

    return !!(
      data &&
      (
        data[id] === true ||
        data[String(id)] === true
      )
    );
  }

  function practiceDone(id) {
    const data = readJSON("quran_practice_" + id, null);

    if (!data) return false;

    if (data === true) return true;

    if (typeof data === "object") {
      return !!(
        data.bujhechi ||
        data.understood ||
        data.porechi ||
        data.read ||
        data.onushilon ||
        data.practice
      );
    }

    return false;
  }

  function lessonURL(id) {
    return "/quran/lesson/" + id;
  }

  function calculate() {
    let current = 1;

    for (let id = 1; id <= TOTAL; id++) {
      const score = getScore(id);

      if (
        isCompleted(id) ||
        (score !== null && score >= PASS_SCORE)
      ) {
        current = id + 1;
      } else {
        current = id;
        break;
      }
    }

    if (current > TOTAL) {
      return {
        lesson: TOTAL,
        state: "complete",
        title: "🎉 Academy Complete",
        message: "সব 20টি Lesson সম্পন্ন হয়েছে। নিয়মিত Revision চালিয়ে যান।",
        button: "Dashboard →",
        url: "/quran",
        score: null
      };
    }

    const score = getScore(current);

    if (score !== null && score < PASS_SCORE) {
      return {
        lesson: current,
        state: "revision",
        title: "Lesson " + current + " Revision করুন",
        message: "Quiz Score " + score + "%। আগে Revision করে আবার চেষ্টা করুন।",
        button: "Revision →",
        url: lessonURL(current),
        score: score
      };
    }

    if (practiceDone(current)) {
      return {
        lesson: current,
        state: "quiz",
        title: "Lesson " + current + " Quiz দিন",
        message: "Practice সম্পন্ন হয়েছে। এবার Quiz দিয়ে আপনার শেখা যাচাই করুন।",
        button: "Quiz প্রস্তুতি →",
        url: lessonURL(current),
        score: null
      };
    }

    return {
      lesson: current,
      state: "practice",
      title: "Lesson " + current + " শুরু করুন",
      message: "Lesson পড়ুন, Practice সম্পন্ন করুন, তারপর Quiz দিন।",
      button: "Lesson খুলুন →",
      url: lessonURL(current),
      score: null
    };
  }

  function render() {
    const root = document.querySelector(
      "[data-quran-unified-control]"
    );

    if (!root) return;

    const data = calculate();

    root.querySelector("[data-unified-now]").textContent =
      data.state === "complete"
        ? "Academy Complete"
        : data.title;

    root.querySelector("[data-unified-lesson]").textContent =
      data.state === "complete"
        ? "20 / 20"
        : "Lesson " + data.lesson;

    root.querySelector("[data-unified-action-title]").textContent =
      data.title;

    root.querySelector("[data-unified-action-message]").textContent =
      data.message;

    root.querySelector("[data-unified-status]").textContent =
      data.state === "revision"
        ? "Revision"
        : data.state === "quiz"
          ? "Ready for Quiz"
          : data.state === "complete"
            ? "Complete"
            : "Practice";

    root.querySelector("[data-unified-score]").textContent =
      data.score === null
        ? "Score: —"
        : "Score: " + data.score + "%";

    const button = root.querySelector(
      "[data-unified-action-button]"
    );

    button.href = data.url;
    button.textContent = data.button;

    root.querySelectorAll("[data-unified-step]").forEach(function (step) {
      step.classList.remove("active");
    });

    const active =
      data.state === "revision"
        ? "revision"
        : data.state === "quiz"
          ? "quiz"
          : data.state === "complete"
            ? "next"
            : "practice";

    const activeStep = root.querySelector(
      '[data-unified-step="' + active + '"]'
    );

    if (activeStep) {
      activeStep.classList.add("active");
    }
  }

  window.AIZoneRefreshQuranUnifiedControl = render;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }

})();

/* AI-ZONE-QURAN-UNIFIED-CONTROL-CENTER-JS-END */



