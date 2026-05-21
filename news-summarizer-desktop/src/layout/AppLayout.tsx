import React from "react";
import { Link } from "wouter";

const navLinkClass = (active: boolean) =>
  `rounded-md px-3 py-1.5 text-sm transition ${
    active
      ? "bg-gray-700 text-white"
      : "text-gray-400 hover:bg-gray-800 hover:text-gray-200"
  }`;

export const AppLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="flex min-h-screen flex-col bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-100">
      <header className="flex gap-4 border-b border-gray-800 bg-gray-900 px-5 py-3">
        <Link href="/" className={navLinkClass}>
          Home
        </Link>
        <Link href="/settings" className={navLinkClass}>
          Settings
        </Link>
        <Link href="/models" className={navLinkClass}>
          Models
        </Link>
      </header>

      <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-8">{children}</main>
    </div>
  );
};
