import { apiGet, apiPost } from "./base";

export interface Digest {
  id: string;
  title: string;
  summary: string;
  source: string;
  published_at: string;
  read?: boolean; // Optional, but you should set a default elsewhere if not present
}

export function ensureDigestHasRead(digest: Omit<Digest, 'read'> & Partial<Pick<Digest, 'read'>>): Digest {
  return {
    ...digest,
    read: digest.read ?? false
  };
}

export async function getDigests(): Promise<Digest[]> {
  return apiGet<Digest[]>("/digests");
}

export async function refreshDigests(): Promise<Digest[]> {
  return apiPost<Digest[]>("/digests/refresh");
}

export async function markAsRead(id: string): Promise<{ status: string; id: string; read: boolean }> {
  return apiPost<{ status: string; id: string; read: boolean }>(`/digests/${id}/read`);
}

