import React, { useState } from "react";
import type { Digest } from "../api/digests";
import { Button } from "./ui/Button";
import { Card } from "./ui/Card";

interface Props {
  digest: Digest;
  onMarkRead: (id: string) => Promise<void>;
  onOpenDetail: (digest: Digest) => void;
}

export const DigestCard: React.FC<Props> = ({ digest, onMarkRead, onOpenDetail }) => {
  const [status, setStatus] = useState<"idle" | "loading" | "done">("idle");

  async function handleMark() {
    setStatus("loading");
    await onMarkRead(digest.id);
    setStatus("done");
    setTimeout(() => setStatus("idle"), 600);
  }

  return (
    <Card
      className="cursor-pointer hover:-translate-y-0.5 hover:shadow-md"
      onClick={() => onOpenDetail(digest)}
    >
      <div className="mb-2 flex justify-between text-xs text-gray-500 dark:text-gray-400">
        <span className="font-medium">{digest.source}</span>
        <span>{digest.published_at}</span>
      </div>

      <h3 className="mb-1 text-lg font-semibold leading-snug">{digest.title}</h3>

      <p className="line-clamp-4 text-sm leading-relaxed text-gray-700 dark:text-gray-300">
        {digest.summary}
      </p>

      <div className="mt-3 flex justify-end">
        {!digest.read && status === "idle" && (
          <Button
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              handleMark();
            }}
          >
            Mark as read
          </Button>
        )}

        {status === "loading" && (
          <div
            className="h-[18px] w-[18px] animate-spin rounded-full border-[3px] border-gray-300 border-t-green-400"
            aria-label="Loading"
          />
        )}
        {status === "done" && (
          <span className="text-xl text-green-400" aria-label="Done">
            ✔
          </span>
        )}
      </div>
    </Card>
  );
};
