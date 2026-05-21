import React from "react";

const selectClass =
  "w-full rounded border border-gray-300 bg-white px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-800";

export const Select: React.FC<React.SelectHTMLAttributes<HTMLSelectElement>> = ({
  className = "",
  ...props
}) => {
  return <select className={`${selectClass} ${className}`} {...props} />;
};
