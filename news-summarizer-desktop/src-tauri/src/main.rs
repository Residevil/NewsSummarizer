#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{AppHandle, Manager, WindowEvent};
use std::process::{Command, Child};
use std::sync::Mutex;
use std::path::PathBuf;
use reqwest::blocking::Client;

// === State ===
struct BackendProcess(Mutex<Option<Child>>);

// === Resolve backend binary path (Tauri 2.x API) ===
fn backend_binary_path(app: &AppHandle) -> PathBuf {
    let resource_dir = app
        .path()
        .resource_dir()
        .expect("Failed to get resource dir");

    println!("=== RESOURCE DIR ===");
    println!("{}", resource_dir.display());
    println!("====================");

    #[cfg(target_os = "windows")]
    return resource_dir.join("binaries/run_backend.exe");
}

#[cfg(debug_assertions)]
const DEV_MODE: bool = true;

#[cfg(not(debug_assertions))]
const DEV_MODE: bool = false;

// === Commands ===
#[tauri::command]
fn start_backend(app: AppHandle, state: tauri::State<BackendProcess>) {
    if DEV_MODE {
        println!("DEV MODE: Skipping backend EXE startup");
        return;
    }

    let binary = backend_binary_path(&app);

    let child = Command::new(binary)
        .spawn()
        .expect("Failed to start backend");

    *state.0.lock().unwrap() = Some(child);
}

#[tauri::command]
fn wait_for_backend() -> bool {
    let client = Client::new();
    for _ in 0..50 {
        if let Ok(resp) = client.get("http://127.0.0.1:39231/health").send() {
            if resp.status().is_success() {
                return true;
            }
        }
        std::thread::sleep(std::time::Duration::from_millis(200));
    }
    false
}

fn api() -> String {
    "http://127.0.0.1:39231".into()
}

#[tauri::command]
fn list_models() -> Result<String, String> {
    Client::new()
        .get(format!("{}/models", api()))
        .send()
        .and_then(|r| r.text())
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn download_model(name: String) -> Result<String, String> {
    Client::new()
        .post(format!("{}/models/download", api()))
        .json(&serde_json::json!({ "name": name }))
        .send()
        .and_then(|r| r.text())
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn delete_model(name: String) -> Result<String, String> {
    Client::new()
        .delete(format!("{}/models/{}", api(), name))
        .send()
        .and_then(|r| r.text())
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn select_model(name: String) -> Result<String, String> {
    Client::new()
        .post(format!("{}/models/select", api()))
        .json(&serde_json::json!({ "name": name }))
        .send()
        .and_then(|r| r.text())
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn test_model(name: String) -> Result<String, String> {
    Client::new()
        .post(format!("{}/models/test", api()))
        .json(&serde_json::json!({ "name": name }))
        .send()
        .and_then(|r| r.text())
        .map_err(|e| e.to_string())
}

// === Main (Tauri 2.x) ===
fn main() {
    tauri::Builder::default()
        .manage(BackendProcess(Mutex::new(None)))
        .invoke_handler(tauri::generate_handler![
            start_backend,
            wait_for_backend,
            list_models,
            download_model,
            delete_model,
            select_model,
            test_model
        ])
        .on_window_event(|window, event| {
            if let WindowEvent::CloseRequested { .. } = event {
                let app = window.app_handle();
                let state = app.state::<BackendProcess>();
                if let Some(mut child) = state.0.lock().unwrap().take() {
                    let _ = child.kill();
                };
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
