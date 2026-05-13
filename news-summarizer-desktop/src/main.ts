import { invoke } from "@tauri-apps/api/core";

// --- Backend Startup Logic ---
async function initBackend() {
  try {
    await invoke("start_backend");
    const ready = await invoke("wait_for_backend");

    if (!ready) {
      console.error("Backend failed to start");
    } else {
      console.log("Backend is ready");
    }
  } catch (err) {
    console.error("Error starting backend:", err);
  }
}

initBackend();
// --- End Backend Startup Logic ---

// --- Existing Demo Code (unchanged) ---
let greetInputEl: HTMLInputElement | null;
let greetMsgEl: HTMLElement | null;

async function greet() {
  if (greetMsgEl && greetInputEl) {
    greetMsgEl.textContent = await invoke("greet", {
      name: greetInputEl.value,
    });
  }
}

window.addEventListener("DOMContentLoaded", () => {
  greetInputEl = document.querySelector("#greet-input");
  greetMsgEl = document.querySelector("#greet-msg");
  document.querySelector("#greet-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    greet();
  });
});
