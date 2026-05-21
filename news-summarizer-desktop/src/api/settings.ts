import { apiGet, apiPost } from "./base";

export interface Settings {
  refresh_interval_minutes: number;
  model: string;
  sources: string[];
  max_articles: number;
}

export async function getSettings(): Promise<Settings> {
  return apiGet<Settings>("/settings");
}

// export async function saveSettings(
//   partial: Partial<Settings>
// ): Promise<{ success: boolean }> {
//   return apiPost<{ success: boolean }>("/settings", partial);
// }

export async function saveSettings(settings: Settings) {
  return apiPost("/settings", settings);
}
