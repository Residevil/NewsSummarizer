import React from "react";

const sizes = {
  sm: "px-3 py-1 text-sm",
  md: "px-3 py-1.5 text-sm",
};

const variants = {
  primary: "bg-blue-600 text-white hover:bg-blue-700",
  danger: "bg-red-600 text-white hover:bg-red-700",
  ghost:
    "bg-gray-200 text-gray-900 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600",
};

export const Button: React.FC<
  React.ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?: keyof typeof variants;
    size?: keyof typeof sizes;
  }
> = ({ variant = "primary", size = "md", className = "", ...props }) => {
  const base = "rounded font-medium transition disabled:opacity-50";

  return (
    <button
      className={`${base} ${sizes[size]} ${variants[variant]} ${className}`}
      {...props}
    />
  );
};
