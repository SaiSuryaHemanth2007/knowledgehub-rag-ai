"use client";

import {
  MessageSquare,
  Upload,
  Files,
  Settings,
} from "lucide-react";

const menuItems = [
  {
    title: "Chat",
    icon: MessageSquare,
  },
  {
    title: "Upload",
    icon: Upload,
  },
  {
    title: "Documents",
    icon: Files,
  },
  {
    title: "Settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  return (
    <aside className="flex h-screen w-72 flex-col border-r bg-white shadow-sm">

      <div className="border-b p-6">
        <h1 className="text-2xl font-bold">
          KnowledgeHub
        </h1>
      </div>

      <nav className="flex-1 p-4">

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.title}
              className="mb-2 flex w-full items-center gap-3 rounded-lg p-3 transition hover:bg-gray-100"
            >
              <Icon size={20} />

              <span>{item.title}</span>

            </button>
          );
        })}

      </nav>

    </aside>
  );
}