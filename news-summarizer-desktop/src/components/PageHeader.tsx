import React from "react";

interface Props {
  title: string;
  actions?: React.ReactNode;
}

export const PageHeader: React.FC<Props> = ({ title, actions }) => {
  return (
    <div className="mb-6 flex items-center justify-between gap-4">
      <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
      {actions}
    </div>
  );
};
