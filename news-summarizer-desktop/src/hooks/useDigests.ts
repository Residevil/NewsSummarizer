import { useState, useEffect, useCallback } from "react";
import { Digest, getDigests, ensureDigestHasRead } from "../api/digests";

/**
 * Hook to fetch digests, optionally auto-load on mount.
 */
export function useDigests(autoLoad: boolean = true) {
  const [digests, setDigests] = useState<Digest[]>([]);
  const [loading, setLoading] = useState<boolean>(!!autoLoad);
  const [error, setError] = useState<Error | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getDigests();
      setDigests(data.map(ensureDigestHasRead));
    } catch (e) {
      setError(e as Error);
    }
    setLoading(false);
  }, []);

  // Auto load on mount
  useEffect(() => {
    if (autoLoad) load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { digests, setDigests, loading, error, reload: load };
}



