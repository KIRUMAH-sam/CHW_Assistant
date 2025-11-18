// frontend/db.js
let db;

const request = indexedDB.open("CHWDecisionAssistant", 1);

request.onupgradeneeded = (event) => {
  db = event.target.result;
  const store = db.createObjectStore("pendingCases", { keyPath: "id", autoIncrement: true });
  store.createIndex("synced", "synced", { unique: false });
};

request.onsuccess = (event) => {
  db = event.target.result;
};

request.onerror = (event) => {
  console.error("IndexedDB error:", event.target.errorCode);
};

function saveCaseOffline(data) {
  const tx = db.transaction(["pendingCases"], "readwrite");
  const store = tx.objectStore("pendingCases");
  store.add({ ...data, synced: false });
}

function getPendingCases(callback) {
  const tx = db.transaction(["pendingCases"], "readonly");
  const store = tx.objectStore("pendingCases");
  const request = store.getAll();
  request.onsuccess = () => callback(request.result);
}

function markSynced(id) {
  const tx = db.transaction(["pendingCases"], "readwrite");
  const store = tx.objectStore("pendingCases");
  const request = store.get(id);
  request.onsuccess = () => {
    const data = request.result;
    data.synced = true;
    store.put(data);
  };
}

window.DB = { saveCaseOffline, getPendingCases, markSynced };
