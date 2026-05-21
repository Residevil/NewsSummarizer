import React from "react";

const inputClass =
  "w-full rounded border border-gray-300 bg-white px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-800";

export const Input: React.FC<React.InputHTMLAttributes<HTMLInputElement>> = ({
  className = "",
  ...props
}) => {
  return <input className={`${inputClass} ${className}`} {...props} />;
};
