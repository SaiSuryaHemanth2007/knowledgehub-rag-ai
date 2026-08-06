"use client";

import {
  Moon,
  UserCircle,
} from "lucide-react";

export default function Header() {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-white px-6 shadow-sm">

      <h1 className="text-xl font-semibold">
        KnowledgeHub AI
      </h1>

      <div className="flex items-center gap-5">

        <button className="rounded-lg p-2 hover:bg-gray-100">
          <Moon size={20} />
        </button>

        <button className="rounded-lg p-2 hover:bg-gray-100">
          <UserCircle size={24} />
        </button>

      </div>

    </header>
  );
}