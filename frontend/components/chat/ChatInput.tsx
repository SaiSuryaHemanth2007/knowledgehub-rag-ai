"use client";

import { SendHorizontal } from "lucide-react";

export default function ChatInput() {
  return (
    <div className="mx-auto mt-10 w-full max-w-3xl">
      <div className="flex items-center rounded-2xl border bg-white p-3 shadow-sm">
        <input
          type="text"
          placeholder="Ask anything about your documents..."
          className="flex-1 bg-transparent px-3 py-2 outline-none"
        />

        <button className="rounded-xl bg-black p-3 text-white transition hover:bg-gray-800">
          <SendHorizontal size={18} />
        </button>
      </div>
    </div>
  );
}