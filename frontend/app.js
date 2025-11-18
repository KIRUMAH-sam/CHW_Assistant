// frontend/app.js
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("service-worker.js");
  console.log("Service Worker registered");
}

const form = document.getElementById("triageForm");
const resultDiv = document.getElementById("result");
const riskScoreSpan = document.getElementById("riskScore");
const recommendationSpan = document.getElementById("recommendation");
const printBtn = document.getElementById("printNote");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    sex: document.getElementById("sex").value,
    age_months: parseInt(document.getElementById("age_months").value),
    symptoms: {
      fever: document.getElementById("fever").checked,
      cough: document.getElementById("cough").checked,
      difficulty_breathing: document.getElementById("difficulty_breathing").checked
    },
    vitals: {
      temp_c: parseFloat(document.getElementById("temp_c").value) || 0
    }
  };

  const response = await API.submitCase(payload);
  if (response.offline) {
    alert("No connection — case saved offline!");
    return;
  }

  riskScoreSpan.textContent = response.risk_score;
  recommendationSpan.textContent = response.referral_note.recommended_action;
  resultDiv.classList.remove("hidden");
});

printBtn.addEventListener("click", () => window.print());

window.addEventListener("online", () => API.syncOfflineCases());
