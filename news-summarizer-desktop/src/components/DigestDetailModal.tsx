import React from "react";
import type { Digest } from "../api/digests";
import { Button } from "./ui/Button";

interface Props {
  digest: Digest | null;
  onClose: () => void;
}

export const DigestDetailModal: React.FC<Props> = ({ digest, onClose }) => {
  if (!digest) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/45 p-4"
      onClick={onClose}
    >
      <div
        className="max-h-[80vh] w-full max-w-lg overflow-y-auto rounded-xl bg-white p-6 shadow-xl dark:bg-gray-800"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="mb-3 text-xl font-semibold">{digest.title}</h2>

        <div className="mb-4 text-sm text-gray-500 dark:text-gray-400">
          {digest.source} • {digest.published_at}
        </div>

        <p className="whitespace-pre-line leading-relaxed text-gray-700 dark:text-gray-300">
          {digest.summary}
        </p>

        <div className="mt-6 flex justify-end">
          <Button variant="ghost" onClick={onClose}>
            Close
          </Button>
        </div>
      </div>
    </div>
  );
};
