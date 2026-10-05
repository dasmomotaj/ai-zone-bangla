(function () {
  "use strict";

  const STORAGE_KEY = "ai_zone_quran_quiz_v1";
  const PASS_SCORE = 70;

  function getQuizData() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    } catch (e) {
      return {};
    }
  }

  function saveQuizData(data) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  }

  function initQuiz(quiz) {
    const lessonId = quiz.dataset.lessonId;
    const questions = Array.from(
      quiz.querySelectorAll("[data-quiz-question]")
    );

    const submitButton = quiz.querySelector("[data-quiz-submit]");
    const retryButton = quiz.querySelector("[data-quiz-retry]");
    const resultBox = quiz.querySelector("[data-quiz-result]");

    if (!submitButton || !resultBox) {
      return;
    }

    function resetQuiz() {
      questions.forEach(function (question) {
        question.querySelectorAll("input[type='radio']").forEach(function (input) {
          input.checked = false;
        });

        question.classList.remove("quiz-correct", "quiz-wrong");
      });

      resultBox.textContent = "";
      resultBox.className = "quran-quiz-result";

      submitButton.hidden = false;

      if (retryButton) {
        retryButton.hidden = true;
      }
    }

    submitButton.addEventListener("click", function () {
      let answered = 0;
      let correct = 0;

      questions.forEach(function (question) {
        const selected = question.querySelector(
          "input[type='radio']:checked"
        );

        question.classList.remove("quiz-correct", "quiz-wrong");

        if (!selected) {
          return;
        }

        answered++;

        const correctAnswer = String(question.dataset.answer);
        const selectedAnswer = String(selected.value);

        if (selectedAnswer === correctAnswer) {
          correct++;
          question.classList.add("quiz-correct");
        } else {
          question.classList.add("quiz-wrong");
        }
      });

      if (answered < questions.length) {
        resultBox.textContent =
          "⚠️ সব প্রশ্নের উত্তর নির্বাচন করুন।";

        resultBox.className =
          "quran-quiz-result warning";

        return;
      }

      const score = Math.round(
        (correct / questions.length) * 100
      );

      const passed = score >= PASS_SCORE;

      const data = getQuizData();

      data[String(lessonId)] = {
        score: score,
        correct: correct,
        total: questions.length,
        passed: passed,
        updatedAt: new Date().toISOString()
      };

      saveQuizData(data);

      if (passed) {
        resultBox.textContent =
          "🎉 Quiz Passed! আপনার স্কোর " +
          score +
          "%. Lesson Complete করা হয়েছে।";

        resultBox.className =
          "quran-quiz-result success";

        if (window.AIZoneQuranComplete) {
          window.AIZoneQuranComplete(Number(lessonId));
        }

        submitButton.hidden = true;

        if (retryButton) {
          retryButton.hidden = false;
        }
      } else {
        resultBox.textContent =
          "📚 আপনার স্কোর " +
          score +
          "%. Pass করতে কমপক্ষে " +
          PASS_SCORE +
          "% প্রয়োজন। আবার চেষ্টা করুন।";

        resultBox.className =
          "quran-quiz-result fail";

        if (retryButton) {
          retryButton.hidden = false;
        }
      }
    });

    if (retryButton) {
      retryButton.addEventListener("click", resetQuiz);
    }
  }

  function init() {
    document
      .querySelectorAll("[data-quran-quiz]")
      .forEach(initQuiz);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
