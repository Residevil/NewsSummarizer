import { useState, useCallback } from "react";
import { markAsRead } from "../api/digests";

/**
 * Hook to mark a digest as read.
 */
export function useMarkAsRead(onSuccess?: (id: string) => void) {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  const mark = useCallback(
    async (id: string) => {
      setLoading(true);
      setError(null);
      try {
        await markAsRead(id);
        if (onSuccess) onSuccess(id);
      } catch (e) {
        setError(e as Error);
      }
      setLoading(false);
    },
    [onSuccess]
  );

  return { markAsRead: mark, loading, error };
}