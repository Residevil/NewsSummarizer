import { invoke } from "@tauri-apps/api/core";

export interface Model {
  name: string;
  size_mb: number | null;
  installed: boolean;
  last_used?: string | null;
}

export async function getModels(): Promise<Model[]> {
  const raw = (await invoke("list_models")) as string;
  return JSON.parse(raw) as Model[];
}

export async function downloadModel(name: string): Promise<void> {
  await invoke("download_model", { name });
}

export async function deleteModel(name: string): Promise<void> {
  await invoke("delete_model", { name });
}

export async function selectModel(name: string): Promise<void> {
  await invoke("select_model", { name });
}

export async function testModel(name: string): Promise<unknown> {
  const raw = (await invoke("test_model", { name })) as string;
  return JSON.parse(raw);
}
