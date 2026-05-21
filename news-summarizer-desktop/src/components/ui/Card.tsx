import React from "react";

export const Card: React.FC<{
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}> = ({ children, className = "", onClick }) => {
  return (
    <div
      onClick={onClick}
      className={`rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition dark:border-gray-700 dark:bg-gray-800 ${className}`}
    >
      {children}
    </div>
  );
};
