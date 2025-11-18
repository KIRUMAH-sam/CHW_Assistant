// frontend/api.js
const API_URL = "https://chw-backend.onrender.com/api/v1"; // Change when deploying

async function submitCase(payload) {
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`${API_URL}/cases/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error("Network error");
    return await res.json();
  } catch (err) {
    console.warn("Offline mode active, saving locally");
    DB.saveCaseOffline(payload);
    return { offline: true };
  }
}

async function syncOfflineCases() {
  DB.getPendingCases(async (cases) => {
    if (cases.length === 0) return;
    console.log("Syncing offline cases...");
    const token = localStorage.getItem("token");
    try {
      const res = await fetch(`${API_URL}/cases/sync`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ cases })
      });
      if (res.ok) {
        cases.forEach(c => DB.markSynced(c.id));
        console.log("Synced successfully");
      }
    } catch (err) {
      console.warn("Sync failed, retry later");
    }
  });
}

window.API = { submitCase, syncOfflineCases };
