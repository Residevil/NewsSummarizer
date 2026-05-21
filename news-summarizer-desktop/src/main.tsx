import React from "react";
import ReactDOM from "react-dom/client";
import { App } from "./App";
import { ToastProvider } from "./components/toast/ToastContext";
import { invoke } from "@tauri-apps/api/core";
import "./styles/tailwind.css";

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

initBackend().then(() => {
  ReactDOM.createRoot(document.getElementById("app") as HTMLElement).render(
    <React.StrictMode>
      <ToastProvider>
        <App />
      </ToastProvider>
    </React.StrictMode>
  );
});
