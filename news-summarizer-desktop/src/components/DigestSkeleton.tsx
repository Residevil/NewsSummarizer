import React from "react";
import { Card } from "./ui/Card";

export const DigestSkeleton: React.FC = () => {
  return (
    <Card className="animate-pulse">
      <div className="mb-3 h-5 w-2/3 rounded bg-gray-300 dark:bg-gray-700" />
      <div className="mb-2 h-4 w-1/3 rounded bg-gray-300 dark:bg-gray-700" />
      <div className="mb-1 h-4 w-full rounded bg-gray-300 dark:bg-gray-700" />
      <div className="h-4 w-5/6 rounded bg-gray-300 dark:bg-gray-700" />
    </Card>
  );
};
