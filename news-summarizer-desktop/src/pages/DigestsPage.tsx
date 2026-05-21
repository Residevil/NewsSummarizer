import React, { useEffect, useState } from "react";
import type { Digest } from "../api/digests";
import { DigestCard } from "../components/DigestCard";
import { DigestDetailModal } from "../components/DigestDetailModal";
import { DigestSkeleton } from "../components/DigestSkeleton";
import { PageHeader } from "../components/PageHeader";
import { Button } from "../components/ui/Button";
import { useToast } from "../components/toast/ToastContext";
import { useDigests } from "../hooks/useDigests";
import { useMarkAsRead } from "../hooks/useMarkAsRead";

export const DigestsPage: React.FC = () => {
  const [selected, setSelected] = useState<Digest | null>(null);
  const { showToast } = useToast();
  const { digests, setDigests, loading, error, reload } = useDigests();

  useEffect(() => {
    if (error) showToast("Failed to load digests.");
  }, [error, showToast]);

  const { markAsRead: markDigestAsRead } = useMarkAsRead((id) => {
    showToast("Marked as read.");
    setDigests((prev) =>
      prev.map((d) => (d.id === id ? { ...d, read: true } : d))
    );
  });

  return (
    <>
      <PageHeader
        title="News Digests"
        actions={
          <Button onClick={reload} disabled={loading}>
            Refresh
          </Button>
        }
      />

      {loading && (
        <div className="flex flex-col gap-4">
          <DigestSkeleton />
          <DigestSkeleton />
          <DigestSkeleton />
        </div>
      )}

      {!loading && (
        <div className="flex flex-col gap-4">
          {digests.map((digest) => (
            <DigestCard
              key={digest.id}
              digest={digest}
              onMarkRead={markDigestAsRead}
              onOpenDetail={setSelected}
            />
          ))}
        </div>
      )}

      <DigestDetailModal digest={selected} onClose={() => setSelected(null)} />
    </>
  );
};
